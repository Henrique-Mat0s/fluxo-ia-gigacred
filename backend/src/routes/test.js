// Rotas de teste — sem persistência, sem WhatsApp.
// Servem pro painel ter um "playground" da Giovanna.

import { Router } from "express";
import { chamarIA } from "../ia/gemini.js";
import { getIAConfig } from "../db/supabase.js";

const router = Router();

// Prompt fallback caso Supabase não esteja configurado
const PROMPT_FALLBACK = `Você é a Giovanna, consultora virtual da GIGACRED Correspondente.
Sua função é qualificar leads que querem antecipar FGTS, INSS ou consignado privado.

REGRAS:
- Tom caloroso, direto, brasileiro. Sem formalidades excessivas.
- NUNCA mais de 2 frases por mensagem.
- UMA pergunta por mensagem.
- Se o lead não fez adesão ao Saque-Aniversário, EXPLIQUE como fazer no app FGTS.
- NUNCA dê taxa específica ou prometa aprovação — isso é função do closer.

O QUE DESCOBRIR (BANT adaptado):
1. Saldo FGTS estimado
2. Adesão ao Saque-Aniversário (CRITÉRIO ELIMINATÓRIO)
3. Motivo do dinheiro
4. Urgência
5. Vínculo de trabalho

FORMATO DE SAÍDA (JSON estrito):
{
  "reply": "<texto curto pro lead, sem markdown>",
  "qualificacao": {
    "saldo_fgts_estimado": <numero ou null>,
    "fez_adesao": <true | false | null>,
    "motivo": "<texto livre ou null>",
    "urgencia": "<imediato|semana|mes|sem_prazo|desconhecido>",
    "vinculo": "<clt|inss|autonomo|publico|desconhecido>",
    "score": <0-100>,
    "acao_recomendada": "handoff_now|continue_qualifying|park|discard|remover_base"
  }
}`;

/**
 * POST /api/test/conversa
 * Body: {
 *   historico: [{ autor: "lead"|"ia", texto: "..." }, ...],
 *   novaMensagem: "...",
 *   promptCustom: "..." (opcional - sobrepõe o prompt do banco)
 * }
 * Retorna: { reply, qualificacao, _meta, modoMock?: bool }
 */
router.post("/conversa", async (req, res) => {
  try {
    const { historico = [], novaMensagem, promptCustom } = req.body || {};

    if (!novaMensagem || typeof novaMensagem !== "string") {
      return res.status(400).json({ erro: "novaMensagem (string) é obrigatório" });
    }

    // Define prompt: custom > config do banco > fallback
    let systemPrompt = promptCustom;
    if (!systemPrompt) {
      try {
        const cfg = await getIAConfig();
        systemPrompt = cfg?.system_prompt || PROMPT_FALLBACK;
      } catch {
        systemPrompt = PROMPT_FALLBACK;
      }
    }

    // Monta contexto
    const contexto = historico.length
      ? historico.map(m => `[${m.autor}] ${m.texto}`).join("\n")
      : "(primeira mensagem da conversa)";

    // Se Gemini não configurado, devolve resposta mock
    if (!process.env.GEMINI_API_KEY) {
      return res.json(respostaMock(novaMensagem, historico));
    }

    const r = await chamarIA({
      systemPrompt,
      contexto: `Histórico:\n${contexto}`,
      novaMensagem,
    });

    res.json(r);
  } catch (e) {
    console.error("[test/conversa] erro:", e);
    res.status(500).json({ erro: e.message });
  }
});

// Resposta mock pra quando Gemini não está configurado.
// Não substitui a IA real — só dá uma noção do fluxo pra quem nunca viu.
function respostaMock(novaMsg, historico) {
  const turno = historico.length;
  const lower = novaMsg.toLowerCase();

  const respostas = [
    {
      reply: "Oi! Tudo bem? Sou a Giovanna da GIGACRED. Você já fez a adesão ao Saque-Aniversário do FGTS no app da Caixa?",
      qualificacao: { score: 10, acao_recomendada: "continue_qualifying" },
    },
    {
      reply: lower.includes("sim") || lower.includes("já") || lower.includes("ja")
        ? "Ótimo! E você sabe mais ou menos quanto tem hoje de saldo no FGTS?"
        : "Sem problema! Pra antecipar o FGTS, basta abrir o app FGTS da Caixa, ir em \"Saque-Aniversário\" e fazer a adesão. Quer que eu te ajude depois que você fizer?",
      qualificacao: {
        fez_adesao: lower.includes("sim") || lower.includes("já") || lower.includes("ja"),
        score: lower.includes("sim") || lower.includes("já") || lower.includes("ja") ? 35 : 15,
        acao_recomendada: "continue_qualifying"
      },
    },
    {
      reply: "Beleza! E pra que você quer usar o dinheiro?",
      qualificacao: {
        saldo_fgts_estimado: extrairNumero(novaMsg),
        score: 55,
        acao_recomendada: "continue_qualifying",
      },
    },
    {
      reply: "Entendo. Você quer começar quando — essa semana, esse mês, ou sem pressa?",
      qualificacao: { motivo: novaMsg, score: 70, acao_recomendada: "continue_qualifying" },
    },
    {
      reply: "Show! Vou te passar pra um consultor da equipe agora pra fechar tudo certinho. Pode me confirmar seu nome completo?",
      qualificacao: {
        urgencia: lower.includes("semana") || lower.includes("urgente") || lower.includes("hoje") ? "imediato" : "mes",
        score: 88,
        acao_recomendada: "handoff_now",
      },
    },
  ];

  const r = respostas[Math.min(turno, respostas.length - 1)];
  return {
    ...r,
    _meta: {
      modoMock: true,
      aviso: "GEMINI_API_KEY não configurado — esta é uma resposta SIMULADA. Configure o .env pra ver a Giovanna real.",
      latency_ms: 50,
      tokens_in: 0,
      tokens_out: 0,
      modelo: "mock",
    },
  };
}

function extrairNumero(txt) {
  const m = txt.match(/(\d+(?:[.,]\d+)?)\s*(?:mil|k)/i);
  if (m) return parseFloat(m[1].replace(",", ".")) * 1000;
  const m2 = txt.match(/\d+/);
  if (m2) return parseInt(m2[0], 10);
  return null;
}

export default router;

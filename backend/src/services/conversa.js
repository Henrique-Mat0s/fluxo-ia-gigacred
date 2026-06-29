// Service que orquestra: mensagem chega → busca contexto → chama Giovanna → salva tudo.

import {
  findLeadByTelefone, createLead, updateLead,
  getUltimasMensagens, insertMensagem, getIAConfig,
} from "../db/supabase.js";
import { getInstanciaPorNome } from "../db/instancias.js";
import { chamarIA } from "../ia/gemini.js";

/**
 * Processa uma mensagem que chegou pelo webhook da Evolution.
 *
 * @param {object} msg
 * @param {string} msg.telefone        - número do lead (E.164, sem +)
 * @param {string} msg.nome            - nome (se a Evolution passar)
 * @param {string} msg.texto           - texto da mensagem
 * @param {string} [msg.instanciaNome] - qual chip recebeu (multi-instância)
 */
export async function processarMensagem(msg) {
  // Resolve instancia_id pra registrar nas mensagens (best-effort)
  let instanciaId = null;
  if (msg.instanciaNome) {
    try {
      const inst = await getInstanciaPorNome(msg.instanciaNome);
      instanciaId = inst?.id || null;
    } catch { /* ignora */ }
  }

  // 1. Acha ou cria o lead
  let lead = await findLeadByTelefone(msg.telefone);
  if (!lead) {
    lead = await createLead({
      telefone: msg.telefone,
      nome: msg.nome || null,
      status: "em_conversa",
      origem: "whatsapp_organico",
    });
  } else if (lead.status === "disparado" || lead.status === "base") {
    // Lead da base respondeu — vira em_conversa
    await updateLead(lead.id, { status: "em_conversa" });
    lead.status = "em_conversa";
  }

  // 2. Salva a mensagem do lead
  await insertMensagem({
    lead_id: lead.id,
    autor: "lead",
    texto: msg.texto,
    instancia_id: instanciaId,
  });

  // 3. Verifica se a IA está ativa
  const config = await getIAConfig();
  if (!config?.ativa) {
    return { reply: null, score: lead.score, acao: "ia_pausada" };
  }

  // 4. Monta contexto (histórico + dados do lead)
  const historico = await getUltimasMensagens(lead.id, 20);
  const contexto = montarContexto(lead, historico.reverse());

  // 5. Chama a Giovanna
  const r = await chamarIA({
    systemPrompt: config.system_prompt,
    contexto,
    novaMensagem: msg.texto,
  });

  // 6. Salva a resposta + métricas
  if (r.reply) {
    await insertMensagem({
      lead_id: lead.id,
      autor: "ia",
      texto: r.reply,
      modelo: r._meta.modelo,
      tokens_in: r._meta.tokens_in,
      tokens_out: r._meta.tokens_out,
      latency_ms: r._meta.latency_ms,
      instancia_id: instanciaId,
    });
  }

  // 7. Atualiza qualificação do lead
  const q = r.qualificacao || {};
  const novoStatus = decidirNovoStatus(q.acao_recomendada, lead.status);
  const patch = {
    score: q.score ?? lead.score,
    saldo_fgts_estimado: q.saldo_fgts_estimado ?? lead.saldo_fgts_estimado,
    fez_adesao_saque_aniversario: q.fez_adesao ?? lead.fez_adesao_saque_aniversario,
    motivo: q.motivo ?? lead.motivo,
    vinculo: q.vinculo ?? lead.vinculo,
    status: novoStatus,
    ultima_msg_em: new Date().toISOString(),
  };
  if (novoStatus === "qualificado" && lead.status !== "qualificado") {
    patch.qualificado_em = new Date().toISOString();
    patch.resumo_ia = montarResumo(q, lead);
  }
  await updateLead(lead.id, patch);

  return {
    reply: r.reply,
    score: q.score,
    acao: q.acao_recomendada,
    handoff: novoStatus === "qualificado",
  };
}

function montarContexto(lead, mensagens) {
  const dados = [
    `telefone: ${lead.telefone}`,
    `nome: ${lead.nome || "(não capturado)"}`,
    `origem: ${lead.origem || "desconhecida"}`,
    `score_atual: ${lead.score}`,
    `saldo_fgts_estimado: ${lead.saldo_fgts_estimado ?? "?"}`,
    `fez_adesao: ${lead.fez_adesao_saque_aniversario ?? "?"}`,
    `vinculo: ${lead.vinculo ?? "?"}`,
    `motivo: ${lead.motivo ?? "?"}`,
  ].join("\n");

  const historico = mensagens
    .map(m => `[${m.autor}] ${m.texto}`)
    .join("\n");

  return `Dados conhecidos do lead:\n${dados}\n\nHistórico da conversa (mais antigo primeiro):\n${historico}`;
}

function decidirNovoStatus(acao, statusAtual) {
  switch (acao) {
    case "handoff_now":    return "qualificado";
    case "park":           return "park";
    case "discard":        return "perdido";
    case "remover_base":   return "bloqueado";
    case "continue_qualifying":
    default:               return statusAtual === "novo" ? "em_conversa" : statusAtual;
  }
}

function montarResumo(q, lead) {
  const partes = [];
  if (lead.nome) partes.push(lead.nome);
  if (q.saldo_fgts_estimado) partes.push(`saldo ~R$ ${q.saldo_fgts_estimado}`);
  if (q.fez_adesao === true) partes.push("adesão OK");
  if (q.fez_adesao === false) partes.push("SEM adesão");
  if (q.urgencia && q.urgencia !== "desconhecido") partes.push(`urgência: ${q.urgencia}`);
  if (q.motivo) partes.push(`motivo: ${q.motivo}`);
  if (q.vinculo && q.vinculo !== "desconhecido") partes.push(`vínculo: ${q.vinculo}`);
  return partes.join(" · ");
}

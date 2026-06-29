// Teste rápido: faz 1 chamada à Giovanna simulando uma mensagem.
// Uso: node scripts/test-gemini.js

import "dotenv/config";
import { chamarIA } from "../src/ia/gemini.js";

const SYSTEM_PROMPT = `Você é a Giovanna, consultora virtual da GIGACRED Correspondente.
Sua função é qualificar leads que querem antecipar FGTS.

REGRAS:
- Tom caloroso, direto, brasileiro.
- NUNCA mais de 2 frases por mensagem.
- UMA pergunta por mensagem.
- NUNCA dê taxa ou prometa aprovação.

DEVE DESCOBRIR (BANT):
1. Saldo FGTS
2. Adesão ao Saque-Aniversário
3. Motivo
4. Urgência
5. Vínculo

FORMATO DE SAÍDA (JSON estrito):
{
  "reply": "...",
  "qualificacao": {
    "score": 0-100,
    "acao_recomendada": "handoff_now|continue_qualifying|park|discard"
  }
}`;

const contexto = `Dados conhecidos:
telefone: 5511999998888
nome: Maria
origem: instagram_ads
score_atual: 0`;

const novaMsg = "Oi! vi seu anuncio, quanto consigo de FGTS?";

console.log(`Chamando Giovanna com modelo ${process.env.GEMINI_MODEL || "gemini-1.5-flash"}...\n`);

try {
  const r = await chamarIA({
    systemPrompt: SYSTEM_PROMPT,
    contexto,
    novaMensagem: novaMsg,
  });
  console.log("=== Resposta da Giovanna ===");
  console.log("Reply:", JSON.stringify(r.reply));
  console.log("Qualificação:", JSON.stringify(r.qualificacao, null, 2));
  console.log("Métricas:", JSON.stringify(r._meta, null, 2));
} catch (e) {
  console.error("ERRO:", e.message);
  process.exit(1);
}

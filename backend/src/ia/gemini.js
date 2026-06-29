// Cliente Gemini — chama a API e parseia o JSON da resposta.

import { GoogleGenerativeAI } from "@google/generative-ai";

const apiKey = process.env.GEMINI_API_KEY;
const modelName = process.env.GEMINI_MODEL || "gemini-1.5-flash";

let genAI = null;
let model = null;

function initModel() {
  if (!apiKey) {
    throw new Error("GEMINI_API_KEY não configurado no .env");
  }
  if (!genAI) {
    genAI = new GoogleGenerativeAI(apiKey);
    model = genAI.getGenerativeModel({
      model: modelName,
      generationConfig: {
        temperature: 0.4,
        maxOutputTokens: 400,
        responseMimeType: "application/json",
      },
    });
  }
  return model;
}

/**
 * Chama o Gemini com system prompt + histórico + mensagem nova.
 * Retorna { reply, qualificacao, _meta: { tokens_in, tokens_out, latency_ms } }
 */
export async function chamarBia({ systemPrompt, contexto, novaMensagem }) {
  const m = initModel();

  const prompt = `${systemPrompt}

<contexto_do_lead>
${contexto}
</contexto_do_lead>

<nova_mensagem_do_lead>
${novaMensagem}
</nova_mensagem_do_lead>

Responda em JSON estrito conforme o formato definido nas instruções.`;

  const inicio = Date.now();
  const result = await m.generateContent(prompt);
  const latency = Date.now() - inicio;

  const response = result.response;
  const text = response.text();

  // Parse robusto — Gemini às vezes envolve em ```json ... ```
  const limpo = text.replace(/^```json\s*/i, "").replace(/```\s*$/, "").trim();
  let parsed;
  try {
    parsed = JSON.parse(limpo);
  } catch (e) {
    console.error("[gemini] Falha ao parsear JSON:", text);
    parsed = {
      reply: "Pode repetir, por favor? Não entendi direito.",
      qualificacao: { score: 0, acao_recomendada: "continue_qualifying" },
    };
  }

  // Metadados de uso (se a API devolveu)
  const usage = response.usageMetadata || {};
  parsed._meta = {
    tokens_in: usage.promptTokenCount || 0,
    tokens_out: usage.candidatesTokenCount || 0,
    latency_ms: latency,
    modelo: modelName,
  };

  return parsed;
}

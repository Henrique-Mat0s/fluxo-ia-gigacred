// Cliente para Evolution API — envio de mensagens e status da instância.
// Docs: https://doc.evolution-api.com

const URL = process.env.EVOLUTION_URL;
const KEY = process.env.EVOLUTION_API_KEY;
const INSTANCE = process.env.EVOLUTION_INSTANCE || "default";

function headers() {
  return {
    apikey: KEY,
    "Content-Type": "application/json",
  };
}

function checkConfig() {
  if (!URL || !KEY) {
    throw new Error("Evolution não configurada. Defina EVOLUTION_URL e EVOLUTION_API_KEY no .env");
  }
}

/**
 * Envia uma mensagem de texto.
 * @param {string} telefone - E.164 sem + (ex: 5531987654321)
 * @param {string} texto
 * @param {object} [opts]
 * @param {number} [opts.delayMs] - delay antes de enviar (simula digitação)
 */
export async function enviarTexto(telefone, texto, opts = {}) {
  checkConfig();

  const body = {
    number: telefone,
    text: texto,
    delay: opts.delayMs ?? 1200,
  };

  const r = await fetch(`${URL}/message/sendText/${INSTANCE}`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify(body),
  });

  if (!r.ok) {
    const erro = await r.text();
    throw new Error(`Evolution sendText ${r.status}: ${erro}`);
  }
  return r.json();
}

/**
 * Estado de conexão da instância (open | connecting | close).
 */
export async function getConnectionState() {
  checkConfig();
  const r = await fetch(`${URL}/instance/connectionState/${INSTANCE}`, {
    headers: headers(),
  });
  if (!r.ok) throw new Error(`Evolution state ${r.status}`);
  return r.json();
}

/**
 * Verifica se um número existe no WhatsApp antes de disparar.
 * Útil pra não queimar disparo em número que nem é WhatsApp.
 */
export async function numeroExiste(telefone) {
  checkConfig();
  try {
    const r = await fetch(`${URL}/chat/whatsappNumbers/${INSTANCE}`, {
      method: "POST",
      headers: headers(),
      body: JSON.stringify({ numbers: [telefone] }),
    });
    if (!r.ok) return true; // se erro, assume que existe (não bloqueia disparo)
    const arr = await r.json();
    return arr?.[0]?.exists === true;
  } catch {
    return true;
  }
}

// Cliente para Evolution API — agora MULTI-INSTÂNCIA.
// Aceita o nome da instância em cada chamada. O .env só precisa de URL + API key.
// Docs: https://doc.evolution-api.com

const URL = process.env.EVOLUTION_URL;
const KEY = process.env.EVOLUTION_API_KEY;
// Fallback caso alguma chamada não passe instância (modo single-instance legado)
const INSTANCE_PADRAO = process.env.EVOLUTION_INSTANCE || "default";

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
 * @param {string} [opts.instance] - nome da instância (default: EVOLUTION_INSTANCE)
 * @param {number} [opts.delayMs] - delay antes de enviar
 */
export async function enviarTexto(telefone, texto, opts = {}) {
  checkConfig();
  const instance = opts.instance || INSTANCE_PADRAO;
  const body = {
    number: telefone,
    text: texto,
    delay: opts.delayMs ?? 1200,
  };
  const r = await fetch(`${URL}/message/sendText/${instance}`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify(body),
  });
  if (!r.ok) {
    const erro = await r.text();
    throw new Error(`Evolution sendText[${instance}] ${r.status}: ${erro}`);
  }
  return r.json();
}

/**
 * Estado de conexão da instância.
 */
export async function getConnectionState(instance = INSTANCE_PADRAO) {
  checkConfig();
  const r = await fetch(`${URL}/instance/connectionState/${instance}`, {
    headers: headers(),
  });
  if (!r.ok) throw new Error(`Evolution state[${instance}] ${r.status}`);
  return r.json();
}

/**
 * Cria uma nova instância na Evolution (necessário antes de escanear QR).
 */
export async function criarInstancia(nome) {
  checkConfig();
  const r = await fetch(`${URL}/instance/create`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({
      instanceName: nome,
      qrcode: true,
      integration: "WHATSAPP-BAILEYS",
    }),
  });
  if (!r.ok) throw new Error(`Evolution create[${nome}] ${r.status}: ${await r.text()}`);
  return r.json();
}

/**
 * Pega o QR code (base64) da instância pra escanear no celular.
 */
export async function getQR(instance) {
  checkConfig();
  const r = await fetch(`${URL}/instance/connect/${instance}`, {
    headers: headers(),
  });
  if (!r.ok) throw new Error(`Evolution connect[${instance}] ${r.status}`);
  return r.json();
}

/**
 * Desconecta (logout) a instância.
 */
export async function desconectar(instance) {
  checkConfig();
  const r = await fetch(`${URL}/instance/logout/${instance}`, {
    method: "DELETE",
    headers: headers(),
  });
  if (!r.ok) throw new Error(`Evolution logout[${instance}] ${r.status}`);
  return r.json();
}

/**
 * Verifica se um número existe no WhatsApp antes de disparar.
 */
export async function numeroExiste(telefone, instance = INSTANCE_PADRAO) {
  checkConfig();
  try {
    const r = await fetch(`${URL}/chat/whatsappNumbers/${instance}`, {
      method: "POST",
      headers: headers(),
      body: JSON.stringify({ numbers: [telefone] }),
    });
    if (!r.ok) return true;
    const arr = await r.json();
    return arr?.[0]?.exists === true;
  } catch {
    return true;
  }
}

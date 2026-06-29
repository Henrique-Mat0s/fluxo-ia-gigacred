// Acesso à tabela `instancias` e view `instancias_status`.

const url = process.env.SUPABASE_URL;
const key = process.env.SUPABASE_SERVICE_KEY;

function headers() {
  return {
    apikey: key,
    Authorization: `Bearer ${key}`,
    "Content-Type": "application/json",
    Prefer: "return=representation",
  };
}

async function rest(path, opts = {}) {
  if (!url || !key) throw new Error("Supabase não configurado.");
  const r = await fetch(`${url}/rest/v1/${path}`, {
    ...opts,
    headers: { ...headers(), ...(opts.headers || {}) },
  });
  if (!r.ok) throw new Error(`Supabase ${r.status}: ${await r.text()}`);
  return r.status === 204 ? null : r.json();
}

/** Lista todas as instâncias (com métricas do dia). */
export async function listarInstancias() {
  return rest("instancias_status?order=ordem_disparo.asc,nome.asc");
}

/** Apenas as ativas, em ordem de disparo. */
export async function listarInstanciasAtivas() {
  return rest("instancias_status?ativa=eq.true&order=ordem_disparo.asc,nome.asc");
}

export async function getInstanciaPorNome(nome) {
  const arr = await rest(`instancias?nome=eq.${encodeURIComponent(nome)}&limit=1`);
  return arr[0] || null;
}

export async function getInstanciaPorId(id) {
  const arr = await rest(`instancias?id=eq.${id}&limit=1`);
  return arr[0] || null;
}

export async function criarRegistroInstancia({ nome, numero = null, observacao = null }) {
  // Calcula próximo ordem_disparo
  const todas = await rest("instancias?select=ordem_disparo&order=ordem_disparo.desc&limit=1");
  const proxOrdem = todas.length ? (todas[0].ordem_disparo || 0) + 1 : 1;

  const arr = await rest("instancias", {
    method: "POST",
    body: JSON.stringify({ nome, numero, observacao, ordem_disparo: proxOrdem }),
  });
  return arr[0];
}

export async function atualizarInstancia(id, patch) {
  const arr = await rest(`instancias?id=eq.${id}`, {
    method: "PATCH",
    body: JSON.stringify(patch),
  });
  return arr[0];
}

export async function deletarInstancia(id) {
  await rest(`instancias?id=eq.${id}`, { method: "DELETE" });
}

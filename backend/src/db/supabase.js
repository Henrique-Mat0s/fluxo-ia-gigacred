// Cliente Supabase via REST (sem SDK — usa fetch direto).
// Mantemos zero dependência externa pra Supabase.

const url = process.env.SUPABASE_URL;
const key = process.env.SUPABASE_SERVICE_KEY;

if (!url || !key) {
  console.warn("[supabase] SUPABASE_URL ou SUPABASE_SERVICE_KEY não configurados — operando em modo MOCK.");
}

const headers = () => ({
  apikey: key,
  Authorization: `Bearer ${key}`,
  "Content-Type": "application/json",
  Prefer: "return=representation",
});

async function rest(path, opts = {}) {
  if (!url || !key) {
    throw new Error("Supabase não configurado. Defina SUPABASE_URL e SUPABASE_SERVICE_KEY no .env");
  }
  const r = await fetch(`${url}/rest/v1/${path}`, {
    ...opts,
    headers: { ...headers(), ...(opts.headers || {}) },
  });
  if (!r.ok) {
    const body = await r.text();
    throw new Error(`Supabase ${r.status}: ${body}`);
  }
  return r.status === 204 ? null : r.json();
}

// ---------- Leads ----------
export async function findLeadByTelefone(telefone) {
  const arr = await rest(`leads?telefone=eq.${encodeURIComponent(telefone)}&select=*&limit=1`);
  return arr[0] || null;
}

export async function createLead(data) {
  const arr = await rest("leads", {
    method: "POST",
    body: JSON.stringify(data),
  });
  return arr[0];
}

export async function updateLead(id, patch) {
  const arr = await rest(`leads?id=eq.${id}`, {
    method: "PATCH",
    body: JSON.stringify(patch),
  });
  return arr[0];
}

export async function getLeadsByStatus(status, limit = 50) {
  return rest(`leads?status=eq.${status}&order=score.desc&limit=${limit}&select=*`);
}

export async function getLeadsParaDisparar(limit = 150) {
  return rest(`leads?status=eq.base&limit=${limit}&select=*`);
}

// ---------- Mensagens ----------
export async function insertMensagem(data) {
  const arr = await rest("mensagens", {
    method: "POST",
    body: JSON.stringify(data),
  });
  return arr[0];
}

export async function getUltimasMensagens(leadId, limit = 20) {
  return rest(
    `mensagens?lead_id=eq.${leadId}&order=criado_em.desc&limit=${limit}&select=*`
  );
}

// ---------- Config IA ----------
export async function getIAConfig() {
  const arr = await rest("ia_config?id=eq.1&select=*");
  return arr[0];
}

export async function updateIAConfig(patch) {
  const arr = await rest("ia_config?id=eq.1", {
    method: "PATCH",
    body: JSON.stringify({ ...patch, atualizado_em: new Date().toISOString() }),
  });
  return arr[0];
}

// ---------- Métricas ----------
export async function contarDisparosHoje() {
  // Conta mensagens enviadas hoje pela IA com autor=ia
  const hoje = new Date().toISOString().slice(0, 10);
  const arr = await rest(
    `mensagens?autor=eq.ia&criado_em=gte.${hoje}&select=id`
  );
  return arr.length;
}

export async function contarBloqueadosHoje() {
  const hoje = new Date().toISOString().slice(0, 10);
  const arr = await rest(
    `leads?status=eq.bloqueado&criado_em=gte.${hoje}&select=id`
  );
  return arr.length;
}

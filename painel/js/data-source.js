// Abstração que decide se usa MOCK ou Supabase real.
// Quando você plugar o Supabase de verdade, só edita as funções abaixo —
// as telas (index.html, ligar.html, config.html) continuam iguais.

const CONFIG = {
  // Pra ativar Supabase real, preencha estes 2 valores:
  SUPABASE_URL: "",   // ex: "https://xxxxxxx.supabase.co"
  SUPABASE_KEY: "",   // public anon key

  // Evolution API (opcional — se quiser puxar status real da instância)
  EVOLUTION_URL: "",       // ex: "https://evolution.seudominio.com"
  EVOLUTION_API_KEY: "",
  EVOLUTION_INSTANCE: "gigacred-bot-01",
};

const DataSource = {
  isMock() {
    return !CONFIG.SUPABASE_URL || !CONFIG.SUPABASE_KEY;
  },

  // ---------- Status da Evolution / instância ----------
  async getInstanciaStatus() {
    if (this.isMock()) {
      return window.MOCK_DATA.instancia;
    }
    // Real: chama Evolution API
    const r = await fetch(
      `${CONFIG.EVOLUTION_URL}/instance/connectionState/${CONFIG.EVOLUTION_INSTANCE}`,
      { headers: { apikey: CONFIG.EVOLUTION_API_KEY } }
    );
    return await r.json();
  },

  // ---------- Conversas ativas (IA trabalhando agora) ----------
  async getConversasAtivas() {
    if (this.isMock()) {
      return window.MOCK_DATA.conversas_ativas;
    }
    // Real: query no Supabase
    // SELECT * FROM leads WHERE status='em_conversa' ORDER BY ultima_msg_em DESC
    const r = await fetch(
      `${CONFIG.SUPABASE_URL}/rest/v1/leads?status=eq.em_conversa&order=ultima_msg_em.desc`,
      { headers: { apikey: CONFIG.SUPABASE_KEY, Authorization: `Bearer ${CONFIG.SUPABASE_KEY}` } }
    );
    return await r.json();
  },

  // ---------- Leads qualificados (pra ligar) ----------
  async getLeadsPraLigar() {
    if (this.isMock()) {
      return window.MOCK_DATA.pra_ligar;
    }
    const r = await fetch(
      `${CONFIG.SUPABASE_URL}/rest/v1/leads?status=eq.qualificado&order=score.desc`,
      { headers: { apikey: CONFIG.SUPABASE_KEY, Authorization: `Bearer ${CONFIG.SUPABASE_KEY}` } }
    );
    return await r.json();
  },

  // ---------- Config da IA ----------
  async getConfigIA() {
    if (this.isMock()) {
      return window.MOCK_DATA.config_ia;
    }
    const r = await fetch(
      `${CONFIG.SUPABASE_URL}/rest/v1/ia_config?id=eq.1`,
      { headers: { apikey: CONFIG.SUPABASE_KEY, Authorization: `Bearer ${CONFIG.SUPABASE_KEY}` } }
    );
    const arr = await r.json();
    return arr[0];
  },

  async saveConfigIA(updates) {
    if (this.isMock()) {
      Object.assign(window.MOCK_DATA.config_ia, updates);
      return window.MOCK_DATA.config_ia;
    }
    const r = await fetch(
      `${CONFIG.SUPABASE_URL}/rest/v1/ia_config?id=eq.1`,
      {
        method: "PATCH",
        headers: {
          apikey: CONFIG.SUPABASE_KEY,
          Authorization: `Bearer ${CONFIG.SUPABASE_KEY}`,
          "Content-Type": "application/json",
          Prefer: "return=representation",
        },
        body: JSON.stringify(updates),
      }
    );
    return await r.json();
  },

  // ---------- Marcar lead como ligado ----------
  async marcarComoLigado(leadId, resultado) {
    if (this.isMock()) {
      // só remove da lista
      window.MOCK_DATA.pra_ligar = window.MOCK_DATA.pra_ligar.filter(l => l.id !== leadId);
      return { ok: true };
    }
    // Real: insere em ligacoes + atualiza status do lead
    await fetch(`${CONFIG.SUPABASE_URL}/rest/v1/ligacoes`, {
      method: "POST",
      headers: {
        apikey: CONFIG.SUPABASE_KEY,
        Authorization: `Bearer ${CONFIG.SUPABASE_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ lead_id: leadId, resultado }),
    });
    const novoStatus = resultado === "fechou" ? "fechou" : resultado === "nao_atendeu" ? "qualificado" : "em_negociacao";
    await fetch(`${CONFIG.SUPABASE_URL}/rest/v1/leads?id=eq.${leadId}`, {
      method: "PATCH",
      headers: {
        apikey: CONFIG.SUPABASE_KEY,
        Authorization: `Bearer ${CONFIG.SUPABASE_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ status: novoStatus }),
    });
    return { ok: true };
  },
};

window.DataSource = DataSource;
window.CONFIG = CONFIG;

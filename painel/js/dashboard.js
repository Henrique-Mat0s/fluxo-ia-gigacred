// Página "Dashboard" — métricas agregadas (vem do backend).

const $ = (sel) => document.querySelector(sel);

const BACKEND_URL = (function() {
  const q = new URLSearchParams(location.search).get("backend");
  if (q) return q;
  if (location.hostname.includes("github.io")) {
    return null;  // sem backend deployado → usa mock embarcado
  }
  return "http://localhost:3000";
})();

const PRODUTO_LABEL = {
  fgts: "Antecipação FGTS",
  consignado_inss: "Consignado INSS",
  consignado_privado: "Consignado Privado",
  outro: "Outros",
};

async function carregar() {
  let metricas;
  try {
    if (BACKEND_URL) {
      const r = await fetch(`${BACKEND_URL}/api/dashboard/metricas`);
      if (!r.ok) throw new Error(`Backend ${r.status}`);
      metricas = await r.json();
    } else {
      throw new Error("sem backend");
    }
  } catch (e) {
    metricas = mockMetricas();
  }

  const badge = $("#badge-fonte");
  if (metricas.modoMock) {
    badge.textContent = "MODO DEMO (dados mock)";
    badge.className = "badge-data-source mock";
  } else {
    badge.textContent = "AO VIVO";
    badge.className = "badge-data-source live";
  }

  renderKpis(metricas);
  renderFunil(metricas.funil_hoje);
  renderProduto(metricas.por_produto_30d);
  renderBancos(metricas.por_banco_30d);

  // Badge contador
  try {
    const leads = await DataSource.getLeadsPraLigar();
    $("#badge-ligar").textContent = leads.length;
  } catch {}
}

function renderKpis(m) {
  const h = m.hoje;
  const fmt = (n) => n.toLocaleString("pt-BR");
  const fmtMoeda = (n) => n.toLocaleString("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 0 });

  $("#kpis").innerHTML = `
    <div class="kpi">
      <div class="kpi-label">Leads recebidos hoje</div>
      <div class="kpi-big primary">${fmt(h.recebidos)}</div>
      <div class="kpi-sub">${fmt(h.em_conversa)} em conversa agora</div>
    </div>
    <div class="kpi">
      <div class="kpi-label">Qualificados pela IA</div>
      <div class="kpi-big success">${fmt(h.qualificados)}</div>
      <div class="kpi-sub">${h.recebidos > 0 ? Math.round(h.qualificados / h.recebidos * 100) : 0}% taxa de qualificação</div>
    </div>
    <div class="kpi">
      <div class="kpi-label">Fechados hoje</div>
      <div class="kpi-big success">${fmt(h.fechados)}</div>
      <div class="kpi-sub">${m.taxa_conversao_pct}% conversão</div>
    </div>
    <div class="kpi">
      <div class="kpi-label">Volume liberado (30d)</div>
      <div class="kpi-big header">${fmtMoeda(m.volume_liberado_30d)}</div>
      <div class="kpi-sub">ticket médio ${fmtMoeda(m.ticket_medio)}</div>
    </div>
  `;
}

function renderFunil(funil) {
  const max = Math.max(...funil.map(f => f.qtd), 1);
  $("#funil").innerHTML = funil.map(f => {
    const pct = (f.qtd / max) * 100;
    const cor = f.nome === "Fecharam" ? "var(--c-header)"
             : f.nome === "Closer ligou" || f.nome === "Qualificados" ? "var(--c-success)"
             : "var(--c-primary)";
    return `
      <div class="funil-row">
        <div class="funil-label">${f.nome}</div>
        <div class="funil-bar-wrap">
          <div class="funil-bar" style="width:${pct}%; background:${cor};"></div>
        </div>
        <div class="funil-qtd">${f.qtd}</div>
      </div>
    `;
  }).join("");
}

function renderProduto(produtos) {
  if (!produtos || produtos.length === 0) {
    $("#por-produto").innerHTML = `<div class="empty">Sem dados</div>`;
    return;
  }
  const max = Math.max(...produtos.map(p => p.qtd), 1);
  $("#por-produto").innerHTML = produtos.map(p => {
    const pct = (p.qtd / max) * 100;
    return `
      <div class="bar-row">
        <div class="bar-label">${PRODUTO_LABEL[p.produto] || p.produto}</div>
        <div class="bar-bar-wrap">
          <div class="bar-bar" style="width:${pct}%;"></div>
        </div>
        <div class="bar-qtd">${p.qtd}</div>
      </div>
    `;
  }).join("");
}

function renderBancos(bancos) {
  if (!bancos || bancos.length === 0) {
    $("#por-banco").innerHTML = `<div class="empty">Sem fechamentos ainda</div>`;
    return;
  }
  const max = Math.max(...bancos.map(b => b.volume), 1);
  const fmt = (v) => v.toLocaleString("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 0 });
  $("#por-banco").innerHTML = bancos.map(b => {
    const pct = (b.volume / max) * 100;
    return `
      <div class="bar-row">
        <div class="bar-label">${b.banco}</div>
        <div class="bar-bar-wrap">
          <div class="bar-bar success" style="width:${pct}%;"></div>
        </div>
        <div class="bar-qtd">${fmt(b.volume)}</div>
      </div>
    `;
  }).join("");
}

function mockMetricas() {
  return {
    hoje: {
      recebidos: 47, em_conversa: 11, qualificados: 23, fechados: 11, perdidos: 2,
    },
    funil_hoje: [
      { nome: "Recebidos", qtd: 47 },
      { nome: "Em conversa IA", qtd: 34 },
      { nome: "Qualificados", qtd: 23 },
      { nome: "Closer ligou", qtd: 18 },
      { nome: "Fecharam", qtd: 11 },
    ],
    por_produto_30d: [
      { produto: "fgts", qtd: 247 },
      { produto: "consignado_inss", qtd: 68 },
      { produto: "consignado_privado", qtd: 31 },
      { produto: "outro", qtd: 9 },
    ],
    volume_liberado_30d: 58420,
    por_banco_30d: [
      { banco: "BMG",      volume: 142000 },
      { banco: "Daycoval", volume: 98000 },
      { banco: "C6 Bank",  volume: 76000 },
      { banco: "Pan",      volume: 41000 },
    ],
    ticket_medio: 5310,
    taxa_conversao_pct: 23.4,
    modoMock: true,
  };
}

carregar();
setInterval(carregar, 30000);

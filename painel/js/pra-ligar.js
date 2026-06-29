// Página "Pra Ligar" — lista de leads qualificados aguardando contato.

const $ = (sel) => document.querySelector(sel);

async function carregar() {
  const badge = $("#badge-fonte");
  if (DataSource.isMock()) {
    badge.textContent = "MODO DEMO (dados mock)";
    badge.className = "badge-data-source mock";
  } else {
    badge.textContent = "AO VIVO";
    badge.className = "badge-data-source live";
  }

  const leads = await DataSource.getLeadsPraLigar();
  $("#badge-ligar").textContent = leads.length;

  const lista = $("#lista-leads");

  if (leads.length === 0) {
    lista.innerHTML = `<div class="empty">
      <h3>Nenhum lead aguardando ligação</h3>
      <p>Quando a IA qualificar alguém, aparece aqui.</p>
    </div>`;
    return;
  }

  lista.innerHTML = leads.map(l => renderLead(l)).join("");

  // Liga handlers dos botões
  document.querySelectorAll("[data-acao]").forEach(btn => {
    btn.addEventListener("click", async (e) => {
      e.stopPropagation();
      const card = e.target.closest("[data-lead-id]");
      const leadId = card.dataset.leadId;
      const acao = btn.dataset.acao;

      btn.disabled = true;
      btn.textContent = "...";
      await DataSource.marcarComoLigado(leadId, acao);
      card.classList.add("removendo");
      setTimeout(carregar, 400);
    });
  });

  // Botão "WhatsApp" abre direto no WhatsApp Web
  document.querySelectorAll("[data-tel]").forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const tel = btn.dataset.tel.replace(/\D/g, "");
      window.open(`https://wa.me/${tel}`, "_blank");
    });
  });
}

function fmtMoeda(v) {
  return v.toLocaleString("pt-BR", { style: "currency", currency: "BRL", minimumFractionDigits: 0 });
}

function scoreClass(score) {
  if (score >= 80) return "high";
  if (score >= 60) return "mid";
  return "low";
}

function renderLead(l) {
  return `
    <div class="lead-card" data-lead-id="${l.id}">
      <div class="lead-card-header">
        <div class="avatar">${l.iniciais}</div>
        <div class="lead-info">
          <div class="lead-name">${l.nome}</div>
          <div class="lead-channel">${l.telefone}</div>
        </div>
        <span class="score-pill ${scoreClass(l.score)}">${l.score}</span>
      </div>

      <div class="lead-card-body">
        <div class="lead-resumo">${l.resumo}</div>
        <div class="lead-tags">
          <span class="product-tag">${l.produto}</span>
          <span class="valor-est">${fmtMoeda(l.valor_estimado)}</span>
          <span class="lead-tempo">${l.qualificado_ha}</span>
        </div>
      </div>

      <div class="lead-card-actions">
        <button class="btn" data-tel="${l.telefone}">📞 Ligar</button>
        <button class="btn secondary" data-tel="${l.telefone}">WhatsApp</button>
      </div>

      <div class="lead-card-outcome">
        <span class="hint">Depois da ligação:</span>
        <button class="outcome-btn fechou" data-acao="fechou">Fechou</button>
        <button class="outcome-btn pensar" data-acao="vai_pensar">Vai pensar</button>
        <button class="outcome-btn nao-fechou" data-acao="nao_fechou">Não fechou</button>
        <button class="outcome-btn nao-atendeu" data-acao="nao_atendeu">Não atendeu</button>
      </div>
    </div>
  `;
}

carregar();

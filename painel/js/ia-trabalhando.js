// Página "IA Trabalhando" — mostra conversas ativas em tempo real.

const $ = (sel) => document.querySelector(sel);

async function carregar() {
  // Badge de fonte (mock vs real)
  const badge = $("#badge-fonte");
  if (DataSource.isMock()) {
    badge.textContent = "MODO DEMO (dados mock)";
    badge.className = "badge-data-source mock";
  } else {
    badge.textContent = "AO VIVO";
    badge.className = "badge-data-source live";
  }

  // Status da Evolution
  const inst = await DataSource.getInstanciaStatus();
  const dot = $("#instancia-dot");
  const txt = $("#instancia-texto");
  if (inst.estado === "open") {
    dot.style.background = "#22c55e";
    txt.innerHTML = `Evolution conectada · ${inst.numero} · ${inst.mensagens_hoje}/${inst.limite_dia} mensagens hoje`;
  } else {
    dot.style.background = "#dc3545";
    txt.innerHTML = `Evolution desconectada (estado: ${inst.estado}) — gere novo QR nas configurações`;
  }

  // Conversas ativas
  const conversas = await DataSource.getConversasAtivas();
  const lista = $("#lista-conversas");

  if (conversas.length === 0) {
    lista.innerHTML = `<div class="empty">
      <h3>Nenhuma conversa ativa agora</h3>
      <p>Quando alguém responder a IA, aparece aqui em tempo real.</p>
    </div>`;
    return;
  }

  lista.innerHTML = conversas.map(c => renderConversa(c)).join("");

  // Badge contador de leads pra ligar
  const leads = await DataSource.getLeadsPraLigar();
  $("#badge-ligar").textContent = leads.length;
}

function scoreClass(score) {
  if (score >= 80) return "high";
  if (score >= 60) return "mid";
  return "low";
}

function proximaAcaoLabel(acao) {
  return {
    aguardando_resposta: "Aguardando lead responder",
    qualificando: "IA qualificando",
    ia_digitando: "IA está digitando...",
    removido: "Lead removido (pediu pra parar)",
  }[acao] || acao;
}

function renderConversa(c) {
  const isRemovido = c.proxima_acao === "removido";
  const isPronto   = c.score_atual >= 80;
  const isDigitando = c.ia_digitando;

  return `
    <div class="conversa-card ${isPronto ? 'pronto' : ''} ${isRemovido ? 'removido' : ''}">
      <div class="conversa-header">
        <div class="avatar">${c.iniciais}</div>
        <div class="conversa-info">
          <div class="lead-name">${c.nome}</div>
          <div class="lead-channel">${c.telefone} · iniciou ${c.iniciou_em}</div>
        </div>
        <div class="conversa-meta">
          <span class="score-pill ${scoreClass(c.score_atual)}">${c.score_atual}</span>
          <div class="msg-count">${c.mensagens_trocadas} msgs</div>
        </div>
      </div>

      <div class="conversa-msgs">
        ${c.ultima_msg_lead ? `
          <div class="msg msg-lead">
            <div class="msg-label">Lead</div>
            <div class="msg-text">"${c.ultima_msg_lead}"</div>
          </div>` : ""}
        ${isDigitando ? `
          <div class="msg msg-ia digitando">
            <div class="msg-label">Giovanna (IA)</div>
            <div class="msg-text"><span class="dot-typing"></span><span class="dot-typing"></span><span class="dot-typing"></span> digitando resposta...</div>
          </div>` : (c.ultima_msg_ia ? `
          <div class="msg msg-ia">
            <div class="msg-label">Giovanna (IA)</div>
            <div class="msg-text">"${c.ultima_msg_ia}"</div>
          </div>` : "")}
      </div>

      <div class="conversa-footer">
        <span class="proximo">▸ ${proximaAcaoLabel(c.proxima_acao)}</span>
        ${isPronto ? '<span class="badge-pronto">PRONTO PRA HANDOFF</span>' : ""}
      </div>
    </div>
  `;
}

carregar();

// Atualiza a cada 8 segundos (simulação de tempo real)
setInterval(carregar, 8000);

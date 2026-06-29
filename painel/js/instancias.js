// Tela "Chips" — gerencia instâncias da Evolution.

const $ = (sel) => document.querySelector(sel);

const BACKEND_URL = (function() {
  const q = new URLSearchParams(location.search).get("backend");
  if (q) return q;
  if (location.hostname.includes("github.io")) return null;
  return "http://localhost:3000";
})();

// Mock pra quando não tem backend
const MOCK_INSTANCIAS = [
  {
    id: "i1",
    nome: "gigacred-bot-01",
    numero: "+55 31 99988-7766",
    estado: "open",
    ativa: true,
    ordem_disparo: 1,
    mensagens_hoje: 87,
    bloqueios_hoje: 2,
    limite_dia: 150,
    observacao: "Chip principal",
  },
  {
    id: "i2",
    nome: "gigacred-bot-02",
    numero: "+55 31 98877-6655",
    estado: "open",
    ativa: true,
    ordem_disparo: 2,
    mensagens_hoje: 64,
    bloqueios_hoje: 1,
    limite_dia: 150,
    observacao: "Chip 2 — em rotação",
  },
];

async function carregar() {
  const badge = $("#badge-fonte");
  let lista;
  let isMock = false;

  if (BACKEND_URL) {
    try {
      const r = await fetch(`${BACKEND_URL}/api/instancias`);
      if (!r.ok) throw new Error(`Backend ${r.status}`);
      lista = await r.json();
      badge.textContent = "AO VIVO";
      badge.className = "badge-data-source live";
    } catch (e) {
      lista = MOCK_INSTANCIAS;
      isMock = true;
      badge.textContent = "MODO DEMO (backend offline)";
      badge.className = "badge-data-source mock";
    }
  } else {
    lista = MOCK_INSTANCIAS;
    isMock = true;
    badge.textContent = "MODO DEMO (dados mock)";
    badge.className = "badge-data-source mock";
  }

  renderResumo(lista);
  renderLista(lista, isMock);

  // badge contador de leads pra ligar
  try {
    const leads = await DataSource.getLeadsPraLigar();
    $("#badge-ligar").textContent = leads.length;
  } catch {}
}

function renderResumo(lista) {
  const conectados = lista.filter(i => i.estado === "open").length;
  const msgs = lista.reduce((s, i) => s + (i.mensagens_hoje || 0), 0);
  const capacidade = lista
    .filter(i => i.ativa && i.estado === "open")
    .reduce((s, i) => s + Math.max(0, (i.limite_dia || 150) - (i.mensagens_hoje || 0)), 0);
  const bloqueios = lista.reduce((s, i) => s + (i.bloqueios_hoje || 0), 0);

  $("#r-conectados").innerHTML = `${conectados} <span class="muted">de ${lista.length}</span>`;
  $("#r-mensagens").textContent = msgs;
  $("#r-capacidade").textContent = capacidade;
  $("#r-bloqueios").innerHTML = bloqueios > 0
    ? `<span style="color:var(--c-danger)">${bloqueios}</span>`
    : `<span style="color:var(--c-success)">0</span>`;
}

function renderLista(lista, isMock) {
  const cont = $("#lista-instancias");
  if (lista.length === 0) {
    cont.innerHTML = `<div class="empty">
      <h3>Nenhum chip cadastrado ainda</h3>
      <p>Clique em "Adicionar novo chip" pra começar.</p>
    </div>`;
    return;
  }

  cont.innerHTML = lista.map(i => renderCard(i, isMock)).join("");

  document.querySelectorAll("[data-toggle-ativa]").forEach(el => {
    el.addEventListener("change", async (e) => {
      const id = e.target.dataset.toggleAtiva;
      const ativa = e.target.checked;
      if (BACKEND_URL) {
        await fetch(`${BACKEND_URL}/api/instancias/${id}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ativa }),
        });
      }
      carregar();
    });
  });

  document.querySelectorAll("[data-qr]").forEach(b => {
    b.addEventListener("click", () => abrirQR(b.dataset.qr));
  });

  document.querySelectorAll("[data-desconectar]").forEach(b => {
    b.addEventListener("click", async () => {
      if (!confirm("Desconectar este chip? Será necessário escanear QR de novo.")) return;
      if (BACKEND_URL) {
        await fetch(`${BACKEND_URL}/api/instancias/${b.dataset.desconectar}/desconectar`, {
          method: "POST",
        });
      }
      carregar();
    });
  });
}

function renderCard(i, isMock) {
  const limite = i.limite_dia || 150;
  const pctUso = Math.min(100, ((i.mensagens_hoje || 0) / limite) * 100);
  const corBarra = pctUso > 80 ? "var(--c-danger)" : pctUso > 60 ? "var(--c-warning)" : "var(--c-primary)";

  const estadoLabel = {
    open: { txt: "Conectado", cor: "var(--c-success)", dot: "var(--c-success)" },
    connecting: { txt: "Conectando", cor: "var(--c-warning)", dot: "var(--c-warning)" },
    close: { txt: "Desconectado", cor: "var(--c-danger)", dot: "var(--c-danger)" },
    desconhecido: { txt: "Desconhecido", cor: "var(--c-muted)", dot: "var(--c-muted)" },
  }[i.estado] || { txt: i.estado, cor: "var(--c-muted)", dot: "var(--c-muted)" };

  return `
    <div class="card instancia-card">
      <div class="instancia-header">
        <div>
          <div class="lead-name">${i.nome}</div>
          <div class="lead-channel">${i.numero || "(não conectado ainda)"}</div>
          ${i.observacao ? `<div class="obs">${escapeHtml(i.observacao)}</div>` : ""}
        </div>
        <div class="estado-pill">
          <span class="dot" style="background:${estadoLabel.dot}"></span>
          <span style="color:${estadoLabel.cor}; font-weight:700;">${estadoLabel.txt}</span>
        </div>
      </div>

      <div class="instancia-metricas">
        <div class="kv">
          <div class="label">Mensagens hoje</div>
          <div class="value">${i.mensagens_hoje || 0} <span class="muted">/ ${limite}</span></div>
          <div class="sla-bar" style="margin-top:6px;">
            <div style="width:${pctUso}%; background:${corBarra};"></div>
          </div>
        </div>
        <div class="kv">
          <div class="label">Bloqueios hoje</div>
          <div class="value" style="color:${i.bloqueios_hoje > 0 ? 'var(--c-danger)' : 'var(--c-success)'};">${i.bloqueios_hoje || 0}</div>
        </div>
        <div class="kv">
          <div class="label">Na rotação</div>
          <label class="toggle">
            <input type="checkbox" data-toggle-ativa="${i.id}" ${i.ativa ? "checked" : ""} ${isMock ? "disabled" : ""}>
            <span class="slider"></span>
          </label>
        </div>
      </div>

      <div class="instancia-actions">
        <button class="btn secondary" data-qr="${i.id}">Mostrar QR</button>
        ${i.estado === "open"
          ? `<button class="btn secondary danger-outline" data-desconectar="${i.id}">Desconectar</button>`
          : `<button class="btn" data-qr="${i.id}">Conectar</button>`}
      </div>
    </div>
  `;
}

function abrirQR(id) {
  $("#modal-qr").style.display = "flex";
  $("#qr-imagem").innerHTML = "Carregando QR...";
  if (!BACKEND_URL) {
    $("#qr-imagem").innerHTML = `<div class="msg-info aviso">Modo demo: QR não disponível. Conecte o backend pra ver o QR real.</div>`;
    return;
  }
  fetch(`${BACKEND_URL}/api/instancias/${id}/qr`).then(r => r.json()).then(data => {
    if (data.qrcode) {
      const img = data.qrcode.startsWith("data:") ? data.qrcode : `data:image/png;base64,${data.qrcode}`;
      $("#qr-imagem").innerHTML = `<img src="${img}" alt="QR Code">`;
    } else if (data.pairingCode) {
      $("#qr-imagem").innerHTML = `<div class="pairing-code">Código de pareamento: <b>${data.pairingCode}</b></div>`;
    } else {
      $("#qr-imagem").innerHTML = `<div class="msg-info erro">${data.erro || "QR não disponível agora"}</div>`;
    }
  }).catch(e => {
    $("#qr-imagem").innerHTML = `<div class="msg-info erro">Erro: ${e.message}</div>`;
  });
}

function escapeHtml(s) {
  const d = document.createElement("div");
  d.textContent = s;
  return d.innerHTML;
}

// Modal novo
$("#btn-novo").addEventListener("click", () => {
  $("#modal-novo").style.display = "flex";
  $("#novo-nome").value = "";
  $("#novo-obs").value = "";
  $("#novo-erro").style.display = "none";
  $("#novo-nome").focus();
});
$("#btn-cancelar").addEventListener("click", () => {
  $("#modal-novo").style.display = "none";
});
$("#btn-criar").addEventListener("click", async () => {
  const nome = $("#novo-nome").value.trim();
  const obs = $("#novo-obs").value.trim();
  if (!/^[a-z0-9-]+$/.test(nome)) {
    $("#novo-erro").textContent = "Nome inválido. Use só letras minúsculas, números e hífen.";
    $("#novo-erro").style.display = "block";
    return;
  }
  if (!BACKEND_URL) {
    $("#novo-erro").textContent = "Modo demo: criação real só funciona com o backend rodando.";
    $("#novo-erro").style.display = "block";
    return;
  }
  $("#btn-criar").disabled = true;
  try {
    const r = await fetch(`${BACKEND_URL}/api/instancias`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nome, observacao: obs || null }),
    });
    const data = await r.json();
    if (!r.ok) {
      $("#novo-erro").textContent = data.erro || "Erro";
      $("#novo-erro").style.display = "block";
      return;
    }
    $("#modal-novo").style.display = "none";
    // Mostra QR direto
    $("#modal-qr").style.display = "flex";
    if (data.qrcode) {
      const img = data.qrcode.startsWith("data:") ? data.qrcode : `data:image/png;base64,${data.qrcode}`;
      $("#qr-imagem").innerHTML = `<img src="${img}" alt="QR Code">`;
    } else if (data.pairingCode) {
      $("#qr-imagem").innerHTML = `<div class="pairing-code">Código de pareamento: <b>${data.pairingCode}</b></div>`;
    } else {
      $("#qr-imagem").innerHTML = `<div class="msg-info aviso">Instância criada. Escaneie o QR em "Mostrar QR" do card.</div>`;
    }
    carregar();
  } finally {
    $("#btn-criar").disabled = false;
  }
});

$("#btn-fechar-qr").addEventListener("click", () => {
  $("#modal-qr").style.display = "none";
});
$("#btn-atualizar-qr").addEventListener("click", () => {
  carregar();
});

carregar();
setInterval(carregar, 15000);  // refresh a cada 15s pra ver mudanças de estado

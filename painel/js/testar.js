// Página "Testar Giovanna" — chat stateless com a IA via backend.

const $ = (sel) => document.querySelector(sel);

// URL do backend — se rodar local, http://localhost:3000.
// Em produção (painel no GitHub Pages), aponta pro backend deployado.
const BACKEND_URL = (function() {
  // Permite override via ?backend=URL na query string
  const q = new URLSearchParams(location.search).get("backend");
  if (q) return q;
  // Se está no GitHub Pages, usa um placeholder (vc edita aqui depois do deploy)
  if (location.hostname.includes("github.io")) {
    return "https://SEU_BACKEND_AQUI.com";  // <-- TROCAR depois do deploy
  }
  return "http://localhost:3000";
})();

const historico = [];

const CENARIOS = {
  quente: [
    "Oi, queria antecipar meu FGTS, urgente",
    "Sim, já fiz a adesão",
    "Acho que tenho uns 12 mil",
    "Preciso pagar uma dívida que vence essa semana",
    "Sou CLT, trabalho na mesma empresa há 5 anos",
  ],
  frio: [
    "vi seu anuncio",
    "nao sei se ja fiz isso na caixa",
    "deve ter uns 500 reais",
    "nao tenho nada urgente",
  ],
  confuso: [
    "oi",
    "o que voce faz mesmo?",
    "nao sei como funciona",
    "tenho FGTS mas nao sei quanto",
  ],
  agressivo: [
    "para de me mandar mensagem",
    "como vc pegou meu numero?",
    "nao tenho interesse, me bloqueia",
  ],
};

// Init
$("#badge-fonte").textContent = "BACKEND: " + BACKEND_URL;
$("#badge-fonte").className = "badge-data-source live";

renderHist();

async function enviar() {
  const input = $("#input-msg");
  const texto = input.value.trim();
  if (!texto) return;

  input.value = "";
  input.disabled = true;
  $("#btn-enviar").disabled = true;

  // Adiciona msg do lead
  historico.push({ autor: "lead", texto });
  renderHist();
  mostrarDigitando(true);

  try {
    const r = await fetch(`${BACKEND_URL}/api/test/conversa`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        historico: historico.slice(0, -1),  // tudo menos a última (que é a "novaMensagem")
        novaMensagem: texto,
      }),
    });

    if (!r.ok) {
      throw new Error(`Backend respondeu ${r.status}`);
    }

    const resposta = await r.json();
    mostrarDigitando(false);

    if (resposta.erro) {
      renderErro(resposta.erro);
      return;
    }

    // Adiciona msg da IA
    historico.push({
      autor: "ia",
      texto: resposta.reply,
      qualificacao: resposta.qualificacao,
      meta: resposta._meta,
    });
    renderHist();
    atualizarPainel(resposta);

    if (resposta._meta?.modoMock) {
      mostrarAviso(resposta._meta.aviso);
    }
  } catch (e) {
    mostrarDigitando(false);
    renderErro(`Falha ao chamar backend: ${e.message}\n\nVerifique se o backend está rodando em ${BACKEND_URL}`);
  } finally {
    input.disabled = false;
    $("#btn-enviar").disabled = false;
    input.focus();
  }
}

function renderHist() {
  const cont = $("#chat-msgs");
  if (historico.length === 0) {
    cont.innerHTML = `<div class="msg-info">Mande uma mensagem pra começar. Digite como se fosse um lead.</div>`;
    return;
  }
  cont.innerHTML = historico.map((m, i) => {
    if (m.autor === "lead") {
      return `<div class="bubble lead-bubble">${escapeHtml(m.texto)}</div>`;
    }
    return `<div class="bubble ia-bubble">${escapeHtml(m.texto)}</div>`;
  }).join("");
  cont.scrollTop = cont.scrollHeight;
}

function mostrarDigitando(on) {
  const cont = $("#chat-msgs");
  const existente = cont.querySelector(".digitando-msg");
  if (existente) existente.remove();
  if (on) {
    cont.insertAdjacentHTML("beforeend",
      `<div class="bubble ia-bubble digitando-msg"><span class="dot-typing"></span><span class="dot-typing"></span><span class="dot-typing"></span></div>`
    );
    cont.scrollTop = cont.scrollHeight;
  }
}

function renderErro(msg) {
  const cont = $("#chat-msgs");
  cont.insertAdjacentHTML("beforeend",
    `<div class="msg-info erro">⚠ ${escapeHtml(msg)}</div>`
  );
  cont.scrollTop = cont.scrollHeight;
}

function mostrarAviso(msg) {
  const cont = $("#chat-msgs");
  cont.insertAdjacentHTML("beforeend",
    `<div class="msg-info aviso">ℹ ${escapeHtml(msg)}</div>`
  );
  cont.scrollTop = cont.scrollHeight;
}

function atualizarPainel(resposta) {
  const q = resposta.qualificacao || {};
  $("#score-atual").textContent = q.score ?? "—";
  $("#acao-atual").textContent = q.acao_recomendada ?? "—";
  $("#turnos").textContent = Math.ceil(historico.length / 2);
  if (resposta._meta?.latency_ms) {
    $("#latencia").textContent = `${resposta._meta.latency_ms} ms`;
  }
  // Cor do score
  const el = $("#score-atual");
  el.style.color = (q.score ?? 0) >= 80 ? "var(--c-success)"
                 : (q.score ?? 0) >= 60 ? "var(--c-warning)"
                 : "var(--c-muted)";
}

function escapeHtml(s) {
  const d = document.createElement("div");
  d.textContent = s;
  return d.innerHTML;
}

// Event handlers
$("#btn-enviar").addEventListener("click", enviar);
$("#input-msg").addEventListener("keydown", e => {
  if (e.key === "Enter") enviar();
});

$("#btn-reset").addEventListener("click", () => {
  if (historico.length > 0 && !confirm("Resetar a conversa atual?")) return;
  historico.length = 0;
  renderHist();
  $("#score-atual").textContent = "0";
  $("#score-atual").style.color = "";
  $("#acao-atual").textContent = "—";
  $("#turnos").textContent = "0";
  $("#latencia").textContent = "—";
});

$("#btn-cenarios").addEventListener("click", () => {
  const m = $("#cenarios-menu");
  m.style.display = m.style.display === "none" ? "block" : "none";
});

document.querySelectorAll("[data-cenario]").forEach(b => {
  b.addEventListener("click", async () => {
    if (historico.length > 0 && !confirm("Resetar conversa atual e rodar cenário?")) return;
    historico.length = 0;
    renderHist();
    $("#cenarios-menu").style.display = "none";
    const seq = CENARIOS[b.dataset.cenario];
    for (const msg of seq) {
      $("#input-msg").value = msg;
      await enviar();
      await new Promise(r => setTimeout(r, 600));  // pequena pausa entre msgs
    }
  });
});

// Carrega contador de leads pra ligar (badge no nav)
(async () => {
  try {
    const leads = await DataSource.getLeadsPraLigar();
    $("#badge-ligar").textContent = leads.length;
  } catch {}
})();

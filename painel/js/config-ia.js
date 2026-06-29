// Página "Configurações da IA"

const $ = (sel) => document.querySelector(sel);

const PROMPT_PADRAO = `Você é a Bia, consultora virtual da GIGACRED Correspondente.
Sua função é qualificar leads que querem antecipar FGTS, INSS ou consignado privado.

REGRAS:
- Tom caloroso, direto, brasileiro. Sem formalidades excessivas.
- NUNCA mais de 2 frases por mensagem.
- UMA pergunta por mensagem.
- Se o lead não fez adesão ao Saque-Aniversário, EXPLIQUE como fazer no app FGTS.
- NUNCA dê taxa específica ou prometa aprovação — isso é função do closer.

O QUE DESCOBRIR (BANT adaptado):
1. Saldo FGTS estimado
2. Adesão ao Saque-Aniversário (CRITÉRIO ELIMINATÓRIO)
3. Motivo do dinheiro
4. Urgência
5. Vínculo de trabalho`;

async function carregar() {
  const badge = $("#badge-fonte");
  if (DataSource.isMock()) {
    badge.textContent = "MODO DEMO (dados mock)";
    badge.className = "badge-data-source mock";
  } else {
    badge.textContent = "AO VIVO";
    badge.className = "badge-data-source live";
  }

  // Status IA
  const cfg = await DataSource.getConfigIA();
  $("#toggle-ia").checked = cfg.ativa;
  $("#ia-estado-texto").textContent = cfg.ativa ? "Ativa — respondendo automaticamente" : "Pausada — leads ficam sem resposta";
  $("#ia-estado-texto").className = "status-texto " + (cfg.ativa ? "ok" : "alerta");

  $("#gemini-uso").innerHTML = `${cfg.requisicoes_hoje}/${cfg.limite_dia} chamadas hoje · modelo: <b>${cfg.modelo}</b>`;
  $("#prompt-textarea").value = cfg.system_prompt;

  // Status Evolution
  const inst = await DataSource.getInstanciaStatus();
  const evEstado = $("#evolution-estado");
  if (inst.estado === "open") {
    evEstado.innerHTML = `<span class="status-ok">● Conectada</span> · ${inst.numero}`;
  } else {
    evEstado.innerHTML = `<span class="status-alerta">● Desconectada</span> · gere novo QR`;
  }

  $("#ev-instancia").textContent = inst.nome;
  $("#ev-numero").textContent = inst.numero;
  $("#ev-msgs").innerHTML = `${inst.mensagens_hoje} <span class="muted">/ ${inst.limite_dia}</span>`;
  $("#ev-bloqueio").innerHTML = `${inst.taxa_bloqueio}% <span class="muted">(${inst.bloqueios_hoje} hoje)</span>`;

  // Badge contador de leads pra ligar
  const leads = await DataSource.getLeadsPraLigar();
  $("#badge-ligar").textContent = leads.length;
}

// Toggle IA
$("#toggle-ia").addEventListener("change", async (e) => {
  const ativa = e.target.checked;
  await DataSource.saveConfigIA({ ativa });
  $("#ia-estado-texto").textContent = ativa
    ? "Ativa — respondendo automaticamente"
    : "Pausada — leads ficam sem resposta";
  $("#ia-estado-texto").className = "status-texto " + (ativa ? "ok" : "alerta");
});

// Salvar prompt
$("#btn-salvar-prompt").addEventListener("click", async () => {
  const novo = $("#prompt-textarea").value.trim();
  if (!novo) return alert("Prompt não pode ficar vazio.");
  await DataSource.saveConfigIA({ system_prompt: novo });
  const msg = $("#salvo-msg");
  msg.textContent = "✓ Salvo. As próximas conversas já usam este prompt.";
  msg.className = "salvo-msg ok";
  setTimeout(() => { msg.textContent = ""; }, 4000);
});

// Restaurar padrão
$("#btn-restaurar").addEventListener("click", () => {
  if (!confirm("Restaurar o prompt padrão? A versão atual será perdida.")) return;
  $("#prompt-textarea").value = PROMPT_PADRAO;
});

// Reconectar Evolution (apenas mostra instruções no modo mock)
$("#btn-reconectar").addEventListener("click", () => {
  alert(
    "No ambiente real (Evolution conectada), este botão geraria um novo QR Code.\n\n" +
    "Você abriria no celular → WhatsApp → Configurações → Aparelhos conectados → " +
    "Conectar um aparelho → escaneia o QR.\n\n" +
    "No modo demo, é simulado."
  );
});

carregar();

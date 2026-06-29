// Simula o webhook que a Evolution dispararia ao receber uma mensagem.
// Uso: node scripts/test-webhook.js  (com servidor rodando em :3000)

const BACKEND = process.env.BACKEND_URL || "http://localhost:3000";

const payload = {
  event: "messages.upsert",
  data: {
    key: { remoteJid: "5511999998888@s.whatsapp.net", fromMe: false },
    pushName: "Maria Silva",
    message: { conversation: "Oi! vi seu anuncio sobre antecipar FGTS, quanto consigo?" },
  },
};

console.log(`Enviando webhook simulado para ${BACKEND}/webhook/evolution ...\n`);

const r = await fetch(`${BACKEND}/webhook/evolution`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(payload),
});

const j = await r.json();
console.log(`Status: ${r.status}`);
console.log("Resposta:", JSON.stringify(j, null, 2));

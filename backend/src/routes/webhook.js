// Webhook que a Evolution chama quando uma mensagem nova chega.
// Pra configurar na Evolution: webhook URL = https://SEU_BACKEND/webhook/evolution

import { Router } from "express";
import crypto from "crypto";
import { processarMensagem } from "../services/conversa.js";
import { enviarTexto } from "../evolution/client.js";

const router = Router();
const WEBHOOK_SECRET = process.env.WEBHOOK_SECRET;

// Valida assinatura HMAC opcional (recomendado).
// Evolution suporta envio do header `x-webhook-signature` ou similar.
function validarAssinatura(req) {
  if (!WEBHOOK_SECRET) return true;  // sem segredo definido = não valida
  const sig = req.headers["x-webhook-signature"] || req.headers["x-hub-signature-256"];
  if (!sig) return false;
  const calc = crypto.createHmac("sha256", WEBHOOK_SECRET)
    .update(JSON.stringify(req.body))
    .digest("hex");
  return crypto.timingSafeEqual(Buffer.from(calc), Buffer.from(sig.replace(/^sha256=/, "")));
}

router.post("/evolution", async (req, res) => {
  try {
    if (!validarAssinatura(req)) {
      return res.status(401).json({ erro: "assinatura inválida" });
    }

    const body = req.body;

    // Evolution dispara vários tipos de evento — só processamos messages.upsert
    if (body.event !== "messages.upsert") {
      return res.json({ ignorado: true, motivo: "evento_irrelevante", event: body.event });
    }

    const msg = body.data;
    // Evolution multi-instância: payload tem qual instância recebeu
    const instanciaNome = body.instance || body.instanceName || null;

    // Ignora mensagens do próprio bot (fromMe = true)
    if (msg.key?.fromMe) {
      return res.json({ ignorado: true, motivo: "from_me" });
    }

    // Extrai dados
    const telefone = (msg.key?.remoteJid || "").replace(/@.*$/, "");
    const nome = msg.pushName || null;
    const texto = msg.message?.conversation
      || msg.message?.extendedTextMessage?.text
      || msg.message?.imageMessage?.caption
      || "";

    if (!telefone || !texto) {
      return res.json({ ignorado: true, motivo: "sem_telefone_ou_texto" });
    }

    // Processa (IA Giovanna responde) — passa instância pra a resposta sair pelo mesmo chip
    const r = await processarMensagem({ telefone, nome, texto, instanciaNome });

    // Envia resposta de volta via Evolution pela MESMA instância
    if (r.reply) {
      const delayMs = 1000 + Math.floor(Math.random() * 2000);
      await enviarTexto(telefone, r.reply, { delayMs, instance: instanciaNome });
    }

    res.json({
      ok: true,
      reply_enviado: !!r.reply,
      score: r.score,
      handoff: r.handoff || false,
      acao: r.acao,
    });
  } catch (e) {
    console.error("[webhook] erro:", e);
    res.status(500).json({ erro: e.message });
  }
});

export default router;

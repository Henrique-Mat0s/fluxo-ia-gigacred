// Rotas pra gerenciar instâncias (chips de WhatsApp) da Evolution.

import { Router } from "express";
import {
  listarInstancias, getInstanciaPorId, getInstanciaPorNome,
  criarRegistroInstancia, atualizarInstancia, deletarInstancia,
} from "../db/instancias.js";
import {
  criarInstancia, getQR, getConnectionState, desconectar,
} from "../evolution/client.js";

const router = Router();

/** GET /api/instancias — lista todas + métricas do dia */
router.get("/", async (req, res) => {
  try {
    const arr = await listarInstancias();

    // Atualiza estado consultando a Evolution (best-effort)
    for (const inst of arr) {
      try {
        const st = await getConnectionState(inst.nome);
        const novoEstado = st?.instance?.state || st?.state || "desconhecido";
        if (novoEstado !== inst.estado) {
          await atualizarInstancia(inst.id, { estado: novoEstado });
          inst.estado = novoEstado;
        }
      } catch {
        // Evolution offline ou instância inexistente lá — não bloqueia listagem
      }
    }

    res.json(arr);
  } catch (e) {
    res.status(500).json({ erro: e.message });
  }
});

/** POST /api/instancias — cria nova instância (cria na Evolution + registra no banco) */
router.post("/", async (req, res) => {
  try {
    const { nome, observacao } = req.body || {};
    if (!nome || !/^[a-z0-9-]+$/.test(nome)) {
      return res.status(400).json({ erro: "nome obrigatório (apenas letras minúsculas, números, hífen)" });
    }

    const existente = await getInstanciaPorNome(nome);
    if (existente) {
      return res.status(409).json({ erro: "Já existe instância com esse nome" });
    }

    // Cria na Evolution
    let qrData = null;
    try {
      const resp = await criarInstancia(nome);
      qrData = resp;
    } catch (e) {
      return res.status(500).json({ erro: `Falha ao criar na Evolution: ${e.message}` });
    }

    // Registra no banco
    const inst = await criarRegistroInstancia({ nome, observacao });

    res.json({
      ok: true,
      instancia: inst,
      qrcode: qrData?.qrcode?.base64 || qrData?.base64 || null,
      pairingCode: qrData?.qrcode?.pairingCode || qrData?.pairingCode || null,
    });
  } catch (e) {
    res.status(500).json({ erro: e.message });
  }
});

/** GET /api/instancias/:id/qr — pega QR atual pra escanear */
router.get("/:id/qr", async (req, res) => {
  try {
    const inst = await getInstanciaPorId(req.params.id);
    if (!inst) return res.status(404).json({ erro: "Instância não encontrada" });

    const data = await getQR(inst.nome);
    res.json({
      nome: inst.nome,
      qrcode: data?.base64 || data?.qrcode?.base64 || null,
      pairingCode: data?.pairingCode || data?.qrcode?.pairingCode || null,
      raw: data,
    });
  } catch (e) {
    res.status(500).json({ erro: e.message });
  }
});

/** PATCH /api/instancias/:id — ativa/pausa, atualiza observação ou limite */
router.patch("/:id", async (req, res) => {
  try {
    const permitidos = ["ativa", "observacao", "limite_dia", "ordem_disparo", "numero"];
    const patch = {};
    for (const k of permitidos) {
      if (req.body[k] !== undefined) patch[k] = req.body[k];
    }
    const inst = await atualizarInstancia(req.params.id, patch);
    res.json(inst);
  } catch (e) {
    res.status(500).json({ erro: e.message });
  }
});

/** POST /api/instancias/:id/desconectar — força logout (gera necessidade de novo QR) */
router.post("/:id/desconectar", async (req, res) => {
  try {
    const inst = await getInstanciaPorId(req.params.id);
    if (!inst) return res.status(404).json({ erro: "Não encontrada" });
    await desconectar(inst.nome);
    await atualizarInstancia(inst.id, { estado: "close" });
    res.json({ ok: true });
  } catch (e) {
    res.status(500).json({ erro: e.message });
  }
});

/** DELETE /api/instancias/:id — remove o registro local (não desfaz na Evolution) */
router.delete("/:id", async (req, res) => {
  try {
    await deletarInstancia(req.params.id);
    res.json({ ok: true });
  } catch (e) {
    res.status(500).json({ erro: e.message });
  }
});

export default router;

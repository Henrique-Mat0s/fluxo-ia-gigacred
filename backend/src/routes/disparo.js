// Rotas de disparo em massa e API administrativa.

import { Router } from "express";
import { iniciarDisparo, disparoStatus } from "../services/disparador.js";
import {
  getIAConfig, updateIAConfig,
  getLeadsByStatus, contarDisparosHoje, contarBloqueadosHoje,
} from "../db/supabase.js";
import { getConnectionState } from "../evolution/client.js";

const router = Router();

// --- Disparo ---
router.post("/disparo/iniciar", async (req, res) => {
  try {
    const r = await iniciarDisparo();
    res.json(r);
  } catch (e) {
    res.status(500).json({ erro: e.message });
  }
});

router.get("/disparo/status", async (req, res) => {
  try {
    const enviados = await contarDisparosHoje();
    const bloqueados = await contarBloqueadosHoje();
    res.json({
      ...disparoStatus(),
      enviados_hoje: enviados,
      bloqueados_hoje: bloqueados,
      taxa_bloqueio_pct: enviados > 0 ? +(bloqueados / enviados * 100).toFixed(2) : 0,
    });
  } catch (e) {
    res.status(500).json({ erro: e.message });
  }
});

// --- Config IA ---
router.get("/config", async (req, res) => {
  try {
    const c = await getIAConfig();
    res.json(c);
  } catch (e) {
    res.status(500).json({ erro: e.message });
  }
});

router.patch("/config", async (req, res) => {
  try {
    const permitidos = ["ativa", "system_prompt", "modelo"];
    const patch = {};
    for (const k of permitidos) {
      if (req.body[k] !== undefined) patch[k] = req.body[k];
    }
    const c = await updateIAConfig(patch);
    res.json(c);
  } catch (e) {
    res.status(500).json({ erro: e.message });
  }
});

// --- Leads ---
router.get("/leads/qualificados", async (req, res) => {
  try {
    const leads = await getLeadsByStatus("qualificado", 50);
    res.json(leads);
  } catch (e) {
    res.status(500).json({ erro: e.message });
  }
});

router.get("/leads/em-conversa", async (req, res) => {
  try {
    const leads = await getLeadsByStatus("em_conversa", 50);
    res.json(leads);
  } catch (e) {
    res.status(500).json({ erro: e.message });
  }
});

// --- Status geral ---
router.get("/status", async (req, res) => {
  try {
    let evolution = null;
    try {
      evolution = await getConnectionState();
    } catch (e) {
      evolution = { erro: e.message };
    }
    const config = await getIAConfig();
    const enviados = await contarDisparosHoje();
    res.json({
      ia: { ativa: config?.ativa, modelo: config?.modelo },
      evolution,
      disparo: { ...disparoStatus(), enviados_hoje: enviados },
      uptime_s: Math.round(process.uptime()),
    });
  } catch (e) {
    res.status(500).json({ erro: e.message });
  }
});

export default router;

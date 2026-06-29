// Endpoint que agrega métricas pro dashboard.

import { Router } from "express";

const router = Router();

const url = process.env.SUPABASE_URL;
const key = process.env.SUPABASE_SERVICE_KEY;

async function supaSelect(path) {
  if (!url || !key) return null;
  const r = await fetch(`${url}/rest/v1/${path}`, {
    headers: { apikey: key, Authorization: `Bearer ${key}` },
  });
  if (!r.ok) throw new Error(`Supabase ${r.status}: ${await r.text()}`);
  return r.json();
}

/**
 * GET /api/dashboard/metricas
 * Retorna agregados do dia + 30 dias.
 */
router.get("/metricas", async (req, res) => {
  try {
    // Se Supabase não configurado, devolve mock
    if (!url || !key) {
      return res.json(mockMetricas());
    }

    const hoje = new Date().toISOString().slice(0, 10);
    const inicio30 = new Date(Date.now() - 30 * 86400000).toISOString().slice(0, 10);

    // Conta por status (hoje)
    const leadsHoje = await supaSelect(`leads?criado_em=gte.${hoje}&select=status`);
    const contadores = {
      base: 0, disparado: 0, em_conversa: 0, qualificado: 0,
      em_negociacao: 0, fechou: 0, perdido: 0, park: 0, bloqueado: 0,
    };
    for (const l of leadsHoje) contadores[l.status] = (contadores[l.status] || 0) + 1;

    // Distribuição por produto (30d)
    const produtos30 = await supaSelect(`leads?criado_em=gte.${inicio30}&select=produto`);
    const porProduto = {};
    for (const p of produtos30) {
      const k = p.produto || "outro";
      porProduto[k] = (porProduto[k] || 0) + 1;
    }

    // Volume liberado (30d)
    const fechados30 = await supaSelect(`leads?status=eq.fechou&fechado_em=gte.${inicio30}&select=valor_liberado,banco_fechado`);
    const volumeLiberado = fechados30.reduce((s, l) => s + (parseFloat(l.valor_liberado) || 0), 0);
    const porBanco = {};
    for (const f of fechados30) {
      if (!f.banco_fechado) continue;
      porBanco[f.banco_fechado] = (porBanco[f.banco_fechado] || 0) + (parseFloat(f.valor_liberado) || 0);
    }

    res.json({
      hoje: {
        recebidos: contadores.disparado + contadores.em_conversa + contadores.qualificado +
                    contadores.fechou + contadores.perdido + contadores.park,
        em_conversa: contadores.em_conversa,
        qualificados: contadores.qualificado,
        fechados: contadores.fechou,
        perdidos: contadores.perdido,
      },
      funil_hoje: [
        { nome: "Recebidos", qtd: leadsHoje.length },
        { nome: "Em conversa IA", qtd: contadores.em_conversa },
        { nome: "Qualificados", qtd: contadores.qualificado },
        { nome: "Closer ligou", qtd: contadores.em_negociacao + contadores.fechou + contadores.perdido },
        { nome: "Fecharam", qtd: contadores.fechou },
      ],
      por_produto_30d: Object.entries(porProduto).map(([k, v]) => ({ produto: k, qtd: v })),
      volume_liberado_30d: volumeLiberado,
      por_banco_30d: Object.entries(porBanco).map(([k, v]) => ({ banco: k, volume: v }))
        .sort((a, b) => b.volume - a.volume),
      ticket_medio: fechados30.length > 0 ? volumeLiberado / fechados30.length : 0,
      taxa_conversao_pct: leadsHoje.length > 0
        ? +(contadores.fechou / leadsHoje.length * 100).toFixed(1)
        : 0,
      modoMock: false,
    });
  } catch (e) {
    console.error("[dashboard] erro:", e);
    res.status(500).json({ erro: e.message });
  }
});

function mockMetricas() {
  return {
    hoje: {
      recebidos: 47,
      em_conversa: 11,
      qualificados: 23,
      fechados: 11,
      perdidos: 2,
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

export default router;

// Entrypoint do backend.
// Roda: node src/server.js (ou npm start)

import "dotenv/config";
import express from "express";
import webhookRoutes from "./routes/webhook.js";
import apiRoutes from "./routes/disparo.js";
import testRoutes from "./routes/test.js";
import dashboardRoutes from "./routes/dashboard.js";

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json({ limit: "1mb" }));

// CORS aberto pro painel (em produção, restringir o origin)
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Content-Type, Authorization");
  res.header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS");
  if (req.method === "OPTIONS") return res.sendStatus(204);
  next();
});

// Logging mínimo
app.use((req, _res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
  next();
});

// Healthcheck
app.get("/", (_req, res) => {
  res.json({
    nome: "fluxo-ia-gigacred-backend",
    status: "ok",
    versao: "0.1.0",
    rotas: {
      webhook: "POST /webhook/evolution",
      api: "GET /api/status, POST /api/disparo/iniciar, GET /api/config",
    },
  });
});

app.use("/webhook", webhookRoutes);
app.use("/api", apiRoutes);
app.use("/api/test", testRoutes);
app.use("/api/dashboard", dashboardRoutes);

// Handler de erros
app.use((err, _req, res, _next) => {
  console.error("[server] erro não tratado:", err);
  res.status(500).json({ erro: err.message || "Erro interno" });
});

app.listen(PORT, () => {
  console.log(`\n  fluxo-ia-gigacred backend rodando em http://localhost:${PORT}`);
  console.log(`  webhook Evolution: POST http://localhost:${PORT}/webhook/evolution`);
  console.log(`  status:           GET  http://localhost:${PORT}/api/status\n`);
  if (!process.env.SUPABASE_URL) {
    console.warn("  [aviso] SUPABASE_URL não configurado — banco não disponível");
  }
  if (!process.env.GEMINI_API_KEY) {
    console.warn("  [aviso] GEMINI_API_KEY não configurado — IA não disponível");
  }
  if (!process.env.EVOLUTION_URL) {
    console.warn("  [aviso] EVOLUTION_URL não configurado — bot não disponível");
  }
});

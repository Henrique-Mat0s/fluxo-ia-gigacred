-- =====================================================================
-- CRM mínimo para controlar a operação da IA SDR
-- Banco: PostgreSQL 14+ (testado em Supabase)
-- =====================================================================
-- Objetivo: cobrir o ciclo completo lead → conversa → score → handoff
-- sem virar um Salesforce. 5 tabelas, RLS opcional, índices só onde dói.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. leads — todo contato que entrou pelo bot
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS leads (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  -- Identificação
  channel         TEXT NOT NULL CHECK (channel IN ('whatsapp','site','instagram','telegram','manual')),
  channel_id      TEXT NOT NULL,            -- número WA, session_id site, etc.
  name            TEXT,
  email           TEXT,
  phone           TEXT,

  -- Origem
  utm_source      TEXT,
  utm_campaign    TEXT,
  utm_medium      TEXT,

  -- Status do funil
  stage           TEXT NOT NULL DEFAULT 'new'
                    CHECK (stage IN ('new','engaged','qualifying','qualified','handoff','won','lost','dormant')),
  score           INTEGER NOT NULL DEFAULT 0 CHECK (score BETWEEN 0 AND 100),

  -- Atribuição
  assigned_closer UUID,                     -- FK para users.id quando handoff acontece
  handoff_at      TIMESTAMPTZ,

  UNIQUE (channel, channel_id)
);

CREATE INDEX idx_leads_stage ON leads(stage);
CREATE INDEX idx_leads_score ON leads(score DESC) WHERE stage IN ('qualifying','qualified');
CREATE INDEX idx_leads_closer ON leads(assigned_closer) WHERE assigned_closer IS NOT NULL;


-- ---------------------------------------------------------------------
-- 2. conversations — histórico completo de mensagens (lead ↔ IA)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS conversations (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id         UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  role            TEXT NOT NULL CHECK (role IN ('user','assistant','system','closer')),
  content         TEXT NOT NULL,

  -- Métricas da chamada de IA (preenchido só quando role='assistant')
  model           TEXT,                     -- ex: 'gpt-4o-mini'
  tokens_in       INTEGER,
  tokens_out      INTEGER,
  latency_ms      INTEGER,
  cost_usd        NUMERIC(10,6)
);

CREATE INDEX idx_conversations_lead ON conversations(lead_id, created_at);


-- ---------------------------------------------------------------------
-- 3. qualifications — snapshot da qualificação BANT/SPIN
-- ---------------------------------------------------------------------
-- Uma linha por tentativa de qualificação. Mantemos histórico para
-- entender se a IA "mudou de ideia" sobre o lead ao longo da conversa.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS qualifications (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id         UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  -- BANT
  budget          TEXT,                     -- ex: '500-1000', 'sem orçamento', 'não respondeu'
  authority       TEXT,                     -- decisor / influenciador / usuário final
  need            TEXT,                     -- descrição livre da dor
  timeline        TEXT,                     -- 'imediato' / '30 dias' / '90 dias' / 'sem prazo'

  -- Scoring detalhado (a IA preenche)
  score_budget    INTEGER CHECK (score_budget BETWEEN 0 AND 25),
  score_authority INTEGER CHECK (score_authority BETWEEN 0 AND 25),
  score_need      INTEGER CHECK (score_need BETWEEN 0 AND 25),
  score_timeline  INTEGER CHECK (score_timeline BETWEEN 0 AND 25),
  score_total     INTEGER GENERATED ALWAYS AS
                    (COALESCE(score_budget,0) + COALESCE(score_authority,0) +
                     COALESCE(score_need,0) + COALESCE(score_timeline,0)) STORED,

  reasoning       TEXT,                     -- a IA explica o porquê do score
  recommended_action TEXT                   -- 'handoff_now' / 'continue_qualifying' / 'park' / 'discard'
);

CREATE INDEX idx_qualifications_lead ON qualifications(lead_id, created_at DESC);


-- ---------------------------------------------------------------------
-- 4. handoffs — registro de cada vez que IA → closer
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS handoffs (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id         UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  qualification_id UUID REFERENCES qualifications(id),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  closer_id       UUID,                     -- quem recebeu
  delivery_method TEXT NOT NULL CHECK (delivery_method IN ('webhook','slack','whatsapp','email','dashboard')),
  webhook_url     TEXT,
  payload         JSONB NOT NULL,           -- snapshot completo enviado
  delivery_status TEXT NOT NULL DEFAULT 'pending'
                    CHECK (delivery_status IN ('pending','delivered','failed','retrying')),
  delivery_attempts INTEGER NOT NULL DEFAULT 0,
  delivered_at    TIMESTAMPTZ,
  closer_response_at TIMESTAMPTZ,           -- quando o closer abriu/respondeu
  outcome         TEXT                      -- 'won','lost','no_show','still_negotiating'
);

CREATE INDEX idx_handoffs_status ON handoffs(delivery_status) WHERE delivery_status != 'delivered';
CREATE INDEX idx_handoffs_closer ON handoffs(closer_id, created_at DESC);


-- ---------------------------------------------------------------------
-- 5. users — closers e admins do CRM
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  email           TEXT UNIQUE NOT NULL,
  name            TEXT NOT NULL,
  role            TEXT NOT NULL CHECK (role IN ('admin','closer','viewer')),
  active          BOOLEAN NOT NULL DEFAULT TRUE,

  -- Capacidade do closer (quantos leads em paralelo aguenta)
  max_concurrent  INTEGER DEFAULT 10,
  notification_webhook TEXT                 -- onde notificar handoffs (slack/discord/zap)
);

ALTER TABLE leads
  ADD CONSTRAINT fk_leads_closer
  FOREIGN KEY (assigned_closer) REFERENCES users(id);

ALTER TABLE handoffs
  ADD CONSTRAINT fk_handoffs_closer
  FOREIGN KEY (closer_id) REFERENCES users(id);


-- ---------------------------------------------------------------------
-- 6. View útil: leads_dashboard — agrega tudo que o closer precisa ver
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW leads_dashboard AS
SELECT
  l.id,
  l.created_at,
  l.name,
  l.channel,
  l.stage,
  l.score,
  l.assigned_closer,
  u.name AS closer_name,
  (SELECT COUNT(*) FROM conversations c WHERE c.lead_id = l.id) AS msg_count,
  (SELECT MAX(created_at) FROM conversations c WHERE c.lead_id = l.id) AS last_message_at,
  (SELECT reasoning FROM qualifications q WHERE q.lead_id = l.id ORDER BY created_at DESC LIMIT 1) AS latest_reasoning
FROM leads l
LEFT JOIN users u ON u.id = l.assigned_closer;


-- ---------------------------------------------------------------------
-- 7. Trigger: atualiza leads.updated_at automaticamente
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION touch_updated_at() RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_leads_updated_at
  BEFORE UPDATE ON leads
  FOR EACH ROW EXECUTE FUNCTION touch_updated_at();

-- =====================================================================
-- Schema simplificado para GIGACRED — 4 tabelas
-- Rodar no Supabase SQL Editor (uma vez, antes de subir o backend)
-- =====================================================================

-- 1. leads -------------------------------------------------------------
create table if not exists leads (
  id                    uuid primary key default gen_random_uuid(),
  nome                  text,
  telefone              text not null unique,
  cpf                   text,
  origem                text,
  campanha              text,

  -- Produto / dados financeiros
  produto               text check (produto in ('fgts','consignado_inss','consignado_privado','outro')),
  saldo_fgts_estimado   numeric(10,2),
  valor_estimado        numeric(10,2),
  valor_liberado        numeric(10,2),
  banco_fechado         text,
  taxa_aplicada         numeric(5,3),

  -- BANT
  fez_adesao_saque_aniversario boolean,
  vinculo               text,
  motivo                text,

  -- Estado
  status                text not null default 'novo' check (status in (
                          'base','disparado','em_conversa','qualificado',
                          'em_negociacao','fechou','perdido','park','bloqueado'
                        )),
  score                 integer not null default 0 check (score between 0 and 100),
  resumo_ia             text,
  variante_isca         text,        -- 'A'..'E' — qual variante disparou
  closer_email          text,

  -- Timestamps
  criado_em             timestamptz default now(),
  ultima_msg_em         timestamptz,
  qualificado_em        timestamptz,
  fechado_em            timestamptz
);

create index if not exists idx_leads_status     on leads(status);
create index if not exists idx_leads_score_qual on leads(score desc) where status='qualificado';
create index if not exists idx_leads_campanha   on leads(campanha, criado_em);


-- 2. mensagens ---------------------------------------------------------
create table if not exists mensagens (
  id           uuid primary key default gen_random_uuid(),
  lead_id      uuid not null references leads(id) on delete cascade,
  autor        text not null check (autor in ('lead','ia','closer','sistema')),
  texto        text not null,
  -- Métricas (preenchido quando autor='ia')
  modelo       text,
  tokens_in    integer,
  tokens_out   integer,
  latency_ms   integer,
  criado_em    timestamptz default now()
);

create index if not exists idx_mensagens_lead on mensagens(lead_id, criado_em);


-- 3. ligacoes ----------------------------------------------------------
create table if not exists ligacoes (
  id            uuid primary key default gen_random_uuid(),
  lead_id       uuid not null references leads(id) on delete cascade,
  closer_email  text not null,
  resultado     text check (resultado in ('fechou','vai_pensar','nao_fechou','nao_atendeu')),
  motivo_perda  text,
  observacao    text,
  ligado_em     timestamptz default now()
);


-- 4. ia_config ---------------------------------------------------------
-- Linha única (id=1) que o painel edita: prompt, toggle ativa/pausada
create table if not exists ia_config (
  id              integer primary key default 1 check (id = 1),
  ativa           boolean default true,
  modelo          text default 'gemini-1.5-flash',
  system_prompt   text not null,
  atualizado_em   timestamptz default now()
);

-- Seed inicial
insert into ia_config (id, ativa, modelo, system_prompt)
values (1, true, 'gemini-1.5-flash', $$Você é a Giovanna, consultora virtual da GIGACRED Correspondente.
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
5. Vínculo de trabalho

FORMATO DE SAÍDA (JSON estrito):
{
  "reply": "<texto curto pro lead, sem markdown>",
  "qualificacao": {
    "saldo_fgts_estimado": <numero ou null>,
    "fez_adesao": <true | false | null>,
    "motivo": "<texto livre ou null>",
    "urgencia": "<imediato|semana|mes|sem_prazo|desconhecido>",
    "vinculo": "<clt|inss|autonomo|publico|desconhecido>",
    "score": <0-100>,
    "acao_recomendada": "handoff_now|continue_qualifying|park|discard|remover_base"
  }
}$$)
on conflict (id) do nothing;


-- 5. View: leads_dashboard (atalho pro painel) -------------------------
create or replace view leads_dashboard as
select
  l.id, l.nome, l.telefone, l.produto, l.score, l.status, l.resumo_ia,
  l.valor_estimado, l.qualificado_em, l.closer_email,
  l.criado_em, l.ultima_msg_em,
  (select count(*) from mensagens m where m.lead_id = l.id) as msg_count,
  (select texto from mensagens m where m.lead_id = l.id order by criado_em desc limit 1) as ultima_msg
from leads l;

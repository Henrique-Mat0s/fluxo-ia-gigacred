# API do CRM — Endpoints mínimos

Backend Node.js + Express. Todos os endpoints retornam JSON. Auth por token Bearer (Supabase JWT ou token customizado).

## Convenções

- `POST` cria, `GET` lê, `PATCH` atualiza parcial, `DELETE` remove
- Erros seguem RFC 7807 (problem+json): `{ type, title, status, detail }`
- Paginação por cursor: `?limit=20&cursor=<uuid>`

---

## 1. Leads

### `POST /api/leads`
Cria um lead. Idempotente por `(channel, channel_id)`.

```json
{
  "channel": "whatsapp",
  "channel_id": "5511999998888",
  "name": "Maria Silva",
  "utm_source": "instagram_ads",
  "utm_campaign": "junho_terapia"
}
```

**Retorno:** `201` com o lead criado, ou `200` se já existia (idempotência).

### `GET /api/leads`
Lista leads com filtros.

| Query param | Tipo | Default |
|---|---|---|
| `stage` | string | qualquer |
| `min_score` | int | 0 |
| `closer_id` | uuid | qualquer |
| `limit` | int | 20 |
| `cursor` | uuid | nenhum |

### `GET /api/leads/:id`
Retorna o lead **com** as últimas 50 mensagens e a qualificação mais recente embutida — uma chamada só pra montar a tela do closer.

### `PATCH /api/leads/:id`
Atualiza campos editáveis (`name`, `email`, `phone`, `stage`).
Manter `score` e `assigned_closer` em endpoints separados (abaixo).

---

## 2. Conversations

### `POST /api/leads/:id/messages`
Adiciona uma mensagem. Usado tanto pela IA quanto pelo closer.

```json
{
  "role": "assistant",
  "content": "Olá Maria, posso te entender melhor...",
  "model": "gpt-4o-mini",
  "tokens_in": 850,
  "tokens_out": 120,
  "latency_ms": 740,
  "cost_usd": 0.000234
}
```

### `GET /api/leads/:id/messages`
Lista mensagens em ordem cronológica. Paginação por cursor.

---

## 3. Qualifications

### `POST /api/leads/:id/qualifications`
A IA grava uma qualificação. Pode ser chamado N vezes durante a conversa — guardamos histórico.

```json
{
  "budget": "500-1500",
  "authority": "decisor",
  "need": "ansiedade crônica há 2 anos",
  "timeline": "imediato",
  "score_budget": 20,
  "score_authority": 25,
  "score_need": 22,
  "score_timeline": 25,
  "reasoning": "Lead decisor, dor clara, prazo curto, orçamento dentro da faixa do serviço básico.",
  "recommended_action": "handoff_now"
}
```

**Side effect:** se `recommended_action = 'handoff_now'`, dispara automaticamente o webhook (ver §4).

---

## 4. Handoffs

### `POST /api/leads/:id/handoff`
Força um handoff manual (atalho para closer humano puxar o lead sem esperar IA decidir).

```json
{
  "closer_id": "uuid-do-closer",
  "delivery_method": "whatsapp",
  "reason": "Lead VIP indicado pelo dono"
}
```

### `GET /api/handoffs`
Lista handoffs com filtros: `closer_id`, `delivery_status`, `outcome`.

### `PATCH /api/handoffs/:id`
Closer atualiza `outcome` ao final do atendimento.

```json
{ "outcome": "won" }
```

---

## 5. Webhook de entrada (a IA chama isto)

### `POST /api/webhook/inbound`
Endpoint que o bot WhatsApp / chat do site chamam quando uma nova mensagem chega.

```json
{
  "channel": "whatsapp",
  "channel_id": "5511999998888",
  "message": "Olá, quero saber sobre terapia",
  "received_at": "2026-06-29T14:32:11Z"
}
```

**O que faz internamente:**
1. Cria ou recupera o lead (`leads`)
2. Salva a mensagem (`conversations` com `role='user'`)
3. Monta o contexto (últimas N mensagens + dados do lead)
4. Chama a LLM com o prompt do SDR
5. Salva a resposta (`conversations` com `role='assistant'`)
6. Se a IA preencheu qualificação, salva em `qualifications`
7. Se `recommended_action='handoff_now'`, dispara o webhook de saída
8. Retorna a resposta para o bot enviar de volta ao lead

---

## 6. Webhook de saída (CRM → Closer)

Definido em `webhook/payload-exemplo.json`. Dispara automaticamente quando uma qualificação resulta em `recommended_action='handoff_now'`.

---

## 7. Métricas (dashboard admin)

### `GET /api/metrics/funnel`
Retorna contagem por stage nos últimos N dias.

```json
{
  "period_days": 30,
  "stages": {
    "new": 412,
    "engaged": 318,
    "qualifying": 187,
    "qualified": 74,
    "handoff": 71,
    "won": 23,
    "lost": 48
  },
  "conversion_rate": 0.056
}
```

### `GET /api/metrics/ia-cost`
Custo da IA por dia/mês — fundamental pra acompanhar.

### `GET /api/metrics/closer-performance`
Por closer: handoffs recebidos, taxa de conversão, tempo médio de resposta.

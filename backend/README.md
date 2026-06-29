# Backend — Fluxo IA GIGACRED

Backend Node.js (Express, ESM) que:
- **Recebe webhooks da Evolution API** quando um lead manda mensagem no WhatsApp
- **Chama o Gemini** com o prompt da Giovanna, qualifica e responde
- **Dispara mensagens-isca** em massa com cadência anti-ban
- **Expõe API** que o painel HTML consome

Custo zero: roda em qualquer servidor Node 20+. Recomendação: Oracle Cloud Always Free.

## Arquivos

```
backend/
├── package.json
├── .env.example                  ← copie pra .env e preencha
├── scripts/
│   ├── schema.sql                ← rode no Supabase SQL Editor 1x
│   ├── importar-base.js          ← importa CSV pra tabela leads
│   ├── test-gemini.js            ← teste rápido da Giovanna
│   └── test-webhook.js           ← simula uma mensagem entrando
└── src/
    ├── server.js                 ← entrypoint Express
    ├── db/supabase.js            ← REST client do Supabase
    ├── ia/gemini.js              ← chamada à API Gemini
    ├── evolution/client.js       ← cliente Evolution API
    ├── services/
    │   ├── conversa.js           ← orquestra mensagem→IA→resposta
    │   └── disparador.js         ← disparo em massa anti-ban
    └── routes/
        ├── webhook.js            ← POST /webhook/evolution
        └── disparo.js            ← /api/disparo/*, /api/config, /api/status
```

## Setup em 6 passos

### 1. Banco (Supabase) — 5 min
1. Crie conta grátis em https://supabase.com
2. Crie um projeto novo
3. Abra **SQL Editor** e cole o conteúdo de `scripts/schema.sql`. Execute.
4. Em **Project Settings → API**, copie:
   - `Project URL` → vai pro `SUPABASE_URL` do `.env`
   - `service_role` key (a longa, secreta) → vai pro `SUPABASE_SERVICE_KEY`

### 2. IA (Gemini) — 5 min
1. Vá em https://aistudio.google.com
2. Click em **"Get API Key"**
3. Copie a chave → vai pro `GEMINI_API_KEY` do `.env`

### 3. Bot (Evolution API) — 15-30 min
**Opção A (mais rápida):** use uma instância Evolution já pronta (várias empresas oferecem hosting grátis com limite).

**Opção B (self-hosted):** suba a Evolution no Oracle Cloud Free:
```bash
# Na VPS Oracle (Ubuntu 24)
docker compose up -d  # com o docker-compose oficial da Evolution
```

Depois:
1. Abra o **Manager** da Evolution
2. Crie uma instância (nome: `gigacred-bot-01`)
3. Conecte um número escaneando o QR
4. Configure o webhook: `https://SEU_BACKEND/webhook/evolution`
5. Copie URL e API key → `EVOLUTION_URL` e `EVOLUTION_API_KEY` no `.env`

### 4. Backend local — 2 min
```bash
cd backend
cp .env.example .env
# edite .env com as credenciais dos passos 1-3
npm install
npm run dev
```

Deve subir em `http://localhost:3000`.

### 5. Testar isoladamente
```bash
# Testa só a IA (sem precisar de WhatsApp)
npm run test:gemini

# Simula webhook entrando
npm run test:webhook
```

### 6. Importar base e disparar
```bash
# Importa CSV (formato: nome;telefone;origem na 1ª linha como header)
npm run importar-base ./minha-base.csv

# Inicia disparo (vai mandar com cadência anti-ban até bater o limite)
curl -X POST http://localhost:3000/api/disparo/iniciar
```

## Rotas

| Método | Path | Pra que serve |
|---|---|---|
| `POST` | `/webhook/evolution` | Evolution chama quando lead manda msg |
| `GET` | `/api/status` | Saúde geral: IA, Evolution, disparo |
| `POST` | `/api/disparo/iniciar` | Inicia disparo de mensagens-isca |
| `GET` | `/api/disparo/status` | Quantos enviou hoje, taxa de bloqueio |
| `GET` | `/api/config` | Pega configurações da IA |
| `PATCH` | `/api/config` | Edita prompt / liga/pausa IA |
| `GET` | `/api/leads/qualificados` | Lista leads `status=qualificado` |
| `GET` | `/api/leads/em-conversa` | Lista leads `status=em_conversa` |

## Anti-ban (variáveis do `.env`)

| Variável | Padrão | O que faz |
|---|---|---|
| `DISPARO_LIMITE_DIA` | 150 | Máximo de disparos/dia por chip |
| `DISPARO_MIN_INTERVALO_MS` | 40000 | Mínimo entre mensagens (40s) |
| `DISPARO_MAX_INTERVALO_MS` | 90000 | Máximo entre mensagens (90s) |
| `DISPARO_LIMITE_BLOQUEIO_PCT` | 5 | Se >5% bloquearem, para automaticamente |

## Conectar o painel ao backend real

Edite `painel/js/data-source.js`:
```js
const CONFIG = {
  SUPABASE_URL: "https://SEU_PROJETO.supabase.co",
  SUPABASE_KEY: "anon-key (não a service_role!)",
  EVOLUTION_URL: "https://evolution.seudominio.com",
  EVOLUTION_API_KEY: "...",
  EVOLUTION_INSTANCE: "gigacred-bot-01",
};
```

O painel passa a ler dados reais. Pra ações que mutam (toggle IA, salvar prompt), ele chama o backend nas rotas `/api/config`.

## Deploy em prod

**Oracle Cloud Always Free:**
1. Sobe a VPS (Ampere ARM, 4 vCPU + 24GB grátis pra sempre).
2. Instala Node 20, PM2, nginx, certbot.
3. Clona o repo e roda `npm install`.
4. `pm2 start src/server.js --name backend-ia`.
5. Nginx faz reverse proxy + SSL via certbot.

**Alternativa:** Render.com Free (mais simples, mas tem cold start). Bom pra começar.

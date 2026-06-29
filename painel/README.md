# Painel GIGACRED

Painel HTML/CSS/JS puro pro closer ver a IA trabalhando, os leads pra ligar, e ajustar configurações.

## 3 páginas

| Arquivo | O que faz |
|---|---|
| `index.html` | **IA Trabalhando** — stream de conversas ativas em tempo real. Mostra quem a IA está atendendo agora, última mensagem do lead, resposta da IA. |
| `ligar.html`  | **Pra Ligar** — leads que a IA já qualificou. Botão de ligar, abrir WhatsApp, marcar resultado da ligação. |
| `config.html` | **Configurações** — editar prompt da IA, ligar/pausar, status da Evolution API, status do Gemini. |

## Modo demo vs ao vivo

O painel funciona em **modo demo** (dados mock) sem nenhuma configuração — basta abrir `index.html` no navegador. Pra conectar ao Supabase + Evolution real, edite `js/data-source.js`:

```js
const CONFIG = {
  SUPABASE_URL: "https://SEU_PROJETO.supabase.co",
  SUPABASE_KEY: "sua-anon-key",
  EVOLUTION_URL: "https://evolution.seudominio.com",
  EVOLUTION_API_KEY: "seu-token",
  EVOLUTION_INSTANCE: "gigacred-bot-01",
};
```

A interface não muda — só a origem dos dados.

## Stack

- **Zero build step.** Sem npm, sem webpack, sem nada. Abre o HTML e funciona.
- **Vanilla JS** (sem React, sem Vue). Compatível com qualquer hospedagem estática.
- **Supabase via REST direto** (sem precisar do SDK).
- **Evolution API** (`/instance/connectionState/{instance}`) pra status do WhatsApp.

## Como rodar local

```
cd painel
# qualquer servidor estático serve:
python -m http.server 8080
# ou: npx serve .
```

Abra `http://localhost:8080`.

## Como deployar grátis

GitHub Pages: ative no repo apontando pra `/painel`. URL fica `https://Henrique-Mat0s.github.io/fluxo-ia-gigacred/`.

## Próximos passos (não estão neste painel ainda)

- Webhook receiver: backend que recebe mensagens da Evolution e responde via Gemini
- Bot disparador: lê base CSV, dispara mensagens-isca com cadência anti-ban
- Painel admin completo (com gráficos, métricas, base de prospecção como tela própria)

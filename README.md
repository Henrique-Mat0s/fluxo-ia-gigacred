# Fluxo de IA Comercial — GIGACRED

> Template + customização para construir um fluxo de IA comercial completo: bot WhatsApp prospecta a base, IA SDR qualifica via diálogo, CRM enxuto entrega o lead ao closer humano.

**🟢 CUSTO ZERO** — todo o stack em tiers gratuitos. R$0/mês até ~150 conversas/dia.

## Os 3 PDFs do repositório

| Documento | Para quem | Páginas |
|---|---|---|
| `fluxo-ia-empresa.pdf` | Versão completa **genérica** — qualquer empresa. | 23 |
| `fluxo-ia-empresa-simples.pdf` | Versão **simplificada** com 4 mockups embedados. | 12 |
| **`fluxo-ia-gigacred.pdf`** | **Customizado pra GIGACRED**: prospecção ativa, plano de 7 dias pra gerar caixa, prompt da IA Giovanna, schema com campos do nicho FGTS, mockups verde GigaCred. | **20** |

> **Comece pelo `fluxo-ia-gigacred.pdf`**, parte "Plano de 7 dias pra gerar caixa" — é a leitura prioritária.

## O fluxo, em uma frase

> Base de contatos → Bot dispara mensagem-isca → Lead responde → IA Giovanna qualifica → CRM mostra ao closer → Closer liga, simula e libera no PIX.

## Stack tecnológica (tudo grátis)

| Camada | Tecnologia | Limite gratuito |
|---|---|---|
| Bot WhatsApp | `whatsapp-web.js` (Node.js) | ilimitado |
| IA SDR | Google Gemini 1.5 Flash via AI Studio | 1500 req/dia (~150 conversas/dia) |
| Backup IA | Groq + Llama 3.1 8B | rate limit por minuto |
| Backend | Express.js | grátis |
| Banco | Supabase Free Tier | 500MB + 2GB/mês |
| Hospedagem | Oracle Cloud Always Free | 4 vCPUs ARM, 24GB RAM, sem expiração |
| Painel CRM | Retool Free (ou HTML puro) | até 5 closers |
| Notificação | Slack Free | mensagens ilimitadas, 90d histórico |
| DNS/SSL | Cloudflare Free | ilimitado |
| Repo | GitHub Free | público ilimitado |
| Monitoramento | UptimeRobot Free | 50 monitores, ping 5 min |

**Custo total: R$ 0,00/mês.** Único gasto opcional: chip dedicado de WhatsApp (R$ 10 uma vez) + domínio próprio (R$ 40/ano).

## Estrutura do repositório

```
fluxo-ia-gigacred/
├── fluxo-ia-empresa.pdf            # versão completa (23 pág)
├── fluxo-ia-empresa-simples.pdf    # versão simples com prints (12 pág)
├── fluxo-ia-gigacred.pdf           # versão GIGACRED (20 pág)
│
├── gerar-pdf.py                    # gera a versão completa
├── gerar-pdf-simples.py            # gera a versão simples
├── gerar-pdf-gigacred.py           # gera a versão GIGACRED
├── gerar-mockups.py                # gera mockups genéricos
├── gerar-mockups-gigacred.py       # gera mockups GIGACRED
│
├── mockups/                        # PNGs das telas (versão genérica)
│   ├── 01_conversa.png
│   ├── 02_lista_leads.png
│   ├── 03_detalhe_lead.png
│   └── 04_dashboard.png
│
├── mockups-gigacred/               # PNGs das telas (versão GIGACRED)
│   ├── 01_conversa.png             # conversa com bot + IA Giovanna
│   ├── 02_lista_leads.png          # leads qualificados pra ligar
│   ├── 03_detalhe_lead.png         # detalhe + simulação de bancos
│   ├── 04_dashboard.png            # painel com volume liberado
│   └── 05_base_prospeccao.png      # base + status do disparo
│
├── crm-exemplo/                    # esqueleto do CRM
│   ├── schema.sql                  # 5 tabelas (versão completa)
│   └── api-endpoints.md            # endpoints REST documentados
│
├── prompts/
│   └── sdr-prompt-exemplo.md       # prompt da IA SDR comentado
│
├── webhook/
│   └── payload-exemplo.json        # payload IA → Closer com HMAC
│
├── README.md
└── .gitignore
```

## Próximos passos (após ler o PDF)

1. **Imediato (Dia 1):** organizar a base de contatos (clientes antigos, leads de form, indicações).
2. **Dia 2-3:** preparar chip WhatsApp dedicado + aquecimento.
3. **Dia 3-5:** disparo manual com as 5 variantes da mensagem-isca (no PDF).
4. **Dia 6-7:** subir o bot whatsapp-web.js + conectar IA Giovanna no Gemini Free.
5. **Semana 2+:** completar CRM no Retool, conectar notificação no Slack do closer.

## Regerar os PDFs

```bash
pip install fpdf2 Pillow
python gerar-pdf-gigacred.py
python gerar-mockups-gigacred.py
```

Os scripts geram tudo do zero, então qualquer edição de texto/cor/layout é trivial.

## Licença

Uso interno GIGACRED. Os templates genéricos (`fluxo-ia-empresa*.pdf`) podem ser adaptados pra outros nichos.

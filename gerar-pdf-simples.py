# -*- coding: utf-8 -*-
"""
Gera "fluxo-ia-empresa-simples.pdf" — versão enxuta do fluxo em 5 passos,
com mockups (prints) das telas embedados.
"""
from fpdf import FPDF
from pathlib import Path

BASE = Path(__file__).parent
PDF_OUT = BASE / "fluxo-ia-empresa-simples.pdf"
MOCKUPS = BASE / "mockups"
FONTS_DIR = "C:/Windows/Fonts"


class Doc(FPDF):
    NX = "LMARGIN"
    NY = "NEXT"

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(left=22, top=20, right=22)
        self.add_font("Arial", "", f"{FONTS_DIR}/arial.ttf")
        self.add_font("Arial", "B", f"{FONTS_DIR}/arialbd.ttf")
        self.add_font("Arial", "I", f"{FONTS_DIR}/ariali.ttf")
        self.add_font("Consolas", "", f"{FONTS_DIR}/consola.ttf")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Fluxo de IA — versão simplificada — pág. {self.page_no()}",
                  align="C")
        self.set_text_color(0, 0, 0)

    def h1(self, txt):
        self.ln(4)
        self.set_font("Arial", "B", 20)
        self.set_text_color(31, 56, 100)
        self.multi_cell(0, 9, txt, new_x=self.NX, new_y=self.NY)
        self.ln(2)
        self.set_text_color(0, 0, 0)

    def h2(self, txt):
        self.ln(3)
        self.set_font("Arial", "B", 14)
        self.set_text_color(46, 84, 150)
        self.multi_cell(0, 7, txt, new_x=self.NX, new_y=self.NY)
        self.ln(1)
        self.set_text_color(0, 0, 0)

    def h3(self, txt):
        self.ln(2)
        self.set_font("Arial", "B", 12)
        self.set_text_color(46, 84, 150)
        self.multi_cell(0, 6, txt, new_x=self.NX, new_y=self.NY)
        self.set_text_color(0, 0, 0)

    def step_header(self, num, titulo):
        """Cabeçalho destacado de passo: PASSO X em badge colorido."""
        self.ln(4)
        # badge "PASSO N"
        y0 = self.get_y()
        self.set_fill_color(37, 99, 235)
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", "B", 11)
        self.cell(28, 9, f"PASSO {num}", align="C", fill=True,
                  new_x="RIGHT", new_y="TOP")
        # título
        self.set_text_color(31, 56, 100)
        self.set_font("Arial", "B", 16)
        self.cell(0, 9, "  " + titulo, new_x=self.NX, new_y=self.NY)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def p(self, txt):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 5.5, txt, new_x=self.NX, new_y=self.NY)
        self.ln(1.5)

    def bullet(self, items):
        self.set_font("Arial", "", 11)
        for it in items:
            self.multi_cell(0, 5.5, f"•  {it}", new_x=self.NX, new_y=self.NY)
        self.ln(1.5)

    def code(self, txt):
        self.set_font("Consolas", "", 8.5)
        self.set_fill_color(244, 244, 244)
        self.multi_cell(0, 4.5, txt, fill=True, border=0,
                        new_x=self.NX, new_y=self.NY)
        self.set_font("Arial", "", 11)
        self.ln(2)

    def image_full(self, path, caption=None):
        """Insere imagem ocupando largura útil. Aceita keep_aspect_ratio."""
        usable = 210 - 22 - 22  # 166mm
        self.ln(2)
        x = (210 - usable) / 2
        self.image(str(path), x=x, w=usable)
        if caption:
            self.set_font("Arial", "I", 9)
            self.set_text_color(108, 117, 125)
            self.multi_cell(0, 4.5, caption, align="C",
                            new_x=self.NX, new_y=self.NY)
            self.set_text_color(0, 0, 0)
        self.ln(3)

    def pb(self):
        self.add_page()


pdf = Doc()

# =====================================================================
# CAPA
# =====================================================================
pdf.add_page()
pdf.ln(45)
pdf.set_font("Arial", "B", 30)
pdf.set_text_color(31, 56, 100)
pdf.cell(0, 14, "Fluxo de IA Comercial", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)
pdf.set_font("Arial", "B", 16)
pdf.set_text_color(0, 0, 0)
pdf.cell(0, 8, "Versão simplificada em 5 passos",
         align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(20)

# Badge custo zero
pdf.set_font("Arial", "B", 14)
pdf.set_text_color(46, 125, 50)
pdf.cell(0, 9, "CUSTO ZERO — todo o stack em tiers gratuitos",
         align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(18)

# Resumo do fluxo
pdf.set_font("Arial", "B", 13)
pdf.set_text_color(31, 56, 100)
pdf.cell(0, 7, "O fluxo, em uma frase:",
         align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)
pdf.set_font("Arial", "", 12)
pdf.set_text_color(0, 0, 0)
fluxo = ("Bot recebe a mensagem  →  Lead responde  →  IA SDR qualifica  →  "
         "Plataforma exibe nome, telefone e resumo  →  Closer humano liga.")
pdf.set_x(22)
pdf.multi_cell(0, 6, fluxo, align="C",
               new_x="LMARGIN", new_y="NEXT")
pdf.ln(50)

pdf.set_font("Arial", "", 10)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 5, "Versão 1.0 — Junho de 2026", align="C",
         new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, "Inclui mockups das telas do CRM enxuto", align="C",
         new_x="LMARGIN", new_y="NEXT")
pdf.set_text_color(0, 0, 0)

# =====================================================================
# VISÃO GERAL
# =====================================================================
pdf.pb()
pdf.h1("Visão geral")
pdf.p("Este documento mostra, em cinco passos práticos, como funciona um fluxo "
      "de IA comercial enxuto. A IA conversa com o lead pelo WhatsApp, qualifica "
      "via diálogo, e quando identifica que o lead está pronto para fechar, envia "
      "o contato com um resumo curto para uma plataforma — onde um closer humano "
      "abre, lê 5 linhas, e liga.")
pdf.p("Não há venda automática, não há mensagem agendada, não há CRM gigante. "
      "Cinco passos, três tabelas, custo zero.")

pdf.h2("O que cada parte faz")
pdf.bullet([
    "Bot WhatsApp: recebe o que o lead manda e devolve a resposta da IA. "
    "Não pensa, só transporta.",
    "IA SDR: faz as perguntas certas pra descobrir se o lead tem fit. "
    "Decide quando passar pro humano.",
    "Plataforma (CRM enxuto): lista os leads qualificados, mostra o resumo "
    "que a IA escreveu, registra a ligação.",
    "Closer humano: abre a plataforma, vê os leads esperando, escolhe o de "
    "maior score e liga.",
])

pdf.h2("Por que esse fluxo funciona")
pdf.bullet([
    "Velocidade: lead que chegou às 23h domingo é respondido em 1 minuto.",
    "Foco do closer: ele só fala com quem tem fit comprovado — economiza horas/dia.",
    "Sem perda de contexto: o resumo da IA evita que o closer precise refazer perguntas.",
    "Custo zero: Gemini Free + Supabase Free + Oracle Cloud Free atendem até "
    "150 conversas/dia sem nenhum gasto.",
])

# =====================================================================
# DIAGRAMA DO FLUXO
# =====================================================================
pdf.pb()
pdf.h1("O fluxo, visualmente")
pdf.code("""
   [Lead]
     │
     │  manda mensagem no WhatsApp
     ▼
   ┌──────────────┐
   │  PASSO 1     │   Bot recebe a mensagem
   │  Bot WhatsApp│   (whatsapp-web.js)
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │  PASSO 2     │   Lead responde — vira mensagens de ida-e-volta
   │  Conversa    │   (várias trocas até a IA decidir)
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │  PASSO 3     │   IA SDR (Gemini Flash) qualifica via diálogo:
   │  IA SDR      │   descobre orçamento, urgência, dor, decisor
   └──────┬───────┘
          │
          │  score ≥ 80? sim → handoff
          ▼
   ┌──────────────┐
   │  PASSO 4     │   IA escreve resumo curto e envia ao CRM:
   │  Plataforma  │   nome, telefone, score, 3 linhas do que importa
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │  PASSO 5     │   Closer humano abre a plataforma,
   │  Closer      │   vê a lista, escolhe o mais quente,
   │              │   liga para o número.
   └──────────────┘
""")

# =====================================================================
# PASSO 1
# =====================================================================
pdf.pb()
pdf.step_header(1, "Bot envia (e recebe) a mensagem no WhatsApp")

pdf.p("O bot é um programa Node.js rodando 24/7 num servidor (pode ser o Oracle "
      "Cloud Free Tier — gratuito). Ele usa a biblioteca whatsapp-web.js para "
      "manter uma sessão de WhatsApp Web sempre online.")

pdf.p("Quando o lead manda uma mensagem para o número de WhatsApp da empresa, "
      "o bot intercepta e faz uma única coisa: POST para o endpoint do CRM.")

pdf.h2("O que o bot envia ao CRM")
pdf.code("""POST /api/mensagem-recebida
{
  "telefone": "5511999998888",
  "nome": "Maria",
  "texto": "Olá, vi seu anúncio sobre terapia. Como funciona?",
  "recebido_em": "2026-06-29T09:14:22Z"
}""")

pdf.p("E quando o CRM responde com o que a IA disse, o bot envia a resposta "
      "de volta ao lead, simulando um atraso de 1-2 segundos para parecer "
      "humano digitando.")

pdf.h2("Por que whatsapp-web.js (em vez da API oficial)")
pdf.bullet([
    "Grátis. A API oficial Meta cobra R$0,30 a R$0,90 por conversa iniciada.",
    "Aceita áudio, imagem, documento sem configuração extra.",
    "Subida em 1 dia. Você escaneia um QR code com o celular, e pronto.",
    "Contrapartida: a sessão pode cair ocasionalmente (preciso reescanear o QR).",
])

# =====================================================================
# PASSO 2 — Conversa
# =====================================================================
pdf.pb()
pdf.step_header(2, "Lead responde — começa a conversa")

pdf.p("Cada mensagem do lead é uma chamada nova ao CRM. O CRM monta o contexto "
      "(histórico das últimas mensagens, dados que já sabe do lead) e passa "
      "para a IA. A IA gera a resposta, o CRM salva, e o bot envia ao lead.")

pdf.p("Em média, são de 6 a 12 trocas até a IA ter informação suficiente para "
      "decidir se vale ou não passar para um humano.")

pdf.p("Veja como ficaria uma conversa típica:")

pdf.image_full(MOCKUPS / "01_conversa.png",
               caption="Conversa real no WhatsApp do lead. As mensagens verdes são "
                       "geradas pela IA SDR; as brancas são do lead. No final, a IA "
                       "decide que o lead está pronto e dispara handoff.")

# =====================================================================
# PASSO 3 — IA SDR
# =====================================================================
pdf.pb()
pdf.step_header(3, "IA SDR toma conta da qualificação")

pdf.p("A IA SDR é um prompt rodando no Gemini 1.5 Flash (gratuito). Para cada "
      "mensagem que chega, o CRM faz uma chamada à API do Gemini, passando:")
pdf.bullet([
    "Quem a IA é (nome, tom de voz, regras de comunicação).",
    "O contexto da empresa (o que vende, faixa de preço, quem é o cliente ideal).",
    "O histórico das últimas mensagens da conversa.",
    "A nova mensagem do lead.",
])

pdf.p("O Gemini devolve um JSON com duas coisas: o texto da resposta para o "
      "lead, e uma avaliação atualizada do lead — orçamento, urgência, decisor, "
      "dor, e um score de 0 a 100.")

pdf.h2("Sistema de score (BANT)")
pdf.bullet([
    "Budget (0-25): orçamento disponível.",
    "Authority (0-25): é o decisor?",
    "Need (0-25): a dor é específica e real?",
    "Timeline (0-25): quer começar quando?",
])
pdf.p("Score total >= 80 → IA dispara o handoff para a plataforma. "
      "Entre 60 e 79 → continua qualificando. Abaixo de 60 → arquiva "
      "educadamente como 'park' para nurturing futuro.")

pdf.h2("Por que Gemini Flash")
pdf.bullet([
    "1500 requisições/dia grátis — cobre 150 conversas/dia.",
    "Aceita JSON output estruturado (resposta confiável).",
    "Latência baixa (1-2s) — o lead nem percebe.",
    "Sem cartão de crédito necessário no AI Studio.",
])

# =====================================================================
# PASSO 4 — Plataforma recebe
# =====================================================================
pdf.pb()
pdf.step_header(4, "IA passa o número para a plataforma com um resumo")

pdf.p("Quando o score chega em 80+, a IA executa três coisas em sequência:")
pdf.bullet([
    "Escreve um resumo curto de 3 linhas, com o que o closer precisa saber.",
    "Marca o lead como 'qualificado' no banco.",
    "(Opcional) Envia uma notificação no Slack ou WhatsApp do closer.",
])

pdf.p("E o lead aparece na plataforma — uma página web simples que os "
      "closers abrem no navegador. Veja como fica:")

pdf.image_full(MOCKUPS / "02_lista_leads.png",
               caption="Tela 'Leads para você'. Cada linha é um lead qualificado "
                       "pela IA. O closer vê nome, telefone, score e o resumo de "
                       "uma linha — escolhe o de maior score e clica em 'Abrir'.")

pdf.h2("O resumo que a IA escreve")
pdf.p("Não é o histórico completo. São 3 linhas — só o essencial para o "
      "closer começar a ligação sem ter que ler 30 mensagens:")
pdf.code('''"Maria, 34, ansiedade crônica. Quer começar esta semana,
 prefere online à noite (após 19h), orçamento até R$ 1.500/mês."''')

pdf.p("Esse formato é definido no prompt da IA — ela aprende a sempre "
      "escrever no mesmo padrão (dor, prazo, modalidade, orçamento).")

# =====================================================================
# PASSO 5 — Closer liga
# =====================================================================
pdf.pb()
pdf.step_header(5, "Closer pega o número e liga")

pdf.p("O closer abre o lead, lê o resumo (10 segundos), e tem duas opções "
      "claras: ligar ou abrir o WhatsApp. Sem CRM complicado, sem 15 abas, "
      "sem precisar refazer perguntas.")

pdf.image_full(MOCKUPS / "03_detalhe_lead.png",
               caption="Tela do lead. À esquerda: dados + resumo da IA. "
                       "À direita: botão de ligar, contador de SLA, e botões "
                       "para registrar o resultado depois da conversa.")

pdf.h2("Depois da ligação")
pdf.p("O closer volta na plataforma e clica em um dos 4 botões de resultado:")
pdf.bullet([
    "[OK]  Fechou venda — sucesso (a IA aprende com esse padrão).",
    "[ ? ] Vai pensar — agendamento de follow-up.",
    "[X]   Não fechou — registra motivo (preço, timing, sem fit).",
    "[--]  Não atendeu — agendamento para tentar de novo.",
])

pdf.p("Esses resultados alimentam o aprendizado da IA: leads que viram 'won' "
      "ajudam a calibrar o score; leads que viram 'no_show' indicam que talvez "
      "a IA tenha forçado o handoff cedo demais.")

# =====================================================================
# DASHBOARD
# =====================================================================
pdf.pb()
pdf.h1("E o dono da empresa?")

pdf.p("Para quem gerencia, há uma tela extra: o painel do dia. Mostra os "
      "números essenciais sem virar relatório gigante.")

pdf.image_full(MOCKUPS / "04_dashboard.png",
               caption="Dashboard de hoje. 4 métricas no topo, funil completo "
                       "no meio, leads aguardando ligação embaixo. Tudo "
                       "atualizado em tempo real via Supabase Realtime.")

pdf.p("Atualizado em tempo real (Supabase Realtime — também gratuito), o "
      "painel responde 3 perguntas:")
pdf.bullet([
    "Quantos leads chegaram hoje? E são mais ou menos que ontem?",
    "A IA está qualificando bem (quantos viram 'qualificado')?",
    "Os closers estão pegando os leads ou estão se acumulando?",
])

# =====================================================================
# O CRM ENXUTO
# =====================================================================
pdf.pb()
pdf.h1("O CRM enxuto: 3 tabelas só")

pdf.p("Esta versão simplificada não precisa das 5 tabelas da versão completa. "
      "Três resolvem o problema:")

pdf.h2("Schema SQL completo")
pdf.code("""-- 1. leads — todo contato que entrou pelo bot
CREATE TABLE leads (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  nome          TEXT,
  telefone      TEXT NOT NULL UNIQUE,
  score         INTEGER DEFAULT 0,
  status        TEXT DEFAULT 'novo'
                  CHECK (status IN ('novo','em_conversa','qualificado',
                                    'ligado','fechou','perdido','park')),
  resumo_ia     TEXT,
  criado_em     TIMESTAMPTZ DEFAULT NOW(),
  qualificado_em TIMESTAMPTZ
);

-- 2. mensagens — histórico da conversa
CREATE TABLE mensagens (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id       UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  autor         TEXT NOT NULL CHECK (autor IN ('lead','ia','closer')),
  texto         TEXT NOT NULL,
  criado_em     TIMESTAMPTZ DEFAULT NOW()
);

-- 3. ligacoes — registro de cada tentativa de contato do closer
CREATE TABLE ligacoes (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id       UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  closer_email  TEXT NOT NULL,
  resultado     TEXT CHECK (resultado IN ('fechou','vai_pensar',
                                          'nao_fechou','nao_atendeu')),
  observacao    TEXT,
  ligado_em     TIMESTAMPTZ DEFAULT NOW()
);

-- Índices úteis
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_score ON leads(score DESC) WHERE status='qualificado';
CREATE INDEX idx_mensagens_lead ON mensagens(lead_id, criado_em);""")

pdf.h2("Por que 3 tabelas chegam")
pdf.bullet([
    "leads guarda tudo do contato: dados, score, status, resumo da IA.",
    "mensagens é o histórico — útil para auditoria e para o CRM montar o "
    "contexto para a IA a cada novo turno.",
    "ligacoes registra o que o closer fez. Esse dado é o que permite a IA "
    "aprender com o tempo.",
])

# =====================================================================
# CUSTO ZERO RESUMIDO
# =====================================================================
pdf.pb()
pdf.h1("Custo zero — resumo")

pdf.h2("Stack completo (R$ 0,00 / mês)")
pdf.bullet([
    "Bot WhatsApp: whatsapp-web.js (open source, gratuito).",
    "IA: Google Gemini 1.5 Flash via AI Studio — 1500 req/dia grátis.",
    "Backend: Node.js + Express — gratuito.",
    "Banco: Supabase Free — 500MB DB + 2GB bandwidth/mês.",
    "Hospedagem: Oracle Cloud Always Free — 4 vCPUs + 24GB RAM, sem expiração.",
    "Painel CRM: Retool Free (até 5 usuários) ou HTML puro no GitHub Pages.",
    "Notificação ao closer: Slack Free ou o próprio bot WhatsApp.",
    "Domínio (opcional): subdomínio gratuito do Vercel/Netlify/DuckDNS.",
])

pdf.h2("Até onde vai o custo zero")
pdf.bullet([
    "150 conversas completas por dia (limite do Gemini Free).",
    "~100 mil mensagens no banco (limite do Supabase Free).",
    "5 closers no painel (limite do Retool Free).",
])

pdf.p("Acima desses limites, a migração para tier pago é gradual e barata "
      "(R$25-150/mês na primeira escala). Mas você só paga quando o volume "
      "justificar — e até lá já estará tendo receita do que a IA qualificou.")

pdf.h2("O que NÃO está incluso no custo zero")
pdf.bullet([
    "Tempo do operador: 10-20 horas/mês para manter o sistema (revisar prompt, "
    "tratar sessão WhatsApp que cai, treinar closer).",
    "Treinamento do closer: 4-8 horas iniciais.",
    "Chip e número de WhatsApp dedicado: ~R$10 uma vez.",
    "Domínio próprio (opcional): R$40-80/ano.",
])

# =====================================================================
# PRÓXIMOS PASSOS
# =====================================================================
pdf.pb()
pdf.h1("Próximos passos")

pdf.h2("Antes de implementar")
pdf.bullet([
    "Escreva em uma frase: quem é o cliente ideal da empresa?",
    "Escreva os 4 pontos BANT que um lead 'score 90+' tem que ter no seu negócio.",
    "Defina o canal de notificação do closer (Slack? WhatsApp? Painel?).",
    "Crie as contas gratuitas: Google AI Studio, Supabase, Oracle Cloud, GitHub.",
])

pdf.h2("Roadmap de 4 semanas (versão acelerada)")
pdf.h3("Semana 1: Fundação")
pdf.p("Criar Supabase, aplicar o schema das 3 tabelas. Subir backend Node "
      "no Oracle Cloud Free. Configurar bot WhatsApp e testar fluxo de "
      "ida-e-volta sem IA.")

pdf.h3("Semana 2: IA SDR")
pdf.p("Obter API key Gemini no AI Studio. Implementar prompt do SDR. "
      "Salvar resposta da IA em mensagens. Testar com 5 conversas simuladas.")

pdf.h3("Semana 3: Plataforma")
pdf.p("Montar painel no Retool Free (ou HTML simples) com 3 telas: lista "
      "de leads, detalhe do lead, dashboard do dia. Implementar registro "
      "de ligação.")

pdf.h3("Semana 4: Piloto e ajustes")
pdf.p("Rodar 20 leads reais. Acompanhar resultado de cada ligação. Ajustar "
      "prompt da IA com base no que aprendeu. Documentar runbook básico "
      "(o que fazer quando sessão do WhatsApp cai). Lançar.")

pdf.h2("Métricas para acompanhar")
pdf.bullet([
    "Tempo até primeira resposta: alvo < 1 minuto.",
    "Taxa de qualificação (leads recebidos → qualificados): 30-50%.",
    "Taxa de conversão (qualificados → fechou): 20-40%.",
    "Custo financeiro: R$ 0,00/mês.",
])

pdf.h2("Quando saber que está funcionando")
pdf.p("Quando o closer disser: 'antes eu falava com 50 leads ruins por "
      "semana, agora falo com 10 leads quentes — minha vida mudou'.")

# =====================================================================
pdf.output(str(PDF_OUT))
print(f"PDF gerado: {PDF_OUT}")
print(f"Tamanho: {PDF_OUT.stat().st_size / 1024:.1f} KB")
print(f"Páginas: {pdf.page_no()}")

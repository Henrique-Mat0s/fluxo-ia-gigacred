# -*- coding: utf-8 -*-
"""
Gera "fluxo-ia-gigacred.pdf" — versão customizada para GIGACRED Correspondente.
Foco: antecipação saque-aniversário FGTS, consignados, IA SDR adaptada.
"""
from fpdf import FPDF
from pathlib import Path

BASE = Path(__file__).parent
PDF_OUT = BASE / "fluxo-ia-gigacred.pdf"
MOCKUPS = BASE / "mockups-gigacred"
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
        self.cell(0, 8, f"GIGACRED — Fluxo de IA — pág. {self.page_no()}",
                  align="C")
        self.set_text_color(0, 0, 0)

    # Paleta GigaCred (verde escuro + amarelo)
    C_HEADER = (21, 87, 36)
    C_PRIMARY = (40, 167, 69)
    C_ACCENT = (255, 193, 7)
    C_TEXT_MUTED = (108, 117, 125)

    def h1(self, txt):
        self.ln(4)
        self.set_font("Arial", "B", 20)
        self.set_text_color(*self.C_HEADER)
        self.multi_cell(0, 9, txt, new_x=self.NX, new_y=self.NY)
        self.ln(2)
        self.set_text_color(0, 0, 0)

    def h2(self, txt):
        self.ln(3)
        self.set_font("Arial", "B", 14)
        self.set_text_color(*self.C_PRIMARY)
        self.multi_cell(0, 7, txt, new_x=self.NX, new_y=self.NY)
        self.ln(1)
        self.set_text_color(0, 0, 0)

    def h3(self, txt):
        self.ln(2)
        self.set_font("Arial", "B", 12)
        self.set_text_color(*self.C_PRIMARY)
        self.multi_cell(0, 6, txt, new_x=self.NX, new_y=self.NY)
        self.set_text_color(0, 0, 0)

    def step_header(self, num, titulo):
        self.ln(4)
        self.set_fill_color(*self.C_PRIMARY)
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", "B", 11)
        self.cell(28, 9, f"PASSO {num}", align="C", fill=True,
                  new_x="RIGHT", new_y="TOP")
        self.set_text_color(*self.C_HEADER)
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
        self.set_fill_color(244, 247, 245)
        self.multi_cell(0, 4.5, txt, fill=True, border=0,
                        new_x=self.NX, new_y=self.NY)
        self.set_font("Arial", "", 11)
        self.ln(2)

    def callout(self, titulo, txt):
        """Caixa de destaque com borda amarela (alerta importante)."""
        self.ln(2)
        x = self.get_x()
        y0 = self.get_y()
        # Calcula altura do texto (aprox)
        self.set_font("Arial", "", 11)
        lines = len(txt) // 80 + txt.count("\n") + 1
        h = 12 + lines * 5.5

        self.set_fill_color(255, 248, 220)
        self.set_draw_color(*self.C_ACCENT)
        self.set_line_width(0.5)
        self.rect(x, y0, 166, h, style="DF")

        self.set_xy(x + 4, y0 + 3)
        self.set_font("Arial", "B", 11)
        self.set_text_color(*self.C_HEADER)
        self.cell(0, 5, f"[!]  {titulo}", new_x=self.NX, new_y=self.NY)
        self.set_text_color(0, 0, 0)

        self.set_xy(x + 4, y0 + 9)
        self.set_font("Arial", "", 11)
        self.multi_cell(158, 5.5, txt, new_x=self.NX, new_y=self.NY)
        self.ln(3)

    def image_full(self, path, caption=None):
        usable = 210 - 22 - 22
        self.ln(2)
        x = (210 - usable) / 2
        self.image(str(path), x=x, w=usable)
        if caption:
            self.set_font("Arial", "I", 9)
            self.set_text_color(*self.C_TEXT_MUTED)
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
pdf.ln(40)

# Logo simulado: GIGA + CRED em cores
pdf.set_font("Arial", "B", 36)
pdf.set_text_color(*pdf.C_HEADER)
# Centralizar manualmente: largura de "GIGA" + "CRED"
giga_w = pdf.get_string_width("GIGA")
cred_w = pdf.get_string_width("CRED")
total_w = giga_w + cred_w
start = (210 - total_w) / 2
pdf.set_x(start)
pdf.cell(giga_w, 14, "GIGA", new_x="RIGHT", new_y="TOP")
pdf.set_text_color(*pdf.C_ACCENT)
pdf.cell(cred_w, 14, "CRED", new_x="LMARGIN", new_y="NEXT")
pdf.set_text_color(0, 0, 0)

pdf.ln(2)
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 7, "Correspondente Bancário", align="C",
         new_x="LMARGIN", new_y="NEXT")
pdf.ln(20)

pdf.set_font("Arial", "B", 24)
pdf.set_text_color(*pdf.C_HEADER)
pdf.cell(0, 12, "Fluxo de IA Comercial", align="C",
         new_x="LMARGIN", new_y="NEXT")
pdf.set_text_color(0, 0, 0)
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 8, "Plano de 7 dias pra gerar caixa + automação completa",
         align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Arial", "", 12)
pdf.cell(0, 7, "Antecipação FGTS, Consignado INSS e Privado",
         align="C", new_x="LMARGIN", new_y="NEXT")

pdf.ln(15)
pdf.set_font("Arial", "B", 13)
pdf.set_text_color(46, 125, 50)
pdf.cell(0, 9, "CUSTO ZERO — todo o stack em tiers gratuitos",
         align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_text_color(0, 0, 0)

pdf.ln(15)
pdf.set_font("Arial", "B", 12)
pdf.set_text_color(*pdf.C_HEADER)
pdf.cell(0, 6, "O fluxo, em uma frase:", align="C",
         new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)
pdf.set_font("Arial", "", 11)
pdf.set_text_color(0, 0, 0)
fluxo = ("Base de contatos  →  Bot dispara mensagem-isca  →  Lead responde  →  IA Giovanna "
         "qualifica  →  CRM mostra ao closer  →  closer liga, simula e libera.")
pdf.multi_cell(0, 5.5, fluxo, align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(35)

pdf.set_font("Arial", "", 10)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 5, "Versão 1.0 — Junho de 2026", align="C",
         new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, "Customizado para GIGACRED — Instagram @gigacredcorrespondente",
         align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_text_color(0, 0, 0)

# =====================================================================
# SEÇÃO PRIORITÁRIA — RESOLVER FALTA DE CAIXA EM 7 DIAS
# =====================================================================
pdf.pb()
pdf.h1("Plano de 7 dias pra gerar caixa")

pdf.callout(
    "Leia esta seção primeiro",
    "Se o problema imediato da GIGACRED é falta de entrada de caixa, esta é "
    "a parte que importa AGORA. O fluxo completo (8 semanas) entrega o "
    "sistema redondo, mas você não precisa esperar 8 semanas pra ver "
    "antecipação fechando. Em 7 dias, com a base que JÁ TEM, dá pra colocar "
    "comissão na conta."
)

pdf.h2("A lógica do plano relâmpago")
pdf.p("Você não precisa do CRM bonitinho, da IA perfeita, do dashboard "
      "redondo pra começar a gerar receita. Precisa de três coisas:")
pdf.bullet([
    "Uma base de contatos (você já tem — clientes antigos, indicações, "
    "formulários do site, parceiros).",
    "Uma mensagem-isca testada (template pronto neste documento, Variantes "
    "A-E na Parte 1).",
    "Disciplina pra ligar rápido em quem responder (sem isso, lead esfria).",
])

pdf.p("Com esses 3, dá pra rodar manual nos primeiros dias enquanto a "
      "automação completa é montada. Receita entra na primeira semana.")

pdf.h2("Cronograma de 7 dias — dia a dia")

pdf.h3("Dia 1 (hoje) — Organizar a base")
pdf.bullet([
    "Junte TODOS os contatos que tem: planilha de clientes antigos, "
    "lista do formulário do site, exportar contatos do WhatsApp Business.",
    "Limpe duplicatas e contatos óbvios sem fit (estranhos, números errados).",
    "Meta: 200-500 contatos organizados em uma planilha (nome, telefone, origem).",
    "Prioridade: REATIVAÇÃO — clientes que já fecharam FGTS antes têm conversão "
    "muito maior porque já conhecem você.",
])

pdf.h3("Dia 2 — Preparar chip e mensagem")
pdf.bullet([
    "Compre um chip novo (R$10) E AQUEÇA por 2 dias antes de disparar em "
    "massa: mande 10-15 mensagens reais pra contatos seus (familiares, amigos) "
    "e RECEBA respostas. Isso cria histórico no número.",
    "Configure 5 variantes da mensagem-isca (Variantes A-E na Parte 1 deste doc).",
    "Defina horário do disparo: 9h-11h ou 14h-17h são os melhores (lead "
    "responde mais rápido nesses períodos).",
])

pdf.h3("Dia 3 — Primeiro disparo MANUAL (sem automação)")
pdf.bullet([
    "Dispare 30-50 mensagens MANUALMENTE pela manhã (variando entre as "
    "5 variantes). Não precisa de bot ainda — você faz pelo WhatsApp Web.",
    "Anote quem respondeu numa planilha.",
    "Quem responder, VOCÊ mesmo (ou um closer) puxa conversa imediatamente: "
    "pergunta saldo, adesão, urgência (manual ainda, sem IA).",
    "Meta realista do dia: 10 respostas → 5 conversas qualificadas → 1-2 "
    "antecipações fechadas até amanhã.",
])

pdf.h3("Dia 4 — Repetir e simular nos bancos")
pdf.bullet([
    "Outras 30-50 mensagens, manhã e tarde (intervalo de 1-2 minutos entre "
    "envios manuais).",
    "Para cada lead qualificado de ontem e hoje: SIMULE nos 3 bancos "
    "(BMG, Daycoval, C6) e mande o valor.",
    "Quem topar, gere proposta e envie pro lead assinar.",
    "Meta acumulada: 4-6 antecipações fechadas até dia 5.",
])

pdf.h3("Dia 5 — Primeira receita entra")
pdf.bullet([
    "Antecipações fechadas dia 3-4 começam a liberar (BMG libera em 24-48h).",
    "Comissão cai na conta da GIGACRED — primeira entrada de caixa do plano.",
    "Em paralelo: continua disparo (50-80 mensagens, sempre dentro do limite).",
])

pdf.h3("Dia 6 — Montar bot básico")
pdf.bullet([
    "Com receita entrando, agora vale investir tempo (não dinheiro — ainda "
    "custo zero) no bot. Subir whatsapp-web.js no Oracle Free.",
    "Bot dispara a isca automaticamente pros próximos 100 da base.",
    "IA Giovanna ainda não — você assume manual as respostas. Só o disparo "
    "vira automático.",
])

pdf.h3("Dia 7 — Conectar a IA Giovanna")
pdf.bullet([
    "Criar conta Google AI Studio (custo zero), pegar API key Gemini.",
    "Configurar prompt da Giovanna (template pronto na Parte 3 deste doc).",
    "Giovanna agora responde automaticamente; você só pega quando ela passa o lead.",
    "A partir daí, o fluxo roda sozinho enquanto você dorme.",
])

pdf.h2("Receita estimada na primeira semana")
pdf.bullet([
    "Base disparada: 200-300 contatos (manual + bot).",
    "Taxa de resposta esperada (base de reativação): 25-40%.",
    "Respostas qualificadas: 30-60 conversas.",
    "Fechamento: 8-15 antecipações.",
    "Ticket médio FGTS: R$ 4.500 liberado.",
    "Comissão típica do correspondente (5%): R$ 225 por antecipação.",
])

pdf.callout(
    "Receita realista da primeira semana",
    "8 a 15 antecipações × R$ 225 de comissão = R$ 1.800 a R$ 3.375 de "
    "caixa NOVA na primeira semana. Custo do plano: R$ 10 (chip novo). "
    "ROI absurdo, mas só funciona com DISCIPLINA — ligar rápido em "
    "TODO lead que responder, não deixar esfriar."
)

pdf.h2("O erro que mata o plano de 7 dias")
pdf.p("O motivo número 1 pelo qual esse plano falha é SIMPLES: o dono "
      "manda as mensagens, lead responde, e o dono não consegue ligar "
      "rápido porque está ocupado com outra coisa. Resultado: lead esfria, "
      "responde 'depois eu vejo', e nunca fecha.")

pdf.p("Solução: nos primeiros 7 dias, dedique 2 BLOCOS de 2 horas por dia "
      "(manhã + tarde) exclusivamente pra responder e ligar. Sem essa "
      "disciplina, o plano não funciona — não importa quão boa seja a base.")

# =====================================================================
# CONTEXTO DO NEGÓCIO
# =====================================================================
pdf.pb()
pdf.h1("Por que a GIGACRED precisa desse fluxo")

pdf.h2("O cenário do correspondente bancário em 2026")
pdf.p("O mercado de antecipação do saque-aniversário FGTS é o mais competitivo "
      "do segmento de crédito consignado. Centenas de correspondentes anunciam "
      "no Instagram e Facebook todos os dias, com promessas similares. O que "
      "diferencia quem fecha e quem perde o lead é uma única variável: "
      "velocidade de resposta.")

pdf.callout(
    "O dado que define o jogo",
    "Lead que clica no anúncio e não recebe resposta em até 5 minutos tem "
    "80% mais chance de já ter clicado em outro correspondente. Em 30 minutos, "
    "essa chance vira praticamente 100%. A IA resolve isso respondendo em "
    "menos de 1 minuto, 24 horas por dia, 7 dias por semana."
)

pdf.h2("Os 3 problemas que a GIGACRED resolve com IA")
pdf.bullet([
    "Volume crescente de leads no Instagram: hoje você responde manualmente, "
    "perde os de madrugada/fim-de-semana, e o time fica sobrecarregado.",
    "Leads ruins ocupando o closer: muitos perguntam só por curiosidade ou "
    "têm restrição no FGTS (não fizeram a adesão na Caixa). O closer perde "
    "tempo descobrindo isso na ligação.",
    "Sem dados pra evoluir: você não sabe quais campanhas trazem leads que "
    "fecham, qual banco está dando melhor taxa, qual horário converte mais.",
])

pdf.h2("O que a IA SDR vai fazer pela GIGACRED")
pdf.bullet([
    "Responder TODO lead em até 1 minuto, no Instagram e WhatsApp.",
    "Perguntar as 5 informações que definem se vale a ligação: saldo FGTS "
    "estimado, se já fez adesão ao saque-aniversário, motivo do dinheiro, "
    "urgência, e produto certo (FGTS, INSS, privado).",
    "Passar pro closer só os leads viáveis, com resumo de 3 linhas.",
    "Registrar tudo no CRM para você ver: quantos leads fecharam, qual banco "
    "deu melhor taxa, qual closer converte mais.",
])

# =====================================================================
# VISÃO GERAL DO FLUXO
# =====================================================================
pdf.pb()
pdf.h1("O fluxo, visualmente")
pdf.code("""
   ┌──────────────┐
   │  PASSO 0     │   Base de prospecção
   │  Base        │   (planilha CSV importada: clientes antigos,
   │              │    leads de form, indicações, parceiros)
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │  PASSO 1     │   Bot dispara mensagem-isca em massa
   │  Bot WhatsApp│   (cadência controlada — evita ban)
   │              │   "Oi! Sabia que dá pra antecipar FGTS?"
   └──────┬───────┘
          │
          │  lead respondeu? sim →
          ▼
   ┌──────────────┐
   │  PASSO 2     │   IA Giovanna ASSUME a conversa
   │  IA Giovanna (SDR)│   imediatamente que o lead responde
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │  PASSO 3     │   IA descobre via diálogo:
   │  Qualificação│   - Saldo FGTS estimado
   │              │   - Já fez adesão ao Saque-Aniv?
   │              │   - Motivo + urgência
   │              │   - Produto certo (FGTS/INSS/Privado)
   └──────┬───────┘
          │
          │  score ≥ 80? sim → handoff
          ▼
   ┌──────────────┐
   │  PASSO 4     │   IA escreve resumo + recomenda banco,
   │  Plataforma  │   lead aparece na lista do closer
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │  PASSO 5     │   Closer abre, lê resumo,
   │  Closer      │   simula, liga, libera no PIX.
   └──────────────┘
""")

# =====================================================================
# PASSO 0 — BASE DE PROSPECÇÃO
# =====================================================================
pdf.pb()
pdf.step_header(0, "Montar a base de prospecção")

pdf.p("O fluxo da GIGACRED parte de uma BASE de contatos já conhecidos — "
      "não espera o lead vir pelo anúncio. Quanto melhor a base, melhor o "
      "resultado. Disparo pra base ruim gera ban do número e zero conversão.")

pdf.h2("De onde vêm os contatos da base (em ordem de qualidade)")
pdf.bullet([
    "REATIVAÇÃO: clientes da GIGACRED que JÁ FECHARAM antes. FGTS pode renovar "
    "todo ano — base de OURO, conversão alta, zero risco de ban.",
    "Lead Magnet: quem baixou simulador, ebook, calculadora de FGTS no site.",
    "Formulário do site: quem pediu simulação e não fechou na época.",
    "Indicação: clientes antigos que indicaram conhecidos.",
    "Parceiros: contadores, consultores de RH, vendedores autônomos.",
])

pdf.callout(
    "Base com opt-in vs base fria",
    "Quem deixou o telefone num formulário do site, baixou um lead magnet, "
    "ou foi indicado: tem opt-in implícito ou expresso e é a base SEGURA. "
    "Lista comprada na internet ou raspagem do Instagram: ILEGAL pela LGPD e "
    "gera ban em horas. Comece SÓ com base própria — funciona melhor mesmo."
)

pdf.h2("Como o CRM enxerga a base")
pdf.image_full(MOCKUPS / "05_base_prospeccao.png",
               caption="Tela 'Base de prospecção'. 1.247 contatos importados, "
                       "127 disparados hoje (limite seguro 150/chip/dia), 31 "
                       "responderam — IA já assumiu, qualificou ou está em "
                       "conversa com cada um. Taxa de bloqueio 2.4% (saudável).")

pdf.p("Antes de iniciar o disparo, você importa um CSV simples (nome, telefone, "
      "origem). O CRM marca cada disparo, registra resposta, identifica quem "
      "bloqueou — sinal pra parar IMEDIATAMENTE se passar de 5% de bloqueio.")

# =====================================================================
# PASSO 1 — DISPARO EM MASSA
# =====================================================================
pdf.pb()
pdf.step_header(1, "Bot dispara mensagem-isca em massa")

pdf.p("O bot pega a base e começa a disparar mensagens, uma por vez, com "
      "intervalo entre cada envio. Não é spam massivo — é cadência controlada "
      "que simula comportamento humano e evita ban do Meta.")

pdf.h2("As 4 regras pra não tomar ban do WhatsApp")
pdf.bullet([
    "Limite diário: máximo 150 disparos/dia POR CHIP. Acima disso, o Meta "
    "começa a marcar o número como spam e bane.",
    "Intervalo entre envios: 40 a 90 segundos aleatórios (nunca igual). "
    "Bot que dispara a cada 5 segundos é banido em 1 hora.",
    "Mensagens variadas: 5 a 10 templates diferentes da mesma isca, "
    "escolhidos aleatoriamente. Mensagem idêntica em 100 envios = ban certo.",
    "Aquecimento do chip: chip novo NÃO dispara em massa. Por 2-4 semanas, "
    "manda 20-40 msg/dia, conversa real, recebe respostas. Depois sobe gradual.",
])

pdf.h2("5 variantes da mensagem-isca (exemplo pronto)")
pdf.code("""Variante A:
"Oi! Tudo bem? Aqui é a Giovanna da GIGACRED. Você sabia que dá pra
antecipar até 7 anos do seu saque-aniversário do FGTS e receber
tudo no PIX?"

Variante B:
"Olá! Sou a Giovanna, consultora da GIGACRED. Posso te mandar uma
simulação rápida de quanto dá pra antecipar do seu FGTS?"

Variante C:
"Oi, tudo bem? Giovanna aqui da GIGACRED. Tem alguns minutos pra eu
te explicar como antecipar o FGTS sem complicação?"

Variante D:
"Olá! Aqui é a GIGACRED. Você sabia que pode receber o seu FGTS
agora, sem esperar o aniversário? Quer simular sem compromisso?"

Variante E:
"Oi! Sou a Giovanna. Trabalho com antecipação de FGTS — em 1-2 dias
úteis o dinheiro cai no seu PIX. Te interessa saber quanto dá?\"""")

pdf.h2("Cálculo do volume seguro (1 chip)")
pdf.bullet([
    "150 disparos/dia → taxa de resposta 20-30% → 30-45 leads novos/dia.",
    "Desses, 40-50% são qualificados pela IA → 12-22 leads pro closer/dia.",
    "Pra DOBRAR sem aumentar custo: 2 chips em rotação (300 disparos/dia).",
    "Pra escalar muito: API oficial Meta com templates aprovados — "
    "custa R$0,30-0,90/conversa, mas é legal e SEM risco de ban.",
])

pdf.callout(
    "Sinal de alerta: taxa de bloqueio > 5%",
    "Se mais de 5% dos contatos bloquearem o número, PARE o disparo no mesmo "
    "dia. Algo está errado: base muito fria ou mensagem soa como spam. "
    "Ajuste o texto, troque origem da base e teste com 30 contatos antes "
    "de soltar 150."
)

# =====================================================================
# PASSO 2 — IA ASSUME NA HORA
# =====================================================================
pdf.pb()
pdf.step_header(2, "Lead responde — IA Giovanna assume na hora")

pdf.p("Assim que o lead responde QUALQUER coisa (\"sim\", \"o que é isso?\", "
      "\"quanto?\", \"para de me mandar mensagem\"), a IA Giovanna entra em ação "
      "em segundos. Ela analisa a resposta e decide o que fazer:")
pdf.bullet([
    "Lead interessado → começa a qualificar (BANT adaptado).",
    "Lead curioso mas reticente → tira a dúvida e tenta engatar.",
    "Lead irritado / pediu pra parar → responde educado, dá baixa imediata e "
    "REMOVE o contato da base (compliance LGPD: direito de oposição).",
    "Lead pediu humano direto → faz handoff imediato sem qualificar.",
])

pdf.p("Veja como fica uma conversa típica do lead que engaja:")

pdf.image_full(MOCKUPS / "01_conversa.png",
               caption="Conversa começa com a isca da IA (mensagem verde no "
                       "topo, 14:20). Lead responde 'Sério? quanto da?' e a "
                       "IA assume. Em 6 minutos descobriu saldo, adesão, "
                       "motivo, urgência. Score 88 → handoff disparado.")

# =====================================================================
# PASSO 3 — IA BIA
# =====================================================================
pdf.pb()
pdf.step_header(3, "A IA Giovanna qualifica via diálogo")

pdf.p("A IA Giovanna é um prompt rodando no Gemini 1.5 Flash (gratuito até 1500 "
      "chamadas/dia). Para cada mensagem que chega, o CRM faz uma chamada à "
      "API do Gemini com:")
pdf.bullet([
    "Quem é a Giovanna: consultora virtual da GIGACRED, tom caloroso e direto.",
    "O que a GIGACRED faz: correspondente de FGTS, INSS, Privado, bancos parceiros.",
    "Histórico das últimas mensagens da conversa.",
    "A nova mensagem do lead.",
])

pdf.h2("As 5 informações que a Giovanna DEVE descobrir")
pdf.bullet([
    "Saldo FGTS estimado (o lead geralmente sabe de cabeça).",
    "Se já fez adesão ao Saque-Aniversário na Caixa (sem isso, NÃO dá pra "
    "antecipar — é critério eliminatório).",
    "Motivo do dinheiro (pra calibrar a urgência e o tom da abordagem).",
    "Quando precisa receber (hoje? semana? sem pressa?).",
    "Vínculo de trabalho (CLT, aposentado, autônomo) — define o produto.",
])

pdf.h2("Sistema de score adaptado pro nicho")
pdf.bullet([
    "Saldo (0-25): R$10k+ = 25 pts; R$5-10k = 20; R$2-5k = 15; <R$2k = 5.",
    "Adesão FGTS (0-25): fez = 25 pts; pode fazer = 15; modo saque-rescisão = 0.",
    "Urgência (0-25): hoje/amanhã = 25; semana = 18; mês = 10; sem prazo = 5.",
    "Vínculo + qualidade (0-25): CLT estável = 25; INSS = 22; autônomo = 12.",
])
pdf.p("Score ≥ 80 → handoff imediato pro closer. Entre 60-79 → continua "
      "qualificando ou agenda follow-up. Abaixo de 60 → park educado.")

pdf.h2("Exemplo do prompt da Giovanna (trecho)")
pdf.code("""Você é a Giovanna, consultora virtual da GIGACRED Correspondente.
Sua função é qualificar leads que querem antecipar FGTS, INSS ou
consignado privado. Você NÃO simula valores definitivos, NÃO fecha
contrato, NÃO promete taxa — isso é função do closer humano.

REGRAS:
- Tom caloroso, direto, brasileiro. Sem formalidades excessivas.
- NUNCA mais de 2 frases por mensagem.
- UMA pergunta por mensagem.
- Se o lead não fez adesão ao Saque-Aniversário, EXPLIQUE como
  fazer no app FGTS da Caixa (não desqualifica, agenda follow-up).
- Se perguntarem taxa exata, diga: "Vou pedir pra o Carlos do
  time te passar a taxa atualizada — o BMG e o Daycoval estão
  competitivos hoje."

O QUE DESCOBRIR (BANT adaptado):
1. Saldo FGTS estimado
2. Adesão ao Saque-Aniversário (CRITÉRIO ELIMINATÓRIO)
3. Motivo do dinheiro
4. Urgência
5. Vínculo de trabalho""")

# =====================================================================
# PASSO 4
# =====================================================================
pdf.pb()
pdf.step_header(4, "IA passa o lead para a plataforma")

pdf.p("Score chegou em 80+? A IA Giovanna faz 3 coisas:")
pdf.bullet([
    "Escreve um resumo de 3 linhas com tudo que o closer precisa.",
    "Recomenda os 3 bancos com melhor taxa pro perfil (BMG, Daycoval, C6 ou Pan).",
    "Marca o lead como 'qualificado' e envia notificação no Slack do closer.",
])

pdf.p("E o lead aparece na plataforma — uma página que os closers da GIGACRED "
      "abrem no navegador. Veja:")

pdf.image_full(MOCKUPS / "02_lista_leads.png",
               caption="Tela 'Leads pra ligar agora'. Cada linha é um lead qualificado, "
                       "com produto, valor estimado, score, motivo. Total estimado do dia "
                       "já calculado no topo. Closer escolhe o de maior score e clica em 'Ligar'.")

pdf.h2("O resumo que a Giovanna escreve (formato padronizado)")
pdf.code('''"José, 34, CLT, quer antecipar FGTS — URGENTE.
 Saldo ~R$ 8k, já fez adesão. Motivo: quitar dívida.
 Expectativa: R$ 4,5-5,2k no PIX em 1-2 dias.
 Recomendado: simular BMG ou Daycoval."''')

pdf.p("Esse formato é definido no prompt — a Giovanna sempre escreve no mesmo "
      "padrão (perfil + saldo + adesão + motivo + valor estimado + banco "
      "recomendado). O closer lê em 10 segundos e já sabe o que falar.")

# =====================================================================
# PASSO 5
# =====================================================================
pdf.pb()
pdf.step_header(5, "Closer pega o número, simula e liga")

pdf.p("O closer abre o lead, lê o resumo, e tem tudo na mão: telefone, "
      "produto, valor estimado, motivo, banco recomendado.")

pdf.image_full(MOCKUPS / "03_detalhe_lead.png",
               caption="Tela do lead José. À esquerda: dados + resumo da IA. "
                       "À direita: botão de ligar, SLA contando, e bloco de "
                       "'Simulação sugerida' com 4 bancos comparados.")

pdf.h2("Bloco diferencial: simulação sugerida")
pdf.p("Esse é o ganho de tempo grande do closer da GIGACRED. Antes de ligar, "
      "ele já vê os 4 bancos com valor estimado e taxa. Pode chegar na "
      "ligação dizendo: 'José, simulei aqui pra você — pelo BMG dá R$ 5.180 "
      "no PIX, taxa 1.79% ao mês. Topa fechar?'")

pdf.h2("Depois da ligação — registrar resultado")
pdf.bullet([
    "[OK]  Fechou antecipação — registra banco, valor liberado, taxa.",
    "[ ? ] Vai pensar — agendar follow-up em 24h.",
    "[X]   Não fechou — registrar motivo (taxa, valor abaixo do esperado, "
    "outro correspondente, restrição encontrada).",
    "[--]  Não atendeu — agendar 2ª tentativa em 1h.",
])

# =====================================================================
# DASHBOARD
# =====================================================================
pdf.pb()
pdf.h1("Para o dono: painel de acompanhamento")

pdf.p("O painel mostra os números essenciais sem virar relatório complexo. "
      "Em tempo real, você sabe se a operação está saudável.")

pdf.image_full(MOCKUPS / "04_dashboard.png",
               caption="Painel do dia. 4 métricas no topo (leads recebidos, qualificados, "
                       "fechados, volume liberado), funil completo, distribuição por produto "
                       "e por banco. Atualizado em tempo real via Supabase Realtime.")

pdf.h2("As perguntas que o painel responde")
pdf.bullet([
    "Quantos leads chegaram hoje? Mais ou menos que ontem? "
    "(Identificar campanhas Instagram que estão performando.)",
    "Qual produto está dando mais resultado este mês? "
    "(FGTS vs INSS vs Privado — pra calibrar o budget de Ads.)",
    "Qual banco está liberando mais? E com qual taxa? "
    "(Pra negociar comissão melhor com os parceiros.)",
    "Qual closer está convertendo mais? "
    "(Pra premiar quem performa e treinar quem está abaixo.)",
])

# =====================================================================
# O CRM ENXUTO ADAPTADO
# =====================================================================
pdf.pb()
pdf.h1("O CRM enxuto: 3 tabelas adaptadas pro nicho")

pdf.p("Esta versão tem campos específicos pra correspondente bancário "
      "(saldo FGTS, banco escolhido, valor liberado, taxa). O schema todo "
      "cabe em 3 tabelas e roda no Supabase Free (gratuito).")

pdf.code("""-- 1. leads — todo contato que entrou pelo bot
CREATE TABLE leads (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  nome            TEXT,
  telefone        TEXT NOT NULL UNIQUE,
  cpf             TEXT,                       -- opcional, capturar só no closer

  -- Origem e atribuição
  origem          TEXT,                       -- 'instagram_ads', 'facebook', 'indicacao'
  campanha        TEXT,                       -- nome da campanha de ads
  closer_email    TEXT,                       -- quem está atendendo

  -- Produto e financeiro
  produto         TEXT CHECK (produto IN ('fgts','consignado_inss',
                                          'consignado_privado','outro')),
  saldo_fgts_estimado  NUMERIC(10,2),
  valor_estimado       NUMERIC(10,2),         -- quanto a IA estimou que dá pra liberar
  valor_liberado       NUMERIC(10,2),         -- depois que fecha
  banco_fechado        TEXT,                  -- 'bmg', 'daycoval', 'c6', 'pan', 'master'
  taxa_aplicada        NUMERIC(5,3),          -- ex: 1.790 (% am)

  -- Critérios qualificadores
  fez_adesao_saque_aniversario  BOOLEAN,      -- crítico pra FGTS
  vinculo               TEXT,                  -- 'clt', 'inss', 'autonomo', 'publico'
  motivo                TEXT,                  -- texto livre

  -- Status e score
  status          TEXT DEFAULT 'novo'
                    CHECK (status IN ('novo','em_conversa','qualificado',
                                      'em_negociacao','fechou','perdido','park')),
  score           INTEGER DEFAULT 0,
  resumo_ia       TEXT,

  -- Timestamps
  criado_em       TIMESTAMPTZ DEFAULT NOW(),
  qualificado_em  TIMESTAMPTZ,
  fechado_em      TIMESTAMPTZ
);

-- 2. mensagens — histórico da conversa
CREATE TABLE mensagens (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id     UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  autor       TEXT NOT NULL CHECK (autor IN ('lead','ia','closer','sistema')),
  texto       TEXT NOT NULL,
  criado_em   TIMESTAMPTZ DEFAULT NOW()
);

-- 3. ligacoes — cada tentativa de contato do closer
CREATE TABLE ligacoes (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id         UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  closer_email    TEXT NOT NULL,
  resultado       TEXT CHECK (resultado IN ('fechou','vai_pensar',
                                            'nao_fechou','nao_atendeu')),
  motivo_perda    TEXT,                       -- se nao_fechou: 'taxa','valor',
                                              -- 'outro_corresp','restricao_fgts'
  observacao      TEXT,
  ligado_em       TIMESTAMPTZ DEFAULT NOW()
);

-- Índices essenciais
CREATE INDEX idx_leads_status_score ON leads(status, score DESC);
CREATE INDEX idx_leads_produto ON leads(produto);
CREATE INDEX idx_leads_origem ON leads(origem, criado_em);""")

# =====================================================================
# CUSTO ZERO
# =====================================================================
pdf.pb()
pdf.h1("Custo zero — stack completo da GIGACRED")

pdf.h2("Componentes (todos R$0/mês)")
pdf.bullet([
    "Bot WhatsApp: whatsapp-web.js (open source).",
    "IA SDR: Gemini 1.5 Flash via AI Studio — 1500 req/dia grátis.",
    "Backend: Node.js + Express.",
    "Banco: Supabase Free (500MB + 2GB bandwidth).",
    "Hospedagem: Oracle Cloud Always Free (4 vCPUs + 24GB RAM).",
    "Painel: Retool Free (até 5 closers) ou HTML/JS no GitHub Pages.",
    "Notificação: Slack Free.",
    "Monitoramento: UptimeRobot Free (avisa se WhatsApp cair).",
])

pdf.h2("Até onde o custo zero atende a GIGACRED")
pdf.bullet([
    "Volume: até 150 conversas qualificadas por dia (= ~450 leads brutos/dia).",
    "Banco: ~100 mil mensagens guardadas (cobre 6+ meses tranquilo).",
    "Closers: até 5 usuários simultâneos no painel.",
])

pdf.callout(
    "Quando vai precisar pagar algo",
    "Quando o volume passar de 4.500 conversas qualificadas no mês ou o time "
    "passar de 5 closers. Aí: Retool Team (USD 10/closer extra) ou Gemini "
    "Pay-as-You-Go (~USD 10-30/mês). Mesmo nessa fase, custo total fica abaixo "
    "de R$ 300/mês — irrelevante perto do volume liberado."
)

pdf.h2("ROI estimado (cenário realista)")
pdf.p("Considere uma operação de porte médio em correspondente bancário:")
pdf.bullet([
    "Volume: 30 leads novos/dia (Instagram Ads).",
    "Taxa de qualificação pela IA: 45% → 14 leads qualificados/dia.",
    "Taxa de fechamento pelo closer: 35% → 5 antecipações/dia.",
    "Ticket médio FGTS: R$ 4.500 liberado.",
    "Comissão típica do correspondente: 4-7% do liberado.",
])
pdf.p("Resultado por dia:")
pdf.bullet([
    "Volume liberado: R$ 22.500.",
    "Comissão estimada (5%): R$ 1.125/dia.",
    "Mensal (22 dias úteis): R$ 24.750.",
    "Custo do stack: R$ 0,00.",
])

# =====================================================================
# LGPD E COMPLIANCE
# =====================================================================
pdf.pb()
pdf.h1("Compliance — LGPD e regulação financeira")

pdf.callout(
    "Dado de FGTS é categoria sensível",
    "Saldo de FGTS, vínculo trabalhista, CPF, valores de operação financeira "
    "são dados pessoais que exigem cuidado especial. A LGPD prevê multas "
    "altas para vazamento — implementar compliance desde o início custa muito "
    "menos do que arrumar depois."
)

pdf.h2("Checklist LGPD pra correspondente bancário")
pdf.bullet([
    "Política de privacidade visível no link do Instagram e no início "
    "da conversa do WhatsApp (texto curto + link).",
    "Base legal explícita: 'tratamento para execução de procedimento "
    "preliminar a contrato' (LGPD art. 7º, V) — não precisa consentimento "
    "explícito, mas precisa transparência.",
    "Capacidade de excluir TODOS os dados de um lead se ele pedir — endpoint "
    "DELETE /api/lead/{id} que apaga em cascade leads + mensagens + ligacoes.",
    "Não enviar CPF ou saldo FGTS por canais não-seguros (e-mail comum, "
    "Telegram público). Manter dentro do CRM com HTTPS.",
    "Logs de quem acessou cada lead — pra rastreabilidade se houver "
    "questionamento. (Campo 'closer_email' em ligacoes já ajuda.)",
    "Backups criptografados (Supabase já faz por padrão).",
    "Retenção: dados de lead que não fechou devem ser deletados após "
    "12 meses sem contato (rotina mensal).",
])

pdf.h2("Para o Banco Central (regulação de correspondente)")
pdf.bullet([
    "Correspondente NÃO pode prometer aprovação ('garanto que aprovam'). "
    "O prompt da Giovanna deve evitar essa linguagem — sempre usar 'estimado', "
    "'simulação inicial', 'depende da análise do banco'.",
    "Não pode aplicar taxa diferente da informada pelo banco — a Giovanna NUNCA "
    "diz taxa específica, isso fica com o closer (que olha a tabela atualizada).",
    "Não pode oferecer 'dinheiro na hora' (publicidade enganosa). FGTS sai "
    "em 1-2 dias úteis e isso deve ser dito sempre.",
])

# =====================================================================
# PRÓXIMOS PASSOS
# =====================================================================
pdf.pb()
pdf.h1("Próximos passos pra GIGACRED")

pdf.h2("Roadmap acelerado de 4 semanas")

pdf.h3("Semana 1 — Fundação")
pdf.bullet([
    "Criar contas: Supabase Free, Google AI Studio (gerar API key Gemini), "
    "Oracle Cloud Free, GitHub.",
    "Aplicar o schema SQL (3 tabelas adaptadas) no Supabase.",
    "Subir backend Node básico no Oracle Cloud Free.",
    "Testar endpoint POST /api/mensagem-recebida com Postman.",
])

pdf.h3("Semana 2 — Bot WhatsApp + IA Giovanna v1")
pdf.bullet([
    "Pegar um chip dedicado (R$ 10) para o número de WhatsApp da operação IA. "
    "Não usar o número pessoal do dono.",
    "Implementar bot whatsapp-web.js conectado ao backend.",
    "Implementar prompt da Giovanna no Gemini, focado em FGTS no início.",
    "Testar com 10 conversas simuladas (você simula o lead).",
])

pdf.h3("Semana 3 — Plataforma + closer no fluxo")
pdf.bullet([
    "Montar painel no Retool Free com as 4 telas: lista, detalhe, dashboard, "
    "registrar ligação.",
    "Cadastrar os closers (e-mail + senha simples).",
    "Conectar notificação de handoff ao Slack (canal #leads-quentes).",
    "Treinar o time pra usar: 1h de treinamento + 1 dia de acompanhamento.",
])

pdf.h3("Semana 4 — Piloto e ajustes")
pdf.bullet([
    "Ligar o anúncio do Instagram apontando para o WhatsApp da IA.",
    "Acompanhar 20-30 leads reais, ler todos os transcripts, anotar onde a "
    "Giovanna errou (não perguntou X, perguntou de forma confusa, etc).",
    "Ajustar prompt da Giovanna 2-3 vezes com base nos erros reais.",
    "Estender prompt pra cobrir Consignado INSS e Privado também.",
    "Lançar oficial.",
])

pdf.h2("Métricas pra acompanhar nas primeiras 4 semanas")
pdf.bullet([
    "Tempo médio de primeira resposta: alvo < 30 segundos.",
    "Taxa de qualificação (recebidos → qualificados): alvo 40-50%.",
    "Taxa de fechamento (qualificados → fechou): alvo 30-40%.",
    "Volume liberado/semana: comparar com o mesmo período sem IA.",
    "Satisfação do closer: pergunta direta: 'os leads estão melhores?'",
])

pdf.h2("Sinais de sucesso aos 30 dias")
pdf.bullet([
    "Closer dizendo: 'estou ligando pra menos leads, mas fechando mais'.",
    "Volume liberado crescente sem aumentar custo de Ads proporcionalmente.",
    "Giovanna respondendo lead da madrugada (que antes ficava sem resposta) "
    "e esse lead fechando no dia seguinte.",
    "Você (dono) abrindo o painel pela manhã e sabendo em 30 segundos "
    "como foi o dia anterior.",
])

# =====================================================================
pdf.output(str(PDF_OUT))
print(f"PDF gerado: {PDF_OUT}")
print(f"Tamanho: {PDF_OUT.stat().st_size / 1024:.1f} KB")
print(f"Páginas: {pdf.page_no()}")

# -*- coding: utf-8 -*-
"""
Gera o documento "fluxo-ia-empresa.pdf" usando fpdf2.
Execução: py gerar-pdf.py
"""
from fpdf import FPDF
from pathlib import Path

OUT_DIR = Path(__file__).parent
PDF_OUT = OUT_DIR / "fluxo-ia-empresa.pdf"

# Fontes do sistema Windows (suportam unicode)
FONTS_DIR = "C:/Windows/Fonts"

class Doc(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(left=22, top=20, right=22)

        # Registra Arial em regular, bold, italic
        self.add_font("Arial", "", f"{FONTS_DIR}/arial.ttf")
        self.add_font("Arial", "B", f"{FONTS_DIR}/arialbd.ttf")
        self.add_font("Arial", "I", f"{FONTS_DIR}/ariali.ttf")
        self.add_font("Consolas", "", f"{FONTS_DIR}/consola.ttf")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Fluxo de IA Comercial — versão custo zero — pág. {self.page_no()}",
                  align="C")
        self.set_text_color(0, 0, 0)

    # ---- helpers ----
    # multi_cell com new_x="LMARGIN", new_y="NEXT" garante que cursor
    # volta pra margem esquerda na próxima linha após cada bloco.
    NX = "LMARGIN"
    NY = "NEXT"

    def h1(self, txt):
        self.ln(6)
        self.set_font("Arial", "B", 18)
        self.set_text_color(31, 56, 100)
        self.multi_cell(0, 8, txt, new_x=self.NX, new_y=self.NY)
        self.ln(2)
        self.set_text_color(0, 0, 0)

    def h2(self, txt):
        self.ln(3)
        self.set_font("Arial", "B", 13)
        self.set_text_color(46, 84, 150)
        self.multi_cell(0, 7, txt, new_x=self.NX, new_y=self.NY)
        self.ln(1)
        self.set_text_color(0, 0, 0)

    def h3(self, txt):
        self.ln(2)
        self.set_font("Arial", "B", 11)
        self.set_text_color(46, 84, 150)
        self.multi_cell(0, 6, txt, new_x=self.NX, new_y=self.NY)
        self.set_text_color(0, 0, 0)

    def p(self, txt):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 5.5, txt, new_x=self.NX, new_y=self.NY)
        self.ln(1.5)

    def i(self, txt):
        self.set_font("Arial", "I", 11)
        self.multi_cell(0, 5.5, txt, new_x=self.NX, new_y=self.NY)
        self.ln(1.5)
        self.set_font("Arial", "", 11)

    def bullet(self, items):
        self.set_font("Arial", "", 11)
        for it in items:
            self.multi_cell(0, 5.5, f"•  {it}", new_x=self.NX, new_y=self.NY)
        self.ln(1.5)

    def code(self, txt):
        self.set_font("Consolas", "", 8.5)
        self.set_fill_color(244, 244, 244)
        self.multi_cell(0, 4.5, txt, fill=True, border=0, new_x=self.NX, new_y=self.NY)
        self.set_font("Arial", "", 11)
        self.ln(2)

    def pb(self):
        self.add_page()


pdf = Doc()

# ======================================================================
# CAPA
# ======================================================================
pdf.add_page()
pdf.ln(40)
pdf.set_font("Arial", "B", 28)
pdf.set_text_color(31, 56, 100)
pdf.cell(0, 14, "Fluxo de IA Comercial", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(4)
pdf.set_font("Arial", "B", 14)
pdf.set_text_color(0, 0, 0)
pdf.cell(0, 8, "Guia para construir do zero — do primeiro contato ao closer humano",
         align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(20)

# Badge custo zero
pdf.set_font("Arial", "B", 14)
pdf.set_text_color(46, 125, 50)
pdf.cell(0, 9, "VERSÃO CUSTO ZERO — usando apenas tiers gratuitos",
         align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(8)
pdf.set_text_color(0, 0, 0)

pdf.set_font("Arial", "I", 11)
pdf.cell(0, 6, "Bots de captura · IA SDR com webhook · CRM próprio · Closer humano",
         align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(40)

pdf.set_font("Arial", "", 10)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 5, "Versão 1.0 — Junho de 2026", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, "Documento técnico-executivo", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_text_color(0, 0, 0)

# ======================================================================
# SUMÁRIO EXECUTIVO
# ======================================================================
pdf.pb()
pdf.h1("Sumário executivo")

pdf.p("Este documento descreve, do ponto de vista técnico e operacional, como uma empresa pode construir do zero um fluxo de IA comercial que automatiza a qualificação de leads e entrega contatos prontos para um vendedor humano (closer) fechar.")

pdf.p("TODO o stack desta versão usa exclusivamente tiers gratuitos. A operação roda sem custo financeiro até aproximadamente 100-150 conversas por dia (4500/mês), o que cobre a fase de validação e os primeiros meses da maioria das operações comerciais pequenas. O documento deixa claros os limites de cada free tier e o ponto em que será necessário migrar para tier pago.")

pdf.p("O fluxo é organizado em cinco camadas independentes mas interconectadas. Cada camada pode ser construída isoladamente, validada, e só então integrada à próxima — o que reduz risco e permite que pequenas equipes (1-3 pessoas) entreguem em 8 semanas.")

pdf.h2("O que você vai encontrar")
pdf.bullet([
    "Arquitetura completa em 5 camadas, com diagrama em texto e explicação por camada.",
    "Stack tecnológica 100% gratuita (Gemini, Supabase, Oracle Cloud, Retool, Slack, Cloudflare — todos em free tier).",
    "Schema de banco de dados de um CRM mínimo (PostgreSQL/Supabase) — 5 tabelas resolvem o problema.",
    "Endpoints REST do CRM — o que precisa expor para o time operar.",
    "Prompt comentado para a IA SDR, com anti-padrões reais de produção.",
    "Payload JSON do webhook IA-para-Closer, com assinatura HMAC.",
    "Roadmap de 8 semanas, semana a semana.",
    "Detalhamento do que cada free tier suporta e quando deixa de ser custo zero.",
    "Riscos e anti-padrões que custam caro descobrir tarde.",
])

pdf.h2("Para quem este documento serve")
pdf.bullet([
    "Founder ou CTO planejando o primeiro fluxo automatizado da empresa.",
    "Gerente comercial que precisa explicar o projeto ao time técnico.",
    "Desenvolvedor responsável por implementar — encontrará arquitetura, schemas e prompts prontos para adaptar.",
    "Consultor vendendo este tipo de solução para clientes — use como template.",
])

pdf.h2("O que este documento NÃO é")
pdf.bullet([
    "Não é um tutorial passo-a-passo de código pronto para copiar e colar.",
    "Não é específico para um nicho (ecommerce, educação, saúde) — é um esqueleto adaptável.",
    "Não substitui consultoria especializada em casos de alta complexidade regulatória (LGPD, saúde, financeiro).",
])

# ======================================================================
# PARTE 1
# ======================================================================
pdf.pb()
pdf.h1("Parte 1 — Visão geral do fluxo de IA comercial")

pdf.h2("O problema que esse fluxo resolve")
pdf.p("Times comerciais pequenos enfrentam um dilema: leads chegam em volume crescente (Instagram Ads, Google, indicações, WhatsApp), mas a maioria não tem fit. Quando o closer humano precisa atender todos, três coisas acontecem:")
pdf.bullet([
    "O closer queima tempo com leads desqualificados e perde os leads quentes que esperam demais.",
    "A taxa de resposta cai (lead que espera mais de 5 minutos converte 80% menos, segundo benchmark Harvard Business Review).",
    "O closer fica frustrado e a qualidade do atendimento aos leads quentes também cai.",
])
pdf.p('A solução não é "automatizar o fechamento" — isso quase sempre falha porque venda complexa exige confiança humana. A solução é automatizar a triagem: deixar uma IA conversar com todos os leads, descobrir quem está pronto, e entregar ao closer só os contatos com fit comprovado.')

pdf.h2("A analogia da recepcionista qualificada")
pdf.p("Pense num consultório de alto padrão. Quando você liga, quem atende não é o médico — é uma recepcionista treinada. Ela faz perguntas (qual sua queixa, tem convênio, tem urgência), agenda os casos certos para o especialista certo, e descarta educadamente os casos que não são para aquele consultório.")
pdf.p("A IA SDR é essa recepcionista. Ela não tenta substituir o médico (closer humano). Ela protege o tempo do médico, garante que cada consulta marcada seja com alguém que tem fit, e cria uma experiência boa mesmo para quem foi recusado.")

pdf.h2("Os três princípios fundamentais")
pdf.h3("1. A IA qualifica, o humano fecha")
pdf.p("Esta é a regra que não pode ser quebrada. A IA pode descobrir orçamento, urgência, decisor e dor. A IA não pode dar preço final, prometer prazo, ou enviar contrato. O ponto de handoff é onde tudo isso passa para o humano. Quebrar essa regra causa erros caros: IA prometendo prazo que não dá, dando desconto que não pode, ou inventando funcionalidade.")
pdf.h3("2. Tudo passa pelo CRM próprio")
pdf.p("O CRM não é só armazenamento — é o sistema de controle da operação. Toda mensagem da IA, toda decisão de score, todo handoff fica registrado e auditável. Sem isso, você não consegue (a) melhorar a IA com base em dados reais, (b) saber se o closer está convertendo, (c) responder à LGPD em caso de pedido de exclusão.")
pdf.h3("3. Webhook é contrato — versionado")
pdf.p('O payload que vai da IA para o closer é um contrato de API. Mudou um campo, é breaking change. Tratá-lo como código (versionado em git, com testes, com schema) evita o cenário "atualizei a IA e o painel do closer parou de funcionar".')

# ======================================================================
# PARTE 2
# ======================================================================
pdf.pb()
pdf.h1("Parte 2 — Arquitetura em 5 camadas")
pdf.h2("Diagrama do fluxo")
pdf.code("""+---------------------------+
|    CANAIS DE ENTRADA      |
|  WhatsApp / Site / IG /   |
|  Telegram / Indicações    |
+-------------+-------------+
              |
              v
+-------------+-------------+
|  CAMADA 1 — BOTS          |
|  Recebem mensagens,       |
|  identificam o lead,      |
|  chamam o CRM via API     |
+-------------+-------------+
              |
              v
+-------------+-------------+         +-----------------+
|  CAMADA 2 — IA SDR        |<------->|  CAMADA 4 —     |
|  Qualifica via conversa,  |   API   |  CRM PRÓPRIO    |
|  decide próxima ação      |         |  (PostgreSQL +  |
+-------------+-------------+         |  Painel Web)    |
              |                       +-----------------+
       handoff_now?                          ^
              | sim                          |
              v                              |
+-------------+-------------+                |
|  CAMADA 3 — WEBHOOK       |----------------+
|  Empacota payload e       |   registra
|  notifica closer          |   handoff
+-------------+-------------+
              |
              v
+-------------+-------------+
|  CAMADA 5 — CLOSER        |
|  Humano recebe brief,     |
|  fecha venda,             |
|  registra outcome no CRM  |
+---------------------------+""")

pdf.h2("Por que 5 camadas e não 1 sistema monolítico")
pdf.p("Cada camada tem uma responsabilidade única e pode ser substituída sem afetar as outras. Isso parece engenharia exagerada para um time pequeno — mas vira o oposto na prática:")
pdf.bullet([
    "Você pode trocar de modelo de IA (Gemini para OpenAI, ou vice-versa) sem mexer no bot ou no CRM.",
    "Você pode adicionar um novo canal (Instagram, Telegram) sem mexer na IA — só plug no CRM.",
    "Você pode trocar o canal de notificação do closer (de WhatsApp para Slack) sem mexer em mais nada.",
    "Cada camada é testável isoladamente. Se algo quebra, você sabe onde.",
])

pdf.h2("Resumo da responsabilidade de cada camada")
pdf.h3("Camada 1 — Bots de captura")
pdf.p("Função: receber mensagens dos canais (WhatsApp, site, Instagram, Telegram), identificar o lead (criar no CRM se não existir), e repassar a mensagem para a IA SDR via API. Também devolve a resposta da IA ao canal.")
pdf.h3("Camada 2 — IA SDR")
pdf.p("Função: conversar com o lead, descobrir BANT (Budget, Authority, Need, Timeline), atribuir score, e decidir a próxima ação (continuar qualificando, fazer handoff, arquivar, descartar). É um processo, não uma chamada única — pode conversar 5, 10, 20 mensagens.")
pdf.h3("Camada 3 — Webhook & handoff")
pdf.p('Função: quando a IA decide "handoff_now", empacotar todo o contexto do lead num payload estruturado e enviar para onde o closer está (WhatsApp, Slack, e-mail, painel). Inclui retry policy, assinatura HMAC, e log auditável.')
pdf.h3("Camada 4 — CRM próprio")
pdf.p("Função: persistir tudo. Cada lead, cada mensagem, cada qualificação, cada handoff, cada métrica. Expor APIs para as outras camadas e um painel web para o time operar. É o cérebro da operação.")
pdf.h3("Camada 5 — Closer humano")
pdf.p('Função: receber o brief do lead qualificado, conduzir a conversa final, fechar (ou perder) a venda, e registrar o outcome de volta no CRM. O outcome alimenta o aprendizado da IA — leads que viram "won" servem de exemplo positivo para refinar o prompt.')

# ======================================================================
# PARTE 3
# ======================================================================
pdf.pb()
pdf.h1("Parte 3 — Camada 1: Bots de captura")
pdf.h2("O que um bot de captura faz (e não faz)")
pdf.p("Um bot de captura é um adaptador entre um canal específico (WhatsApp, site, Instagram) e o CRM. Ele tem três responsabilidades exclusivas:")
pdf.bullet([
    "Receber a mensagem do lead no formato do canal (WhatsApp envia objetos diferentes de Instagram).",
    "Normalizar a mensagem para o formato padrão do CRM (POST /api/webhook/inbound).",
    "Receber a resposta da IA do CRM e enviar de volta no formato do canal.",
])
pdf.p("O que ele NÃO faz: não tem inteligência, não decide nada, não armazena estado. Se o bot caiu e subiu, nada se perde — o estado todo está no CRM. Isso é fundamental para resiliência.")

pdf.h2("Bot WhatsApp — opções e escolha")
pdf.h3("Opção A: whatsapp-web.js (Node.js) — RECOMENDADO PARA CUSTO ZERO")
pdf.p("Biblioteca não-oficial que conversa com o WhatsApp Web. Gratuita, funcional, comunidade ativa. É a única opção que mantém custo zero.")
pdf.bullet([
    "Prós: zero custo, fácil de subir, suporta multi-mídia (áudio, imagem, documento).",
    "Contras: precisa de um celular físico ou QR pareado a cada deploy; sessão pode cair sem aviso; risco baixo mas existente de ban do número.",
    "Quando usar: até ~1000 mensagens/dia por número. Acima disso, considere API oficial.",
])
pdf.h3("Opção B: API Oficial Meta WhatsApp Business (paga — sai do custo zero)")
pdf.p("API paga, oficial, com SLA. Cobra por conversa iniciada (R$0,30 a R$0,90).")
pdf.h3("Opção C: Z-API, WPPConnect, Twilio (mensalidade)")
pdf.p("Plataformas que envelopam whatsapp-web.js ou API oficial. Cobram mensalidade (~R$50-300/mês).")
pdf.p("Recomendação para começar: whatsapp-web.js. Migre apenas quando a dor de gerenciar sessão custar mais do que a mensalidade da alternativa.")

pdf.h2("Bot site (chat widget)")
pdf.p("No site, o widget é um componente JavaScript que mostra um chat flutuante no canto inferior direito. Para custo zero, a opção é build próprio em HTML+CSS+JS puro, hospedado no GitHub Pages.")

pdf.h2("Contrato do bot com o CRM")
pdf.p("Independente da implementação, todo bot deve falar com o CRM da mesma forma. Isso é o que permite trocar de bot sem afetar o resto.")
pdf.code("""POST /api/webhook/inbound
Authorization: Bearer <BOT_API_KEY>
Content-Type: application/json

{
  "channel": "whatsapp" | "site" | "instagram" | "telegram",
  "channel_id": "<id único do lead naquele canal>",
  "message": "<texto que o lead enviou>",
  "received_at": "<ISO 8601 timestamp>",
  "metadata": {
    "name": "<se o canal forneceu>",
    "media_url": "<se for áudio/imagem>",
    "utm_source": "<se vier da landing page>"
  }
}

Resposta esperada:
{
  "reply": "<texto que o bot deve enviar de volta>",
  "delay_ms": 1500
}""")

# ======================================================================
# PARTE 4
# ======================================================================
pdf.pb()
pdf.h1("Parte 4 — Camada 2: IA SDR (qualificação)")

pdf.h2("O que é um SDR")
pdf.p("SDR (Sales Development Representative) é uma função clássica em times de vendas B2B. O SDR não fecha — ele descobre se o lead vale a pena ser passado para o closer. Em times humanos, é geralmente alguém júnior, treinado para fazer perguntas específicas e identificar fit rapidamente.")
pdf.p("O modelo BANT (Budget, Authority, Need, Timeline), criado pela IBM nos anos 60, é o framework mais usado até hoje. Ele cabe em quatro perguntas que cobrem 90% do necessário para decidir se um lead é qualificado.")

pdf.h2("Por que uma IA é boa nesse papel")
pdf.bullet([
    "Disponibilidade 24/7: lead que chega às 23h domingo não espera até segunda.",
    "Paciência infinita: a IA não cansa de fazer a mesma pergunta de 50 maneiras diferentes.",
    "Consistência: mesma qualidade no lead 1 e no lead 1000 do dia.",
    "Custo zero (até o teto do free tier): Gemini Flash atende grátis até 150 conversas/dia.",
    "Escalabilidade: 1 ou 10000 conversas simultâneas, sem mudança operacional.",
])

pdf.h2("Por que uma IA é ruim no fechamento")
pdf.bullet([
    "Pressão emocional: fechamento exige ler entonação, urgência implícita, sinais não-verbais.",
    "Negociação: descontos, condições especiais, encaixe de horário exigem julgamento e autoridade.",
    "Confiança: pagar 5000 reais para alguém que pode ser um robô é fricção que faz desistir.",
    "Erros caros: IA prometendo prazo errado custa muito mais do que o custo de ter um humano.",
])

pdf.h2("A escolha do modelo — versão custo zero")
pdf.p("O SDR é a função mais chamada do fluxo — toda mensagem do lead vira uma chamada. Como esta versão é custo zero, a escolha do modelo é a decisão mais crítica para manter a operação gratuita.")

pdf.h3("1. gemini-1.5-flash via Google AI Studio (RECOMENDADO)")
pdf.p("O Google oferece via AI Studio um tier gratuito generoso: 15 requisições por minuto e 1500 requisições por dia, sem cobrança. Para o nosso fluxo, isso equivale a aproximadamente 150 conversas completas por dia (10 turnos cada). É a opção certa para começar.")
pdf.bullet([
    "Prós: gratuito, contexto enorme (1M tokens), suporta JSON output, latência aceitável (1-2s).",
    "Contras: peculiaridades de prompt (mais literal que GPT), rate limit de 15 RPM exige fila se chegar pico.",
    "Limite real: 1500 req/dia. Acima disso, falhas até a meia-noite UTC.",
    "Como obter chave: aistudio.google.com, opção Get API Key. Sem cartão de crédito.",
])

pdf.h3("2. gemini-2.0-flash-exp (também grátis)")
pdf.p("Versão mais recente do Flash, ainda mais rápida (500-900ms) e com melhor raciocínio. Tier gratuito similar. Por ser experimental, pode ter mudança de API sem aviso.")

pdf.h3("3. groq.com com llama-3.1-8b (custo zero — backup)")
pdf.p("Groq oferece inferência gratuita de modelos open source com latência ultra-baixa (300-500ms). Use como fallback se Gemini estourar o limite diário. JSON output menos confiável, então exige validação extra.")

pdf.h3("4. Quando deixar de ser custo zero")
pdf.p("Se a operação ultrapassar 1500 conversas por dia consistentemente, considere:")
pdf.bullet([
    "Opção A: criar múltiplas chaves Gemini (uma por projeto Google Cloud) e rotacionar — escala linearmente sem custo.",
    "Opção B: migrar para Gemini Pay-as-You-Go (custo de ~USD 0.075/M tokens input — ainda barato).",
    "Opção C: alternar OpenAI gpt-4o-mini como segundo provedor.",
])

pdf.h2("Anatomia do prompt do SDR")
pdf.p("O prompt completo está em prompts/sdr-prompt-exemplo.md. Aqui está o resumo:")
pdf.bullet([
    "System prompt: quem a IA é, o que faz, regras de comunicação, contexto da empresa, formato de saída.",
    "User prompt (dinâmico): dados do lead, qualificação atual, histórico das últimas mensagens, nova mensagem do lead.",
    "Response format: JSON estruturado com reply (texto pro lead) e qualification (atualização do estado).",
])

pdf.h2("Sistema de scoring")
pdf.p("O score total vai de 0 a 100, distribuído em 4 dimensões de 0-25 cada:")
pdf.bullet([
    "Budget (0-25): 0 se rejeitou o preço, 25 se confirmou orçamento dentro da faixa.",
    "Authority (0-25): 0 se é apenas usuário sem influência, 25 se é decisor confirmado.",
    "Need (0-25): 0 se a dor é vaga ou inventada, 25 se é específica, recente e ele articulou bem.",
    "Timeline (0-25): 0 sem prazo definido, 25 se quer começar imediatamente.",
])
pdf.p("Thresholds recomendados como ponto de partida (calibre com dados reais):")
pdf.bullet([
    "0-30: discard (spam, troll, totalmente fora do perfil)",
    "31-60: park (não tem fit agora, mas arquivado educadamente para nurturing futuro)",
    "61-80: continue_qualifying (vale insistir mais 2-3 mensagens)",
    "81-100: handoff_now (passa pro closer)",
])

pdf.h2("O ciclo iterativo")
pdf.p("O SDR não decide na primeira mensagem. Ele conversa, descobre uma dimensão, conversa mais. Em média, leva 6-12 mensagens. Em cada turno:")
pdf.bullet([
    "1. CRM monta o contexto (lead + qualificação atual + histórico)",
    "2. Chama a LLM com o prompt",
    "3. LLM retorna reply + qualification atualizada + recommended_action",
    "4. CRM persiste tudo",
    "5. Se recommended_action = handoff_now, dispara webhook",
    "6. Se não, devolve reply para o bot enviar ao lead",
])

# ======================================================================
# PARTE 5
# ======================================================================
pdf.pb()
pdf.h1("Parte 5 — Camada 3: Webhook & handoff")

pdf.h2("O que é um webhook (sem mistério)")
pdf.p('Webhook é uma chamada HTTP POST que o seu sistema faz para outra URL quando algo acontece. No nosso caso, o evento é "lead foi qualificado" e a URL é onde o closer humano fica esperando (Slack, n8n, Make, ou um sistema próprio).')
pdf.p("Diferente de uma chamada de API normal (onde você puxa dados), no webhook é o sistema que empurra dados quando algo acontece. Por isso é também chamado de reverse API ou push notification.")

pdf.h2("Por que webhook e não polling")
pdf.bullet([
    "Polling (closer checa o CRM a cada minuto): desperdiça requisições, demora a notificar, escala mal.",
    "Webhook (CRM avisa o closer): latência de segundos, escala perfeitamente, eficiente.",
])

pdf.h2("Anatomia do payload de handoff")
pdf.p("O payload completo está em webhook/payload-exemplo.json. Os blocos essenciais:")
pdf.h3("Bloco 1: metadados do evento")
pdf.p("event, event_id (idempotência), timestamp, version. event_id permite ao receptor detectar webhook duplicado (retry).")
pdf.h3("Bloco 2: lead")
pdf.p("Dados básicos do contato: nome, canal, telefone, e-mail, score, UTMs.")
pdf.h3("Bloco 3: qualification")
pdf.p("Snapshot da qualificação que motivou o handoff: BANT detalhado, score por dimensão, reasoning escrito pela IA.")
pdf.h3("Bloco 4: conversation_summary")
pdf.p("Resumo da conversa: número de mensagens, duração, citações-chave que mostram a dor, link para o transcript completo.")
pdf.h3("Bloco 5: closer_brief")
pdf.p("Resumo executivo de 3 linhas para o closer ler em 10 segundos antes de iniciar o atendimento. Headline + best_action + watch_out.")
pdf.h3("Bloco 6: delivery")
pdf.p("Quem deve receber (closer_id), método (whatsapp, slack, email), SLA esperado.")
pdf.h3("Bloco 7: signature (HMAC)")
pdf.p("Assinatura HMAC-SHA256 do corpo, usando segredo compartilhado entre CRM e closer-notifier. Permite ao receptor validar que o webhook é genuíno.")

pdf.h2("Retry policy")
pdf.p("Webhook falha. Internet cai, servidor reinicia, rate limit estoura. O CRM precisa ter política de retry:")
pdf.bullet([
    "Tentativa 1: imediata.",
    "Tentativa 2: após 30 segundos.",
    "Tentativa 3: após 5 minutos.",
    "Tentativa 4: após 30 minutos.",
    "Tentativa 5: após 2 horas.",
    "Depois disso, marca como falha permanente e notifica admin.",
])

pdf.h2("Idempotência")
pdf.p("Se o receptor recebe o mesmo event_id duas vezes (porque o CRM achou que falhou e retentou), ele deve processar uma vez só. Por isso o event_id é obrigatório e único. Receptor mantém cache de event_ids processados nas últimas 24h.")

pdf.h2("Onde o closer recebe (versão custo zero)")
pdf.h3("Opção 1: Slack Free (RECOMENDADO)")
pdf.p('Profissional, com canal dedicado por closer ou por estágio. Slack tem API de incoming webhooks pronta. Permite reactions para "aceito" / "passa". Free tier mantém 90 dias de histórico, suficiente.')
pdf.h3("Opção 2: WhatsApp via o mesmo bot")
pdf.p("Reaproveita o bot whatsapp-web.js para enviar a notificação ao número do closer. Custo zero adicional.")
pdf.h3("Opção 3: Painel web do CRM")
pdf.p('O CRM tem uma tela "leads para mim", o closer abre e vê. Funciona bem se o closer já fica no painel do CRM o dia todo.')

# ======================================================================
# PARTE 6
# ======================================================================
pdf.pb()
pdf.h1("Parte 6 — Camada 4: CRM próprio para controle da IA")

pdf.h2("Por que não usar Pipedrive, HubSpot, RD Station?")
pdf.p("CRMs comerciais resolvem o problema do humano: registrar reunião, salvar contato, mover card no kanban. Eles NÃO resolvem o problema da IA: armazenar histórico granular de conversa, scoring detalhado por dimensão, métricas de custo de IA, debug de prompt. Além disso, todos cobram mensalidade — sai do custo zero.")
pdf.p("Você pode integrar (CRM próprio para IA + Pipedrive para closers humanos). Mas o CRM próprio é o que faz a IA evoluir — sem ele, você está cego.")

pdf.h2("O que o CRM próprio precisa fazer")
pdf.bullet([
    "Armazenar cada mensagem com tokens consumidos, latência e custo.",
    "Armazenar cada qualificação como snapshot (histórico, não só estado atual).",
    "Armazenar cada handoff com payload completo e status de entrega.",
    "Permitir busca rápida por lead, score, estágio, closer.",
    "Mostrar métricas: funil, custo de IA por dia, performance por closer.",
    "Permitir intervenção humana: editar dados do lead, forçar handoff, parar a IA.",
])

pdf.h2("Schema do banco")
pdf.p("O schema completo está em crm-exemplo/schema.sql. São 5 tabelas:")
pdf.bullet([
    "leads: cada contato que entrou pelo bot.",
    "conversations: cada mensagem (user, assistant, system, closer).",
    "qualifications: snapshots da qualificação BANT (histórico).",
    "handoffs: registro de cada handoff IA para closer com payload completo.",
    "users: closers e admins do CRM.",
])
pdf.p("Mais uma view (leads_dashboard) que agrega tudo que o closer precisa ver numa tela.")

pdf.h2("Stack para o CRM (custo zero)")
pdf.h3("Backend")
pdf.p("Node.js + Express. Hospedado no Oracle Cloud Always Free (4 vCPUs ARM + 24GB RAM gratuitos para sempre).")
pdf.h3("Banco")
pdf.p("Supabase Free Tier (PostgreSQL gerenciado). Entrega banco, auth, realtime, storage e dashboard. 500MB de banco e 2GB de bandwidth/mês.")
pdf.h3("Frontend do painel")
pdf.p("Duas opções gratuitas:")
pdf.bullet([
    "Retool Free Tier: até 5 usuários internos. Monta CRUD sobre as 5 tabelas em 1-2 dias.",
    "HTML + CSS + JS puro hospedado no GitHub Pages: leve, gratuito, sem build step.",
])

pdf.h2("Telas mínimas")
pdf.h3("Tela 1: Funil")
pdf.p("Contagem de leads em cada estágio nos últimos 30 dias. Filtro por canal, por UTM, por período. Mostra conversão entre estágios.")
pdf.h3("Tela 2: Lista de leads")
pdf.p("Tabela paginada com: nome, canal, score, estágio, último contato, closer. Filtros por estágio e min_score. Busca por nome ou telefone.")
pdf.h3("Tela 3: Detalhe do lead")
pdf.p('Tudo sobre o lead em uma tela: dados, qualificações (histórico), transcript da conversa, handoffs anteriores. Botão "forçar handoff" e "pausar IA neste lead".')
pdf.h3("Tela 4: Painel do closer")
pdf.p("Lista dos leads atribuídos a um closer, ordenados por SLA. Em cada card, o closer_brief. Ação rápida: marcar outcome (won, lost, no_show).")
pdf.h3("Tela 5: Métricas de IA")
pdf.p("Custo da IA por dia/semana/mês (mesmo sendo zero, vale acompanhar uso do free tier). Tokens consumidos. Latência média. Modelos mais usados.")

pdf.h2("Como o CRM evolui o prompt da IA")
pdf.p("Esta é a parte que separa um CRM-armário de um CRM-cérebro. Use os dados para:")
pdf.bullet([
    'Listar handoffs que viraram "lost" e estudar os transcripts — onde a IA errou na qualificação?',
    'Listar handoffs que viraram "no_show" — o lead realmente queria fechar ou a IA o forçou cedo demais?',
    "Listar leads que ficaram em qualifying por mais de 20 mensagens — a IA está indecisa, prompt precisa de regra clara.",
    "Listar mensagens com latency > 3s — algo no prompt ficou gordo.",
])

# ======================================================================
# PARTE 7
# ======================================================================
pdf.pb()
pdf.h1("Parte 7 — Camada 5: Closer humano")

pdf.h2("O que o closer recebe")
pdf.p("No momento do handoff, o closer recebe três coisas (no canal escolhido — Slack, WhatsApp, painel):")
pdf.bullet([
    'Notificação: "Você tem 1 lead novo (Maria Silva, score 92)".',
    "Brief executivo: o closer_brief do payload — 3 linhas para ler em 10 segundos.",
    "Link para o transcript completo no painel do CRM.",
])

pdf.h2("O que o closer faz nos primeiros 30 minutos")
pdf.bullet([
    "Lê o brief.",
    "Confirma o contato (WhatsApp ou ligação, conforme preferência do lead).",
    "Apresenta-se como humano, validando a expectativa criada pela IA.",
    "Confirma os 4 pontos BANT que a IA descobriu (não para refazer, mas para mostrar que ouviu).",
    "Apresenta a proposta concreta (preço, prazo, modalidade).",
    "Fecha ou agenda próximo passo (proposta formal, reunião).",
])

pdf.h2("O que o closer NÃO deve fazer")
pdf.bullet([
    "Pedir as informações de novo (frustra o lead que já contou).",
    'Contradizer a IA (se a IA disse "esta semana", não diga "vamos ver mês que vem").',
    "Demorar mais que o SLA (30 minutos é o padrão; acima de 1 hora, o lead esfria).",
    "Esquecer de marcar outcome no CRM (sem isso, a IA não aprende).",
])

pdf.h2("O feedback loop")
pdf.p('Toda venda perdida é dado de ouro. Quando o closer marca outcome = "lost", ele preenche o motivo:')
pdf.bullet([
    "price: lead achou caro (IA precisa qualificar Budget melhor).",
    "timing: lead queria mas postergou (IA precisa qualificar Timeline melhor).",
    "no_fit: descobriu-se que não era o cliente ideal (IA falhou em Need).",
    "lost_to_competitor: foi para concorrente (não é falha da IA, é mercado).",
    "no_show: lead sumiu (IA forçou handoff cedo).",
])
pdf.p('Mensalmente, o admin revisa os "lost" + "no_show" e usa como input para evoluir o prompt. Padrões repetidos viram regra no system prompt.')

# ======================================================================
# PARTE 8
# ======================================================================
pdf.pb()
pdf.h1("Parte 8 — Stack tecnológica (custo zero)")

pdf.h2("Stack completo grátis")
pdf.bullet([
    "Linguagem: Node.js 20+ (single language em todo o stack ajuda time pequeno)",
    "Bot WhatsApp: whatsapp-web.js — biblioteca gratuita, open source",
    "Bot site: HTML + CSS + JS puro — zero dependências, entrega via GitHub Pages",
    "Backend CRM: Express.js — gratuito",
    "Banco: Supabase Free Tier — 500MB de banco, 2GB de bandwidth/mês",
    "IA: Google Gemini 1.5 Flash via AI Studio — 1500 req/dia grátis, sem cartão",
    "Painel CRM: Retool Free Tier — até 5 usuários internos grátis",
    "Notificação closer: Slack Free Tier (90 dias de histórico, infinitos canais)",
    "Hospedagem backend: Oracle Cloud Always Free — 4 vCPUs ARM, 24GB RAM, sem expiração",
    "Alternativa hospedagem: PC de casa + Cloudflare Tunnel (gratuito, precisa internet estável)",
    "Hospedagem site/landing: GitHub Pages (gratuito) ou Vercel Hobby (gratuito)",
    "DNS/SSL: Cloudflare Free Tier",
    "Domínio: opcional R$40/ano, ou subdomínio gratuito (DuckDNS, FreeDNS)",
    "Repositório de código: GitHub gratuito (público) ou Private Free (até 3 colaboradores)",
    "Monitoramento: UptimeRobot Free — 50 monitores grátis, ping a cada 5 min",
    "Logs: console.log + Supabase ou Better Stack Free (50MB/mês)",
])

pdf.h2("O que cada free tier suporta")
pdf.h3("Supabase Free")
pdf.p("Suporta até ~100 mil mensagens no banco, 50000 usuários autenticados, queries ilimitadas. 12 a 18 meses de operação típica. Banco pausa após 7 dias inativos — reativação automática.")

pdf.h3("Gemini Free (AI Studio)")
pdf.p("15 requisições por minuto e 1500 por dia para gemini-1.5-flash. Uma conversa típica usa 10 chamadas, então 1500/dia = 150 conversas/dia. Cobre 200-300 leads novos/dia.")

pdf.h3("Oracle Cloud Always Free")
pdf.p("4 vCPUs ARM + 24GB de RAM, com 200GB de storage, sempre gratuito. Não expira. Precisa cartão de crédito no cadastro mas não cobra. Suporta Ubuntu 24.04, PM2, Nginx, Node, Postgres.")

pdf.h3("Retool Free")
pdf.p("Até 5 usuários internos, conexão direta com Supabase, drag-and-drop. Suficiente para painel admin com 5 telas.")

pdf.h3("Slack Free")
pdf.p("Mensagens ilimitadas, canais ilimitados, integrações ilimitadas, retenção de 90 dias. Para handoffs, 90 dias é suficiente.")

pdf.h2("Quando deixar de ser custo zero")
pdf.bullet([
    "Volume: ~150 conversas de qualificação por dia (4500/mês).",
    "Banco: ~100k mensagens armazenadas (12-18 meses).",
    "Closers: até 5 usuários no painel (Retool Free).",
    "Histórico de handoffs no Slack: 90 dias.",
])
pdf.p("Migração mínima recomendada (do mais barato pro mais caro):")
pdf.bullet([
    "Mais closers: Retool Team — USD 10/usuário/mês.",
    "Mais conversas IA: múltiplas chaves Gemini Free com rotação (custo zero) ou Gemini Pay-as-You-Go (~USD 5-30/mês).",
    "Mais banco: Supabase Pro — USD 25/mês (8GB).",
    "Maior processamento: Oracle Free já segura até VPS pago. Migrar só se precisar de IP fixo dedicado.",
])

# ======================================================================
# PARTE 9
# ======================================================================
pdf.pb()
pdf.h1("Parte 9 — Roadmap de implementação (8 semanas)")

pdf.h2("Semana 1 — Fundação")
pdf.bullet([
    "Criar conta Supabase e aplicar o schema.sql.",
    'Criar projeto Node com Express. Subir endpoint POST /api/webhook/inbound stub (recebe, salva mensagem, responde "ok").',
    "Subir VPS no Oracle Cloud Always Free, instalar Node, PM2, Nginx, configurar HTTPS via Cloudflare Tunnel.",
    "Configurar repo no GitHub.",
])
pdf.h2("Semana 2 — Bot WhatsApp")
pdf.bullet([
    "Implementar bot com whatsapp-web.js que escuta mensagens.",
    "Conectar bot ao endpoint /api/webhook/inbound.",
    "Implementar envio de resposta de volta ao lead.",
    "Teste end-to-end: lead manda mensagem, vira lead no Supabase, mensagem fica salva, bot devolve resposta fixa.",
])
pdf.h2("Semana 3 — IA SDR v1")
pdf.bullet([
    "Criar conta Google AI Studio (aistudio.google.com) e gerar API key Gemini (custo zero).",
    "Implementar chamada à API Gemini dentro do endpoint /api/webhook/inbound (biblioteca @google/generative-ai).",
    "Implementar prompt do SDR (system + user dinâmico) seguindo prompts/sdr-prompt-exemplo.md.",
    "Salvar resposta da IA em conversations com tokens, latência, modelo.",
    "Teste: lead conversa com IA, IA responde com lógica de SDR.",
])
pdf.h2("Semana 4 — Qualificação e scoring")
pdf.bullet([
    "Forçar IA a retornar JSON estruturado com qualification.",
    "Persistir qualifications a cada turno.",
    "Implementar lógica de decisão (handoff, continue, park, discard) baseada no recommended_action.",
    "Teste: 5 conversas simuladas com perfis diferentes (quente, frio, indeciso, spam, sem fit).",
])
pdf.h2("Semana 5 — Webhook de handoff")
pdf.bullet([
    "Implementar montagem do payload de handoff.",
    "Configurar canal de entrega (Slack Free recomendado).",
    "Implementar retry policy.",
    "Implementar assinatura HMAC.",
    "Teste: lead chega quente, IA decide handoff, payload aparece no Slack.",
])
pdf.h2("Semana 6 — Painel CRM")
pdf.bullet([
    "Configurar Retool Free conectado ao Supabase.",
    "Criar tela 1 (Funil) e tela 2 (Lista de leads).",
    "Criar tela 3 (Detalhe do lead) com transcript embutido.",
    "Criar tela 4 (Painel do closer) com leads atribuídos.",
    "Criar tela 5 (Métricas de IA).",
])
pdf.h2("Semana 7 — Closer no fluxo")
pdf.bullet([
    "Treinar closer humano: como ler o brief, como confirmar BANT sem refazer.",
    "Implementar marcação de outcome no painel.",
    "Implementar feedback loop: handoffs perdidos com motivo.",
    "Teste piloto: 20 leads reais, monitorar conversão e satisfação.",
])
pdf.h2("Semana 8 — Refinamento e launch")
pdf.bullet([
    "Revisar handoffs perdidos da semana piloto.",
    "Ajustar prompt com base nos padrões observados.",
    "Adicionar 2-3 anti-padrões específicos identificados.",
    "Documentar runbook para problemas comuns (sessão WhatsApp caiu, Gemini quota estourou).",
    "Launch oficial.",
])

# ======================================================================
# PARTE 10
# ======================================================================
pdf.pb()
pdf.h1("Parte 10 — Operação custo zero")

pdf.h2("Resumo: R$0,00 de gasto financeiro até o teto")
pdf.p("Esta versão do fluxo é projetada para rodar com R$0 de gasto recorrente até atingir um teto de uso bem definido.")

pdf.h2("Custo total mensal: R$0,00")
pdf.p("Sim, literalmente zero. O único gasto opcional é um domínio próprio (~R$5/mês amortizado anual) se você considerar que vale a credibilidade. Mesmo sem domínio, a operação funciona — usando subdomínio gratuito.")

pdf.h2("Custos ocultos não-financeiros")
pdf.p("Mesmo sendo custo zero em reais, há custos em tempo que você precisa contabilizar:")
pdf.bullet([
    "Manutenção da sessão whatsapp-web.js: 2-4 horas/mês.",
    "Evolução do prompt da IA: 4-8 horas/mês.",
    "Treinamento de novo closer: 4-8 horas iniciais + acompanhamento da primeira semana.",
    "Monitoramento e resposta a alertas: 1-2 horas/mês.",
])
pdf.p("Esse é o custo real: cerca de 10-20 horas/mês de tempo do operador para manter a operação saudável. Em dinheiro, é zero — em foco e disciplina, não.")

pdf.h2("Por que custo zero é estratégico no começo")
pdf.bullet([
    "Validação sem pressão: você descobre se o fluxo funciona sem queimar capital.",
    "Disciplina arquitetural: free tiers têm limites — você é forçado a otimizar prompt, evitar over-engineering.",
    "Vantagem competitiva sustentável: depois que cruzar os tetos, terá dados reais para justificar cada gasto.",
])

# ======================================================================
# PARTE 11
# ======================================================================
pdf.pb()
pdf.h1("Parte 11 — Riscos e anti-padrões")

pdf.h2("Anti-padrão 1: tentar fechar com IA")
pdf.p('Inevitavelmente alguém vai sugerir: "se a IA já tá conversando, por que não deixa ela fechar?" Não deixe. Os erros caros vêm exatamente daí: IA dando desconto, prometendo prazo, confirmando funcionalidade inexistente. Quanto mais sucesso a IA tem qualificando, mais a tentação. Resista.')

pdf.h2("Anti-padrão 2: prompt único gigante")
pdf.p("Engenheiros novatos colocam tudo num system prompt de 3000 palavras. O modelo perde performance, custa mais por ser longo (em pay-as-you-go), e fica impossível de evoluir. Mantenha o system prompt em <1000 palavras e use o user prompt (dinâmico) para o contexto específico.")

pdf.h2("Anti-padrão 3: não logar tudo")
pdf.p("Storage é barato (no free tier do Supabase, é zero). Não logar é caro. Salve cada mensagem com tokens, latência, custo, modelo. Quando o sistema bugar (vai bugar), só os logs te salvam.")

pdf.h2("Anti-padrão 4: sessão WhatsApp num único servidor sem backup")
pdf.p("Sessão whatsapp-web.js cai. Quando cai, você precisa parear de novo via QR. Se for em horário comercial e o dono do número não tá no escritório, a operação para. Mitigações: monitoramento ativo via UptimeRobot, alerta no Slack, número de backup.")

pdf.h2("Anti-padrão 5: ignorar LGPD")
pdf.p("A operação coleta dado pessoal (telefone, nome, conversa). Você precisa: (a) política de privacidade visível, (b) base legal para processamento, (c) capacidade de excluir dados de um lead que pedir, (d) registro de tratamento. Implemente desde o início — retrofit é dor.")

pdf.h2("Anti-padrão 6: closer sem treinamento")
pdf.p("O closer que recebe lead da IA precisa ser treinado especificamente para esse fluxo. Closer não treinado vai refazer perguntas, contradizer a IA, deixar SLA estourar. Um closer mal treinado destrói o ROI do projeto inteiro.")

pdf.h2("Anti-padrão 7: prompt sem versionamento")
pdf.p("Você vai mudar o prompt 50 vezes nos primeiros 6 meses. Sem versionamento, não há como saber qual mudança piorou o quê. Salve prompts em git, com mensagem de commit explicando o porquê.")

pdf.h2("Anti-padrão 8: webhook sem assinatura")
pdf.p("Webhook sem HMAC permite que qualquer um conheça a URL e injete leads falsos no painel do closer. Use HMAC desde o dia 1, mesmo que pareça paranoia.")

pdf.h2("Anti-padrão 9: scoring sem calibração")
pdf.p("O threshold sugerido (handoff em score >= 81) é chute inicial. Calibre com dados reais. Se 50% dos handoffs viram won, o threshold pode estar alto demais. Se 5% viram won, está baixo demais.")

pdf.h2("Anti-padrão 10: confundir conversação com qualificação")
pdf.p("Conversa boa não é qualificação boa. Lead que conversa 30 mensagens e nunca dá orçamento, autoridade, ou prazo, NÃO é qualificado — só gosta de conversar. A IA precisa ter regra explícita: depois de X turnos sem nova informação BANT, declarar park.")

pdf.h2("Anti-padrão 11: estourar limite do free tier sem perceber")
pdf.p("Específico da versão custo zero: se 1500 req/dia do Gemini estouram, a IA simplesmente para de responder até a meia-noite UTC. Configure alertas que avisem ao atingir 80% do limite. Tenha o fallback Groq pronto.")

# ======================================================================
# APÊNDICE A — GLOSSÁRIO
# ======================================================================
pdf.pb()
pdf.h1("Apêndice A — Glossário")
pdf.h3("BANT")
pdf.p("Framework de qualificação criado pela IBM nos anos 60. Acrônimo para Budget (orçamento), Authority (autoridade), Need (necessidade), Timeline (prazo).")
pdf.h3("Closer")
pdf.p("Vendedor humano responsável pelo fechamento da venda, após a qualificação.")
pdf.h3("CRM")
pdf.p("Customer Relationship Management. Sistema que armazena e organiza dados de leads e clientes.")
pdf.h3("Free tier")
pdf.p("Camada gratuita oferecida por provedores de serviço com limites de uso. Acima do limite, cobra-se.")
pdf.h3("Handoff")
pdf.p("Passagem do lead de uma camada para outra (no nosso caso, da IA SDR para o closer humano).")
pdf.h3("HMAC")
pdf.p("Hash-based Message Authentication Code. Técnica para assinar mensagens de forma que o receptor consegue verificar a autenticidade.")
pdf.h3("LLM")
pdf.p("Large Language Model. Modelos como GPT, Gemini, Claude, Llama.")
pdf.h3("SDR")
pdf.p("Sales Development Representative. Profissional (ou IA) responsável pela qualificação de leads antes do fechamento.")
pdf.h3("SLA")
pdf.p("Service Level Agreement. Promessa de tempo de resposta. SLA típico do closer: responder em até 30 minutos.")
pdf.h3("Token")
pdf.p("Unidade de texto processada pelo LLM. ~0.75 palavra em português. Modelos cobram por tokens consumidos.")
pdf.h3("UTM")
pdf.p("Urchin Tracking Module. Parâmetros na URL que identificam origem do tráfego (utm_source, utm_campaign, utm_medium).")
pdf.h3("Webhook")
pdf.p("Notificação HTTP que um sistema envia a outro quando um evento acontece.")

# ======================================================================
# APÊNDICE B — PRÓXIMOS PASSOS
# ======================================================================
pdf.pb()
pdf.h1("Apêndice B — Próximos passos práticos")

pdf.h2("Antes de escrever uma linha de código")
pdf.bullet([
    "Defina o ICP (Ideal Customer Profile) por escrito: idade, dor, orçamento, urgência.",
    "Escreva 10 conversas reais de WhatsApp com leads passados. Anote o que funcionou.",
    'Defina os 4 valores BANT que caracterizam um lead "score 90+" no seu negócio.',
    "Defina o SLA do closer e o canal de notificação preferido.",
    "Crie as contas gratuitas: Supabase, Google AI Studio, Oracle Cloud, GitHub, Slack, Cloudflare, Retool.",
])

pdf.h2("Validação antes do build completo")
pdf.p("Em vez de construir as 8 semanas em sequência, considere um MVP de 1 semana usando ferramentas no-code (todas com free tier):")
pdf.bullet([
    "Crie um Google Sheets (substituindo o CRM).",
    "Use n8n self-hosted (no Oracle Free) ou Make Free para chamar a API Gemini quando uma linha for adicionada.",
    "Manualmente: para cada lead que chegou no WhatsApp, cole a primeira mensagem no Sheets, copie a resposta sugerida pela IA, envie ao lead.",
    "Avalie: as respostas estão boas? O scoring faria sentido?",
])
pdf.p("Se o MVP manual provar valor, então invista nas 8 semanas. Se não provar, ajuste a estratégia antes de gastar tempo construindo.")

pdf.h2("Métricas de sucesso aos 3 meses")
pdf.bullet([
    "Tempo médio até primeira resposta: < 1 minuto.",
    "Taxa de qualificação (qualifying → qualified): 30-50%.",
    "Taxa de conversão (handoff → won): 20-40%.",
    "Custo financeiro: R$0/mês (mantendo o stack custo zero).",
    "Uso do free tier Gemini: idealmente < 80% do limite diário.",
    "Satisfação do closer (NPS interno): > 7.",
    'Satisfação do lead (resposta a "como foi seu atendimento?"): > 8.',
])

pdf.h2("Quando saber que está funcionando")
pdf.p('O sinal definitivo de sucesso não é a quantidade de leads qualificados. É o closer dizer: "antes eu falava com 50 leads ruins por semana, agora falo com 10 leads quentes — minha vida mudou". Quando o closer humano vira fã da operação, o fluxo está pronto.')

pdf.h2("Sobre este documento")
pdf.p("Este documento é um template aberto, parte do repositório fluxo-ia-empresa no GitHub. Use, adapte, melhore. Pull requests com correções e adições são bem-vindos.")
pdf.p("Versão 1.0 — Junho de 2026 — Versão custo zero.")

# ======================================================================
# SALVA
# ======================================================================
pdf.output(str(PDF_OUT))
print(f"PDF gerado: {PDF_OUT}")
print(f"Tamanho: {PDF_OUT.stat().st_size / 1024:.1f} KB")
print(f"Páginas: {pdf.page_no()}")

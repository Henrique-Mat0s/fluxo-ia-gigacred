# -*- coding: utf-8 -*-
"""
Gera mockups PNG das telas do CRM simplificado.
Saída: mockups/01_conversa.png, 02_lista_leads.png, 03_detalhe_lead.png, 04_dashboard.png
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(__file__).parent / "mockups"
OUT.mkdir(exist_ok=True)

FONTS = "C:/Windows/Fonts"

def font(name="arial.ttf", size=14):
    return ImageFont.truetype(f"{FONTS}/{name}", size)

# Paleta
BG_PAGE     = (245, 247, 250)
BG_CARD     = (255, 255, 255)
HEADER      = (31, 56, 100)
TEXT        = (33, 37, 41)
TEXT_MUTED  = (108, 117, 125)
PRIMARY     = (37, 99, 235)
SUCCESS     = (34, 197, 94)
WARNING     = (234, 179, 8)
DANGER      = (239, 68, 68)
BORDER      = (222, 226, 230)
WA_BG       = (236, 229, 221)  # WhatsApp background
WA_OUT      = (220, 248, 198)  # outgoing bubble (verde claro)
WA_IN       = (255, 255, 255)  # incoming bubble (branco)

W, H = 1200, 800


def rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def header_bar(img, title, subtitle):
    """Barra superior padrão do CRM."""
    d = ImageDraw.Draw(img)
    # Fundo
    d.rectangle([0, 0, W, 60], fill=HEADER)
    d.text((30, 18), "CRM • Fluxo IA", font=font("arialbd.ttf", 18), fill=(255, 255, 255))
    d.text((W - 220, 22), "Olá, João Closer v", font=font(size=13), fill=(220, 230, 245))
    # Sub-header
    d.rectangle([0, 60, W, 110], fill=(255, 255, 255))
    d.line([(0, 110), (W, 110)], fill=BORDER, width=1)
    d.text((30, 72), title, font=font("arialbd.ttf", 20), fill=TEXT)
    d.text((30, 95), subtitle, font=font(size=12), fill=TEXT_MUTED)


# =====================================================================
# 1. CONVERSA Bot ↔ Lead (estilo WhatsApp)
# =====================================================================
def mockup_conversa():
    img = Image.new("RGB", (W, H), WA_BG)
    d = ImageDraw.Draw(img)

    # Header WhatsApp
    d.rectangle([0, 0, W, 70], fill=(7, 94, 84))
    # Avatar
    d.ellipse([20, 13, 64, 57], fill=(180, 220, 215))
    d.text((33, 26), "M", font=font("arialbd.ttf", 22), fill=(7, 94, 84))
    d.text((80, 18), "Maria Silva", font=font("arialbd.ttf", 17), fill=(255, 255, 255))
    d.text((80, 42), "+55 11 99999-8888 • online agora", font=font(size=12), fill=(220, 240, 235))

    # Mensagens
    def bubble(y, text, is_out=False, time="09:14"):
        # Calcula altura do texto (aprox 35 chars por linha)
        lines = []
        for raw in text.split("\n"):
            words = raw.split()
            current = ""
            for w in words:
                if len(current) + len(w) > 42:
                    lines.append(current)
                    current = w
                else:
                    current = (current + " " + w).strip()
            lines.append(current)

        bubble_w = 460
        bubble_h = 28 + len(lines) * 20
        if is_out:
            x = W - bubble_w - 30
            fill = WA_OUT
        else:
            x = 30
            fill = WA_IN

        rounded_rect(d, [x, y, x + bubble_w, y + bubble_h], 10, fill=fill)
        for i, line in enumerate(lines):
            d.text((x + 14, y + 10 + i * 20), line, font=font(size=14), fill=TEXT)
        d.text((x + bubble_w - 50, y + bubble_h - 18), time, font=font(size=10), fill=TEXT_MUTED)
        return y + bubble_h + 14

    y = 95
    y = bubble(y, "Olá! Vi seu anúncio sobre terapia. Como funciona?", is_out=False, time="09:14")
    y = bubble(y, "Oi! Sou a Helena, atendo aqui no Centro. Como você se chama?",
               is_out=True, time="09:14")
    y = bubble(y, "Maria", is_out=False, time="09:15")
    y = bubble(y, "Prazer, Maria! Em que momento da vida você está? "
                  "O que te trouxe a procurar terapia hoje?",
               is_out=True, time="09:15")
    y = bubble(y, "Ansiedade que não passa. Já tentei meditar e não adianta. "
                  "Preciso de ajuda profissional.", is_out=False, time="09:17")
    y = bubble(y, "Entendo, Maria. Você está pensando em começar quando? "
                  "Tem alguma preferência de horário?", is_out=True, time="09:17")
    y = bubble(y, "Quero começar essa semana. Só consigo à noite, depois das 19h.",
               is_out=False, time="09:18")

    # Indicador "IA decidiu handoff"
    badge_y = y + 10
    d.rectangle([20, badge_y, W - 20, badge_y + 40], fill=(255, 243, 205))
    d.text((35, badge_y + 12), "🔔 IA SDR detectou lead qualificado (score 92) — handoff disparado para o closer",
           font=font("arialbd.ttf", 13), fill=(133, 100, 4))

    img.save(OUT / "01_conversa.png", "PNG")
    print(f"OK 01_conversa.png")


# =====================================================================
# 2. LISTA DE LEADS na plataforma
# =====================================================================
def mockup_lista_leads():
    img = Image.new("RGB", (W, H), BG_PAGE)
    d = ImageDraw.Draw(img)
    header_bar(img, "Leads para você",
               "5 leads novos qualificados pela IA aguardando contato")

    # Filtros
    rounded_rect(d, [30, 130, 200, 165], 6, fill=BG_CARD, outline=BORDER, width=1)
    d.text((45, 140), "v Todos os status", font=font(size=13), fill=TEXT)
    rounded_rect(d, [215, 130, 380, 165], 6, fill=BG_CARD, outline=BORDER, width=1)
    d.text((230, 140), "v Score: maior primeiro", font=font(size=13), fill=TEXT)

    # Cabeçalho da tabela
    y = 190
    d.rectangle([30, y, W - 30, y + 38], fill=(241, 245, 249))
    cols = [
        ("Lead",          45),
        ("Telefone",      280),
        ("Score",         480),
        ("Resumo da IA",  570),
        ("Status",       1020),
        ("Ação",         1100),
    ]
    for label, x in cols:
        d.text((x, y + 12), label, font=font("arialbd.ttf", 12), fill=TEXT_MUTED)

    leads = [
        ("Maria Silva",    "+55 11 99999-8888", 92, "Ansiedade crônica, começar essa semana, online até 1500", "NOVO",     SUCCESS),
        ("João Mendes",    "+55 21 98888-7777", 87, "Casal em crise, urgência, prefere presencial",            "NOVO",     SUCCESS),
        ("Ana Pereira",    "+55 11 97777-6666", 81, "Avaliar TDAH para filho de 9 anos, particular",           "NOVO",     SUCCESS),
        ("Carlos Souza",   "+55 47 96666-5555", 74, "Insônia, sem urgência, quer entender preço primeiro",     "PARK",     WARNING),
        ("Beatriz Lima",   "+55 31 95555-4444", 68, "Acabou de chegar — IA ainda qualificando",                "EM CONV.", PRIMARY),
    ]

    y += 38
    for idx, (nome, fone, score, resumo, status, status_color) in enumerate(leads):
        row_bg = BG_CARD if idx % 2 == 0 else (250, 251, 253)
        d.rectangle([30, y, W - 30, y + 75], fill=row_bg, outline=BORDER, width=1)

        # Nome + iniciais avatar
        d.ellipse([45, y + 18, 85, y + 58], fill=(220, 234, 254))
        initials = nome.split()[0][0] + nome.split()[1][0]
        d.text((52, y + 25), initials, font=font("arialbd.ttf", 16), fill=PRIMARY)
        d.text((100, y + 22), nome, font=font("arialbd.ttf", 14), fill=TEXT)
        d.text((100, y + 42), "WhatsApp", font=font(size=11), fill=TEXT_MUTED)

        # Telefone
        d.text((280, y + 30), fone, font=font(size=13), fill=TEXT)

        # Score badge
        score_color = SUCCESS if score >= 80 else (WARNING if score >= 60 else DANGER)
        rounded_rect(d, [475, y + 22, 540, y + 52], 14, fill=score_color)
        d.text((492, y + 28), str(score), font=font("arialbd.ttf", 16), fill=(255, 255, 255))

        # Resumo (trunca se passar)
        if len(resumo) > 55:
            resumo = resumo[:52] + "..."
        d.text((570, y + 22), resumo, font=font(size=12), fill=TEXT)
        d.text((570, y + 42), "Gerado pela IA SDR • há 3 min", font=font(size=10), fill=TEXT_MUTED)

        # Status pill
        rounded_rect(d, [1020, y + 27, 1090, y + 47], 10, fill=status_color)
        d.text((1028, y + 30), status, font=font("arialbd.ttf", 10), fill=(255, 255, 255))

        # Botão Ligar
        rounded_rect(d, [1100, y + 22, 1160, y + 52], 6, fill=PRIMARY)
        d.text((1115, y + 30), "Abrir", font=font("arialbd.ttf", 12), fill=(255, 255, 255))

        y += 76

    img.save(OUT / "02_lista_leads.png", "PNG")
    print(f"OK 02_lista_leads.png")


# =====================================================================
# 3. DETALHE DO LEAD com resumo da IA e botão Ligar
# =====================================================================
def mockup_detalhe_lead():
    img = Image.new("RGB", (W, H), BG_PAGE)
    d = ImageDraw.Draw(img)
    header_bar(img, "Maria Silva", "Lead nº 0193 • WhatsApp • Recebido há 4 minutos")

    # Coluna esquerda: card de dados + resumo
    card_x = 30
    card_w = 720
    y = 135

    # CARD: Dados do lead
    rounded_rect(d, [card_x, y, card_x + card_w, y + 130], 8, fill=BG_CARD, outline=BORDER, width=1)
    d.text((card_x + 20, y + 18), "Dados do lead", font=font("arialbd.ttf", 14), fill=TEXT)

    def label_val(lx, ly, label, val):
        d.text((lx, ly), label, font=font(size=11), fill=TEXT_MUTED)
        d.text((lx, ly + 16), val, font=font("arialbd.ttf", 13), fill=TEXT)

    label_val(card_x + 20, y + 50, "TELEFONE", "+55 11 99999-8888")
    label_val(card_x + 230, y + 50, "CANAL", "WhatsApp")
    label_val(card_x + 350, y + 50, "ORIGEM", "Instagram Ads")
    label_val(card_x + 510, y + 50, "PRIMEIRA MSG", "09:14 (há 4min)")

    label_val(card_x + 20, y + 95, "SCORE", "92 / 100")
    label_val(card_x + 230, y + 95, "STATUS", "Qualificado pela IA")

    # CARD: Resumo da IA
    y += 150
    rounded_rect(d, [card_x, y, card_x + card_w, y + 270], 8, fill=BG_CARD, outline=BORDER, width=1)
    d.text((card_x + 20, y + 18), "Resumo da conversa (gerado pela IA SDR)",
           font=font("arialbd.ttf", 14), fill=TEXT)
    d.text((card_x + 20, y + 38), "✓ 7 mensagens trocadas em 4 minutos",
           font=font(size=11), fill=TEXT_MUTED)

    resumo_titulo = "Maria, 34, ansiedade crônica."
    resumo_corpo = [
        "DOR: ansiedade crônica há 2 anos. Já tentou meditação sem resultado,",
        "agora busca acompanhamento profissional.",
        "",
        "PRAZO: quer começar ainda esta semana (urgência alta).",
        "",
        "MODALIDADE: somente online, à noite (após 19h).",
        "",
        "ORÇAMENTO: até R$ 1.500/mês.",
        "",
        "DECISOR: ela mesma (é a paciente final).",
    ]
    d.text((card_x + 20, y + 66), resumo_titulo, font=font("arialbd.ttf", 14), fill=PRIMARY)
    for i, line in enumerate(resumo_corpo):
        d.text((card_x + 20, y + 92 + i * 17), line, font=font(size=12), fill=TEXT)

    # Coluna direita: ações
    right_x = 770
    right_w = 400
    y = 135

    rounded_rect(d, [right_x, y, right_x + right_w, y + 240], 8, fill=BG_CARD, outline=BORDER, width=1)
    d.text((right_x + 20, y + 18), "Próximo passo", font=font("arialbd.ttf", 14), fill=TEXT)

    # Botão primário Ligar
    rounded_rect(d, [right_x + 20, y + 55, right_x + right_w - 20, y + 105], 8, fill=SUCCESS)
    d.text((right_x + 95, y + 70), "📞  Ligar agora",
           font=font("arialbd.ttf", 18), fill=(255, 255, 255))

    # SLA
    d.text((right_x + 20, y + 120), "SLA: responder em até 30 minutos",
           font=font(size=12), fill=TEXT_MUTED)
    rounded_rect(d, [right_x + 20, y + 138, right_x + 20 + 220, y + 150], 5, fill=(220, 234, 254))
    rounded_rect(d, [right_x + 20, y + 138, right_x + 20 + 70, y + 150], 5, fill=PRIMARY)
    d.text((right_x + 20, y + 155), "4 min decorridos de 30",
           font=font(size=11), fill=TEXT_MUTED)

    # Botão secundário WhatsApp
    rounded_rect(d, [right_x + 20, y + 185, right_x + right_w - 20, y + 220], 6,
                 fill=BG_CARD, outline=PRIMARY, width=2)
    d.text((right_x + 110, y + 192), "Abrir conversa no WhatsApp",
           font=font("arialbd.ttf", 13), fill=PRIMARY)

    # Card de resultado da ligação
    y += 260
    rounded_rect(d, [right_x, y, right_x + right_w, y + 220], 8, fill=BG_CARD, outline=BORDER, width=1)
    d.text((right_x + 20, y + 18), "Depois de ligar",
           font=font("arialbd.ttf", 14), fill=TEXT)
    d.text((right_x + 20, y + 48), "Como foi?", font=font(size=12), fill=TEXT_MUTED)

    # Botões de outcome
    outcomes = [
        ("✓ Fechou venda",     SUCCESS),
        ("○ Vai pensar",       WARNING),
        ("✗ Não fechou",       DANGER),
        ("⊘ Não atendeu",      TEXT_MUTED),
    ]
    by = y + 75
    for label, color in outcomes:
        rounded_rect(d, [right_x + 20, by, right_x + right_w - 20, by + 28], 6,
                     fill=BG_CARD, outline=color, width=1)
        d.text((right_x + 35, by + 7), label, font=font("arialbd.ttf", 12), fill=color)
        by += 32

    img.save(OUT / "03_detalhe_lead.png", "PNG")
    print(f"OK 03_detalhe_lead.png")


# =====================================================================
# 4. DASHBOARD SIMPLES (números do dia)
# =====================================================================
def mockup_dashboard():
    img = Image.new("RGB", (W, H), BG_PAGE)
    d = ImageDraw.Draw(img)
    header_bar(img, "Painel de hoje", "Atualizado em tempo real • 29/jun, 09:42")

    # Cards de métricas (4 em linha)
    metrics = [
        ("Leads recebidos hoje",          "28",  "+6 vs ontem",      PRIMARY),
        ("Qualificados pela IA",          "12",  "43% taxa",         SUCCESS),
        ("Ligados pelos closers",         "9",   "75% dos quali.",   SUCCESS),
        ("Fechamentos",                   "4",   "44% conversão",    SUCCESS),
    ]
    card_w = 270
    card_h = 130
    gap = 20
    total_w = card_w * 4 + gap * 3
    start_x = (W - total_w) // 2
    y = 140
    for i, (label, big, sub, color) in enumerate(metrics):
        x = start_x + i * (card_w + gap)
        rounded_rect(d, [x, y, x + card_w, y + card_h], 10, fill=BG_CARD, outline=BORDER, width=1)
        d.text((x + 20, y + 18), label, font=font("arialbd.ttf", 13), fill=TEXT_MUTED)
        d.text((x + 20, y + 42), big, font=font("arialbd.ttf", 42), fill=color)
        d.text((x + 20, y + 100), sub, font=font(size=12), fill=TEXT_MUTED)

    # Funil do dia
    y = 300
    rounded_rect(d, [30, y, W - 30, y + 230], 10, fill=BG_CARD, outline=BORDER, width=1)
    d.text((50, y + 20), "Funil do dia", font=font("arialbd.ttf", 16), fill=TEXT)

    funnel = [
        ("Recebidos",       28, PRIMARY),
        ("Em conversa IA",  18, PRIMARY),
        ("Qualificados",    12, SUCCESS),
        ("Ligados",         9,  SUCCESS),
        ("Fecharam",        4,  SUCCESS),
    ]
    bar_y = y + 60
    max_w = W - 380
    for label, qtd, color in funnel:
        d.text((50, bar_y), label, font=font(size=13), fill=TEXT)
        bar_w = int(max_w * qtd / 28)
        rounded_rect(d, [200, bar_y - 2, 200 + bar_w, bar_y + 24], 4, fill=color)
        d.text((210 + bar_w, bar_y + 2), str(qtd), font=font("arialbd.ttf", 14), fill=TEXT)
        bar_y += 32

    # Próximos handoffs
    y = 560
    rounded_rect(d, [30, y, W - 30, y + 200], 10, fill=BG_CARD, outline=BORDER, width=1)
    d.text((50, y + 20), "Aguardando ligação (ordem por SLA)",
           font=font("arialbd.ttf", 16), fill=TEXT)

    items = [
        ("Maria Silva",   "score 92", "há 4 min",  "Maria, 34, ansiedade, esta semana, online até R$1500", SUCCESS),
        ("João Mendes",   "score 87", "há 12 min", "Casal em crise, urgência, prefere presencial",         SUCCESS),
        ("Ana Pereira",   "score 81", "há 25 min", "TDAH filho 9 anos, particular",                        WARNING),
    ]
    iy = y + 55
    for nome, score, tempo, brief, cor in items:
        rounded_rect(d, [50, iy, W - 50, iy + 38], 6, fill=(250, 251, 253), outline=BORDER, width=1)
        d.text((65, iy + 8), nome, font=font("arialbd.ttf", 13), fill=TEXT)
        d.text((220, iy + 11), score, font=font(size=11), fill=cor)
        d.text((310, iy + 11), tempo, font=font(size=11), fill=TEXT_MUTED)
        d.text((430, iy + 11), brief, font=font(size=12), fill=TEXT)
        iy += 45

    img.save(OUT / "04_dashboard.png", "PNG")
    print(f"OK 04_dashboard.png")


mockup_conversa()
mockup_lista_leads()
mockup_detalhe_lead()
mockup_dashboard()
print(f"\nMockups salvos em: {OUT}")

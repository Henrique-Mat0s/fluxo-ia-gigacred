# -*- coding: utf-8 -*-
"""
Mockups customizados pra GIGACRED Correspondente.
Saída: mockups-gigacred/01..04.png
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(__file__).parent / "mockups-gigacred"
OUT.mkdir(exist_ok=True)
FONTS = "C:/Windows/Fonts"

def font(name="arial.ttf", size=14):
    return ImageFont.truetype(f"{FONTS}/{name}", size)

# Paleta GigaCred (verde/amarelo financeiro)
BG_PAGE     = (243, 250, 244)        # verde-pastel claro
BG_CARD     = (255, 255, 255)
HEADER      = (21, 87, 36)           # verde escuro
ACCENT      = (255, 193, 7)          # amarelo FGTS
TEXT        = (33, 37, 41)
TEXT_MUTED  = (108, 117, 125)
PRIMARY     = (40, 167, 69)          # verde primary
SUCCESS     = (34, 197, 94)
WARNING     = (234, 179, 8)
DANGER      = (220, 53, 69)
BORDER      = (212, 224, 215)
WA_BG       = (236, 229, 221)
WA_OUT      = (220, 248, 198)
WA_IN       = (255, 255, 255)

W, H = 1200, 800

def rr(d, xy, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)

def header_bar(img, title, subtitle):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 60], fill=HEADER)
    # Logo "GigaCred"
    d.text((30, 14), "GIGA", font=font("arialbd.ttf", 20), fill=(255, 255, 255))
    d.text((85, 14), "CRED", font=font("arialbd.ttf", 20), fill=ACCENT)
    d.text((150, 22), "  •  Painel do Correspondente",
           font=font(size=12), fill=(200, 220, 205))
    d.text((W - 200, 22), "Olá, Carlos v", font=font(size=13), fill=(220, 235, 225))

    d.rectangle([0, 60, W, 110], fill=(255, 255, 255))
    d.line([(0, 110), (W, 110)], fill=BORDER, width=1)
    d.text((30, 72), title, font=font("arialbd.ttf", 20), fill=TEXT)
    d.text((30, 95), subtitle, font=font(size=12), fill=TEXT_MUTED)


# =====================================================================
# 1. CONVERSA Bot ↔ Lead (estilo WhatsApp) — sobre FGTS
# =====================================================================
def mockup_conversa():
    img = Image.new("RGB", (W, H), WA_BG)
    d = ImageDraw.Draw(img)

    # Header WhatsApp
    d.rectangle([0, 0, W, 70], fill=(7, 94, 84))
    d.ellipse([20, 13, 64, 57], fill=(180, 220, 215))
    d.text((33, 26), "J", font=font("arialbd.ttf", 22), fill=(7, 94, 84))
    d.text((80, 18), "José Oliveira", font=font("arialbd.ttf", 17), fill=(255, 255, 255))
    d.text((80, 42), "+55 31 98765-4321  •  online agora",
           font=font(size=12), fill=(220, 240, 235))

    def bubble(y, text, is_out=False, time="14:22"):
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
        bubble_w = 480
        bubble_h = 28 + len(lines) * 20
        if is_out:
            x = W - bubble_w - 30
            fill = WA_OUT
        else:
            x = 30
            fill = WA_IN
        rr(d, [x, y, x + bubble_w, y + bubble_h], 10, fill=fill)
        for i, line in enumerate(lines):
            d.text((x + 14, y + 10 + i * 20), line, font=font(size=14), fill=TEXT)
        d.text((x + bubble_w - 50, y + bubble_h - 18), time,
               font=font(size=10), fill=TEXT_MUTED)
        return y + bubble_h + 12

    y = 95
    # Bot dispara mensagem-isca (out = verde) — captação ativa
    y = bubble(y, "Oi! Tudo bem? Aqui é a Bia da GIGACRED. "
                  "Você sabia que dá pra antecipar até 7 anos do seu "
                  "saque-aniversário do FGTS e receber tudo no PIX?",
               is_out=True, time="14:20")
    # Lead responde (in = branco)
    y = bubble(y, "Sério? quanto da?", is_out=False, time="14:22")
    y = bubble(y, "Depende do seu saldo. Você já fez a adesão "
                  "ao Saque-Aniversário no app da Caixa?",
               is_out=True, time="14:22")
    y = bubble(y, "Já sim, faz 1 ano", is_out=False, time="14:23")
    y = bubble(y, "Boa! E você sabe mais ou menos quanto tem hoje "
                  "de saldo no FGTS?", is_out=True, time="14:23")
    y = bubble(y, "Acho que uns 8 mil", is_out=False, time="14:24")
    y = bubble(y, "Com R$ 8 mil, dá pra antecipar até R$ 5.200 no PIX "
                  "em 1-2 dias. Posso te chamar pra fechar?",
               is_out=True, time="14:25")
    y = bubble(y, "Sim! preciso urgente pra pagar uma dívida",
               is_out=False, time="14:26")

    badge_y = y + 8
    d.rectangle([20, badge_y, W - 20, badge_y + 40], fill=(213, 240, 220))
    d.text((35, badge_y + 12),
           "[OK] IA SDR detectou lead qualificado (score 88) — passando para o closer ligar",
           font=font("arialbd.ttf", 13), fill=(20, 90, 35))

    img.save(OUT / "01_conversa.png", "PNG")
    print("OK 01_conversa.png")


# =====================================================================
# 2. LISTA DE LEADS
# =====================================================================
def mockup_lista_leads():
    img = Image.new("RGB", (W, H), BG_PAGE)
    d = ImageDraw.Draw(img)
    header_bar(img, "Leads pra ligar agora",
               "6 leads qualificados pela IA aguardando contato — total estimado R$ 28.350")

    # Filtros
    rr(d, [30, 130, 220, 165], 6, fill=BG_CARD, outline=BORDER, width=1)
    d.text((45, 140), "v Todos os produtos", font=font(size=13), fill=TEXT)
    rr(d, [235, 130, 425, 165], 6, fill=BG_CARD, outline=BORDER, width=1)
    d.text((250, 140), "v Score: maior primeiro", font=font(size=13), fill=TEXT)
    # Botão exportar
    rr(d, [W-160, 130, W-30, 165], 6, fill=HEADER)
    d.text((W-138, 140), "Exportar CSV", font=font("arialbd.ttf", 12), fill=(255,255,255))

    # Cabeçalho
    y = 190
    d.rectangle([30, y, W - 30, y + 38], fill=(240, 247, 242))
    cols = [
        ("Lead",                40),
        ("Telefone",            260),
        ("Produto",             430),
        ("Valor est.",          580),
        ("Score",               720),
        ("O que precisa",       810),
        ("Ação",                1090),
    ]
    for label, x in cols:
        d.text((x, y + 12), label, font=font("arialbd.ttf", 11), fill=TEXT_MUTED)

    leads = [
        ("José Oliveira",   "+55 31 98765-4321", "FGTS",           "R$ 4.800", 88, "Quitar dívida — urgente",          "NOVO", SUCCESS),
        ("Maria Santos",    "+55 21 99876-5432", "FGTS",           "R$ 6.200", 85, "Reforma de casa, esta semana",     "NOVO", SUCCESS),
        ("Pedro Lima",      "+55 11 97654-3210", "Cons. INSS",     "R$ 3.500", 82, "Aposentado, sem restrição",        "NOVO", SUCCESS),
        ("Ana Souza",       "+55 47 96543-2109", "FGTS",           "R$ 5.100", 79, "Viagem — sem urgência",            "AGUARD.", WARNING),
        ("Carlos Mendes",   "+55 85 95432-1098", "Cons. Privado",  "R$ 7.250", 76, "CLT, valor alto pedido",           "AGUARD.", WARNING),
        ("Lucia Ferreira",  "+55 62 94321-0987", "FGTS",           "R$ 1.500", 62, "Saldo baixo — score limítrofe",    "PARK",     TEXT_MUTED),
    ]

    y += 38
    for idx, (nome, fone, produto, valor, score, precisa, status, status_color) in enumerate(leads):
        row_bg = BG_CARD if idx % 2 == 0 else (250, 252, 251)
        d.rectangle([30, y, W - 30, y + 75], fill=row_bg, outline=BORDER, width=1)

        d.ellipse([45, y + 18, 85, y + 58], fill=(220, 240, 225))
        initials = nome.split()[0][0] + nome.split()[1][0]
        d.text((52, y + 25), initials, font=font("arialbd.ttf", 16), fill=HEADER)
        d.text((100, y + 22), nome, font=font("arialbd.ttf", 14), fill=TEXT)
        d.text((100, y + 42), "WhatsApp", font=font(size=11), fill=TEXT_MUTED)

        d.text((260, y + 30), fone, font=font(size=12), fill=TEXT)
        d.text((430, y + 30), produto, font=font("arialbd.ttf", 12), fill=HEADER)
        d.text((580, y + 22), valor, font=font("arialbd.ttf", 13), fill=TEXT)
        d.text((580, y + 42), "estimado", font=font(size=10), fill=TEXT_MUTED)

        score_color = SUCCESS if score >= 80 else (WARNING if score >= 70 else DANGER)
        rr(d, [715, y + 22, 780, y + 52], 14, fill=score_color)
        d.text((732, y + 28), str(score), font=font("arialbd.ttf", 16), fill=(255,255,255))

        if len(precisa) > 32:
            precisa = precisa[:29] + "..."
        d.text((810, y + 30), precisa, font=font(size=12), fill=TEXT)

        rr(d, [1010, y + 27, 1080, y + 47], 10, fill=status_color)
        d.text((1018, y + 30), status, font=font("arialbd.ttf", 10), fill=(255,255,255))

        rr(d, [1090, y + 22, 1160, y + 52], 6, fill=PRIMARY)
        d.text((1106, y + 30), "Ligar", font=font("arialbd.ttf", 13), fill=(255,255,255))

        y += 76

    img.save(OUT / "02_lista_leads.png", "PNG")
    print("OK 02_lista_leads.png")


# =====================================================================
# 3. DETALHE DO LEAD — FGTS
# =====================================================================
def mockup_detalhe_lead():
    img = Image.new("RGB", (W, H), BG_PAGE)
    d = ImageDraw.Draw(img)
    header_bar(img, "José Oliveira",
               "Lead nº 1847  •  WhatsApp  •  Antecipação FGTS  •  Recebido há 6 minutos")

    card_x = 30
    card_w = 720
    y = 135

    # CARD: Dados do lead
    rr(d, [card_x, y, card_x + card_w, y + 140], 8, fill=BG_CARD, outline=BORDER, width=1)
    d.text((card_x + 20, y + 18), "Dados do lead", font=font("arialbd.ttf", 14), fill=TEXT)

    def lv(lx, ly, label, val, val_color=TEXT):
        d.text((lx, ly), label, font=font(size=10), fill=TEXT_MUTED)
        d.text((lx, ly + 14), val, font=font("arialbd.ttf", 13), fill=val_color)

    lv(card_x + 20, y + 50,  "TELEFONE",         "+55 31 98765-4321")
    lv(card_x + 220, y + 50, "CPF",              "***.***.123-45")
    lv(card_x + 360, y + 50, "ORIGEM",           "Instagram Ads")
    lv(card_x + 520, y + 50, "PRIMEIRA MSG",     "14:22 (há 6min)")

    lv(card_x + 20, y + 95,  "PRODUTO",          "Antecipação FGTS",   HEADER)
    lv(card_x + 220, y + 95, "VALOR ESTIMADO",   "R$ 4.500 a 5.200",   PRIMARY)
    lv(card_x + 420, y + 95, "SCORE",            "88 / 100",           SUCCESS)
    lv(card_x + 540, y + 95, "STATUS",           "Qualificado",        SUCCESS)

    # CARD: Resumo da IA
    y += 160
    rr(d, [card_x, y, card_x + card_w, y + 260], 8, fill=BG_CARD, outline=BORDER, width=1)
    d.text((card_x + 20, y + 18), "Resumo da conversa (gerado pela IA SDR)",
           font=font("arialbd.ttf", 14), fill=TEXT)
    d.text((card_x + 20, y + 38), "9 mensagens trocadas em 4 minutos",
           font=font(size=11), fill=TEXT_MUTED)

    titulo = "José, 34, CLT, quer antecipar FGTS — URGENTE."
    corpo = [
        "SALDO FGTS: ~R$ 8.000 (informado pelo lead, não validado ainda).",
        "JÁ FEZ ADESÃO ao Saque-Aniversário na Caixa há 1 ano  → OK.",
        "",
        "MOTIVO: quitar dívida (urgência alta).",
        "",
        "EXPECTATIVA: receber em 1-2 dias úteis via PIX.",
        "",
        "VALOR ESTIMADO: R$ 4.500 a R$ 5.200 (depende do banco e taxa).",
        "",
        "RECOMENDADO: simular no BMG (taxa competitiva) ou Daycoval.",
    ]
    d.text((card_x + 20, y + 66), titulo, font=font("arialbd.ttf", 14), fill=HEADER)
    for i, line in enumerate(corpo):
        d.text((card_x + 20, y + 90 + i * 17), line, font=font(size=12), fill=TEXT)

    # Coluna direita
    right_x = 770
    right_w = 400
    y = 135

    # Botão Ligar
    rr(d, [right_x, y, right_x + right_w, y + 240], 8, fill=BG_CARD, outline=BORDER, width=1)
    d.text((right_x + 20, y + 18), "Próximo passo", font=font("arialbd.ttf", 14), fill=TEXT)

    rr(d, [right_x + 20, y + 55, right_x + right_w - 20, y + 105], 8, fill=PRIMARY)
    d.text((right_x + 110, y + 70), "Ligar agora",
           font=font("arialbd.ttf", 18), fill=(255, 255, 255))

    d.text((right_x + 20, y + 120), "SLA: responder em até 15 minutos",
           font=font(size=12), fill=TEXT_MUTED)
    rr(d, [right_x + 20, y + 138, right_x + 20 + 220, y + 150], 5, fill=(220, 240, 225))
    rr(d, [right_x + 20, y + 138, right_x + 20 + 88, y + 150], 5, fill=PRIMARY)
    d.text((right_x + 20, y + 155), "6 min decorridos de 15",
           font=font(size=11), fill=TEXT_MUTED)

    rr(d, [right_x + 20, y + 185, right_x + right_w - 20, y + 220], 6,
       fill=BG_CARD, outline=PRIMARY, width=2)
    d.text((right_x + 100, y + 192), "Abrir conversa no WhatsApp",
           font=font("arialbd.ttf", 13), fill=PRIMARY)

    # Card de banco recomendado
    y += 260
    rr(d, [right_x, y, right_x + right_w, y + 220], 8, fill=BG_CARD, outline=BORDER, width=1)
    d.text((right_x + 20, y + 18), "Simulação sugerida",
           font=font("arialbd.ttf", 14), fill=TEXT)

    bancos = [
        ("BMG",       "R$ 5.180", "taxa 1.79% am",   SUCCESS),
        ("Daycoval",  "R$ 5.040", "taxa 1.85% am",   PRIMARY),
        ("C6 Bank",   "R$ 4.890", "taxa 1.91% am",   PRIMARY),
        ("Pan",       "R$ 4.720", "taxa 1.99% am",   TEXT_MUTED),
    ]
    by = y + 50
    for nome_banco, valor, taxa, cor in bancos:
        rr(d, [right_x + 20, by, right_x + right_w - 20, by + 32], 6,
           fill=BG_CARD, outline=BORDER, width=1)
        d.text((right_x + 35, by + 8), nome_banco, font=font("arialbd.ttf", 12), fill=TEXT)
        d.text((right_x + 130, by + 8), valor, font=font("arialbd.ttf", 12), fill=cor)
        d.text((right_x + 230, by + 9), taxa, font=font(size=11), fill=TEXT_MUTED)
        by += 38

    img.save(OUT / "03_detalhe_lead.png", "PNG")
    print("OK 03_detalhe_lead.png")


# =====================================================================
# 4. DASHBOARD
# =====================================================================
def mockup_dashboard():
    img = Image.new("RGB", (W, H), BG_PAGE)
    d = ImageDraw.Draw(img)
    header_bar(img, "Painel de hoje", "Atualizado em tempo real  •  29/jun, 14:42")

    metrics = [
        ("Leads recebidos hoje",       "47",        "+12 vs ontem",       PRIMARY),
        ("Qualificados pela IA",       "23",        "49% taxa",           SUCCESS),
        ("Antecipações fechadas",      "11",        "48% conversão",      SUCCESS),
        ("Volume liberado",            "R$ 58.4k",  "ticket méd. R$5.3k", HEADER),
    ]
    card_w = 270
    gap = 20
    total_w = card_w * 4 + gap * 3
    start_x = (W - total_w) // 2
    y = 140
    for i, (label, big, sub, color) in enumerate(metrics):
        x = start_x + i * (card_w + gap)
        rr(d, [x, y, x + card_w, y + 130], 10, fill=BG_CARD, outline=BORDER, width=1)
        d.text((x + 20, y + 18), label, font=font("arialbd.ttf", 13), fill=TEXT_MUTED)
        d.text((x + 20, y + 42), big, font=font("arialbd.ttf", 38), fill=color)
        d.text((x + 20, y + 100), sub, font=font(size=12), fill=TEXT_MUTED)

    # Funil
    y = 300
    rr(d, [30, y, W - 30, y + 230], 10, fill=BG_CARD, outline=BORDER, width=1)
    d.text((50, y + 20), "Funil do dia", font=font("arialbd.ttf", 16), fill=TEXT)

    funnel = [
        ("Recebidos",                47, PRIMARY),
        ("Em conversa IA",           34, PRIMARY),
        ("Qualificados",             23, SUCCESS),
        ("Closer ligou",             18, SUCCESS),
        ("Fecharam antecipação",     11, HEADER),
    ]
    bar_y = y + 60
    max_w = W - 380
    for label, qtd, color in funnel:
        d.text((50, bar_y), label, font=font(size=13), fill=TEXT)
        bar_w = int(max_w * qtd / 47)
        rr(d, [220, bar_y - 2, 220 + bar_w, bar_y + 24], 4, fill=color)
        d.text((230 + bar_w, bar_y + 2), str(qtd), font=font("arialbd.ttf", 14), fill=TEXT)
        bar_y += 32

    # Distribuição por produto
    y = 560
    rr(d, [30, y, 615, y + 200], 10, fill=BG_CARD, outline=BORDER, width=1)
    d.text((50, y + 20), "Leads por produto (hoje)",
           font=font("arialbd.ttf", 16), fill=TEXT)
    produtos = [
        ("Antecipação FGTS",      32, HEADER),
        ("Consignado INSS",        9, PRIMARY),
        ("Consignado Privado",     4, SUCCESS),
        ("Outros",                 2, WARNING),
    ]
    by = y + 55
    for nome_p, qtd, cor in produtos:
        d.text((50, by + 2), nome_p, font=font(size=13), fill=TEXT)
        bar_w = int(380 * qtd / 47)
        rr(d, [250, by, 250 + bar_w, by + 22], 4, fill=cor)
        d.text((260 + bar_w, by + 2), str(qtd), font=font("arialbd.ttf", 13), fill=TEXT)
        by += 32

    # Volume por banco
    rr(d, [635, y, W - 30, y + 200], 10, fill=BG_CARD, outline=BORDER, width=1)
    d.text((655, y + 20), "Volume por banco (mês)",
           font=font("arialbd.ttf", 16), fill=TEXT)
    bancos = [
        ("BMG",        "R$ 142k", 0.85, PRIMARY),
        ("Daycoval",   "R$ 98k",  0.59, PRIMARY),
        ("C6 Bank",    "R$ 76k",  0.45, SUCCESS),
        ("Pan",        "R$ 41k",  0.24, WARNING),
    ]
    by = y + 55
    for nome_b, vol, prop, cor in bancos:
        d.text((655, by + 2), nome_b, font=font("arialbd.ttf", 13), fill=TEXT)
        bar_w = int(300 * prop)
        rr(d, [760, by, 760 + bar_w, by + 22], 4, fill=cor)
        d.text((770 + bar_w, by + 2), vol, font=font("arialbd.ttf", 13), fill=TEXT)
        by += 32

    img.save(OUT / "04_dashboard.png", "PNG")
    print("OK 04_dashboard.png")


# =====================================================================
# 5. BASE DE PROSPECÇÃO — tela do CRM com contatos a disparar
# =====================================================================
def mockup_base_prospeccao():
    img = Image.new("RGB", (W, H), BG_PAGE)
    d = ImageDraw.Draw(img)
    header_bar(img, "Base de prospecção",
               "Lista importada • 1.247 contatos • disparo controlado para não tomar ban")

    # Bloco de status do disparo
    y = 130
    rr(d, [30, y, W - 30, y + 110], 10, fill=BG_CARD, outline=BORDER, width=1)
    d.text((50, y + 18), "Disparo de hoje — 'Campanha FGTS Junho'",
           font=font("arialbd.ttf", 15), fill=TEXT)

    # Mini-stats da campanha
    stats = [
        ("Enviados",     "127",  "/ 150 limite",      HEADER),
        ("Entregues",    "119",  "94% taxa",          SUCCESS),
        ("Responderam",  "31",   "26% taxa",          PRIMARY),
        ("Bloqueados",   "3",    "2.4% (saudável)",   WARNING),
    ]
    sx = 50
    for label, big, sub, color in stats:
        d.text((sx, y + 50), label, font=font(size=11), fill=TEXT_MUTED)
        d.text((sx, y + 65), big, font=font("arialbd.ttf", 22), fill=color)
        d.text((sx + 55, y + 73), sub, font=font(size=11), fill=TEXT_MUTED)
        sx += 285

    # Botões de ação
    btn_x = W - 320
    rr(d, [btn_x, y + 50, btn_x + 130, y + 80], 6, fill=PRIMARY)
    d.text((btn_x + 25, y + 58), "Iniciar disparo",
           font=font("arialbd.ttf", 12), fill=(255,255,255))
    rr(d, [btn_x + 140, y + 50, btn_x + 290, y + 80], 6,
       fill=BG_CARD, outline=PRIMARY, width=2)
    d.text((btn_x + 160, y + 58), "Importar mais (CSV)",
           font=font("arialbd.ttf", 12), fill=PRIMARY)

    # Aviso anti-ban
    y = 255
    rr(d, [30, y, W - 30, y + 38], 6, fill=(255, 243, 205))
    d.text((50, y + 12),
           "[!] Limite seguro: 150 disparos/dia/chip. Intervalo de 40-90s entre envios. "
           "Mensagem é randomizada entre 5 variantes.",
           font=font("arialbd.ttf", 12), fill=(133, 100, 4))

    # Tabela de contatos
    y = 310
    d.rectangle([30, y, W - 30, y + 38], fill=(240, 247, 242))
    cols = [
        ("Nome",          45),
        ("Telefone",      280),
        ("Origem",        470),
        ("Última msg do bot",  640),
        ("Status",        940),
        ("Resposta",     1080),
    ]
    for label, x in cols:
        d.text((x, y + 12), label, font=font("arialbd.ttf", 11), fill=TEXT_MUTED)

    contatos = [
        ("Roberto Alves",  "+55 11 91234-5678", "Lead Magnet",   "Variante A — 14:08", "ENTREGUE",  "—",          TEXT_MUTED),
        ("Sandra Costa",   "+55 21 92345-6789", "Indicação",     "Variante C — 14:09", "RESPONDEU", "IA ASSUMIU", PRIMARY),
        ("José Oliveira",  "+55 31 98765-4321", "Form. Site",    "Variante B — 14:10", "RESPONDEU", "QUALIFICADO", SUCCESS),
        ("Bruno Pereira",  "+55 47 93456-7890", "Lead Magnet",   "Variante A — 14:11", "ENTREGUE",  "—",          TEXT_MUTED),
        ("Camila Rocha",   "+55 85 94567-8901", "Indicação",     "Variante D — 14:12", "BLOQUEADO", "lead bloqueou", DANGER),
        ("Felipe Santos",  "+55 62 95678-9012", "Form. Site",    "Variante E — 14:13", "RESPONDEU", "EM CONVERSA", PRIMARY),
    ]
    y += 38
    for idx, (nome, fone, origem, ultmsg, status, resposta, cor) in enumerate(contatos):
        row_bg = BG_CARD if idx % 2 == 0 else (250, 252, 251)
        d.rectangle([30, y, W - 30, y + 56], fill=row_bg, outline=BORDER, width=1)

        d.ellipse([45, y + 12, 80, y + 47], fill=(220, 240, 225))
        initials = nome.split()[0][0] + nome.split()[1][0]
        d.text((52, y + 18), initials, font=font("arialbd.ttf", 14), fill=HEADER)
        d.text((100, y + 12), nome, font=font("arialbd.ttf", 13), fill=TEXT)
        d.text((100, y + 30), "WhatsApp", font=font(size=10), fill=TEXT_MUTED)

        d.text((280, y + 20), fone, font=font(size=12), fill=TEXT)
        d.text((470, y + 20), origem, font=font(size=12), fill=TEXT_MUTED)
        d.text((640, y + 20), ultmsg, font=font(size=12), fill=TEXT)

        # Status pill
        status_pill_color = {
            "ENTREGUE": TEXT_MUTED, "RESPONDEU": PRIMARY,
            "BLOQUEADO": DANGER, "ENVIANDO": WARNING,
        }.get(status, TEXT_MUTED)
        rr(d, [930, y + 17, 1020, y + 37], 10, fill=status_pill_color)
        d.text((938, y + 20), status, font=font("arialbd.ttf", 9), fill=(255,255,255))

        # Resposta / próximo passo
        if resposta == "—":
            d.text((1080, y + 20), resposta, font=font(size=12), fill=TEXT_MUTED)
        else:
            d.text((1080, y + 20), resposta, font=font("arialbd.ttf", 11), fill=cor)

        y += 57

    img.save(OUT / "05_base_prospeccao.png", "PNG")
    print("OK 05_base_prospeccao.png")


mockup_conversa()
mockup_lista_leads()
mockup_detalhe_lead()
mockup_dashboard()
mockup_base_prospeccao()
print(f"\nMockups GigaCred salvos em: {OUT}")

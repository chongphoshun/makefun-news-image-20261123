#!/usr/bin/env python3
"""Draw the news-image-20261123 v3 front page: 1024x1024 PNG, stdlib + PIL.

All 38 stories happened or were first reported on Monday, 23 November 2026.
Run:  python3 draw_news.py   -> writes entry.png next to this script.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

INK = (26, 26, 26)
PAPER = (253, 252, 247)
RED = (164, 22, 26)
GREY = (90, 90, 90)
RULE = (150, 150, 150)
BOX = (245, 244, 238)

SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

W, H = 1024, 1024
MARGIN = 28
CW = W - 2 * MARGIN  # 968 content width


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    """Draw lines stacked; return y just below the last line."""
    if leading is None:
        leading = fnt.size + 4
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- stories
LEADS = [
    {
        "kicker": "CLIMATE — ANTALYA, TURKEY",
        "headline": "COP31 COLLAPSES",
        "summary": "UN climate talks end with no deal: the EU and about 130 nations "
                   "reject a text omitting fossil fuels. First collapse since 2009.",
    },
    {
        "kicker": "STRAIT OF HORMUZ",
        "headline": "HORMUZ ABLAZE",
        "summary": "Two supertankers hit mines and catch fire Monday, the IRGC says — "
                   "seven tankers hit since 16 Nov. Trump warns Iranian vessels will "
                   "be \"at the bottom of the sea\".",
    },
    {
        "kicker": "WALL STREET / ASIA",
        "headline": "AI ROUT REVERSES",
        "summary": "Nvidia jumps 31.5% on Monday as its board reinstates Jensen Huang "
                   "as CEO. Friday it closed at $125.53, down 14.01% in a session.",
    },
]

MAINS = [
    ("UKRAINE", "Drone hits flats; boy, 7, survives 14 hours in rubble",
     "Russian drone hits a five-storey block in Dymer; at least 10 killed."),
    ("LIBYA", "Russian corvette sunk",
     "The Merkury is sunk off Benghazi in a suspected Ukrainian sea-drone "
     "attack; a second Russian-linked cargo ship is also hit."),
    ("POLAND", "Russian missiles land in Poland; NATO to meet",
     "Cruise missiles land in south-east Poland. PM Tusk calls it an "
     "\"intentional provocation\"."),
    ("UNITED STATES", "Democrats clinch 258 House seats",
     "A North Carolina recount win gives Democrats 258 House seats — their "
     "largest majority since 1992."),
    ("INDONESIA", "24 killed in candy-factory fire",
     "Fire at a candy factory in Cikande, Banten, kills 24; about 30 are "
     "missing. A suspected air-conditioning short-circuit is blamed."),
    ("MEXICO", "'El Chapo Isidro' captured",
     "Troops capture $5m-reward FBI most-wanted Fausto Isidro Meza-Flores "
     "in Guasave; 11 killed. Mexico will try him at home despite a US order."),
    ("SUDAN", "Drone attacks kill five children",
     "Drone attacks in Khartoum and Omdurman kill five children and damage "
     "a UN building."),
    ("SOUTH SUDAN", "Paramilitary attack kills at least 24",
     "A paramilitary attack kills at least 24 civilians in South Sudan."),
    ("EU — INDONESIA", "Trade deal signed after 10 years",
     "The EU and Indonesia sign a trade deal after a decade of talks, "
     "removing 98.5% of tariffs on EU goods."),
    ("BELGIUM", "Anti-austerity strike shuts airports",
     "A nationwide strike halts air-traffic control and shuts airports in "
     "protest at austerity."),
    ("SOUTH KOREA", "Exports surge 95.2% in November",
     "Customs data on Monday: exports up 95.2% in the first 20 days, at "
     "$77.4bn. Annual exports passed $1tn on 19 Nov, a fourth country ever."),
    ("PORTUGAL", "Marquez wins eighth MotoGP title",
     "Marc Marquez takes his eighth MotoGP title, equalling Agostini, after "
     "finishing eighth in the Portimao race."),
]

BRIEFS = [
    "VYSHNEVE — 23 NOV: Shahed hits supermarket; 3 dead, 13 hurt.",
    "NOVOSHAKHTINSK — 23 NOV: Drones hit Rostov refinery; fire.",
    "GAZA — 23 NOV: Experts say war left widespread contamination.",
    "YEMEN — 23 NOV: Houthis claim Rabigh hit; Saudi strike kills 4.",
    "BAHRAIN — 23 NOV: Iranian strike wounds 2 in Sitra; case to UN.",
    "ISTANBUL — 23 NOV: Thousands rally against media takeover.",
    "RWANDA — 23 NOV: Five EU states accept deportation centres.",
    "IOWA — 23 NOV: Army to detonate 4 tonnes of explosives despite court.",
    "BRASILIA — 23 NOV: Bolsonaro in intensive care, bowel blocked.",
    "NEW DELHI — 23 NOV: Nepal PM Balen Shah welcomed, meets Modi.",
    "INDIA — 23 NOV: Youth Congress vs Meta; India 3rd in Lowy Index.",
    "JAPAN — 23 NOV: Exports jump 20.5% on chips.",
    "VANUATU — 23 NOV: Magnitude 6.5 quake, very deep.",
    "UK — 23 NOV: NHS launches biggest AI breast-cancer trial.",
    "ITALY — 23 NOV: Jeweller Paolo Bulgari dies aged 89.",
    "MALAYSIA — 23 NOV: Selangor flood evacuees rise past 1,800.",
    "DR CONGO — 23 NOV: Fighting hits Ebola response; WHO urges peace.",
    "LIVERPOOL — 23 NOV: Man Utd beaten 4-0; Yoro sent off in 8 minutes.",
    "LAS VEGAS GP — 23 NOV: Verstappen wins; Leclerc, Hamilton collide.",
    "SERIE A — 23 NOV: Atalanta and Inter draw 4-4 in thriller.",
    "ODESA — 23 NOV: Schools go remote 23-27 Nov after grid damage.",
    "INDIA — 23 NOV: Tata Steel to buy $1.67bn pipe-maker stake.",
    "WASHINGTON — 23 NOV: Democrats take Congress; funds end 11 Dec.",
]

NUMBERS = [
    ("258", "House seats — most since 1992"),
    ("-5.8%", "Kospi, intraday Monday"),
    ("24", "killed, Indonesia factory fire"),
    ("10+", "killed, Dymer drone strike"),
    ("2", "supertankers hit by mines, Hormuz"),
    ("+31.5%", "Nvidia, Monday rebound"),
]

# Schematic continents, drawn relative to the map area origin (map_y0).
# Every polygon is a separate landmass with a clear gap to every neighbour;
# Africa is its own polygon, well clear of Europe and Asia.
# Map area is 80px tall; x spans 40..984.
CONTINENTS = [
    # (fill, polygon [(x, y_rel)], dot (x, y_rel), count)
    ((219, 234, 248),
     [(95, 12), (170, 2), (245, 8), (262, 26), (235, 44),
      (185, 50), (140, 44), (100, 40), (82, 26)], (170, 26), 6),
    ((220, 240, 210),
     [(232, 50), (276, 48), (294, 64), (278, 80), (250, 78),
      (230, 64)], (262, 64), 1),
    ((254, 240, 199),
     [(472, 12), (516, 4), (540, 16), (528, 32), (498, 36),
      (476, 26)], (505, 20), 13),
    ((253, 224, 180),
     [(478, 46), (522, 44), (546, 54), (540, 72), (512, 80),
      (486, 72), (472, 58)], (508, 62), 5),
    ((205, 235, 225),
     [(566, 8), (700, 0), (860, 6), (892, 26), (862, 46),
      (780, 54), (680, 50), (600, 40), (560, 24)], (720, 28), 12),
    ((232, 220, 245),
     [(828, 58), (884, 54), (904, 66), (874, 80), (836, 74)],
     (866, 68), 1),
]

DATE = "23 NOV 2026"


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_title = font(SERIF_B, 42)
    f_sub = font(SANS_B, 15)
    f_kick = font(SANS_B, 11)
    f_date = font(SANS, 11)
    f_lead_h = font(SANS_B, 24)
    f_lead_s = font(SANS, 13)
    f_main_h = font(SANS_B, 16)
    f_main_s = font(SANS, 12)
    f_num_v = font(SANS_B, 20)
    f_num_l = font(SANS, 11)
    f_brief = font(SANS, 13)
    f_brief_b = font(SANS_B, 13)
    f_map_t = font(SANS_B, 11)
    f_map_l = font(SANS, 12)
    f_foot = font(SANS, 12)
    f_sec = font(SANS_B, 14)

    # ---- masthead ------------------------------------------------------
    y = 12
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, y), title, font=f_title, fill=INK)
    y += 50
    sub = "MONDAY, 23 NOVEMBER 2026   •   38 STORIES   •   7 REGIONS"
    tw = d.textlength(sub, font=f_sub)
    d.text(((W - tw) / 2, y), sub, font=f_sub, fill=RED)
    y += 24
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2)
    y += 6

    # ---- lead row: 3 columns -------------------------------------------
    col_w = (CW - 2 * 14) // 3
    lead_top = y
    for i, lead in enumerate(LEADS):
        x = MARGIN + i * (col_w + 14)
        cy = lead_top
        d.text((x, cy), lead["kicker"], font=f_kick, fill=RED)
        cy += 15
        d.text((x, cy), DATE, font=f_date, fill=GREY)
        cy += 16
        hl = wrap(d, lead["headline"], f_lead_h, col_w)
        assert len(hl) <= 1, f"lead headline wraps: {lead['headline']}"
        cy = draw_block(d, x, cy, hl, f_lead_h, leading=28)
        cy += 2
        sl = wrap(d, lead["summary"], f_lead_s, col_w)
        assert len(sl) <= 4, f"lead summary too long: {lead['summary']}"
        cy = draw_block(d, x, cy, sl, f_lead_s, leading=17)
        assert cy <= lead_top + 140, "lead column overflow"
    y = lead_top + 140
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
    y += 6

    # ---- schematic map panel -------------------------------------------
    map_top = y
    d.text((MARGIN, y), "SCHEMATIC MAP — NOT TO SCALE", font=f_map_t, fill=GREY)
    right = "38 STORIES ACROSS 7 REGIONS"
    d.text((W - MARGIN - d.textlength(right, font=f_map_t), y), right,
           font=f_map_t, fill=GREY)
    map_y0 = map_top + 16
    for fill, poly, dot, count in CONTINENTS:
        abs_poly = [(px, map_y0 + py) for px, py in poly]
        d.polygon(abs_poly, fill=fill, outline=(60, 60, 60), width=2)
        r = 11
        cx, cy = dot[0], map_y0 + dot[1]
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
                  outline=RED, width=2)
        num = str(count)
        nw = d.textlength(num, font=f_brief_b)
        d.text((cx - nw / 2, cy - 8), num, font=f_brief_b, fill=INK)
    y = map_y0 + 84
    legend = "EUROPE 13   •   ASIA 12   •   N. AMERICA 6   •   AFRICA 5   •   " \
             "S. AMERICA 1   •   OCEANIA 1"
    tw = d.textlength(legend, font=f_map_l)
    d.text(((W - tw) / 2, y), legend, font=f_map_l, fill=INK)
    y += 16
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
    y += 6

    # ---- main grid: 3 x 4 ----------------------------------------------
    d.text((MARGIN, y), "THE MAIN STORIES", font=f_sec, fill=INK)
    y += 18
    grid_top = y
    cell_w = (CW - 2 * 12) // 3
    cell_h = 82
    for i, (kicker, headline, summary) in enumerate(MAINS):
        row, col = divmod(i, 3)
        x = MARGIN + col * (cell_w + 12)
        cy = grid_top + row * cell_h
        d.text((x, cy), f"{kicker} — {DATE}", font=f_kick, fill=RED)
        cy += 14
        hl = wrap(d, headline, f_main_h, cell_w)
        assert len(hl) <= 2, f"main headline too long: {headline}"
        cy = draw_block(d, x, cy, hl, f_main_h, leading=18)
        sl = wrap(d, summary, f_main_s, cell_w)
        # A one-line headline leaves room for a 3-line summary; a two-line
        # headline leaves room for only 2 summary lines in the 82px cell.
        max_sl = 3 if len(hl) == 1 else 2
        assert len(sl) <= max_sl, f"main summary too long: {summary}"
        cy = draw_block(d, x, cy, sl, f_main_s, leading=14)
        assert cy <= grid_top + (row + 1) * cell_h - 2, \
            f"main cell overflow: {headline}"
    y = grid_top + 4 * cell_h
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
    y += 6

    # ---- by the numbers -------------------------------------------------
    d.text((MARGIN, y), "BY THE NUMBERS", font=f_sec, fill=INK)
    y += 18
    box_w = (CW - 5 * 8) // 6
    box_h = 52
    for i, (val, label) in enumerate(NUMBERS):
        x = MARGIN + i * (box_w + 8)
        d.rectangle([x, y, x + box_w, y + box_h], fill=BOX, outline=RULE, width=1)
        vw = d.textlength(val, font=f_num_v)
        d.text((x + (box_w - vw) / 2, y + 4), val, font=f_num_v, fill=RED)
        ll = wrap(d, label, f_num_l, box_w - 10)
        assert len(ll) <= 2, f"number label too long: {label}"
        ly = y + 27
        for line in ll:
            lw = d.textlength(line, font=f_num_l)
            d.text((x + (box_w - lw) / 2, ly), line, font=f_num_l, fill=INK)
            ly += 12
    y += box_h + 4
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
    y += 6

    # ---- briefs: 2 columns ----------------------------------------------
    d.text((MARGIN, y), "IN BRIEF — 23 MORE", font=f_sec, fill=INK)
    y += 17
    brief_top = y
    bcol_w = (CW - 16) // 2
    for i, brief in enumerate(BRIEFS):
        col = 0 if i < 12 else 1
        row = i if i < 12 else i - 12
        x = MARGIN + col * (bcol_w + 16)
        by = brief_top + row * 15
        bw = d.textlength(brief, font=f_brief)
        assert bw <= bcol_w, f"brief too long ({bw:.0f}px > {bcol_w}): {brief}"
        d.text((x, by), brief, font=f_brief, fill=INK)
    y = brief_top + 12 * 15 + 4

    # ---- footer ----------------------------------------------------------
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2)
    y += 6
    foot = "All stories happened or were first reported on Monday, 23 November 2026."
    tw = d.textlength(foot, font=f_foot)
    d.text(((W - tw) / 2, y), foot, font=f_foot, fill=GREY)
    y += 17
    assert y <= H - 4, f"page overflow: y={y}"

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()

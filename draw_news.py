#!/usr/bin/env python3
"""Draw the v2 front page for make.fun news-image-20261123.

1024x1024 PNG newspaper front page: 38 verified stories from Monday
23 November 2026, 7 regions, schematic world map, numbers strip, briefs.
Run: python3 draw_news.py  -> writes entry.png next to this script.
"""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 24
CONTENT_W = W - 2 * MARGIN  # 976

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (90, 90, 90)
RULE = (40, 40, 40)
PAPER = (252, 250, 244)
MAP_BG = (214, 232, 244)
MAP_LAND = (196, 214, 178)
MAP_LINE = (90, 110, 90)
NUM_BG = (238, 234, 222)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines, each fitting max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None,
                 max_lines=None):
    """Draw wrapped text; returns (lines_drawn, height_used).
    Raises if a single word is wider than max_w or lines exceed max_lines."""
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None and len(lines) > max_lines:
        raise ValueError("text needs %d lines, max %d: %r"
                         % (len(lines), max_lines, text[:60]))
    lh = leading or int(fnt.size * 1.22)
    for i, line in enumerate(lines):
        draw.text((x, y + i * lh), line, font=fnt, fill=fill)
    return len(lines), len(lines) * lh


# ---------------------------------------------------------------- stories
LEADS = [
    {
        "kicker": "ANTALYA, TURKEY",
        "headline": "COP31 COLLAPSES IN ANTALYA",
        "summary": ("UN climate talks end with NO deal \u2014 the longest "
                    "COP ever. The EU and ~130 nations reject a text "
                    "omitting fossil fuels."),
    },
    {
        "kicker": "STRAIT OF HORMUZ",
        "headline": "HORMUZ TANKERS ABLAZE",
        "summary": ("Iran's IRGC says 2 supertankers hit mines and caught "
                    "fire Monday. 7 hit since 16 Nov. Trump warns "
                    "blockade-testers will be sunk."),
    },
    {
        "kicker": "ASIA",
        "headline": "AI SELL-OFF SPREADS ACROSS ASIA",
        "summary": ("Kospi fell as much as 5.8% intraday. S&P 500 -3.7% "
                    "and Nasdaq -5.3% Friday; Nvidia -14%. Fears AI "
                    "valuations are unsustainable."),
    },
]

MAINS = [
    ("DYMER, UKRAINE", "Russian drone kills at least 10 in Dymer",
     "A drone hits a 5-storey block. A boy, 7, is pulled alive from the "
     "rubble after 14 hours."),
    ("BENGHAZI, LIBYA", "Russian corvette sunk off Benghazi",
     "Suspected Ukrainian sea-drones sink the Merkury; a second "
     "Russian-linked ship is also hit."),
    ("SOUTH-EAST POLAND", "Russian missiles land in Poland",
     "Cruise missiles land in Poland. NATO is to meet. PM Tusk calls it "
     "an \u201cintentional provocation\u201d."),
    ("WASHINGTON, US", "Democrats clinch 258 House seats",
     "Largest House majority since 1992, after a North Carolina recount "
     "win seals control."),
    ("CIKANDE, BANTEN, JAVA", "24 killed in Java candy-factory fire",
     "About 30 are missing after a fire on Saturday. A suspected AC "
     "short-circuit is blamed."),
    ("SINALOA, MEXICO", "FBI most-wanted cartel boss captured",
     "Meza-Flores, \u201cEl Chapo Isidro\u201d, is captured. A $5m bounty; "
     "he faces US extradition."),
    ("KHARTOUM, SUDAN", "Drone attacks kill 5 children in Sudan",
     "Drone attacks kill 5 children in Khartoum and Omdurman. A UN "
     "building is damaged."),
    ("SOUTH SUDAN", "At least 24 civilians killed in South Sudan",
     "A paramilitary attack kills at least 24 civilians, officials say."),
    ("EU \u2013 INDONESIA", "EU\u2013Indonesia trade deal signed",
     "Deal signed after 10 years of talks. It removes 98.5% of tariffs "
     "on EU goods."),
    ("BELGIUM", "Belgium strike shuts airports",
     "An anti-austerity strike halts air-traffic control and shuts "
     "airports across the country."),
    ("SOUTH KOREA", "South Korea exports surge 95.2%",
     "First-20-days exports hit $77.4bn; annual exports passed "
     "$1 trillion on 19 Nov."),
    ("PORTIMAO, PORTUGAL", "Marquez wins 8th MotoGP title",
     "Marc Marquez equals Agostini with an 8th title, finishing 8th in "
     "the race."),
]

BRIEFS = [
    ("VYSHNEVE, UKRAINE", "Shahed drone hits supermarket; 3 killed, 13 hurt."),
    ("NOVOSHAKHTINSK, RUSSIA", "Drones hit oil refinery; fire breaks out."),
    ("GAZA", "Experts say war left widespread contamination."),
    ("YEMEN", "Houthis claim refinery strike; Saudi hits Hodeida, 4 killed."),
    ("BAHRAIN", "Iranian strike wounds 2 in Sitra; case taken to UN."),
    ("ISTANBUL", "Thousands rally against media takeover."),
    ("RWANDA", "Five EU states accept deportation centres there."),
    ("IOWA, US", "Army to detonate 4 tonnes of explosives despite court order."),
    ("BRASILIA", "Bolsonaro in intensive care with intestinal obstruction."),
    ("NEW DELHI", "Nepal PM Balen Shah welcomed, meets PM Modi."),
    ("INDIA", "Youth Congress protests Meta; India 3rd in Lowy Power Index."),
    ("JAPAN", "Exports jump 20.5% on chips."),
    ("VANUATU REGION", "Magnitude 6.5 earthquake, very deep."),
    ("UK", "NHS launches world's largest AI breast-cancer trial."),
    ("ITALY", "Jeweller Paolo Bulgari dies aged 89."),
    ("MALAYSIA", "Selangor flood evacuees rise past 1,800."),
    ("DR CONGO", "Fighting near Ebola area disrupts response."),
    ("LIVERPOOL 4-0 MAN UTD", "Pochettino nightmare debut; Yoro off early."),
    ("LAS VEGAS GP", "Verstappen wins; Leclerc and Hamilton collide."),
    ("SERIE A", "Atalanta and Inter draw 4-4 in thriller."),
    ("ODESA", "Schools go remote 23\u201327 Nov after power-grid damage."),
    ("INDIA", "Tata Steel to buy $1.67bn stake in pipe maker."),
    ("WASHINGTON", "Democrats take Congress; funding deadline 11 Dec looms."),
]

NUMBERS = [
    ("258", "House seats \u2014 most since 1992"),
    ("-5.8%", "Kospi intraday fall"),
    ("24", "killed, Indonesia factory fire"),
    ("10+", "killed, Dymer drone strike"),
    ("2", "supertankers hit by mines, Hormuz"),
    ("$77.4bn", "Korea exports, first 20 days of Nov"),
]

# Schematic map: polygons in a 0..100 x 0..40 grid, scaled into the panel.
MAP_POLYS = [
    # North America (with Mexico tapering down)
    [(2, 5), (8, 2), (16, 2), (24, 4), (29, 7), (27, 10), (24, 12),
     (25, 15), (21, 18), (18, 21), (15, 18), (12, 14), (7, 12), (3, 9)],
    # Greenland
    [(28, 1), (33, 1), (33, 4), (28, 4)],
    # South America (triangle tapering south)
    [(24, 23), (28, 21), (32, 23), (33, 27), (31, 32), (28, 37),
     (25, 33), (23, 27)],
    # United Kingdom
    [(43, 4), (45, 4), (45, 6), (43, 6)],
    # Europe
    [(45, 3), (49, 1), (53, 2), (55, 5), (53, 8), (49, 9), (46, 7)],
    # Africa (wide top, tapering to a southern point)
    [(47, 11), (52, 10), (56, 12), (58, 16), (57, 21), (55, 26),
     (52, 27), (50, 22), (48, 17), (46, 14)],
    # Arabian peninsula (kept separate so the Middle East dot reads)
    [(58, 13), (61, 12), (63, 14), (62, 17), (59, 17), (57, 15)],
    # Asia (India bump and SE Asia reach down so it reads as a landmass)
    [(56, 2), (64, 1), (72, 1), (80, 2), (88, 4), (91, 7), (89, 10),
     (84, 11), (80, 13), (78, 17), (75, 20), (72, 17), (70, 13),
     (66, 12), (61, 11), (57, 9), (55, 6)],
    # South-east Asia islands
    [(78, 16), (82, 16), (82, 19), (78, 19)],
    [(84, 18), (87, 18), (87, 20), (84, 20)],
    # Oceania (rounder, bigger)
    [(80, 28), (86, 26), (91, 28), (90, 32), (85, 33), (80, 31)],
]
# (grid x, grid y, count, label) — dot centres, each on its own landmass
MAP_DOTS = [
    (14, 9, "4", "NORTH AMERICA"),
    (28, 28, "2", "LATIN AMERICA"),
    (50, 5, "12", "EUROPE"),
    (60, 14, "5", "MIDDLE EAST"),
    (52, 18, "5", "AFRICA"),
    (74, 7, "9", "ASIA"),
    (85, 30, "1", "OCEANIA"),
]

DATE = "23 NOV 2026"


def draw_map(draw, x0, y0, w, h):
    """Schematic world map inside rect (x0, y0, w, h)."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=MAP_BG,
                   outline=RULE, width=1)
    # map area: leave 16px header strip and 18px legend strip
    mx0, my0 = x0 + 8, y0 + 18
    mw, mh = w - 16, h - 18 - 20
    sx, sy = mw / 100.0, mh / 40.0

    def P(pt):
        return (mx0 + pt[0] * sx, my0 + pt[1] * sy)

    draw.text((x0 + 8, y0 + 3),
              "SCHEMATIC MAP \u2014 NOT TO SCALE",
              font=font(SANS_B, 11), fill=INK)
    for poly in MAP_POLYS:
        draw.polygon([P(p) for p in poly], fill=MAP_LAND,
                     outline=MAP_LINE)
    f_dot = font(SANS_B, 11)
    for gx, gy, count, _label in MAP_DOTS:
        cx, cy = P((gx, gy))
        r = 11
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
                     outline=(255, 255, 255), width=2)
        tw = draw.textlength(count, font=f_dot)
        draw.text((cx - tw / 2, cy - 8), count, font=f_dot,
                  fill=(255, 255, 255))
    legend = ("NORTH AMERICA 4   \u00b7   LATIN AMERICA 2   \u00b7   "
              "EUROPE 12   \u00b7   MIDDLE EAST 5   \u00b7   AFRICA 5   "
              "\u00b7   ASIA 9   \u00b7   OCEANIA 1")
    f_leg = font(SANS_B, 11)
    lw = draw.textlength(legend, font=f_leg)
    draw.text((x0 + (w - lw) / 2, y0 + h - 17), legend, font=f_leg,
              fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    boxes = []  # (x0, y0, x1, y1) text-block boxes for overlap checks

    def check_box(x0, y0, x1, y1, name):
        assert 0 <= x0 and x1 <= W and 0 <= y0 and y1 <= H, \
            "box out of page: %s" % name
        for (ax0, ay0, ax1, ay1, an) in boxes:
            assert not (x0 < ax1 and ax0 < x1 and y0 < ay1 and ay0 < y1), \
                "overlap: %s vs %s" % (name, an)
        boxes.append((x0, y0, x1, y1, name))

    y = 10
    # ---- masthead
    f_title = font(SERIF_B, 50)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, y), title, font=f_title, fill=INK)
    check_box((W - tw) / 2, y, (W + tw) / 2, y + 58, "masthead")
    y += 58
    f_sub = font(SANS_B, 15)
    sub = "MONDAY, 23 NOVEMBER 2026  \u00b7  38 STORIES  \u00b7  7 REGIONS"
    tw = d.textlength(sub, font=f_sub)
    d.text(((W - tw) / 2, y), sub, font=f_sub, fill=RED)
    check_box((W - tw) / 2, y, (W + tw) / 2, y + 19, "subline")
    y += 22
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    y += 4
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
    y += 8  # y = 102

    # ---- lead row: 3 columns
    col_w = (CONTENT_W - 2 * 16) // 3  # 314
    lead_top = y
    f_kick = font(SANS_B, 12)
    f_date = font(SANS, 11)
    f_lead_h = font(SANS_B, 24)
    f_lead_b = font(SANS, 13)
    for i, lead in enumerate(LEADS):
        x = MARGIN + i * (col_w + 16)
        cy = lead_top
        d.text((x, cy), lead["kicker"], font=f_kick, fill=RED)
        cy += 16
        d.text((x, cy), DATE, font=f_date, fill=GREY)
        cy += 15
        n, hh = draw_wrapped(d, x, cy, lead["headline"], f_lead_h,
                             col_w, leading=27, max_lines=3)
        cy += hh + 3
        n, hh = draw_wrapped(d, x, cy, lead["summary"], f_lead_b,
                             col_w, leading=16, max_lines=3)
        cy += hh
        check_box(x, lead_top, x + col_w, cy, "lead-%d" % i)
        if i < 2:
            d.line([(x + col_w + 8, lead_top),
                    (x + col_w + 8, cy)], fill=(200, 200, 190), width=1)
    y = lead_top + 150  # lead block height

    # ---- schematic map panel
    map_h = 120
    draw_map(d, MARGIN, y, CONTENT_W, map_h)
    check_box(MARGIN, y, W - MARGIN, y + map_h, "map")
    y += map_h + 6  # y = 384

    # ---- main section header
    f_sec = font(SANS_B, 16)
    d.text((MARGIN, y), "MAIN STORIES", font=f_sec, fill=INK)
    d.line([(MARGIN + 150, y + 10), (W - MARGIN, y + 10)], fill=RULE,
           width=1)
    y += 18  # y = 402

    # ---- main grid 3 x 4
    cell_w = (CONTENT_W - 2 * 16) // 3
    row_h = 88
    f_mkick = font(SANS_B, 11)
    f_mdate = font(SANS, 10)
    f_mhead = font(SANS_B, 15)
    f_mbody = font(SANS, 12)
    for idx, (kicker, headline, summary) in enumerate(MAINS):
        r, c = divmod(idx, 3)
        x = MARGIN + c * (cell_w + 16)
        cy = y + r * row_h
        d.text((x, cy), kicker, font=f_mkick, fill=RED)
        cy += 13
        d.text((x, cy), DATE, font=f_mdate, fill=GREY)
        cy += 12
        n, hh = draw_wrapped(d, x, cy, headline, f_mhead, cell_w,
                             leading=17, max_lines=2)
        cy += hh + 1
        n, hh = draw_wrapped(d, x, cy, summary, f_mbody, cell_w,
                             leading=14, max_lines=2)
        cy += hh
        assert cy <= y + (r + 1) * row_h, "main cell %d overflows row" % idx
        check_box(x, y + r * row_h, x + cell_w, cy, "main-%d" % idx)
    y += 4 * row_h  # y = 754

    # ---- BY THE NUMBERS strip
    y += 6
    f_num_h = font(SANS_B, 14)
    d.text((MARGIN, y), "BY THE NUMBERS", font=f_num_h, fill=INK)
    d.line([(MARGIN + 160, y + 9), (W - MARGIN, y + 9)], fill=RULE, width=1)
    y += 18
    box_w = (CONTENT_W - 5 * 8) // 6  # 156
    box_h = 52
    f_big = font(SANS_B, 19)
    f_lab = font(SANS, 10)
    for i, (val, label) in enumerate(NUMBERS):
        x = MARGIN + i * (box_w + 8)
        d.rectangle([x, y, x + box_w, y + box_h], fill=NUM_BG,
                    outline=(180, 175, 160), width=1)
        vw = d.textlength(val, font=f_big)
        d.text((x + (box_w - vw) / 2, y + 2), val, font=f_big, fill=RED)
        n, hh = draw_wrapped(d, x + 5, y + 26, label, f_lab, box_w - 10,
                             fill=INK, leading=11, max_lines=2)
        assert hh <= 24, "number label too tall: %r" % label
        check_box(x, y, x + box_w, y + box_h, "num-%d" % i)
    y += box_h + 6  # y = 836

    # ---- briefs
    f_br_h = font(SANS_B, 14)
    d.text((MARGIN, y), "IN BRIEF \u2014 23 MORE", font=f_br_h, fill=INK)
    d.line([(MARGIN + 185, y + 9), (W - MARGIN, y + 9)], fill=RULE, width=1)
    y += 16  # y = 852
    f_br = font(SANS, 12)
    f_br_tag = font(SANS_B, 12)
    brief_col_w = (CONTENT_W - 16) // 2  # 480
    lh = 12.5
    left = BRIEFS[:12]
    right = BRIEFS[12:]
    for col_i, col in enumerate((left, right)):
        x = MARGIN + col_i * (brief_col_w + 16)
        cy = y
        for tag, text in col:
            line = tag + " \u2014 " + text
            # measure with tag bold + rest regular: approximate with
            # full-line regular width; assert it fits.
            full_w = (d.textlength(tag + " \u2014 ", font=f_br_tag)
                      + d.textlength(text, font=f_br))
            assert full_w <= brief_col_w, \
                "brief too long (%d px): %r" % (full_w, line)
            d.text((x, cy), tag + " \u2014 ", font=f_br_tag, fill=RED)
            tw_tag = d.textlength(tag + " \u2014 ", font=f_br_tag)
            d.text((x + tw_tag, cy), text, font=f_br, fill=INK)
            cy += lh
        check_box(x, y, x + brief_col_w, cy, "briefs-col-%d" % col_i)
    y += 12 * lh  # y = 1004

    # ---- footer
    f_foot = font(SANS, 11)
    foot = ("All stories happened or were first reported on Monday, "
            "23 November 2026.")
    tw = d.textlength(foot, font=f_foot)
    d.text(((W - tw) / 2, y), foot, font=f_foot, fill=GREY)
    check_box((W - tw) / 2, y, (W + tw) / 2, y + 14, "footer")

    img.save(OUT, "PNG", optimize=True)
    print("wrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))


if __name__ == "__main__":
    main()

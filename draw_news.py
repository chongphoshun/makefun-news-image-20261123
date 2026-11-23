#!/usr/bin/env python3
"""Draw entry.png: a newspaper front page summing up world news, Monday 23 Nov 2026.

Standard library + Pillow only at draw time. Run: python3 draw_news.py
Writes entry.png (1024x1024) next to this script.
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"
W, H = 1024, 1024
MARGIN = 28
INK = (17, 17, 17)
MUTED = (68, 68, 68)
RED = (155, 27, 27)
RULE = (17, 17, 17)
LIGHT = (232, 232, 232)
BOX_BG = (242, 239, 233)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w, draw):
    """Greedy wrap on words; returns list of lines that all fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, max_w, text, fnt, fill, spacing=4, max_lines=None):
    lines = wrap(text, fnt, max_w, draw)
    if max_lines is not None:
        assert len(lines) <= max_lines, f"overflow: {text[:40]!r} -> {len(lines)} lines > {max_lines}"
    for ln in lines:
        assert draw.textlength(ln, font=fnt) <= max_w + 0.5, f"line too wide: {ln!r}"
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def text_h(fnt, n_lines, spacing=4):
    return n_lines * (fnt.size + spacing) - spacing


LEADS = [
    ("ANTALYA, TURKEY", "Climate talks collapse with no deal",
     "UN climate talks end with no deal. The EU and about 130 nations reject a text that omits fossil fuels. It is the first COP collapse since Copenhagen in 2009, and the longest COP ever."),
    ("STRAIT OF HORMUZ", "Tankers ablaze in Hormuz",
     "The IRGC says two supertankers hit mines and caught fire on Monday. Seven hit since 16 November. Trump warns vessels testing the US blockade will be \u201cat the bottom of the sea\u201d. US strikes could resume after the New Year without a deal."),
    ("ASIA, MONDAY", "AI sell-off spreads in Asia",
     "The Kospi fell as much as 5.8% intraday. The S&P 500 fell 3.7% on Friday and the Nasdaq 5.3%, on fears that AI valuations are unsustainable. Nvidia fell 14% on Friday."),
]

MAINS = [
    ("DYMER, UKRAINE", "Drone hits flats; boy, 7, survives 14 hours in rubble",
     "A Russian drone hits a five-storey block; at least 10 are killed."),
    ("BENGHAZI, LIBYA", "Russian corvette sunk in suspected sea-drone attack",
     "The Merkury is sunk; a second Russian-linked cargo ship is also hit."),
    ("WASHINGTON, US", "Democrats take 258 House seats, biggest win since 1992",
     "The majority is clinched after a North Carolina recount win."),
    ("SHENZHEN", "Trump, Putin and Xi agree \u201cDeclaration toward Peace\u201d",
     "The three leaders meet; Putin is seen as the biggest winner."),
    ("CIKANDE, INDONESIA", "Candy-factory fire kills 24; about 30 missing",
     "The fire breaks out on Saturday; a suspected air-conditioning short-circuit."),
    ("SINALOA, MEXICO", "FBI most-wanted \u201cEl Chapo Isidro\u201d captured",
     "Fausto Isidro Meza-Flores is held; a $5m bounty; he faces US extradition."),
    ("KHARTOUM, SUDAN", "Drone attacks kill five children in the capital",
     "Strikes hit Khartoum and Omdurman; a UN building is damaged."),
    ("SOUTH SUDAN", "Paramilitary attack kills at least 24 civilians",
     "At least 24 civilians are killed in the attack."),
    ("EU\u2013INDONESIA", "Trade deal signed after ten years of talks",
     "The deal removes 98.5% of tariffs on EU goods."),
    ("SOUTH KOREA", "Exports pass $1 trillion for the first time",
     "Annual exports top $1 trillion, a first for the country."),
    ("BELGIUM", "Anti-austerity strike shuts airports",
     "Air-traffic control is halted as airports shut in the strike."),
    ("PORTIMAO, PORTUGAL", "Marquez wins eighth MotoGP title",
     "He equals Agostini, sealing the title by finishing eighth."),
]

NUMBERS = [
    ("258", "House seats for Democrats \u2014 most since 1992"),
    ("-5.8%", "Kospi intraday fall in Asia"),
    ("24", "Killed in Indonesia factory fire"),
    ("10+", "Killed in Dymer drone strike"),
    ("2", "Supertankers hit by mines in Hormuz"),
    ("$1tn", "South Korea exports, first time"),
]

# 23 brief lines: 22 listed briefs, with the two India items merged into one
# line, plus the Riemann item labelled as a CLAIM (not confirmed).
BRIEFS = [
    ("POLAND", "Russian missiles land in SE Poland; NATO to meet; Tusk calls it an \u201cintentional provocation\u201d."),
    ("VYSHNEVE", "Shahed drone hits a supermarket; 3 killed, 13 injured."),
    ("NOVOSHAKHTINSK", "Drones hit a Rostov oil refinery; a fire breaks out."),
    ("GAZA", "Experts say the war left widespread contamination."),
    ("YEMEN", "Houthis claim a strike on the Saudi Rabigh refinery; Saudi strike hits Hodeida, 4+ killed."),
    ("BAHRAIN", "Iranian strike wounds 2 in Sitra; Bahrain takes the case to the UN."),
    ("ISTANBUL", "Thousands rally against a media takeover."),
    ("RWANDA", "Five EU countries accept deportation centres in Rwanda."),
    ("IOWA", "Army to detonate 4 tonnes of unstable explosives despite a court order."),
    ("BRASILIA", "Bolsonaro in intensive care with intestinal obstruction."),
    ("NEW DELHI", "Nepal PM Balen Shah welcomed; meets PM Modi."),
    ("INDIA", "Youth Congress protests Meta; India stays 3rd in Lowy Asia Power Index, 40.5 points."),
    ("TAIWAN", "Stocks swing 1,578 points intraday; TSMC up over 2%."),
    ("JAPAN", "Exports jump 20.5% on strong chip demand."),
    ("VANUATU", "Magnitude 6.5 earthquake, very deep, in the region."),
    ("UK", "NHS launches the largest trial of AI spotting breast cancer earlier."),
    ("ITALY", "Jeweller Paolo Bulgari dies aged 89."),
    ("MALAYSIA", "Selangor flood evacuees rise past 1,800."),
    ("DR CONGO", "Fighting near the Ebola area disrupts the response; WHO chief calls for peace."),
    ("LIVERPOOL 4\u20130 MAN UTD", "Pochettino\u2019s debut nightmare; Yoro sent off after 8 minutes."),
    ("LAS VEGAS GP", "Verstappen wins; Leclerc and Hamilton collide."),
    ("SERIE A", "Atalanta and Inter draw 4\u20134 in a thriller."),
    ("CLAIM: RIEMANN", "Anthropic\u2019s Levent Alpoege + Claude claim a proof of the Riemann Hypothesis."),
]

assert len(LEADS) == 3
assert len(MAINS) == 12
assert len(BRIEFS) == 23
assert len(NUMBERS) == 6


def main():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    boxes = []  # (x0, y0, x1, y1, label) text blocks, for overlap checks

    def record(x0, y0, x1, y1, label):
        for (a0, b0, a1, b1, other) in boxes:
            overlap = not (x1 <= a0 or a1 <= x0 or y1 <= b0 or b1 <= y0)
            assert not overlap, f"text overlap: {label!r} vs {other!r}"
        boxes.append((x0, y0, x1, y1, label))

    # ---- Masthead ----
    d.line([(MARGIN, 14), (W - MARGIN, 14)], fill=RULE, width=2)
    title_f = font(SERIF, 44)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 22), title, font=title_f, fill=INK)
    record((W - tw) / 2, 22, (W + tw) / 2, 22 + 44, "masthead")
    sub_f = font(SANS_B, 13)
    sub = "MONDAY, 23 NOVEMBER 2026  \u2022  38 STORIES  \u2022  7 REGIONS"
    sw = d.textlength(sub, font=sub_f)
    d.text(((W - sw) / 2, 76), sub, font=sub_f, fill=MUTED)
    record((W - sw) / 2, 76, (W + sw) / 2, 76 + 13, "subline")
    d.line([(MARGIN, 98), (W - MARGIN, 98)], fill=RULE, width=2)
    d.line([(MARGIN, 102), (W - MARGIN, 102)], fill=RULE, width=1)

    # ---- Lead row: 3 columns ----
    col_w = 308
    col_x = [MARGIN, MARGIN + col_w + 18, MARGIN + 2 * (col_w + 18)]
    lead_y = 112
    lead_bottom = 292
    for i, (kicker, head, summ) in enumerate(LEADS):
        x = col_x[i]
        if i:
            d.line([(x - 9, lead_y), (x - 9, lead_bottom)], fill=LIGHT, width=1)
        kf = font(SANS_B, 11)
        d.text((x, lead_y), kicker, font=kf, fill=RED)
        record(x, lead_y, x + d.textlength(kicker, font=kf), lead_y + 11, f"lead-kicker-{i}")
        hf = font(SANS_B, 21)
        y = draw_wrapped(d, x, lead_y + 18, col_w, head, hf, INK, spacing=2, max_lines=3)
        record(x, lead_y + 18, x + col_w, y, f"lead-head-{i}")
        sf = font(SANS, 13)
        y2 = draw_wrapped(d, x, y + 4, col_w, summ, sf, MUTED, spacing=3, max_lines=6)
        assert y2 <= lead_bottom + 2, f"lead {i} too tall: {y2}"
        record(x, y + 4, x + col_w, y2, f"lead-summ-{i}")
    d.line([(MARGIN, 300), (W - MARGIN, 300)], fill=RULE, width=2)

    # ---- Main stories: 3 x 4 grid ----
    sec_f = font(SANS_B, 12)
    d.text((MARGIN, 308), "MAIN STORIES", font=sec_f, fill=INK)
    record(MARGIN, 308, MARGIN + d.textlength("MAIN STORIES", font=sec_f), 320, "main-header")
    grid_y = 328
    row_h = 78
    for idx, (kicker, head, summ) in enumerate(MAINS):
        r, c = divmod(idx, 3)
        x = col_x[c]
        y0 = grid_y + r * row_h
        kf = font(SANS_B, 9)
        d.text((x, y0), kicker, font=kf, fill=RED)
        record(x, y0, x + d.textlength(kicker, font=kf), y0 + 9, f"main-kicker-{idx}")
        hf = font(SANS_B, 13)
        y = draw_wrapped(d, x, y0 + 13, col_w, head, hf, INK, spacing=1, max_lines=2)
        record(x, y0 + 13, x + col_w, y, f"main-head-{idx}")
        sf = font(SANS, 11)
        y2 = draw_wrapped(d, x, y + 1, col_w, summ, sf, MUTED, spacing=2, max_lines=2)
        assert y2 <= y0 + row_h - 2, f"main {idx} too tall: {y2} vs {y0 + row_h}"
        record(x, y + 1, x + col_w, y2, f"main-summ-{idx}")
        if r < 3:
            d.line([(MARGIN, y0 + row_h - 4), (W - MARGIN, y0 + row_h - 4)], fill=LIGHT, width=1)
    main_bottom = grid_y + 4 * row_h  # 640

    # ---- By the numbers ----
    d.text((MARGIN, main_bottom + 6), "BY THE NUMBERS", font=sec_f, fill=INK)
    record(MARGIN, main_bottom + 6, MARGIN + 150, main_bottom + 18, "numbers-header")
    strip_y = main_bottom + 26
    strip_h = 62
    box_w = (W - 2 * MARGIN - 5 * 8) // 6
    for i, (num, label) in enumerate(NUMBERS):
        x = MARGIN + i * (box_w + 8)
        d.rectangle([x, strip_y, x + box_w, strip_y + strip_h], fill=BOX_BG, outline=LIGHT)
        nf = font(SANS_B, 18)
        d.text((x + 8, strip_y + 6), num, font=nf, fill=RED)
        record(x + 8, strip_y + 6, x + 8 + d.textlength(num, font=nf), strip_y + 24, f"num-{i}")
        lf = font(SANS, 10)
        y = draw_wrapped(d, x + 8, strip_y + 28, box_w - 16, label, lf, INK, spacing=1, max_lines=2)
        assert y <= strip_y + strip_h - 2, f"number box {i} too tall"
        record(x + 8, strip_y + 28, x + box_w - 8, y, f"num-label-{i}")
    numbers_bottom = strip_y + strip_h  # 734

    # ---- Briefs: 2 columns, one line each (auto-fit font) ----
    d.text((MARGIN, numbers_bottom + 8), "IN BRIEF \u2014 23 MORE", font=sec_f, fill=INK)
    record(MARGIN, numbers_bottom + 8, MARGIN + 170, numbers_bottom + 20, "briefs-header")
    brief_y = numbers_bottom + 30
    brief_col_w = 474
    brief_x = [MARGIN, MARGIN + brief_col_w + 20]
    left = BRIEFS[:12]
    right = BRIEFS[12:]
    for ci, col in enumerate((left, right)):
        x = brief_x[ci]
        y = brief_y
        for bi, (tag, text) in enumerate(col):
            full = f"\u2022 {tag} \u2014 {text}"
            # shrink until it fits on one line
            size = 11
            bf = font(SANS, size)
            while d.textlength(full, font=bf) > brief_col_w and size > 8:
                size -= 1
                bf = font(SANS, size)
            assert d.textlength(full, font=bf) <= brief_col_w, f"brief too long: {full!r}"
            # bold tag part: draw tag in bold by overlaying the tag segment
            d.text((x, y), full, font=bf, fill=INK)
            record(x, y, x + brief_col_w, y + size, f"brief-{ci}-{bi}")
            y += 18
        assert y <= 985, f"briefs column {ci} too tall: {y}"

    # ---- Footer ----
    d.line([(MARGIN, 988), (W - MARGIN, 988)], fill=RULE, width=1)
    ff = font(SANS, 10)
    foot = "All stories happened or were first reported on 23 November 2026."
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 996), foot, font=ff, fill=MUTED)
    record((W - fw) / 2, 996, (W + fw) / 2, 1006, "footer")

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()

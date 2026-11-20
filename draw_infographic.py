#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page (1024x1024 PNG).

Fresh layout for the news-image-20261120 entry: a newspaper front page
with one lead story, four panels and an ALSO TODAY strip. All facts were
verified against live reporting on 20 Nov 2026 (Reuters, WSJ, AFP, AP).
Run: python3 draw_infographic.py [out.png]  (default: entry.png)
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 238)
INK = (26, 26, 26)
RED = (179, 39, 30)
BLUE = (31, 78, 121)
GREY = (110, 108, 100)
PANEL_BG = (255, 255, 255)
RULE = (26, 26, 26)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, fill=RULE, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 40  # margin
    CW = W - 2 * M  # content width = 944

    # ---------- masthead ----------
    y = 30
    f_mast = font(SERIF, 64)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, y), title, font=f_mast, fill=INK)
    y += 78
    hline(d, M, W - M, y, width=4)
    y += 10
    f_date = font(SANS_B, 26)
    date = "FRIDAY, 20 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, y), date, font=f_date, fill=RED)
    y += 36
    f_sub = font(SANS, 19)
    sub = "The day's world news in one image  ·  Shenzhen  ·  The Hague  ·  New York  ·  Riyadh"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, y), sub, font=f_sub, fill=GREY)
    y += 30
    hline(d, M, W - M, y, width=4)
    y += 16

    # ---------- lead story ----------
    f_kick = font(SANS_B, 20)
    d.text((M, y), "LEAD  —  SHENZHEN, CHINA", font=f_kick, fill=RED)
    y += 28
    f_lead = font(SERIF, 46)
    lead = "PEACE DECLARATION"
    d.text((M, y), lead, font=f_lead, fill=INK)
    y += 56
    f_lead_sub = font(SERIF, 25)
    sub_lines = wrap(
        d,
        "Trump, Xi and Putin sign a four-point pact after the first-ever "
        "three-way summit — with Ukraine first on the agenda.",
        f_lead_sub, CW)
    y = draw_lines(d, sub_lines, M, y, f_lead_sub, INK, 32)
    y += 10
    # three leader dots: US / CHINA / RUSSIA
    dot_y = y + 8
    cols = [(31, 78, 121), (179, 39, 30), (90, 90, 90)]
    labels = ["UNITED STATES", "CHINA", "RUSSIA"]
    dx = M
    for c, lab in zip(cols, labels):
        d.ellipse([dx, dot_y, dx + 26, dot_y + 26], fill=c)
        d.text((dx + 34, dot_y + 2), lab, font=font(SANS_B, 19), fill=INK)
        dx += 34 + d.textlength(lab, font=font(SANS_B, 19)) + 44
    y = dot_y + 40
    hline(d, M, W - M, y, width=2)
    y += 14

    # ---------- four panels, 2 x 2 ----------
    gap = 16
    pw = (CW - gap) // 2
    ph = 168
    panels = [
        ("COURT: GENOCIDE", RED,
         "ICJ rules 9–6 that Myanmar committed genocide against the "
         "Rohingya — the first state ever held responsible. About 10,000 "
         "killed in 2017; 700,000 fled."),
        ("ANTHROPIC SOARS", BLUE,
         "Shares close up 17% at about $97 on their Nasdaq debut, after "
         "pricing at $83. The $81.3bn raise is the biggest IPO ever."),
        ("RIYADH TOWER HIT", RED,
         "A Houthi missile damages Riyadh's tallest tower, the PIF "
         "headquarters. The Gulf war widens as Iran hits tankers in Hormuz."),
        ("MARKETS SLIDE", BLUE,
         "S&P 500 falls 2.0% for a fifth straight loss and the Nikkei "
         "drops 4.7%, as investors fret over AI valuations."),
    ]
    f_ph = font(SANS_B, 24)
    f_pb = font(SANS, 20)
    py = y
    for i, (head, accent, body) in enumerate(panels):
        col = i % 2
        row = i // 2
        x0 = M + col * (pw + gap)
        y0 = py + row * (ph + gap)
        d.rectangle([x0, y0, x0 + pw, y0 + ph], fill=PANEL_BG,
                    outline=(200, 196, 186), width=1)
        d.rectangle([x0, y0, x0 + pw, y0 + 6], fill=accent)
        d.text((x0 + 14, y0 + 16), head, font=f_ph, fill=accent)
        blines = wrap(d, body, f_pb, pw - 28)
        draw_lines(d, blines, x0 + 14, y0 + 50, f_pb, INK, 25)
    y = py + 2 * ph + gap
    y += 12
    hline(d, M, W - M, y, width=2)
    y += 12

    # ---------- ALSO TODAY strip ----------
    f_at = font(SANS_B, 20)
    d.text((M, y), "ALSO TODAY", font=f_at, fill=RED)
    y += 28
    f_ai = font(SANS, 17)
    items = [
        "Kyiv hit by 4 ballistic missiles",
        "Genoa airport halts flights (drones)",
        "COP31 climate talks end in Antalya",
        "India evacuates 80,000 (Storm Dana)",
        "Israel ends Gaza ground operation",
        "EU proposes €45bn loan for Ukraine",
    ]
    col_w = CW // 3
    for i, item in enumerate(items):
        col = i % 3
        row = i // 3
        x0 = M + col * col_w
        y0 = y + row * 52
        lines = wrap(d, "•  " + item, f_ai, col_w - 18)
        draw_lines(d, lines, x0, y0, f_ai, INK, 21)
    y += 2 * 52 + 8
    hline(d, M, W - M, y, width=2)
    y += 10

    # ---------- footer ----------
    f_ft = font(SANS, 16)
    foot = "Sources: Reuters · The Wall Street Journal · AFP · AP  —  20 November 2026"
    fw = d.textlength(foot, font=f_ft)
    d.text(((W - fw) / 2, y), foot, font=f_ft, fill=GREY)

    img.save(out, "PNG")
    print(f"wrote {out} ({W}x{H})")


if __name__ == "__main__":
    main()

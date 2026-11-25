#!/usr/bin/env python3
"""Render the 25 Nov 2026 world-news infographic (1024x1024 PNG).

Deterministic: no network, no randomness, no timestamps.
Run: python3 build_image.py  -> writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W, H = 1024, 1024
PAPER = (248, 244, 238)
NAVY = (18, 32, 62)
GOLD = (201, 138, 16)
CARD = (255, 255, 255)
INK = (22, 22, 22)
MUTED = (96, 96, 96)
LINE = (205, 198, 188)
ACCENTS = [(178, 34, 34), (25, 90, 140), (90, 60, 140), (20, 110, 70), (150, 80, 20)]

def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_MAST = font("DejaVuSans-Bold.ttf", 54)
F_DATE = font("DejaVuSans-Bold.ttf", 26)
F_LEAD = font("DejaVuSans-Bold.ttf", 40)
F_HEAD = font("DejaVuSans-Bold.ttf", 30)
F_BODY = font("DejaVuSans.ttf", 22)
F_TAG = font("DejaVuSans-Bold.ttf", 19)
F_FOOT = font("DejaVuSans.ttf", 19)

def wrap(text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_icon(d, kind, cx, cy, r, col):
    if kind == "ship":
        d.polygon([(cx - r, cy + 6), (cx + r, cy + 6), (cx + r - 8, cy + r - 4),
                   (cx - r + 8, cy + r - 4)], fill=col)
        d.rectangle([cx - 4, cy - r + 6, cx + 4, cy + 2], fill=col)
        d.polygon([(cx + 4, cy - r + 6), (cx + 22, cy - 2), (cx + 4, cy - 2)], fill=col)
        d.arc([cx - r - 6, cy - r - 14, cx + r + 6, cy + r - 2], 200, 340, fill=col, width=4)
    elif kind == "tower":
        d.polygon([(cx - 12, cy + r), (cx - 8, cy - r + 4), (cx + 8, cy - r + 4),
                   (cx + 12, cy + r)], fill=col)
        d.rectangle([cx - 20, cy + r - 8, cx + 20, cy + r], fill=col)
        d.ellipse([cx - 3, cy - r - 6, cx + 3, cy - r], fill=col)
        for dx in (-26, 26):
            d.line([cx + dx, cy - 6, cx + dx + 6, cy + 2], fill=col, width=3)
    elif kind == "chip":
        d.rectangle([cx - 16, cy - 16, cx + 16, cy + 16], outline=col, width=5)
        d.rectangle([cx - 7, cy - 7, cx + 7, cy + 7], fill=col)
        for i in (-1, 0, 1):
            d.line([cx + i * 11, cy - 26, cx + i * 11, cy - 16], fill=col, width=3)
            d.line([cx + i * 11, cy + 16, cx + i * 11, cy + 26], fill=col, width=3)
            d.line([cx - 26, cy + i * 11, cx - 16, cy + i * 11], fill=col, width=3)
            d.line([cx + 16, cy + i * 11, cx + 26, cy + i * 11], fill=col, width=3)
    elif kind == "radar":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=4)
        d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2], outline=col, width=3)
        d.line([cx, cy, cx + r - 6, cy - r + 12], fill=col, width=4)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=col)
    elif kind == "ribbon":
        d.polygon([(cx, cy - r), (cx + 12, cy - 6), (cx + 6, cy + r),
                   (cx, cy + r - 12), (cx - 6, cy + r), (cx - 12, cy - 6)], fill=col)
        d.ellipse([cx - 10, cy - r - 2, cx + 10, cy - r + 14], outline=col, width=4)

STORIES = [
    ("LEAD  •  UKRAINE–RUSSIA", "ship",
     "Ukraine confirms drone strike on Russian ship",
     "President Zelenskiy says Kyiv hit a Russian cargo ship in the Gulf of Finland; ally Norway urges caution as the war at sea escalates."),
    ("MIDDLE EAST", "tower",
     "Houthi strike hits Riyadh's tallest tower",
     "Saudi civil defence says 11 people were wounded in a drone attack on a tower in Riyadh, as Yemen's war spills deeper into the Gulf."),
    ("TECH  •  US COURT", "chip",
     "Huawei convicted in sprawling US trial",
     "A US jury finds China's Huawei guilty over its Iran business and trade secrets, in one of the biggest corporate criminal cases in years."),
    ("EUROPE  •  NATO", "radar",
     "NATO to send early-warning jets to Poland",
     "The alliance plans to deploy surveillance aircraft after missiles landed in Poland during an attack on Ukraine."),
    ("WORLD  •  25 NOVEMBER", "ribbon",
     "Day against violence towards women",
     "25 November marks the International Day for the Elimination of Violence against Women, observed around the world."),
]

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.rectangle([0, 0, W, 118], fill=NAVY)
d.text((36, 22), "THE WORLD IN ONE IMAGE", font=F_MAST, fill=(255, 255, 255))
d.text((36, 82), "WEDNESDAY  •  25 NOVEMBER 2026", font=F_DATE, fill=GOLD)
d.rectangle([0, 118, W, 124], fill=GOLD)

# ---- lead story ----
x0, y0, x1, y1 = 28, 144, 996, 400
d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=CARD, outline=LINE, width=2)
d.rounded_rectangle([x0, y0, x0 + 14, y1], radius=7, fill=ACCENTS[0])
tag, kind, head, body = STORIES[0]
d.text((x0 + 110, y0 + 18), tag, font=F_TAG, fill=ACCENTS[0])
draw_icon(d, kind, x0 + 62, y0 + 62, 30, ACCENTS[0])
for i, ln in enumerate(wrap(head, F_LEAD, x1 - x0 - 60)):
    d.text((x0 + 30, y0 + 52 + i * 48), ln, font=F_LEAD, fill=INK)
for i, ln in enumerate(wrap(body, F_BODY, x1 - x0 - 60)):
    d.text((x0 + 30, y0 + 158 + i * 30), ln, font=F_BODY, fill=MUTED)

# ---- four smaller stories, 2x2 grid ----
gx, gy, gw, gh, gap = 28, 420, 474, 268, 20
for idx, (tag, kind, head, body) in enumerate(STORIES[1:]):
    col, row = idx % 2, idx // 2
    bx = gx + col * (gw + gap)
    by = gy + row * (gh + gap)
    acc = ACCENTS[idx + 1]
    d.rounded_rectangle([bx, by, bx + gw, by + gh], radius=14, fill=CARD, outline=LINE, width=2)
    d.rounded_rectangle([bx, by, bx + gw, by + 8], radius=7, fill=acc)
    d.text((bx + 96, by + 22), tag, font=F_TAG, fill=acc)
    draw_icon(d, kind, bx + 56, by + 58, 26, acc)
    y = by + 62
    for ln in wrap(head, F_HEAD, gw - 36):
        d.text((bx + 18, y), ln, font=F_HEAD, fill=INK)
        y += 36
    y += 6
    for ln in wrap(body, F_BODY, gw - 36):
        d.text((bx + 18, y), ln, font=F_BODY, fill=MUTED)
        y += 28

# ---- footer ----
d.line([28, 982, 996, 982], fill=LINE, width=2)
d.text((28, 990), "Sources: Reuters, Jagran Josh, Newsmriti, HuddleWorld — public news search, 25 Nov 2026.",
       font=F_FOOT, fill=MUTED)

img.save(os.path.join(HERE, "entry.png"))
print("wrote entry.png", img.size)

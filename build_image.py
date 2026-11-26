#!/usr/bin/env python3
"""Draw the 25 Nov 2026 world-news front page as a 1024x1024 PNG.

Everything is fixed: no network, no random numbers, no clock. Running
it twice gives the same bytes both times.

Usage:
    python3 build_image.py   # writes entry.png next to this file
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = "/usr/share/fonts/truetype/dejavu"

# Page size.
PAGE_W, PAGE_H = 1024, 1024

# Colours.
BACKGROUND = (248, 244, 238)  # warm off-white page
MASTHEAD_BG = (18, 32, 62)    # dark navy banner
RULE_GOLD = (201, 138, 16)    # gold rule and date line
CARD_BG = (255, 255, 255)     # white story card
HEADLINE = (22, 22, 22)       # headline text
BODY_GREY = (96, 96, 96)      # body text
BORDER = (205, 198, 188)      # card edges and footer rule
STORY_COLORS = [
    (178, 34, 34),   # lead: red
    (25, 90, 140),   # middle east: blue
    (90, 60, 140),   # tech: purple
    (20, 110, 70),   # europe: green
    (150, 80, 20),   # world: ochre
]


def font_at(filename, size):
    """Fetch one DejaVu face at the given point size."""
    return ImageFont.truetype(os.path.join(FONTS, filename), size)


TITLE_FONT = font_at("DejaVuSans-Bold.ttf", 54)
DATE_FONT = font_at("DejaVuSans-Bold.ttf", 26)
LEAD_FONT = font_at("DejaVuSans-Bold.ttf", 40)
HEAD_FONT = font_at("DejaVuSans-Bold.ttf", 30)
TEXT_FONT = font_at("DejaVuSans.ttf", 22)
TAG_FONT = font_at("DejaVuSans-Bold.ttf", 19)
FOOT_FONT = font_at("DejaVuSans.ttf", 19)


def wrap(line, font, limit):
    """Break `line` into as few lines as fit inside `limit` pixels."""
    words = line.split()
    out = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if font.getlength(trial) <= limit:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def _draw_ship(pen, cx, cy, r, colour):
    """Cargo ship: hull, mast, sail, wave arc below."""
    pen.polygon(
        [(cx - r, cy + 6), (cx + r, cy + 6),
         (cx + r - 8, cy + r - 4), (cx - r + 8, cy + r - 4)],
        fill=colour,
    )
    pen.rectangle([cx - 4, cy - r + 6, cx + 4, cy + 2], fill=colour)
    pen.polygon(
        [(cx + 4, cy - r + 6), (cx + 22, cy - 2), (cx + 4, cy - 2)],
        fill=colour,
    )
    pen.arc(
        [cx - r - 6, cy - r - 14, cx + r + 6, cy + r - 2],
        200, 340, fill=colour, width=4,
    )


def _draw_tower(pen, cx, cy, r, colour):
    """Tall tower with a beacon dot and signal marks at the sides."""
    pen.polygon(
        [(cx - 12, cy + r), (cx - 8, cy - r + 4),
         (cx + 8, cy - r + 4), (cx + 12, cy + r)],
        fill=colour,
    )
    pen.rectangle([cx - 20, cy + r - 8, cx + 20, cy + r], fill=colour)
    pen.ellipse([cx - 3, cy - r - 6, cx + 3, cy - r], fill=colour)
    for dx in (-26, 26):
        pen.line([cx + dx, cy - 6, cx + dx + 6, cy + 2],
                 fill=colour, width=3)


def _draw_chip(pen, cx, cy, r, colour):
    """Microchip: square outline, inner die, pins on every side."""
    pen.rectangle(
        [cx - 16, cy - 16, cx + 16, cy + 16], outline=colour, width=5,
    )
    pen.rectangle([cx - 7, cy - 7, cx + 7, cy + 7], fill=colour)
    for i in (-1, 0, 1):
        pen.line([cx + i * 11, cy - 26, cx + i * 11, cy - 16],
                 fill=colour, width=3)
        pen.line([cx + i * 11, cy + 16, cx + i * 11, cy + 26],
                 fill=colour, width=3)
        pen.line([cx - 26, cy + i * 11, cx - 16, cy + i * 11],
                 fill=colour, width=3)
        pen.line([cx + 16, cy + i * 11, cx + 26, cy + i * 11],
                 fill=colour, width=3)


def _draw_radar(pen, cx, cy, r, colour):
    """Radar screen: two rings, a sweep arm, a blip in the middle."""
    pen.ellipse(
        [cx - r, cy - r, cx + r, cy + r], outline=colour, width=4,
    )
    half = r // 2
    pen.ellipse(
        [cx - half, cy - half, cx + half, cy + half],
        outline=colour, width=3,
    )
    pen.line([cx, cy, cx + r - 6, cy - r + 12], fill=colour, width=4)
    pen.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=colour)


def _draw_ribbon(pen, cx, cy, r, colour):
    """Awareness ribbon, looped at the top."""
    pen.polygon(
        [(cx, cy - r), (cx + 12, cy - 6), (cx + 6, cy + r),
         (cx, cy + r - 12), (cx - 6, cy + r), (cx - 12, cy - 6)],
        fill=colour,
    )
    pen.ellipse(
        [cx - 10, cy - r - 2, cx + 10, cy - r + 14],
        outline=colour, width=4,
    )


ICON_DRAWERS = {
    "ship": _draw_ship,
    "tower": _draw_tower,
    "chip": _draw_chip,
    "radar": _draw_radar,
    "ribbon": _draw_ribbon,
}


def draw_icon(pen, kind, cx, cy, r, colour):
    """Draw the pictogram for `kind`, centred at (cx, cy)."""
    ICON_DRAWERS[kind](pen, cx, cy, r, colour)


# (tag, icon, headline, body) — five stories from 25 Nov 2026.
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


def render():
    """Lay out the front page and hand back the finished PIL image."""
    img = Image.new("RGB", (PAGE_W, PAGE_H), BACKGROUND)
    pen = ImageDraw.Draw(img)

    # ---- masthead ----
    pen.rectangle([0, 0, PAGE_W, 118], fill=MASTHEAD_BG)
    pen.text((36, 22), "THE WORLD IN ONE IMAGE",
             font=TITLE_FONT, fill=(255, 255, 255))
    pen.text((36, 82), "WEDNESDAY  •  25 NOVEMBER 2026",
             font=DATE_FONT, fill=RULE_GOLD)
    pen.rectangle([0, 118, PAGE_W, 124], fill=RULE_GOLD)

    # ---- lead story (full-width card) ----
    x0, y0, x1, y1 = 28, 144, 996, 400
    pen.rounded_rectangle([x0, y0, x1, y1], radius=14,
                          fill=CARD_BG, outline=BORDER, width=2)
    pen.rounded_rectangle([x0, y0, x0 + 14, y1], radius=7,
                          fill=STORY_COLORS[0])
    tag, kind, head, body = STORIES[0]
    pen.text((x0 + 110, y0 + 18), tag, font=TAG_FONT, fill=STORY_COLORS[0])
    draw_icon(pen, kind, x0 + 62, y0 + 62, 30, STORY_COLORS[0])
    for i, line in enumerate(wrap(head, LEAD_FONT, x1 - x0 - 60)):
        pen.text((x0 + 30, y0 + 52 + i * 48), line,
                 font=LEAD_FONT, fill=HEADLINE)
    for i, line in enumerate(wrap(body, TEXT_FONT, x1 - x0 - 60)):
        pen.text((x0 + 30, y0 + 158 + i * 30), line,
                 font=TEXT_FONT, fill=BODY_GREY)

    # ---- four smaller stories in a 2x2 grid ----
    gx, gy, gw, gh, gap = 28, 420, 474, 268, 20
    for idx, (tag, kind, head, body) in enumerate(STORIES[1:]):
        col, row = idx % 2, idx // 2
        bx = gx + col * (gw + gap)
        by = gy + row * (gh + gap)
        accent = STORY_COLORS[idx + 1]
        pen.rounded_rectangle([bx, by, bx + gw, by + gh], radius=14,
                              fill=CARD_BG, outline=BORDER, width=2)
        pen.rounded_rectangle([bx, by, bx + gw, by + 8], radius=7, fill=accent)
        pen.text((bx + 96, by + 22), tag, font=TAG_FONT, fill=accent)
        draw_icon(pen, kind, bx + 56, by + 58, 26, accent)
        y = by + 62
        for line in wrap(head, HEAD_FONT, gw - 36):
            pen.text((bx + 18, y), line, font=HEAD_FONT, fill=HEADLINE)
            y += 36
        y += 6
        for line in wrap(body, TEXT_FONT, gw - 36):
            pen.text((bx + 18, y), line, font=TEXT_FONT, fill=BODY_GREY)
            y += 28

    # ---- footer ----
    pen.line([28, 982, 996, 982], fill=BORDER, width=2)
    pen.text(
        (28, 990),
        "Sources: Reuters, Jagran Josh, Newsmriti, HuddleWorld — "
        "public news search, 25 Nov 2026.",
        font=FOOT_FONT, fill=BODY_GREY,
    )
    return img


if __name__ == "__main__":
    image = render()
    image.save(os.path.join(HERE, "entry.png"))
    print("wrote entry.png", image.size)

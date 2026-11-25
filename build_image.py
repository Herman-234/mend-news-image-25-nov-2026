#!/usr/bin/env python3
"""Render the 25 Nov 2026 world-news infographic as a 1024x1024 PNG.

No network access, no randomness, no timestamps: running this script
twice produces a byte-identical image.

Usage:
    python3 build_image.py   # writes entry.png next to this file
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

# Canvas size.
WIDTH, HEIGHT = 1024, 1024

# Palette.
PAPER = (248, 244, 238)   # warm off-white page
NAVY = (18, 32, 62)       # masthead background
GOLD = (201, 138, 16)     # masthead rule and date line
CARD = (255, 255, 255)    # story card background
INK = (22, 22, 22)        # headlines
MUTED = (96, 96, 96)      # body copy
RULE = (205, 198, 188)    # card outlines and footer rule
ACCENTS = [
    (178, 34, 34),   # lead story: red
    (25, 90, 140),   # middle east: blue
    (90, 60, 140),   # tech: purple
    (20, 110, 70),   # europe: green
    (150, 80, 20),   # world: ochre
]


def load_font(filename, size):
    """Load a DejaVu font from the system font directory."""
    return ImageFont.truetype(os.path.join(FONT_DIR, filename), size)


FONT_MASTHEAD = load_font("DejaVuSans-Bold.ttf", 54)
FONT_DATE = load_font("DejaVuSans-Bold.ttf", 26)
FONT_LEAD_HEAD = load_font("DejaVuSans-Bold.ttf", 40)
FONT_HEAD = load_font("DejaVuSans-Bold.ttf", 30)
FONT_BODY = load_font("DejaVuSans.ttf", 22)
FONT_TAG = load_font("DejaVuSans-Bold.ttf", 19)
FONT_FOOTER = load_font("DejaVuSans.ttf", 19)


def wrap_text(text, font, max_width):
    """Greedy word-wrap: split `text` into lines fitting `max_width`."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = (current + " " + word).strip()
        if font.getlength(candidate) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _icon_ship(draw, cx, cy, radius, colour):
    """Cargo ship: hull, mast, sail and a wave arc underneath."""
    draw.polygon(
        [(cx - radius, cy + 6), (cx + radius, cy + 6),
         (cx + radius - 8, cy + radius - 4),
         (cx - radius + 8, cy + radius - 4)],
        fill=colour,
    )
    draw.rectangle([cx - 4, cy - radius + 6, cx + 4, cy + 2], fill=colour)
    draw.polygon(
        [(cx + 4, cy - radius + 6), (cx + 22, cy - 2), (cx + 4, cy - 2)],
        fill=colour,
    )
    draw.arc(
        [cx - radius - 6, cy - radius - 14, cx + radius + 6, cy + radius - 2],
        200, 340, fill=colour, width=4,
    )


def _icon_tower(draw, cx, cy, radius, colour):
    """Tall tower with a beacon dot and signal marks on the sides."""
    draw.polygon(
        [(cx - 12, cy + radius), (cx - 8, cy - radius + 4),
         (cx + 8, cy - radius + 4), (cx + 12, cy + radius)],
        fill=colour,
    )
    draw.rectangle([cx - 20, cy + radius - 8, cx + 20, cy + radius], fill=colour)
    draw.ellipse([cx - 3, cy - radius - 6, cx + 3, cy - radius], fill=colour)
    for dx in (-26, 26):
        draw.line([cx + dx, cy - 6, cx + dx + 6, cy + 2], fill=colour, width=3)


def _icon_chip(draw, cx, cy, radius, colour):
    """Microchip: square outline, inner die and pins on all sides."""
    draw.rectangle(
        [cx - 16, cy - 16, cx + 16, cy + 16], outline=colour, width=5,
    )
    draw.rectangle([cx - 7, cy - 7, cx + 7, cy + 7], fill=colour)
    for i in (-1, 0, 1):
        draw.line([cx + i * 11, cy - 26, cx + i * 11, cy - 16],
                  fill=colour, width=3)
        draw.line([cx + i * 11, cy + 16, cx + i * 11, cy + 26],
                  fill=colour, width=3)
        draw.line([cx - 26, cy + i * 11, cx - 16, cy + i * 11],
                  fill=colour, width=3)
        draw.line([cx + 16, cy + i * 11, cx + 26, cy + i * 11],
                  fill=colour, width=3)


def _icon_radar(draw, cx, cy, radius, colour):
    """Radar screen: two rings, a sweep arm and a centre blip."""
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        outline=colour, width=4,
    )
    half = radius // 2
    draw.ellipse(
        [cx - half, cy - half, cx + half, cy + half],
        outline=colour, width=3,
    )
    draw.line([cx, cy, cx + radius - 6, cy - radius + 12],
              fill=colour, width=4)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=colour)


def _icon_ribbon(draw, cx, cy, radius, colour):
    """Awareness ribbon with a loop at the top."""
    draw.polygon(
        [(cx, cy - radius), (cx + 12, cy - 6), (cx + 6, cy + radius),
         (cx, cy + radius - 12), (cx - 6, cy + radius), (cx - 12, cy - 6)],
        fill=colour,
    )
    draw.ellipse(
        [cx - 10, cy - radius - 2, cx + 10, cy - radius + 14],
        outline=colour, width=4,
    )


ICONS = {
    "ship": _icon_ship,
    "tower": _icon_tower,
    "chip": _icon_chip,
    "radar": _icon_radar,
    "ribbon": _icon_ribbon,
}


def draw_icon(draw, kind, cx, cy, radius, colour):
    """Draw the pictogram named by `kind`, centred at (cx, cy)."""
    ICONS[kind](draw, cx, cy, radius, colour)


# (tag, icon kind, headline, body) — the five stories of 25 Nov 2026.
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
    """Compose the front-page infographic and return the PIL image."""
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- masthead ----
    draw.rectangle([0, 0, WIDTH, 118], fill=NAVY)
    draw.text((36, 22), "THE WORLD IN ONE IMAGE",
              font=FONT_MASTHEAD, fill=(255, 255, 255))
    draw.text((36, 82), "WEDNESDAY  •  25 NOVEMBER 2026",
              font=FONT_DATE, fill=GOLD)
    draw.rectangle([0, 118, WIDTH, 124], fill=GOLD)

    # ---- lead story (full-width card) ----
    x0, y0, x1, y1 = 28, 144, 996, 400
    draw.rounded_rectangle([x0, y0, x1, y1], radius=14,
                           fill=CARD, outline=RULE, width=2)
    draw.rounded_rectangle([x0, y0, x0 + 14, y1], radius=7, fill=ACCENTS[0])
    tag, kind, head, body = STORIES[0]
    draw.text((x0 + 110, y0 + 18), tag, font=FONT_TAG, fill=ACCENTS[0])
    draw_icon(draw, kind, x0 + 62, y0 + 62, 30, ACCENTS[0])
    for i, line in enumerate(wrap_text(head, FONT_LEAD_HEAD, x1 - x0 - 60)):
        draw.text((x0 + 30, y0 + 52 + i * 48), line,
                  font=FONT_LEAD_HEAD, fill=INK)
    for i, line in enumerate(wrap_text(body, FONT_BODY, x1 - x0 - 60)):
        draw.text((x0 + 30, y0 + 158 + i * 30), line,
                  font=FONT_BODY, fill=MUTED)

    # ---- four smaller stories in a 2x2 grid ----
    gx, gy, gw, gh, gap = 28, 420, 474, 268, 20
    for idx, (tag, kind, head, body) in enumerate(STORIES[1:]):
        col, row = idx % 2, idx // 2
        bx = gx + col * (gw + gap)
        by = gy + row * (gh + gap)
        accent = ACCENTS[idx + 1]
        draw.rounded_rectangle([bx, by, bx + gw, by + gh], radius=14,
                               fill=CARD, outline=RULE, width=2)
        draw.rounded_rectangle([bx, by, bx + gw, by + 8], radius=7, fill=accent)
        draw.text((bx + 96, by + 22), tag, font=FONT_TAG, fill=accent)
        draw_icon(draw, kind, bx + 56, by + 58, 26, accent)
        y = by + 62
        for line in wrap_text(head, FONT_HEAD, gw - 36):
            draw.text((bx + 18, y), line, font=FONT_HEAD, fill=INK)
            y += 36
        y += 6
        for line in wrap_text(body, FONT_BODY, gw - 36):
            draw.text((bx + 18, y), line, font=FONT_BODY, fill=MUTED)
            y += 28

    # ---- footer ----
    draw.line([28, 982, 996, 982], fill=RULE, width=2)
    draw.text(
        (28, 990),
        "Sources: Reuters, Jagran Josh, Newsmriti, HuddleWorld — "
        "public news search, 25 Nov 2026.",
        font=FONT_FOOTER, fill=MUTED,
    )
    return img


if __name__ == "__main__":
    image = render()
    image.save(os.path.join(HERE, "entry.png"))
    print("wrote entry.png", image.size)

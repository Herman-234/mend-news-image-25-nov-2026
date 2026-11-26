#!/usr/bin/env python3
"""Paint the 25 November 2026 world-news front page, 1024x1024.

One image, five stories, drawn with Pillow from fixed numbers only: no
network, no clock, no dice. Run it twice and the bytes come out identical.

Usage:
    python3 build_image.py   # writes entry.png beside this file
"""

import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W, H = 1024, 1024

# Palette.
PAPER = (248, 244, 238)      # warm off-white page
NAVY = (18, 32, 62)          # masthead
GOLD = (201, 138, 16)        # date line and rules
CARD = (255, 255, 255)       # story cards
INK = (22, 22, 22)           # headlines
GREY = (96, 96, 96)          # body copy
EDGE = (205, 198, 188)       # card borders and footer rule

ACCENTS = [
    (178, 34, 34),   # lead story: red
    (25, 90, 140),   # middle east: blue
    (90, 60, 140),   # tech: purple
    (20, 110, 70),   # europe: green
    (150, 80, 20),   # world: ochre
]


def face(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = face("DejaVuSans-Bold.ttf", 54)
F_DATE = face("DejaVuSans-Bold.ttf", 26)
F_LEAD = face("DejaVuSans-Bold.ttf", 40)
F_HEAD = face("DejaVuSans-Bold.ttf", 30)
F_BODY = face("DejaVuSans.ttf", 22)
F_TAG = face("DejaVuSans-Bold.ttf", 19)
F_FOOT = face("DejaVuSans.ttf", 19)


def split_lines(text, font, max_px):
    """Chop text into the fewest lines that fit inside max_px."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if font.getlength(trial) <= max_px:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# The five stories of the day: (kicker, pictogram, headline, standfirst).
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


def paint_ship(d, cx, cy, s, colour):
    """Little cargo ship: hull, cabin mast, sail, and a wave under it."""
    d.polygon([(cx - s, cy + 4), (cx + s, cy + 4),
               (cx + s - 6, cy + s - 4), (cx - s + 6, cy + s - 4)],
              fill=colour)
    d.rectangle([cx - 3, cy - s + 4, cx + 3, cy], fill=colour)
    d.polygon([(cx + 3, cy - s + 4), (cx + 18, cy - 2), (cx + 3, cy - 2)],
              fill=colour)
    d.arc([cx - s - 5, cy - s - 10, cx + s + 5, cy + s - 2],
          200, 340, fill=colour, width=4)


def paint_tower(d, cx, cy, s, colour):
    """Broadcast tower with a beacon on top and signal ticks at the sides."""
    d.polygon([(cx - 10, cy + s), (cx - 7, cy - s + 4),
               (cx + 7, cy - s + 4), (cx + 10, cy + s)], fill=colour)
    d.rectangle([cx - 17, cy + s - 7, cx + 17, cy + s], fill=colour)
    d.ellipse([cx - 3, cy - s - 5, cx + 3, cy - s + 1], fill=colour)
    for dx in (-22, 22):
        d.line([cx + dx, cy - 5, cx + dx + 5, cy + 2], fill=colour, width=3)


def paint_chip(d, cx, cy, s, colour):
    """Microchip: outer square, inner die, pins sticking out each side."""
    d.rectangle([cx - 14, cy - 14, cx + 14, cy + 14],
                outline=colour, width=5)
    d.rectangle([cx - 6, cy - 6, cx + 6, cy + 6], fill=colour)
    for off in (-9, 0, 9):
        d.line([cx + off, cy - 22, cx + off, cy - 14], fill=colour, width=3)
        d.line([cx + off, cy + 14, cx + off, cy + 22], fill=colour, width=3)
        d.line([cx - 22, cy + off, cx - 14, cy + off], fill=colour, width=3)
        d.line([cx + 14, cy + off, cx + 22, cy + off], fill=colour, width=3)


def paint_radar(d, cx, cy, s, colour):
    """Radar screen: outer ring, inner ring, sweep arm, centre blip."""
    d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=colour, width=4)
    half = s // 2
    d.ellipse([cx - half, cy - half, cx + half, cy + half],
              outline=colour, width=3)
    d.line([cx, cy, cx + s - 5, cy - s + 10], fill=colour, width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=colour)


def paint_ribbon(d, cx, cy, s, colour):
    """Awareness ribbon with its loop at the top."""
    d.polygon([(cx, cy - s), (cx + 10, cy - 5), (cx + 5, cy + s),
               (cx, cy + s - 10), (cx - 5, cy + s), (cx - 10, cy - 5)],
              fill=colour)
    d.ellipse([cx - 9, cy - s - 2, cx + 9, cy - s + 12],
              outline=colour, width=4)


PICTOGRAMS = {
    "ship": paint_ship,
    "tower": paint_tower,
    "chip": paint_chip,
    "radar": paint_radar,
    "ribbon": paint_ribbon,
}


def build_page():
    """Compose the whole front page and return the finished image."""
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # Masthead.
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((36, 22), "THE WORLD IN ONE IMAGE", font=F_TITLE, fill=(255, 255, 255))
    d.text((36, 82), "WEDNESDAY  •  25 NOVEMBER 2026", font=F_DATE, fill=GOLD)
    d.rectangle([0, 118, W, 124], fill=GOLD)

    # Lead story, full width.
    lx0, ly0, lx1, ly1 = 28, 144, 996, 400
    lead_colour = ACCENTS[0]
    d.rounded_rectangle([lx0, ly0, lx1, ly1], radius=14,
                        fill=CARD, outline=EDGE, width=2)
    d.rounded_rectangle([lx0, ly0, lx0 + 14, ly1], radius=7, fill=lead_colour)
    kicker, kind, headline, standfirst = STORIES[0]
    PICTOGRAMS[kind](d, lx0 + 62, ly0 + 62, 30, lead_colour)
    d.text((lx0 + 110, ly0 + 18), kicker, font=F_TAG, fill=lead_colour)
    y = ly0 + 52
    for line in split_lines(headline, F_LEAD, lx1 - lx0 - 60):
        d.text((lx0 + 30, y), line, font=F_LEAD, fill=INK)
        y += 48
    y = ly0 + 158
    for line in split_lines(standfirst, F_BODY, lx1 - lx0 - 60):
        d.text((lx0 + 30, y), line, font=F_BODY, fill=GREY)
        y += 30

    # The other four stories, two by two.
    gx, gy, gw, gh, gap = 28, 420, 474, 268, 20
    for pos, (kicker, kind, headline, standfirst) in enumerate(STORIES[1:]):
        col, row = pos % 2, pos // 2
        bx = gx + col * (gw + gap)
        by = gy + row * (gh + gap)
        colour = ACCENTS[pos + 1]
        d.rounded_rectangle([bx, by, bx + gw, by + gh], radius=14,
                            fill=CARD, outline=EDGE, width=2)
        d.rounded_rectangle([bx, by, bx + gw, by + 8], radius=7, fill=colour)
        PICTOGRAMS[kind](d, bx + 56, by + 58, 26, colour)
        d.text((bx + 96, by + 22), kicker, font=F_TAG, fill=colour)
        y = by + 62
        for line in split_lines(headline, F_HEAD, gw - 36):
            d.text((bx + 18, y), line, font=F_HEAD, fill=INK)
            y += 36
        y += 6
        for line in split_lines(standfirst, F_BODY, gw - 36):
            d.text((bx + 18, y), line, font=F_BODY, fill=GREY)
            y += 28

    # Footer.
    d.line([28, 982, 996, 982], fill=EDGE, width=2)
    d.text((28, 990),
           "Sources: Reuters, Jagran Josh, Newsmriti, HuddleWorld — "
           "public news search, 25 Nov 2026.",
           font=F_FOOT, fill=GREY)
    return page


if __name__ == "__main__":
    finished = build_page()
    finished.save(os.path.join(BASE, "entry.png"))
    print("wrote entry.png", finished.size)

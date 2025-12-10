#!/usr/bin/env python3
"""
Generate placeholder cover images for seeded books using Pillow.
Creates 800x1200 JPG images with solid backgrounds and overlays title/author text.
Output filenames match the fixture entries under static/images/covers/<lang>/<slug>.jpg

Usage:
  python generate_covers.py

Requires:
  pip install pillow
"""
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / 'static' / 'images' / 'covers'

# Ensure directories exist
LANG_DIRS = ['es', 'de', 'it', 'sv']

BOOKS = [
    # Spanish
    ("es", "cien-anos-de-soledad", "Cien años de soledad", "G. García Márquez"),
    ("es", "don-quijote-de-la-mancha", "Don Quijote de la Mancha", "M. de Cervantes"),
    ("es", "la-sombra-del-viento", "La sombra del viento", "C. R. Zafón"),
    ("es", "el-amor-en-los-tiempos-del-colera", "El amor en los tiempos del cólera", "G. García Márquez"),
    ("es", "la-casa-de-los-espiritus", "La casa de los espíritus", "Isabel Allende"),
    ("es", "rayuela", "Rayuela", "Julio Cortázar"),
    ("es", "el-tunel", "El túnel", "Ernesto Sabato"),
    ("es", "como-agua-para-chocolate", "Como agua para chocolate", "Laura Esquivel"),
    ("es", "patria", "Patria", "F. Aramburu"),
    ("es", "el-alquimista", "El alquimista", "Paulo Coelho"),
    # German
    ("de", "der-vorleser", "Der Vorleser", "B. Schlink"),
    ("de", "die-verwandlung", "Die Verwandlung", "F. Kafka"),
    ("de", "im-westen-nichts-neues", "Im Westen nichts Neues", "E. M. Remarque"),
    ("de", "die-physiker", "Die Physiker", "F. Dürrenmatt"),
    ("de", "homo-faber", "Homo Faber", "Max Frisch"),
    ("de", "die-blechtrommel", "Die Blechtrommel", "G. Grass"),
    ("de", "siddhartha", "Siddhartha", "H. Hesse"),
    ("de", "der-prozess", "Der Prozess", "F. Kafka"),
    ("de", "faust", "Faust", "J. W. von Goethe"),
    ("de", "der-zauberberg", "Der Zauberberg", "Thomas Mann"),
    # Italian
    ("it", "il-nome-della-rosa", "Il nome della rosa", "Umberto Eco"),
    ("it", "il-gattopardo", "Il gattopardo", "G. T. di Lampedusa"),
    ("it", "se-questo-e-un-uomo", "Se questo è un uomo", "Primo Levi"),
    ("it", "la-coscienza-di-zeno", "La coscienza di Zeno", "Italo Svevo"),
    ("it", "i-promessi-sposi", "I promessi sposi", "A. Manzoni"),
    ("it", "il-barone-rampante", "Il barone rampante", "Italo Calvino"),
    ("it", "la-divina-commedia", "La Divina Commedia", "Dante Alighieri"),
    ("it", "il-fu-mattia-pascal", "Il fu Mattia Pascal", "L. Pirandello"),
    ("it", "le-avventure-di-pinocchio", "Le avventure di Pinocchio", "C. Collodi"),
    ("it", "il-deserto-dei-tartari", "Il deserto dei Tartari", "Dino Buzzati"),
    # Swedish
    ("sv", "pippi-langstrump", "Pippi Långstrump", "Astrid Lindgren"),
    ("sv", "utvandrarna", "Utvandrarna", "Vilhelm Moberg"),
    ("sv", "doktor-glas", "Doktor Glas", "H. Söderberg"),
    ("sv", "gentlemen", "Gentlemen", "Klas Östergren"),
    ("sv", "kejsarn-av-portugallien", "Kejsarn av Portugallien", "Selma Lagerlöf"),
    ("sv", "roda-rummet", "Röda rummet", "August Strindberg"),
    ("sv", "man-som-hatar-kvinnor", "Män som hatar kvinnor", "Stieg Larsson"),
    ("sv", "aniara", "Aniara", "Harry Martinson"),
    ("sv", "karlsson-pa-taket", "Karlsson på taket", "Astrid Lindgren"),
    ("sv", "handelser-vid-vatten", "Händelser vid vatten", "K. Ekman"),
]

# Colors per language for quick visual distinction
LANG_COLORS = {
    'es': (220, 80, 80),   # red-ish
    'de': (60, 120, 200),  # blue-ish
    'it': (60, 160, 100),  # green-ish
    'sv': (220, 180, 60),  # yellow-ish
}

WIDTH, HEIGHT = 800, 1200
MARGIN = 60

# Try to use a bundled font or system fallback
# You can drop a TTF like static/fonts/DejaVuSans.ttf and point to it here if needed.
FONT_PATHS = [
    str(BASE_DIR / 'static' / 'fonts' / 'DejaVuSans.ttf'),
    '/Library/Fonts/Arial.ttf',
    '/System/Library/Fonts/Supplemental/Arial.ttf',
]

def get_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_PATHS:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def draw_multiline_centered(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, box):
    # Simple centered multiline drawing within a box (left, top, right, bottom)
    left, top, right, bottom = box
    lines = []
    # naive wrap: break lines at ~28 chars, then adjust
    max_chars = 28
    words = text.split()
    line = []
    for w in words:
        tentative = ' '.join(line + [w])
        if len(tentative) <= max_chars:
            line.append(w)
        else:
            lines.append(' '.join(line))
            line = [w]
    if line:
        lines.append(' '.join(line))

    line_heights = []
    for ln in lines:
        bbox = draw.textbbox((0, 0), ln, font=font)
        line_heights.append(bbox[3] - bbox[1])
    total_height = sum(line_heights) + (len(lines) - 1) * 10
    y = top + (bottom - top - total_height) // 2
    for ln, h in zip(lines, line_heights):
        bbox = draw.textbbox((0, 0), ln, font=font)
        text_w = bbox[2] - bbox[0]
        x = left + (right - left - text_w) // 2
        draw.text((x, y), ln, fill=(255, 255, 255), font=font)
        y += h + 10


def generate_cover(lang: str, slug: str, title: str, author: str):
    bg = LANG_COLORS.get(lang, (100, 100, 100))
    img = Image.new('RGB', (WIDTH, HEIGHT), color=bg)
    draw = ImageDraw.Draw(img)

    # Decorative bands
    draw.rectangle([0, 0, WIDTH, 80], fill=(0, 0, 0))
    draw.rectangle([0, HEIGHT - 80, WIDTH, HEIGHT], fill=(0, 0, 0))

    title_font = get_font(60)
    author_font = get_font(36)

    # Title block (centered)
    draw_multiline_centered(draw, title, title_font, (MARGIN, 200, WIDTH - MARGIN, 800))

    # Author (bottom area)
    author_bbox = draw.textbbox((0, 0), author, font=author_font)
    author_w = author_bbox[2] - author_bbox[0]
    x = (WIDTH - author_w) // 2
    y = HEIGHT - 80 - (author_bbox[3] - author_bbox[1]) - 20
    draw.text((x, y), author, fill=(255, 255, 255), font=author_font)

    out_dir = STATIC_DIR / lang
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}.jpg"
    img.save(out_path, format='JPEG', quality=90)
    print(f"Saved {out_path}")


def main():
    for lang in LANG_DIRS:
        (STATIC_DIR / lang).mkdir(parents=True, exist_ok=True)
    for lang, slug, title, author in BOOKS:
        generate_cover(lang, slug, title, author)
    print("Done generating covers.")


if __name__ == '__main__':
    main()

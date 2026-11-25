#!/usr/bin/env python3
"""Deterministic 1024x1024 editorial broadsheet renderer for news-image-20261125."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024

# Editorial broadsheet palette
BG_IVORY = "#F7F2E7"
SURFACE_TINT = "#EFE8D8"
SURFACE_LEAD = "#F3E9DF"
INK_NAVY = "#14264C"
INK_BODY = "#1E293B"
INK_MUTED = "#4B5563"
ACCENT_BURGUNDY = "#7A1F2B"
ACCENT_TEAL = "#0E6B6B"
RULE_COLOR = "#C8BEA8"
RULE_DARK = "#14264C"

FONT_SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

STATS_BAR_TEXT = (
    "MSCI ASIA-PACIFIC EX-JAPAN \u22122.3%  \u2022  "
    "SOUTH KOREA \u22125.3%  \u2022  "
    "NIKKEI \u22122.9%  \u2022  "
    "NVIDIA \u22125.9% TO $155.38  \u2022  "
    "16 TRADING PARTNERS IN SECTION 301 PROBE"
)


@dataclass(frozen=True)
class Panel:
    kicker: str
    headline: str
    summary: str
    is_lead: bool = False
    kicker_color: str = ACCENT_TEAL


PANELS: tuple[Panel, ...] = (
    Panel(
        kicker="TRADE \u2022 WASHINGTON",
        headline="U.S. Set to Release Section 301 Probe Findings on 16 Partners",
        summary=(
            "The Trump administration is set to release \"excess capacity\" probe "
            "findings on 16 major trading partners, with new duties expected. "
            "Asia-Pacific shares tumbled Wednesday morning."
        ),
        is_lead=True,
        kicker_color=ACCENT_BURGUNDY,
    ),
    Panel(
        kicker="ASIA \u2022 SHANGHAI",
        headline="Shanghai Party Chief Chen Jining Placed Under Corruption Probe",
        summary=(
            "Politburo member and Shanghai party chief Chen Jining, 62, is under "
            "investigation for suspected severe violations, Xinhua reported \u2014 the "
            "fourth Politburo member probed since 2025."
        ),
        kicker_color=ACCENT_TEAL,
    ),
    Panel(
        kicker="TECH \u2022 SANTA CLARA",
        headline="Reinstated Nvidia CEO Admits Code Violation, Enters Therapy",
        summary=(
            "CEO Jensen Huang told a Tuesday all-hands he had violated the company's "
            "code of conduct and is in therapy. Shares fell 5.9% Tuesday to $155.38 "
            "after Monday's 31% surge."
        ),
        kicker_color=INK_NAVY,
    ),
    Panel(
        kicker="MIDDLE EAST \u2022 JERUSALEM",
        headline="Eisenkot's Yashar Signs First Post-Election Coalition Pact",
        summary=(
            "Yashar signed a coalition pact with Lieberman's Yisrael Beytenu. "
            "Eisenkot's bloc holds 48 of 120 seats against Likud's 53, with a "
            "Dec 6 mandate deadline."
        ),
        kicker_color=ACCENT_TEAL,
    ),
    Panel(
        kicker="EUROPE \u2022 MINSK",
        headline="Lukashenko Offers to Fly With Zelenskiy to Moscow for Talks",
        summary=(
            "Belarusian leader Alexander Lukashenko told Le Point he has offered to "
            "fly with Zelenskiy to Moscow as his personal safety guarantor for "
            "Kremlin talks."
        ),
        kicker_color=INK_NAVY,
    ),
    Panel(
        kicker="CLIMATE \u2022 ANTALYA",
        headline="COP31 Ended Sunday Without a Deal, First Failure Since 2009",
        summary=(
            "The longest UN climate summit on record collapsed Sunday after "
            "fossil-fuel language was stripped from the text, shifting focus to "
            "next year's COP32 in Addis Ababa."
        ),
        kicker_color=ACCENT_TEAL,
    ),
)

FOOTER_STRIPS: tuple[tuple[str, str, str], ...] = (
    (
        "SPACE \u2022 JIUQUAN",
        ACCENT_TEAL,
        "Shenzhou-24 launched Wednesday at 08:18 Beijing time \u2014 Muhammad Zeeshan Ali, 40, "
        "is the first Pakistani in orbit and the first foreign astronaut to board Tiangong.",
    ),
    (
        "DHAKA",
        ACCENT_BURGUNDY,
        "Garment workers blocked roads in Gazipur on Tuesday amid wage-board talks, "
        "demanding 30,000 taka against the current 12,500.",
    ),
)


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    """Wrap text into lines that fit within max_width pixels."""
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_single_line(
    draw: ImageDraw.ImageDraw,
    text: str,
    font_path: str,
    start_size: int,
    min_size: int,
    max_width: int,
) -> ImageFont.FreeTypeFont:
    """Return the largest font size <= start_size that fits text on one line."""
    for size in range(start_size, min_size - 1, -1):
        font = load_font(font_path, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return font
    return load_font(font_path, min_size)


def draw_panel(
    draw: ImageDraw.ImageDraw,
    panel: Panel,
    box: tuple[int, int, int, int],
) -> None:
    x0, y0, x1, y1 = box
    pad_x = 18
    pad_y = 16

    bg = SURFACE_LEAD if panel.is_lead else BG_IVORY
    border = ACCENT_BURGUNDY if panel.is_lead else RULE_COLOR
    draw.rectangle([x0, y0, x1, y1], fill=bg, outline=border, width=1)

    if panel.is_lead:
        draw.rectangle([x0, y0, x0 + 6, y1], fill=ACCENT_BURGUNDY)

    inner_x = x0 + pad_x + (4 if panel.is_lead else 0)
    inner_w = (x1 - pad_x) - inner_x
    cursor_y = y0 + pad_y

    # Kicker row
    font_kicker = load_font(FONT_SANS_BOLD, 12)
    draw.text((inner_x, cursor_y + 2), panel.kicker, font=font_kicker, fill=panel.kicker_color)

    if panel.is_lead:
        tag_text = "LEAD STORY"
        tag_font = load_font(FONT_SANS_BOLD, 11)
        tb = draw.textbbox((0, 0), tag_text, font=tag_font)
        tag_w = (tb[2] - tb[0]) + 14
        tag_h = 20
        tag_x0 = x1 - pad_x - tag_w
        tag_y0 = cursor_y - 1
        draw.rectangle([tag_x0, tag_y0, tag_x0 + tag_w, tag_y0 + tag_h], fill=ACCENT_BURGUNDY)
        draw.text((tag_x0 + 7, tag_y0 + 3), tag_text, font=tag_font, fill="#FFFFFF")

    cursor_y += 24

    # Headline (bold serif)
    font_head = load_font(FONT_SERIF_BOLD, 20)
    head_lines = wrap_text(draw, panel.headline, font_head, inner_w)
    head_line_h = 25
    for line in head_lines:
        draw.text((inner_x, cursor_y), line, font=font_head, fill=INK_NAVY)
        cursor_y += head_line_h

    cursor_y += 8

    # Thin divider between headline and summary
    draw.line([(inner_x, cursor_y), (inner_x + 48, cursor_y)], fill=panel.kicker_color, width=2)
    cursor_y += 10

    # Summary (clean sans)
    font_body = load_font(FONT_SANS, 14)
    body_lines = wrap_text(draw, panel.summary, font_body, inner_w)
    body_line_h = 22
    for line in body_lines:
        draw.text((inner_x, cursor_y), line, font=font_body, fill=INK_BODY)
        cursor_y += body_line_h

    if cursor_y > y1 - 8:
        raise RuntimeError(
            f"Panel '{panel.kicker}' overflowed: cursor_y={cursor_y} > y1-8={y1 - 8}"
        )


def render(out_path: Path) -> None:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_IVORY)
    draw = ImageDraw.Draw(img)

    margin_x = 36
    content_w = WIDTH - 2 * margin_x

    # Top double rule
    draw.rectangle([margin_x, 22, WIDTH - margin_x, 26], fill=RULE_DARK)
    draw.line([(margin_x, 30), (WIDTH - margin_x, 30)], fill=RULE_DARK, width=1)

    # Masthead
    font_masthead = load_font(FONT_SERIF_BOLD, 54)
    title = "WORLD NEWS"
    tb = draw.textbbox((0, 0), title, font=font_masthead)
    title_w = tb[2] - tb[0]
    draw.text(((WIDTH - title_w) // 2, 36), title, font=font_masthead, fill=INK_NAVY)

    # Date line + thin rule
    font_date = load_font(FONT_SERIF, 15)
    date_text = "Wednesday, 25 November 2026"
    db = draw.textbbox((0, 0), date_text, font=font_date)
    date_w = db[2] - db[0]
    draw.text(((WIDTH - date_w) // 2, 98), date_text, font=font_date, fill=INK_MUTED)
    draw.line([(margin_x, 124), (WIDTH - margin_x, 124)], fill=RULE_DARK, width=1)

    # Verified stats bar
    stats_y0, stats_y1 = 132, 162
    draw.rectangle([margin_x, stats_y0, WIDTH - margin_x, stats_y1], fill=SURFACE_TINT)
    draw.line([(margin_x, stats_y1), (WIDTH - margin_x, stats_y1)], fill=RULE_COLOR, width=1)
    font_stats = fit_single_line(draw, STATS_BAR_TEXT, FONT_SANS_BOLD, 12, 9, content_w - 20)
    sb = draw.textbbox((0, 0), STATS_BAR_TEXT, font=font_stats)
    sw = sb[2] - sb[0]
    sh = sb[3] - sb[1]
    draw.text(
        ((WIDTH - sw) // 2, stats_y0 + (stats_y1 - stats_y0 - sh) // 2 - 1),
        STATS_BAR_TEXT,
        font=font_stats,
        fill=INK_NAVY,
    )

    # 2x3 Panel Grid
    grid_top = 176
    footer_top = 878
    col_gap = 18
    row_gap = 14
    col_w = (content_w - col_gap) // 2
    row_h = (footer_top - grid_top - 2 * row_gap - 14) // 3

    for idx, panel in enumerate(PANELS):
        row = idx // 2
        col = idx % 2
        px0 = margin_x + col * (col_w + col_gap)
        py0 = grid_top + row * (row_h + row_gap)
        draw_panel(draw, panel, (px0, py0, px0 + col_w, py0 + row_h))

    # Footer: two thin strips
    draw.line([(margin_x, footer_top), (WIDTH - margin_x, footer_top)], fill=RULE_DARK, width=2)
    strip_y = footer_top + 10
    strip_h = 54
    strip_gap = 8
    font_strip_kicker = load_font(FONT_SANS_BOLD, 11)
    font_strip_body = load_font(FONT_SANS, 12)

    for i, (kicker, k_color, body) in enumerate(FOOTER_STRIPS):
        sy0 = strip_y + i * (strip_h + strip_gap)
        sy1 = sy0 + strip_h
        draw.rectangle([margin_x, sy0, WIDTH - margin_x, sy1], fill=SURFACE_TINT, outline=RULE_COLOR, width=1)
        draw.rectangle([margin_x, sy0, margin_x + 4, sy1], fill=k_color)

        kx = margin_x + 14
        kb = draw.textbbox((0, 0), kicker, font=font_strip_kicker)
        text_x = kx + (kb[2] - kb[0]) + 14
        max_body_w = (WIDTH - margin_x - 14) - text_x
        lines = wrap_text(draw, body, font_strip_body, max_body_w)
        if len(lines) > 2:
            raise RuntimeError(f"Footer strip '{kicker}' wrapped to {len(lines)} lines (>2)")

        line_h = 19
        block_h = (len(lines) - 1) * line_h + 15
        text_y0 = sy0 + (strip_h - block_h) // 2
        draw.text((kx, text_y0), kicker, font=font_strip_kicker, fill=k_color)
        for li, line in enumerate(lines):
            draw.text((text_x, text_y0 + li * line_h), line, font=font_strip_body, fill=INK_BODY)

    img.save(out_path, format="PNG")


if __name__ == "__main__":
    output = Path(__file__).resolve().parent / "entry.png"
    render(output)
    print(f"rendered {output} ({WIDTH}x{HEIGHT})")

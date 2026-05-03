"""
New Build Protection Guide — PDF build script
================================================

Client:   Loretta Sercy, Realtor® · eXp Realty · TX License #0633703
Brand:    MoveWithClarity — "Move with Clarity. Not Pressure."
Site:     lorettasercy.com
Engine:   ReportLab 4.x (stock Base14 Helvetica, no external fonts)

This script reproduces the New Build Protection Guide PDF from a structured
content model. The original was generated 2026-04-27 with no persisted source;
this file is the canonical source going forward — edit the CONTENT data
section to revise and re-run.

Output: NewBuildProtectionGuide_MoveWithClarity_v2.pdf
        in the same folder as the original.

Usage:
    python new_build_guide.py            # writes default v2 alongside original
    python new_build_guide.py <out.pdf>  # writes to a specific path
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable

from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfdoc import PDFInfo
from reportlab.pdfgen import canvas


# ---------------------------------------------------------------------------
# Geometry & palette  (pulled from original-PDF probe; do not casually change)
# ---------------------------------------------------------------------------

PAGE_W, PAGE_H = 612.0, 792.0   # US Letter portrait

# Brand palette
NAVY            = Color(0.05098,  0.11765,  0.17255)   # cover background  #0d1e21
NAVY_DARKER     = Color(0.03922,  0.09412,  0.12549)   # cover header/footer band  #0a181f
GOLD            = Color(0.75294,  0.62353,  0.37647)   # accent  #c09f60
SAGE            = Color(0.29020,  0.40392,  0.25490)   # primary brand  #4a6741
MIST            = Color(0.78431,  0.84706,  0.75294)   # callout & pill bg  #c8d8c0
CHALK           = Color(0.94118,  0.92941,  0.90196)   # alt table row  #f0ede6
WARM_WHITE      = Color(0.98039,  0.97647,  0.96471)   # body bg / inverted text  #faf9f6
PALE_BLUE       = Color(0.83137,  0.86275,  0.91373)   # cover subtitle  #d4dce8
BLUE_GRAY       = Color(0.54118,  0.60784,  0.71020)   # cover eyebrow / footer  #8a9bb5
CHARCOAL        = Color(0.17255,  0.17255,  0.17255)   # body text  #2c2c2c
STONE           = Color(0.42000,  0.39608,  0.37647)   # page-number text  #6b6560
BLACK           = Color(0,        0,        0)
WHITE           = Color(1,        1,        1)

# Standard layout coordinates (top-down, original PDF convention)
HEADER_BAND_BOT = 46.80          # pages 2+: warm-white header strip ends here
HEADER_RULE_TOP = 44.64          # 2.16pt sage rule under the header band
FOOTER_BAND_TOP = 738.0          # pages 2+: sage footer band starts here
LEFT_TEXT_X     = 52.80          # standard left margin for body text
RIGHT_TEXT_X    = 559.20         # standard right edge for body text
BULLET_INDENT_X = 58.80          # bullets indent +6
BULLET_HANG_X   = 68.80          # second-line indent for wrapped bullets

CONTENT_TOP_Y   = 84.0           # first content baseline-ish on body pages
CONTENT_BOTTOM_Y = 730.0         # absolute bottom of safe zone (above footer)

PILL_X_LEFT     = 52.80          # phase pills span this wide
PILL_X_RIGHT    = 571.20
PILL_HEIGHT     = 31.68          # pill bbox height (74.4 -> 106.08)
PILL_RADIUS     = 5.0
PILL_GOLD_TAB_W = 5.0


# ---------------------------------------------------------------------------
# Content model
# ---------------------------------------------------------------------------

@dataclass
class Block:
    """Base for content blocks. Each block knows how to draw itself and
    advances a cursor (`y_top`, top-down coordinates) to where the next
    block should begin."""
    def draw(self, c: canvas.Canvas, y_top: float) -> float:
        raise NotImplementedError


@dataclass
class PhasePill(Block):
    """Rounded mist pill with gold left tab — used for PHASE/section headers."""
    label: str           # e.g. "PHASE 1  ·  BEFORE YOU SIGN: CONTRACT REVIEW"
    height: float = PILL_HEIGHT
    text_baseline_offset: float = 20.84   # 95.24 - 74.4 from probe
    text_x: float = 68.80                 # text inside pill, after gold tab
    margin_top: float = 0
    margin_bottom: float = 7.93           # gap before first paragraph (113.93 - 106.08)

    def draw(self, c, y_top):
        y_top += self.margin_top
        # Pill: rounded mist rectangle
        rl_y_bot = PAGE_H - (y_top + self.height)
        c.setFillColor(MIST)
        c.roundRect(PILL_X_LEFT, rl_y_bot, PILL_X_RIGHT - PILL_X_LEFT,
                    self.height, PILL_RADIUS, fill=1, stroke=0)
        # Gold left tab (overlays the rounded left corners with a flat strip)
        c.setFillColor(GOLD)
        c.rect(PILL_X_LEFT, rl_y_bot, PILL_GOLD_TAB_W, self.height, fill=1, stroke=0)
        # Label text — Helvetica-Bold 10.5pt, charcoal
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica-Bold", 10.5)
        baseline_topdown = y_top + self.text_baseline_offset
        c.drawString(self.text_x, PAGE_H - baseline_topdown, self.label)
        return y_top + self.height + self.margin_bottom


@dataclass
class Paragraph(Block):
    """Body paragraph. Wraps to RIGHT_TEXT_X minus left."""
    text: str
    font: str = "Helvetica"
    size: float = 10.5
    color: Color = field(default_factory=lambda: CHARCOAL)
    x: float = LEFT_TEXT_X
    right_x: float = RIGHT_TEXT_X
    line_height: float = 16.0       # 14.43 ascent + leading; matches probe gap
    margin_top: float = 0
    margin_bottom: float = 6.0      # gap to next block

    def draw(self, c, y_top):
        y_top += self.margin_top
        c.setFillColor(self.color)
        c.setFont(self.font, self.size)
        max_w = self.right_x - self.x
        baseline_topdown = y_top + 11.29   # 113.93 -> 125.22 = 11.29
        for line in wrap_text(c, self.text, self.font, self.size, max_w):
            c.drawString(self.x, PAGE_H - baseline_topdown, line)
            baseline_topdown += self.line_height
        # Bottom of last line:
        end_top = baseline_topdown - self.line_height + 4.71  # bbox descent
        return end_top + self.margin_bottom


@dataclass
class Subhead(Block):
    """Bold lead-in like 'What to review before signing:'"""
    text: str
    margin_top: float = 6.0     # extra space above subhead vs preceding paragraph
    margin_bottom: float = 4.5

    def draw(self, c, y_top):
        y_top += self.margin_top
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica-Bold", 10.5)
        baseline_topdown = y_top + 11.24
        c.drawString(LEFT_TEXT_X, PAGE_H - baseline_topdown, self.text)
        return y_top + 14.46 + self.margin_bottom


@dataclass
class Bullet(Block):
    """A single dash-bullet line (or wrapped multi-line)."""
    text: str
    line_height: float = 19.0       # gap between bullet baselines (probe: 187.93->206.93=19)
    indent: float = BULLET_INDENT_X
    hang_indent: float = BULLET_HANG_X
    right_x: float = RIGHT_TEXT_X

    def draw(self, c, y_top):
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica", 10.5)
        max_w_first = self.right_x - self.indent
        max_w_cont  = self.right_x - self.hang_indent
        # Wrap honoring hang indent for continuation lines
        lines = wrap_text_hanging(c, self.text, "Helvetica", 10.5,
                                  max_w_first, max_w_cont)
        baseline_topdown = y_top + 11.29
        for i, ln in enumerate(lines):
            x = self.indent if i == 0 else self.hang_indent
            c.drawString(x, PAGE_H - baseline_topdown, ln)
            baseline_topdown += 15.0    # within-bullet line spacing tighter than between bullets
        # Advance cursor by full bullet line height for the FIRST line, then
        # 15pt for each continuation line:
        n = len(lines)
        return y_top + self.line_height + 15.0 * (n - 1) - (15.0 if n > 0 else 0) + (15.0 if n > 1 else 0)


@dataclass
class BulletList(Block):
    """Group of bullets with consistent spacing — replaces N Bullet() blocks
    so that line spacing is uniform."""
    items: list[str]
    line_step: float = 19.0
    indent: float = BULLET_INDENT_X
    hang_indent: float = BULLET_HANG_X
    right_x: float = RIGHT_TEXT_X
    margin_top: float = 0
    margin_bottom: float = 7.0

    def draw(self, c, y_top):
        y_top += self.margin_top
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica", 10.5)
        max_w_first = self.right_x - self.indent
        max_w_cont  = self.right_x - self.hang_indent
        baseline_topdown = y_top + 11.29
        last_top = y_top
        for item in self.items:
            lines = wrap_text_hanging(c, item, "Helvetica", 10.5,
                                      max_w_first, max_w_cont)
            for i, ln in enumerate(lines):
                x = self.indent if i == 0 else self.hang_indent
                c.drawString(x, PAGE_H - baseline_topdown, ln)
                baseline_topdown += 15.0
            # back up — overshoot of last 15.0 — and step to next bullet at line_step
            baseline_topdown -= 15.0
            baseline_topdown += self.line_step
            last_top = baseline_topdown - 11.29
        return last_top - self.line_step + 14.43 + self.margin_bottom


@dataclass
class Callout(Block):
    """Mist-colored highlight rectangle with italic sage text inside."""
    text: str
    rect_pad_x: float = 6.0       # horizontal padding inside box (offset from LEFT_TEXT_X-6)
    rect_top_pad: float = 8.0
    rect_bot_pad: float = 9.0
    text_left_x: float = 60.80
    text_right_x: float = 552.0
    line_height: float = 15.0
    margin_top: float = 17.5
    margin_bottom: float = 14.0

    def draw(self, c, y_top):
        y_top += self.margin_top
        # Compute wrapped lines
        c.setFont("Helvetica-Oblique", 10.5)
        lines = wrap_text(c, self.text, "Helvetica-Oblique", 10.5,
                          self.text_right_x - self.text_left_x)
        # Draw mist rectangle behind
        text_block_h = self.line_height * (len(lines) - 1) + 14.22
        rect_h = self.rect_top_pad + text_block_h + self.rect_bot_pad
        rect_x = 46.80
        rect_w = 565.20 - 46.80
        rl_y_bot = PAGE_H - (y_top + rect_h)
        c.setFillColor(MIST)
        c.rect(rect_x, rl_y_bot, rect_w, rect_h, fill=1, stroke=0)
        # Draw italic sage text
        c.setFillColor(SAGE)
        c.setFont("Helvetica-Oblique", 10.5)
        baseline_topdown = y_top + self.rect_top_pad + 11.23
        for ln in lines:
            c.drawString(self.text_left_x, PAGE_H - baseline_topdown, ln)
            baseline_topdown += self.line_height
        return y_top + rect_h + self.margin_bottom


@dataclass
class Spacer(Block):
    """Vertical gap."""
    height: float
    def draw(self, c, y_top):
        return y_top + self.height


@dataclass
class WarrantyTable(Block):
    """Sage header row + 3 data rows with alternating chalk/warm-white fills."""
    rows: list[tuple[str, str]]  # (coverage, duration)
    header: tuple[str, str] = ("Coverage", "Standard Duration")
    x_left: float = 79.20
    x_right: float = 532.80
    x_split: float = 352.80      # column split (from probe)
    text_x_col1: float = 91.20
    text_x_col2: float = 364.80
    header_h: float = 28.0
    row_h: float = 28.0
    margin_top: float = 8.0
    margin_bottom: float = 7.0

    def draw(self, c, y_top):
        y_top += self.margin_top
        x = self.x_left
        w = self.x_right - self.x_left
        # Header row (sage fill, white bold text)
        rl_y_hdr_bot = PAGE_H - (y_top + self.header_h)
        c.setFillColor(SAGE)
        c.rect(x, rl_y_hdr_bot, w, self.header_h, fill=1, stroke=0)
        c.setFillColor(WARM_WHITE)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(self.text_x_col1, PAGE_H - (y_top + 18.58), self.header[0])
        c.drawString(self.text_x_col2, PAGE_H - (y_top + 18.58), self.header[1])
        # Data rows alternate (warm-white, chalk, warm-white, ...)
        cur_y = y_top + self.header_h
        for i, (col1, col2) in enumerate(self.rows):
            row_fill = WARM_WHITE if i % 2 == 0 else CHALK
            rl_y_row_bot = PAGE_H - (cur_y + self.row_h)
            c.setFillColor(row_fill)
            c.rect(x, rl_y_row_bot, w, self.row_h, fill=1, stroke=0)
            c.setFillColor(BLACK)
            c.setFont("Helvetica", 10.5)
            text_baseline = cur_y + 18.58
            c.drawString(self.text_x_col1, PAGE_H - text_baseline, col1)
            c.drawString(self.text_x_col2, PAGE_H - text_baseline, col2)
            cur_y += self.row_h
        # Mist-colored thin strokes around the table edges + column split
        c.setStrokeColor(MIST)
        c.setLineWidth(0.5)
        # Outer rectangle
        rl_y_bot = PAGE_H - cur_y
        rl_y_top = PAGE_H - y_top
        c.line(x,         rl_y_top, x + w,    rl_y_top)
        c.line(x,         rl_y_bot, x + w,    rl_y_bot)
        c.line(x,         rl_y_top, x,        rl_y_bot)
        c.line(x + w,     rl_y_top, x + w,    rl_y_bot)
        # Internal horizontal separators
        sep_y = y_top + self.header_h
        for _ in range(len(self.rows)):
            c.line(x, PAGE_H - sep_y, x + w, PAGE_H - sep_y)
            sep_y += self.row_h
        # Column split (full height)
        c.line(self.x_split, rl_y_top, self.x_split, rl_y_bot)
        return cur_y + self.margin_bottom


@dataclass
class EyebrowHeading(Block):
    """Small sage uppercase eyebrow label + large charcoal headline.
    Used on 'About this guide' (page 2) and 'Bonus' (page 7)."""
    eyebrow: str
    headline: str
    eyebrow_color: Color = field(default_factory=lambda: SAGE)
    margin_bottom: float = 12.0

    def draw(self, c, y_top):
        c.setFillColor(self.eyebrow_color)
        c.setFont("Helvetica-Bold", 9.0)
        c.drawString(LEFT_TEXT_X, PAGE_H - (y_top + 9.63), self.eyebrow)
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica-Bold", 16.0)
        c.drawString(LEFT_TEXT_X, PAGE_H - (y_top + 32.6), self.headline)
        # 32.6 is approximate baseline of 16pt headline below eyebrow (probe: 87.77->120.40 = ~32.6 diff)
        return y_top + 33.0 + self.margin_bottom


# ---------------------------------------------------------------------------
# Text wrapping helpers
# ---------------------------------------------------------------------------

def wrap_text(c: canvas.Canvas, text: str, font: str, size: float,
              max_width: float) -> list[str]:
    """Wrap a paragraph by words to fit max_width using stringWidth on c."""
    words = text.split(" ")
    lines = []
    current = ""
    for w in words:
        candidate = (current + " " + w) if current else w
        if c.stringWidth(candidate, font, size) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def wrap_text_hanging(c: canvas.Canvas, text: str, font: str, size: float,
                      max_w_first: float, max_w_cont: float) -> list[str]:
    """Word-wrap with different max widths for first vs continuation lines —
    matches a hanging-indent bullet."""
    words = text.split(" ")
    lines: list[str] = []
    current = ""
    is_first = True
    for w in words:
        max_w = max_w_first if is_first else max_w_cont
        candidate = (current + " " + w) if current else w
        if c.stringWidth(candidate, font, size) <= max_w:
            current = candidate
        else:
            if current:
                lines.append(current)
                is_first = False
            current = w
    if current:
        lines.append(current)
    return lines


# ---------------------------------------------------------------------------
# Page chrome (header + footer, drawn on every body page)
# ---------------------------------------------------------------------------

def draw_body_chrome(c: canvas.Canvas, page_num: int) -> None:
    """Draw the warm-white header band, sage rule, sage footer band, and the
    standard tagline + license footer text. `page_num` is the 'pg N' number
    shown in the right side of the header (1 for the first body page)."""
    # Page background = warm white
    c.setFillColor(WARM_WHITE)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Top warm-white band
    c.setFillColor(WARM_WHITE)
    c.rect(0, PAGE_H - HEADER_BAND_BOT, PAGE_W, HEADER_BAND_BOT, fill=1, stroke=0)
    # Sage rule under header
    c.setFillColor(SAGE)
    c.rect(0, PAGE_H - HEADER_BAND_BOT, PAGE_W, HEADER_BAND_BOT - HEADER_RULE_TOP,
           fill=1, stroke=0)

    # Sage footer band
    c.setFillColor(SAGE)
    c.rect(0, 0, PAGE_W, PAGE_H - FOOTER_BAND_TOP, fill=1, stroke=0)

    # Header — left: "LORETTA SERCY" (15pt, sage)
    c.setFillColor(SAGE)
    c.setFont("Helvetica", 15.0)
    c.drawString(46.80, PAGE_H - 28.80, "LORETTA")
    c.setFont("Helvetica-Bold", 15.0)
    # Position "SERCY" after a space following "LORETTA"
    c.drawString(126.00, PAGE_H - 28.80, "SERCY")

    # Header — right: "New Build Protection Guide  ·  pg N" (7.5pt, stone)
    c.setFillColor(STONE)
    c.setFont("Helvetica", 7.5)
    right_text = f"New Build Protection Guide  ·  pg {page_num}"
    c.drawRightString(565.20, PAGE_H - 28.80, right_text)

    # Footer — tagline (italic, mist) and license line (warm-white)
    c.setFillColor(MIST)
    c.setFont("Helvetica-Oblique", 9.0)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 756.00, "Move with Clarity. Not Pressure.")
    c.setFillColor(WARM_WHITE)
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 774.72,
        "Loretta Sercy  |  Realtor®  |  eXp Realty  |  TX License #0633703  |  lorettasercy.com")


# ---------------------------------------------------------------------------
# Cover page (page 1) — hand-drawn special layout
# ---------------------------------------------------------------------------

PHASE_PILL_LABELS = [
    ("01", "Contract"),
    ("02", "Pre-Build"),
    ("03", "Milestone"),
    ("04", "Pre-Drywall"),
    ("05", "Walkthrough"),
    ("06", "Warranty"),
]
# Positions match probe (x of '01' through '06', y for both lines)
PHASE_PILL_X_NUM   = [65.88, 162.36, 258.84, 355.32, 451.80, 548.28]
PHASE_PILL_X_LABEL = [56.88, 152.03, 247.84, 340.78, 435.47, 538.18]
PHASE_PILL_RECT_X  = [27.36, 123.84, 220.32, 316.80, 413.28, 509.76]


def draw_cover(c: canvas.Canvas) -> None:
    # Full-page navy fill
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Gold left edge bar (full height, 15.84pt wide)
    c.setFillColor(GOLD)
    c.rect(0, 0, 15.84, PAGE_H, fill=1, stroke=0)
    # Sage right edge bar (5.76pt wide)
    c.setFillColor(SAGE)
    c.rect(606.24, 0, 5.76, PAGE_H, fill=1, stroke=0)

    # Top darker-navy header band
    c.setFillColor(NAVY_DARKER)
    c.rect(0, PAGE_H - 64.80, PAGE_W, 64.80, fill=1, stroke=0)
    # Bottom darker-navy footer band
    c.setFillColor(NAVY_DARKER)
    c.rect(0, 0, PAGE_W, PAGE_H - 748.80, fill=1, stroke=0)

    # Header brand: "LORETTA" (light, warm-white) + " SERCY" bold
    c.setFillColor(WARM_WHITE)
    c.setFont("Helvetica", 12.0)
    c.drawString(27.36, PAGE_H - 37.44, "LORETTA")
    c.setFont("Helvetica-Bold", 12.0)
    c.drawString(81.36, PAGE_H - 37.44, "SERCY")
    # Small gold dot between header sections (probe: 116.64..120.96, y 31.68..36)
    c.setFillColor(GOLD)
    c.circle((116.64 + 120.96) / 2, PAGE_H - (31.68 + 36) / 2,
             (120.96 - 116.64) / 2, fill=1, stroke=0)

    # Header right: "MOVEWITHCLARITY  ·  NEW CONSTRUCTION SERIES"
    c.setFillColor(BLUE_GRAY)
    c.setFont("Helvetica", 7.5)
    c.drawString(391.70, PAGE_H - 37.44,
                 "MOVEWITHCLARITY  ·  NEW CONSTRUCTION SERIES")

    # Giant "CLARITY" watermark — white at low alpha, drawn behind the title
    c.saveState()
    try:
        c.setFillColor(WHITE)
        c.setFillAlpha(0.10)
        c.setFont("Helvetica-Bold", 110.0)
        c.drawString(110.78, PAGE_H - 532.69, "CLARITY")
    finally:
        c.restoreState()

    # Title block: "New Build" / "Protection" / "Guide" — 52pt, three colors
    c.setFillColor(WARM_WHITE)
    c.setFont("Helvetica", 52.0)
    c.drawString(52.80, PAGE_H - 241.60, "New Build")

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 52.0)
    c.drawString(52.80, PAGE_H - 299.60, "Protection")

    c.setFillColor(WARM_WHITE)
    c.setFont("Helvetica", 52.0)
    c.drawString(52.80, PAGE_H - 357.60, "Guide")

    # Gold horizontal divider
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(166.74, PAGE_H - 387.10, 445.26, PAGE_H - 387.10)

    # Subtitle (pale blue, 12pt) — wraps
    c.setFillColor(PALE_BLUE)
    c.setFont("Helvetica", 12.0)
    c.drawString(52.80, PAGE_H - 415.10,
                 "What every buyer needs to know — before the contract, "
                 "during the build, and at the final")
    c.drawString(52.80, PAGE_H - 433.10, "walkthrough.")

    # 6 phase pills at footer of cover
    pill_y_top = 681.84
    pill_y_bot = 738.0
    pill_h     = pill_y_bot - pill_y_top
    pill_w     = 89.28           # 116.64 - 27.36
    gold_strip_h = 7.20          # gold strip height at top of each pill (681.84..689.04)

    for i, (num, label) in enumerate(PHASE_PILL_LABELS):
        rx = PHASE_PILL_RECT_X[i]
        # Sage rounded rect base
        rl_y_bot = PAGE_H - pill_y_bot
        c.setFillColor(SAGE)
        c.roundRect(rx, rl_y_bot, pill_w, pill_h, PILL_RADIUS, fill=1, stroke=0)
        # Gold top strip
        c.setFillColor(GOLD)
        c.rect(rx, PAGE_H - (pill_y_top + gold_strip_h),
               pill_w, gold_strip_h, fill=1, stroke=0)
        # Number (white, 11pt bold)
        c.setFillColor(WARM_WHITE)
        c.setFont("Helvetica-Bold", 11.0)
        c.drawString(PHASE_PILL_X_NUM[i], PAGE_H - 707.92, num)
        # Label (white, 8pt regular)
        c.setFont("Helvetica", 8.0)
        c.drawString(PHASE_PILL_X_LABEL[i], PAGE_H - 721.92, label)

    # Bottom-of-cover license line (blue-gray)
    c.setFillColor(BLUE_GRAY)
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 774.72,
        "Loretta Sercy  |  Realtor®  |  eXp Realty  "
        "|  TX License #0633703  |  lorettasercy.com")


# ---------------------------------------------------------------------------
# Bonus / CTA page (page 7) — large sage CTA section at the bottom
# ---------------------------------------------------------------------------

def draw_cta_section(c: canvas.Canvas, top_y: float) -> None:
    """Draws the mist divider + sage CTA box + CTA content.

    NOTE: the bonus callout's mist background rectangle (y=330..363) is drawn
    by `compose_bonus` so that the italic callout text it contains is rendered
    on top of (not under) the mist fill."""
    # Mist stroke divider (1pt) at y=381.04
    c.setStrokeColor(MIST)
    c.setLineWidth(1.0)
    c.line(52.80, PAGE_H - 381.04, 559.20, PAGE_H - 381.04)
    # Sage CTA full-bleed rectangle 399.04..567.04
    c.setFillColor(SAGE)
    c.rect(46.80, PAGE_H - 567.04, 565.20 - 46.80, 567.04 - 399.04,
           fill=1, stroke=0)

    # 'Have questions about a new build...' headline (warm-white, bold, 10.5pt)
    c.setFillColor(WARM_WHITE)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(146.71, PAGE_H - 429.54,
                 "Have questions about a new build — or already under contract?")

    # Body text (warm-white, 10.5pt, centered-ish)
    c.setFont("Helvetica", 10.5)
    c.drawString(87.74, PAGE_H - 461.54,
                 "I help buyers navigate new construction without pressure and "
                 "without guesswork. A 20-minute")
    c.drawString(201.82, PAGE_H - 477.54, "conversation can change what you walk into.")

    # 'lorettasercy.com · Comment NEW BUILD on social...'
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(119.26, PAGE_H - 509.54, "lorettasercy.com")
    c.setFont("Helvetica", 10.5)
    c.drawString(203.29, PAGE_H - 509.54,
                 " · Comment NEW BUILD on social for a free copy of this guide")

    # License line inside CTA
    c.setFont("Helvetica", 10.5)
    c.drawString(164.39, PAGE_H - 541.54,
                 "Loretta Sercy | Realtor® | eXp Realty | TX License #0633703")


# ---------------------------------------------------------------------------
# CONTENT — edit here to revise the guide
# ---------------------------------------------------------------------------

# About-this-guide intro paragraphs (page 2). NOTE: the second paragraph is
# the new one added per Edit #6 (was: only paragraphs 1 and 3 existed).
ABOUT_INTRO_PARAGRAPHS: list[str] = [
    "Production builders build hundreds of homes a year. Their contracts are written by their lawyers, "
    "for their protection — not yours. That doesn’t make them bad. It makes them a business. "
    "The buyers who come out ahead aren’t the ones who picked the right builder. They’re the "
    "ones who knew what to ask, what to inspect, and what to document — before anything went sideways.",

    # ── EDIT #6: new paragraph after "...before anything went sideways."
    "Most buyers assume the stress ends once they get under contract. In reality, the most important "
    "decisions — and the biggest opportunities to protect yourself — happen during the build itself.",

    "This guide walks you through every phase of a new construction purchase: contract, build, "
    "inspections, walkthrough, and post-close warranty. Whether you haven’t signed yet or the "
    "foundation is already poured — there’s something here for you.",
]

ALREADY_SIGNED_BOLD = "Already signed?"
ALREADY_SIGNED_BODY = (" Start at Phase 3. The most critical protections happen during the build "
                       "— not before it. You still have time.")

WHATS_INSIDE_ITEMS = [
    "Phase 1 · Before You Sign: Contract Review",
    "Phase 2 · Lot & Pre-Construction: Protect Your Deposit",
    "Phase 3 · During the Build: Milestone Inspections",
    "Phase 4 · Pre-Drywall Inspection: The One You Can't Skip",
    "Phase 5 · Final Walkthrough: Never Waive This",
    "Phase 6 · Post-Close Warranty: Know Your Rights",
    "Bonus · The Documentation Habit That Saves Everything",
]

PHASE_1_INTRO = (
    "The builder's purchase agreement is not the same as a standard TREC residential contract. "
    "It favors the builder on timelines, change orders, price escalations, and dispute resolution. "
    "Know what you're agreeing to before you hand over an earnest deposit."
)
PHASE_1_BULLETS = [
    "– Completion timeline and what happens if the builder misses it",
    "– Price escalation clauses — can they raise your price after contract?",
    "– Change order process — how are upgrades priced and locked in writing?",
    "– Deposit structure — what is refundable and under what conditions?",
    "– Arbitration clause — does it waive your right to sue in court?",
    # ── EDIT #1
    "– Right to use your own buyer's agent (always insist on representation before signing)",
    "– Inspection rights — does the contract allow your own inspector on site?",
]
PHASE_1_CALLOUT = ("If a builder says you don't need representation — "
                   "that's exactly when you do.")

PHASE_2_INTRO = (
    "Once you're under contract and waiting for the build to start, most buyers go quiet. Don't. "
    "This is your opportunity to establish the documentation habits that protect you later."
)
PHASE_2_BULLETS = [
    "– Photograph the lot and any existing grading or drainage conditions",
    "– Get all upgrade selections in writing — verbal promises disappear",
    "– Confirm your build timeline in writing and ask for a milestone schedule",
    "– Request the name and contact of your build superintendent",
    "– Verify HOA rules if applicable — builder sales staff often get this wrong",
    "– Confirm what's included in the base price vs. what requires upgrades",
    # ── EDIT #2: two new bullets
    "– Visit the lot after heavy rain if possible. Drainage issues are easier to identify "
    "before landscaping is completed.",
    "– Pay attention to lot orientation and afternoon sun exposure. West-facing lots can "
    "dramatically affect backyard usability and cooling costs during Texas summers.",
]

PHASE_3_INTRO = (
    "Production builders move fast. Subcontractors work on tight schedules across multiple sites. "
    "Errors happen — and they get covered up. Your right to inspect during the build is the "
    "most valuable protection in your contract. Use it."
)
PHASE_3_MILESTONES = [
    "– Foundation / Pre-Pour — Before concrete is poured. Check rebar placement, "
    "grade beams, post-tension cables if applicable. Impossible to fix after the slab sets.",
    "– Pre-Drywall — The single most important inspection. Full detail in Phase 4.",
    "– Pre-Close / Final — Walk every room, every system, every surface. Take your time.",
]
PHASE_3_RULES = [
    "– Always hire your own independent inspector — never rely on the builder's only",
    "– Visit the site during active construction, not just at scheduled inspections",
    "– Photograph everything — date-stamp your photos",
    "– Put all concerns in writing to your superintendent and agent immediately",
    "– Never sign a punch list as 'complete' unless every item has been resolved",
]

PHASE_4_INTRO = (
    "Once drywall goes up, everything behind it is hidden for the life of the home. Plumbing. "
    "Electrical. Framing. HVAC rough-in. Insulation. A pre-drywall inspection is your only "
    "opportunity to see all of it."
)
PHASE_4_BULLETS = [
    "– Framing — lumber size, proper spacing, headers above openings",
    "– Plumbing rough-in — pipe sizing, slope, drain locations",
    "– Electrical rough-in — panel location, wire gauges, box placement",
    "– HVAC rough-in — duct sizing, return air paths, equipment locations",
    "– Insulation — type, coverage, proper installation in all cavities",
    "– Windows & exterior sheathing — flashing, waterproofing details",
    "– Fireblocking and draft stopping in required locations",
]
PHASE_4_CALLOUT = (
    "This inspection typically costs $350–$500. It has saved buyers tens of thousands in "
    "repairs that would have been invisible — and uncoverable — after closing."
)

PHASE_5_INTRO = (
    "The final walkthrough is your last opportunity to document issues before you own them. "
    "Never waive it. Never rush it. Never accept verbal assurances that something will be fixed "
    "after closing."
)
PHASE_5_BULLETS = [
    "– Every door and window — open, close, lock, and check for gaps",
    "– All outlets and switches — test every single one",
    "– All appliances — run a cycle on every appliance included in the contract",
    "– HVAC — run both heat and cool, check all registers for airflow",
    "– Water heater — check temperature setting and pressure relief valve",
    "– All faucets and toilets — check for leaks, proper water pressure",
    "– Garage door — test auto-reverse safety feature",
    "– Exterior — grading slopes away from foundation, no standing water",
    "– Paint — check all walls, ceilings, trim for missed spots or damage",
    "– Every item on your punch list from prior walkthroughs — confirm resolved",
]
PHASE_5_CALLOUT = (
    "Anything unresolved goes on a written punch list signed by the builder's rep before you "
    "leave the walkthrough. Get a completion date in writing."
)

# ── EDIT #3: replace warranty intro paragraph
PHASE_6_INTRO = (
    "Most Texas builders provide limited workmanship and structural warranties, often backed by "
    "third-party warranty providers. Coverage terms, exclusions, and durations vary by builder "
    "and contract. Always review your warranty documents carefully and keep copies of everything "
    "provided at closing."
)
PHASE_6_TABLE_ROWS = [
    ("Workmanship & materials", "1 year"),
    ("Plumbing, electrical, HVAC systems", "2 years"),
    ("Structural defects", "10 years"),
]
PHASE_6_BULLETS = [
    "– Document and submit ALL warranty claims in writing — never verbal only",
    "– Photograph every issue before it's repaired",
    # ── EDIT #4
    "– Keep records of all warranty communications, repair requests, and response timelines",
    # ── EDIT #5
    "– Before your structural warranty expires, consider a professional inspection to "
    "identify issues while coverage may still apply",
]

BONUS_INTRO = (
    "Most disputes between buyers and builders come down to one thing: who said what, and when. "
    "The buyer rarely wins without a paper trail."
)
BONUS_BULLETS = [
    "– Create a dedicated folder (phone, cloud, or both) labeled with your address",
    "– Every email, text, or written communication with the builder goes in the folder",
    "– Date-stamp every photo — turn on location tagging if you're comfortable with it",
    "– After every site visit or meeting, send a brief follow-up email summarizing what was discussed",
    "– Keep your original contract, all addenda, and every change order together",
    "– Save inspection reports with photos in the same folder",
    "– When something is promised verbally, follow up in writing: "
    "'Just confirming our conversation...'",
]
BONUS_CALLOUT = (
    "This folder becomes your entire case if something goes wrong — and your peace of mind "
    "when it doesn't."
)


# ---------------------------------------------------------------------------
# Page composition
# ---------------------------------------------------------------------------

def compose_intro_page(c: canvas.Canvas) -> None:
    """Page 2 — About this guide / What's inside.

    Layout is cursor-driven so the new paragraph from Edit #6 cleanly pushes
    the 'Already signed?' callout and the 'WHAT'S INSIDE' list down without
    colliding."""
    draw_body_chrome(c, page_num=1)

    # 'ABOUT THIS GUIDE' eyebrow + headline (fixed at top of page)
    c.setFillColor(SAGE)
    c.setFont("Helvetica-Bold", 9.0)
    c.drawString(LEFT_TEXT_X, PAGE_H - 97.40, "ABOUT THIS GUIDE")
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 16.0)
    c.drawString(LEFT_TEXT_X, PAGE_H - 120.40,
                 "The truth about new builds in North Texas")

    # Body paragraphs (3 after Edit #6 — original had 2)
    y_text = 142.90
    line_h = 16.0
    para_gap = 6.0
    for para in ABOUT_INTRO_PARAGRAPHS:
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica", 10.5)
        for line in wrap_text(c, para, "Helvetica", 10.5,
                              RIGHT_TEXT_X - LEFT_TEXT_X):
            c.drawString(LEFT_TEXT_X, PAGE_H - y_text, line)
            y_text += line_h
        y_text += para_gap

    # 'Already signed?' callout — mist rectangle, sized to actual text height.
    callout_top = y_text + 14.0
    rect_top_pad = 8.0
    rect_bot_pad = 9.0
    italic_line_h = 15.0

    # Pre-compute layout: bold lead-in + a leading space + italic body, wrapped.
    bold_w = c.stringWidth(ALREADY_SIGNED_BOLD, "Helvetica-BoldOblique", 10.5)
    space_w = c.stringWidth(" ", "Helvetica-Oblique", 10.5)
    body_text = ALREADY_SIGNED_BODY.lstrip()  # we render the leading space explicitly
    # First line gets the residual width after bold + one space; continuation
    # lines get the full row width.
    text_left  = 60.80
    text_right = 552.0
    first_max = text_right - (text_left + bold_w + space_w)
    cont_max  = text_right - text_left
    rest_lines = wrap_text_two_widths(c, body_text, "Helvetica-Oblique", 10.5,
                                      first_max, cont_max)
    n_lines = max(1, len(rest_lines))
    rect_h = rect_top_pad + 14.22 + italic_line_h * (n_lines - 1) + rect_bot_pad

    # Mist background
    rl_y_bot = PAGE_H - (callout_top + rect_h)
    c.setFillColor(MIST)
    c.rect(46.80, rl_y_bot, 565.20 - 46.80, rect_h, fill=1, stroke=0)

    # Bold lead-in (sage, BoldOblique)
    c.setFillColor(SAGE)
    c.setFont("Helvetica-BoldOblique", 10.5)
    base_y = callout_top + rect_top_pad + 11.23
    c.drawString(text_left, PAGE_H - base_y, ALREADY_SIGNED_BOLD)
    # First italic line offset by bold + a real space character
    c.setFont("Helvetica-Oblique", 10.5)
    if rest_lines:
        c.drawString(text_left + bold_w, PAGE_H - base_y, " " + rest_lines[0])
        next_y = base_y + italic_line_h
        for ln in rest_lines[1:]:
            c.drawString(text_left, PAGE_H - next_y, ln)
            next_y += italic_line_h

    # ‘WHAT'S INSIDE' — placed dynamically below the callout (with breathing room)
    inside_y = callout_top + rect_h + 28.0
    c.setFillColor(SAGE)
    c.setFont("Helvetica-Bold", 9.0)
    c.drawString(LEFT_TEXT_X, PAGE_H - inside_y, "WHAT'S INSIDE")

    # Phase list — 22pt spacing between items per probe
    item_y = inside_y + 17.5
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica", 10.5)
    for label in WHATS_INSIDE_ITEMS:
        c.drawString(LEFT_TEXT_X, PAGE_H - item_y, label)
        item_y += 22.0


def wrap_text_two_widths(c, text, font, size, max_w_first, max_w_cont):
    """First line gets max_w_first, rest get max_w_cont."""
    words = text.split(" ")
    lines: list[str] = []
    current = ""
    is_first = True
    for w in words:
        max_w = max_w_first if is_first else max_w_cont
        candidate = (current + " " + w) if current else w
        if c.stringWidth(candidate, font, size) <= max_w:
            current = candidate
        else:
            if current:
                lines.append(current)
                is_first = False
            current = w
    if current:
        lines.append(current)
    return lines


def render_blocks(c: canvas.Canvas, blocks: Iterable[Block], y_start: float) -> float:
    y = y_start
    for blk in blocks:
        y = blk.draw(c, y)
    return y


def compose_phase_1_and_2(c: canvas.Canvas) -> None:
    """Page 3 — Phase 1 + Phase 2."""
    draw_body_chrome(c, page_num=2)
    blocks: list[Block] = [
        PhasePill(label="PHASE 1  ·  BEFORE YOU SIGN: CONTRACT REVIEW"),
        Paragraph(text=PHASE_1_INTRO),
        Subhead(text="What to review before signing:"),
        BulletList(items=PHASE_1_BULLETS),
        Callout(text=PHASE_1_CALLOUT),
        PhasePill(label="PHASE 2  ·  LOT & PRE-CONSTRUCTION", margin_top=2),
        Paragraph(text=PHASE_2_INTRO),
        Subhead(text="Actions to take before the slab is poured:"),
        BulletList(items=PHASE_2_BULLETS),
    ]
    render_blocks(c, blocks, y_start=74.40)


def compose_phase_3_and_4(c: canvas.Canvas) -> None:
    """Page 4 — Phase 3 + Phase 4."""
    draw_body_chrome(c, page_num=3)
    blocks: list[Block] = [
        PhasePill(label="PHASE 3  ·  DURING THE BUILD: MILESTONE INSPECTIONS"),
        Paragraph(text=PHASE_3_INTRO),
        Subhead(text="The three milestones that matter most:"),
        BulletList(items=PHASE_3_MILESTONES),
        Subhead(text="General inspection rules:", margin_top=8.0),
        BulletList(items=PHASE_3_RULES),
        PhasePill(label="PHASE 4  ·  PRE-DRYWALL: THE ONE YOU CAN’T SKIP",
                  margin_top=2),
        Paragraph(text=PHASE_4_INTRO),
        Subhead(text="What a qualified inspector checks pre-drywall:"),
        BulletList(items=PHASE_4_BULLETS),
        Callout(text=PHASE_4_CALLOUT),
    ]
    render_blocks(c, blocks, y_start=74.40)


def compose_phase_5(c: canvas.Canvas) -> None:
    """Page 5 — Phase 5 alone (Phase 6 promoted to its own page to absorb
    the longer warranty paragraph from Edit #3 and Edit #5)."""
    draw_body_chrome(c, page_num=4)
    blocks: list[Block] = [
        PhasePill(label="PHASE 5  ·  FINAL WALKTHROUGH: NEVER WAIVE THIS"),
        Paragraph(text=PHASE_5_INTRO),
        Subhead(text="Walkthrough checklist — room by room:"),
        BulletList(items=PHASE_5_BULLETS),
        Callout(text=PHASE_5_CALLOUT),
    ]
    render_blocks(c, blocks, y_start=74.40)


def compose_phase_6(c: canvas.Canvas) -> None:
    """Page 6 — Phase 6 alone (warranty)."""
    draw_body_chrome(c, page_num=5)
    blocks: list[Block] = [
        PhasePill(label="PHASE 6  ·  POST-CLOSE WARRANTY: KNOW YOUR RIGHTS"),
        Paragraph(text=PHASE_6_INTRO),
        WarrantyTable(rows=PHASE_6_TABLE_ROWS),
        BulletList(items=PHASE_6_BULLETS, margin_top=8.0),
    ]
    render_blocks(c, blocks, y_start=74.40)


def compose_bonus(c: canvas.Canvas) -> None:
    """Page 7 — Bonus + sage CTA section.

    All vertical positions match the original probe exactly — no content edits
    target this page, so we use fixed coordinates rather than the cursor-based
    layout used elsewhere."""
    draw_body_chrome(c, page_num=6)

    # Bonus eyebrow (gold) + large charcoal headline
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(LEFT_TEXT_X, PAGE_H - 94.90, "BONUS")
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 16.0)
    c.drawString(LEFT_TEXT_X, PAGE_H - 116.40,
                 "The Documentation Habit That Saves Everything")

    # Intro paragraph — wrapped, baseline at y=138.90 (probe)
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica", 10.5)
    y_text = 138.90
    for line in wrap_text(c, BONUS_INTRO, "Helvetica", 10.5,
                          RIGHT_TEXT_X - LEFT_TEXT_X):
        c.drawString(LEFT_TEXT_X, PAGE_H - y_text, line)
        y_text += 16.0

    # Subhead at fixed y=176.90 (probe)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(LEFT_TEXT_X, PAGE_H - 176.90, "Build your file from day one:")

    # Bullets at fixed y, 19pt spacing, starting at y=196.90 (probe)
    bullet_y = 196.90
    c.setFont("Helvetica", 10.5)
    for item in BONUS_BULLETS:
        # Wrap honoring hanging indent
        lines = wrap_text_hanging(c, item, "Helvetica", 10.5,
                                  RIGHT_TEXT_X - BULLET_INDENT_X,
                                  RIGHT_TEXT_X - BULLET_HANG_X)
        for i, ln in enumerate(lines):
            x = BULLET_INDENT_X if i == 0 else BULLET_HANG_X
            c.drawString(x, PAGE_H - bullet_y, ln)
            if i < len(lines) - 1:
                bullet_y += 15.0
        bullet_y += 19.0

    # Bonus callout — fixed mist rectangle at y=330.20..363.20 (probe)
    c.setFillColor(MIST)
    c.rect(46.80, PAGE_H - 363.20, 565.20 - 46.80, 363.20 - 330.20,
           fill=1, stroke=0)
    # Italic sage text inside the callout, baseline at y=349.70 (probe)
    c.setFillColor(SAGE)
    c.setFont("Helvetica-Oblique", 10.5)
    c.drawString(60.80, PAGE_H - 349.70, BONUS_CALLOUT)

    # CTA section (sage box + headline + body) — fixed coords from probe
    draw_cta_section(c, top_y=330.20)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

DEFAULT_OUT = (Path(r"C:/Users/aserc/Desktop/Alan AI Stack/Veritas AI Partners/"
                    r"lorettasercy.com")
               / "NewBuildProtectionGuide_MoveWithClarity_v2.pdf")


def build(out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out_path), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("New Build Protection Guide")
    c.setAuthor("Loretta Sercy, Realtor® — eXp Realty")
    c.setSubject("Texas New Construction Buyer Guide")
    c.setKeywords("MoveWithClarity, new build, Texas, real estate")

    # Page 1 — cover
    draw_cover(c)
    c.showPage()

    # Page 2 — intro / TOC
    compose_intro_page(c)
    c.showPage()

    # Page 3 — Phase 1 + Phase 2
    compose_phase_1_and_2(c)
    c.showPage()

    # Page 4 — Phase 3 + Phase 4
    compose_phase_3_and_4(c)
    c.showPage()

    # Page 5 — Phase 5 (alone — Phase 6 promoted to its own page to absorb
    # the longer warranty paragraph from Edit #3)
    compose_phase_5(c)
    c.showPage()

    # Page 6 — Phase 6
    compose_phase_6(c)
    c.showPage()

    # Page 7 — Bonus + CTA
    compose_bonus(c)
    c.showPage()

    c.save()


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    build(out)
    print(f"Wrote: {out}")

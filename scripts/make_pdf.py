"""Generate submission PDFs from markdown sources using reportlab only.

Usage:  python scripts/make_pdf.py submission/blog.md submission/blog.pdf
        python scripts/make_pdf.py concept_summary.md submission/concept_summary.pdf

Supports: #/##/### headings, **bold** inline, bullet/numbered lists,
blockquotes (>), inline code and fenced code, paragraph breaks,
and simple horizontal rules. Everything else is folded into paragraphs.
"""
import re
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer,
                                HRFlowable)


def parse(src):
    out = []
    for raw in src.splitlines():
        line = raw.rstrip("\n")
        if not line.strip():
            continue
        code = re.match(r"^(\s*)(`{3}|`)(.*)$", line)
        if code and code.group(2) == "```":
            if out and isinstance(out[-1], tuple) and out[-1][0] == "code":
                out.pop()
            else:
                out.append(("code", ""))
            continue
        if re.match(r"^\s*>", line):
            out.append(("quote", re.sub(r"^\s*>\s?", "", line)))
            continue
        if re.match(r"^\s*[-*]\s+", line):
            out.append(("bullet", re.sub(r"^\s*[-*]\s+", "", line)))
            continue
        if re.match(r"^\s*\d+\.\s+", line):
            out.append(("num", re.sub(r"^\s*\d+\.\s+", "", line)))
            continue
        if re.match(r"^\s*#{1,6}\s", line):
            level = len(re.match(r"^\s*(#+)", line).group(1))
            out.append(("h%d" % min(level, 3),
                        re.sub(r"^\s*#+\s*", "", line)))
            continue
        if re.match(r"^\s*(\*\*\*|---|___)\s*\n?$", line) or \
                re.match(r"^\s*(-{3,}|={3,}|~{3,})\s*$", line):
            out.append(("rule", line))
            continue
        out.append(("p", line))
    return out


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(t, bold_re=r"\*\*(.+?)\*\*"):
    t = re.sub(r"(?<!`)``?([^`])``?(?!`)", r"\1", t)
    parts = re.split(bold_re, t)
    if len(parts) == 1:
        return esc(parts[0])
    out, i = [], 0
    for i in range(0, len(parts) - 1, 2):
        out.append(esc(parts[i]))
        out.append("<b>%s</b>" % esc(parts[i + 1]))
    out.append(esc(parts[-1]))
    return "".join(out)


STYLES = {
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=17,
                         leading=21, spaceBefore=14, spaceAfter=4,
                         alignment=TA_LEFT, textColor=colors.HexColor("#111")),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=13,
                         leading=16, spaceBefore=10, spaceAfter=3,
                         textColor=colors.HexColor("#222")),
    "h3": ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=11,
                         leading=14, spaceBefore=8, spaceAfter=2,
                         textColor=colors.HexColor("#333")),
    "p": ParagraphStyle("p", fontName="Helvetica", fontSize=10,
                        leading=14, spaceAfter=6),
    "quote": ParagraphStyle("quote", fontName="Helvetica-Oblique",
                            fontSize=10, leading=14, leftIndent=16,
                            spaceAfter=6, textColor=colors.HexColor("#222")),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=10,
                             leading=14, leftIndent=18, bulletIndent=4,
                             spaceAfter=3),
    "num": ParagraphStyle("num", fontName="Helvetica", fontSize=10,
                          leading=14, leftIndent=18, spaceAfter=3),
    "code": ParagraphStyle("code", fontName="Courier", fontSize=8.5,
                           leading=11, leftIndent=12, backColor=colors.HexColor("#f4f4f4"), spaceAfter=6),
}


def main(src, dst, title=None):
    doc = SimpleDocTemplate(dst, pagesize=letter,
                            leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                            topMargin=0.8 * inch, bottomMargin=0.8 * inch,
                            title=title or src)
    story, codebox = [], []
    for kind, text in parse(open(src, encoding="utf-8").read()):
        if kind == "code":
            codebox = [" " * 0 + l for l in text.splitlines()] if text else []
            for ln in codebox:
                story.append(Paragraph(esc(ln), STYLES["code"]))
            continue
        if kind == "rule":
            story.append(Spacer(1, 6))
            story.append(HRFlowable(width="100%", thickness=0.5,
                                    color=colors.grey))
            story.append(Spacer(1, 6))
            continue
        if kind == "bullet":
            story.append(Paragraph(render(text), STYLES["bullet"],
                                   bulletText="\u2022"))
            continue
        if kind == "num":
            story.append(Paragraph(render(text), STYLES["num"],
                                   bulletText="\u2022"))
            continue
        style = STYLES.get(kind, STYLES["p"])
        if kind.startswith("h"):
            story.append(Paragraph(render(text), style))
        else:
            story.append(Paragraph(render(text), style))
    doc.build(story)
    print(f"wrote {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        raise SystemExit(1)
    main(sys.argv[1], sys.argv[2])
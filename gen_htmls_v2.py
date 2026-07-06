#!/usr/bin/env python3
"""
Generates print-ready A4 HTML manuals for ES, EN, NL from Markdown sources.
v2: Minimal page breaks (only between main color categories), no browser header/footer,
compact layout targeting ~18 pages.
"""

import re

def read_md(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


# ============================================================
#  Language-specific content for title page
# ============================================================
VERSIONS = {
    "es": {
        "lang": "es",
        "title": 'EL MANUAL DEL<br>"GUERRERO BONT"',
        "subtitle": "DHL TIEL",
        "tagline": "Logística de Clase Mundial: De Operario a Maestro del Proceso",
        "version_text": "VERSIÓN 0.1 — BORRADOR PERSONAL",
        "author": "Boris Orlando Antequera Vargas",
        "role": "Operador BONT con interés en desarrollo y optimización de procesos",
        "quote": "\"Conocimiento compartido es eficiencia multiplicada.\"",
        "date_location": "Mayo 2026 — DHL Tiel, Sección BONT",
        "disclaimer": "Uso personal. No oficial. No distribuido por DHL.",
        "page_footer": "Manual del Guerrero BONT – v0.1 (Borrador no oficial)",
    },
    "en": {
        "lang": "en",
        "title": 'THE<br>"BONT WARRIOR" MANUAL',
        "subtitle": "DHL TIEL",
        "tagline": "World-Class Logistics: From Operator to Process Master",
        "version_text": "VERSION 0.1 — PERSONAL DRAFT",
        "author": "Boris Orlando Antequera Vargas",
        "role": "BONT Operator with interest in development and process optimization",
        "quote": "\"Shared knowledge is multiplied efficiency.\"",
        "date_location": "May 2026 — DHL Tiel, BONT Section",
        "disclaimer": "Personal use. Not official. Not distributed by DHL.",
        "page_footer": "BONT Warrior Manual – v0.1 (Unofficial draft)",
    },
    "nl": {
        "lang": "nl",
        "title": 'HET<br>"BONT KRIJGER" HANDBOEK',
        "subtitle": "DHL TIEL",
        "tagline": "Wereldklasse Logistiek: Van Operator tot Processmeester",
        "version_text": "VERSIE 0.1 — PERSOONLIJK CONCEPT",
        "author": "Boris Orlando Antequera Vargas",
        "role": "BONT-Operator met interesse in ontwikkeling en procesoptimalisatie",
        "quote": "\"Gedeelde kennis is vermenigvuldigde efficiëntie.\"",
        "date_location": "Mei 2026 — DHL Tiel, BONT Sectie",
        "disclaimer": "Persoonlijk gebruik. Niet officieel. Niet verspreid door DHL.",
        "page_footer": "BONT Krijger Handboek – v0.1 (Niet-officieel concept)",
    },
}


# ============================================================
#  Category definitions for page-break logic
#  These are the h2 headers that should start on a new page.
# ============================================================
CATEGORY_TRIGGERS = [
    "🔴 CATEGORÍA ROJA", "🔴 RED CATEGORY", "🔴 RODE CATEGORIE",
    "🟡 CATEGORÍA AMARILLA", "🟡 YELLOW CATEGORY", "🟡 GELE CATEGORIE",
    "🟢 CATEGORÍA VERDE", "🟢 GREEN CATEGORY", "🟢 GROENE CATEGORIE",
    "🟠 CATEGORÍA NARANJA", "🟠 ORANGE CATEGORY", "🟠 ORANJE CATEGORIE",
    "🔵 CATEGORÍA AZUL", "🔵 BLUE CATEGORY", "🔵 BLAUWE CATEGORIE",
    "🟣 CATEGORÍA MORADA", "🟣 PURPLE CATEGORY", "🟣 PAARSE CATEGORIE",
]


def is_page_break_trigger(h2_text):
    """Returns True if this h2 should start on a new page."""
    upper = h2_text.upper()
    for trigger in CATEGORY_TRIGGERS:
        if trigger.upper() in upper:
            return True
    return False


def get_section_class(content):
    """Detect category from emoji and return CSS class name."""
    is_cat = "CATEGOR" in content.upper() or "CATEGORIE" in content.upper()
    if "🔴" in content and is_cat:   return "section-red"
    if "🟡" in content and is_cat:   return "section-yellow"
    if "🟢" in content and is_cat:   return "section-green"
    if "🟠" in content and is_cat:   return "section-orange"
    if "🔵" in content and is_cat:   return "section-blue"
    if "🟣" in content and (is_cat or "Categorie" in content or "Categoria" in content):
        return "section-purple"
    if "COMPROMISO" in content.upper() or "COMMITMENT" in content.upper() or "TOEWIJDING" in content.upper():
        return "section-commitment"
    return ""


def md_to_html_body(md_text):
    """Convert markdown body (after front-matter) to HTML."""
    lines = md_text.split("\n")
    result = []
    in_table = False
    table_rows = []
    in_ul = False
    in_ol = False
    in_code = False
    first_h2_added = False  # Track if we've already added the automatic h2 page-break

    # Find content start (skip h1, h2, ---)
    start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("---") and i > 1:
            start = i + 1
            break

    i = start
    while i < len(lines):
        line = lines[i]

        # ---- CODE BLOCKS ----
        if line.strip().startswith("```"):
            if in_code:
                result.append("</code></pre>\n")
                in_code = False
            else:
                result.append("<pre><code>")
                in_code = True
            i += 1
            continue
        if in_code:
            escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            result.append("\n" + escaped if result[-1].endswith(">") else escaped)
            i += 1
            continue

        # ---- CLOSE TABLE ----
        if in_table:
            if not line.startswith("|"):
                in_table = False
                result.append(build_table_html(table_rows))
                table_rows = []

        # ---- TABLE ----
        if line.startswith("|"):
            parts = [p.strip() for p in line.split("|") if p.strip()]
            # skip separator rows (|---|:---:|---|)
            if all(p.replace("-", "").replace(":", "").strip() == "" for p in parts):
                if not in_table:
                    in_table = True
                    table_rows = []
                i += 1
                continue
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(parts)
            i += 1
            continue

        # ---- HORIZONTAL RULE ----
        if line.strip() == "---":
            if in_ul:
                result.append("</ul>\n"); in_ul = False
            if in_ol:
                result.append("</ol>\n"); in_ol = False
            result.append("<hr>\n")
            i += 1
            continue

        # ---- HEADERS ----
        hm = re.match(r"^(#{1,3})\s+(.+)$", line)
        if hm:
            level = len(hm.group(1))
            content = hm.group(2)
            cclass = get_section_class(content)

            # Close open lists
            if in_ul: result.append("</ul>\n"); in_ul = False
            if in_ol: result.append("</ol>\n"); in_ol = False

            # Insert page breaks only before category h2 headers
            if level == 2 and is_page_break_trigger(content):
                # Skip page-break for the FIRST h2 (usually disclaimer/rules block)
                # Don't skip any — but only add page-break for category triggers
                result.append('<div class="page-break"></div>\n')
                first_h2_added = True

            if cclass:
                result.append(f'<h{level} class="{cclass}">{content}</h{level}>\n')
            else:
                result.append(f"<h{level}>{content}</h{level}>\n")
            i += 1
            continue

        # ---- CLOSE LISTS ON NON-LIST ITEMS ----
        if in_ul and not line.startswith("-"):
            result.append("</ul>\n"); in_ul = False
        if in_ol and not re.match(r"^\d+\.", line):
            result.append("</ol>\n"); in_ol = False

        # ---- CHECKLIST ----
        cm = re.match(r"^- \[([ x])\]\s+(.*)", line)
        if cm:
            chk = "☑ " if cm.group(1) == "x" else "☐ "
            result.append(f'<p class="checklist-item">{chk}{cm.group(2)}</p>\n')
            i += 1
            continue

        # ---- UNORDERED LIST ----
        um = re.match(r"^-\s+(.*)", line)
        if um:
            if not in_ul:
                result.append("<ul>\n")
                in_ul = True
            result.append(f"<li>{um.group(1)}</li>\n")
            i += 1
            continue

        # ---- ORDERED LIST ----
        om = re.match(r"^\d+\.\s+(.*)", line)
        if om:
            if not in_ol:
                result.append("<ol>\n")
                in_ol = True
            result.append(f"<li>{om.group(1)}</li>\n")
            i += 1
            continue

        # ---- EMPTY LINE ----
        if line.strip() == "":
            i += 1
            continue

        # ---- BLOCKQUOTE ----
        if line.startswith(">"):
            txt = line[1:].strip()
            result.append(f"<blockquote>{txt}</blockquote>\n")
            i += 1
            continue

        # ---- BOLD-ONLY PARAGRAPH ----
        bm = re.match(r"^\*\*(.+)\*\*$", line)
        if bm:
            result.append(f"<p><strong>{bm.group(1)}</strong></p>\n")
            i += 1
            continue

        # ---- REGULAR PARAGRAPH ----
        result.append(f"<p>{line}</p>\n")
        i += 1

    # Close leftover tags
    if in_table and table_rows:
        result.append(build_table_html(table_rows))
    if in_ul:
        result.append("</ul>\n")
    if in_ol:
        result.append("</ol>\n")

    return "".join(result)


def build_table_html(rows):
    if not rows:
        return ""
    html = "<table>\n"
    has_header = len(rows) > 1
    if has_header:
        html += "<thead><tr>\n"
        for c in rows[0]:
            html += f"<th>{c}</th>\n"
        html += "</tr></thead>\n<tbody>\n"
        for row in rows[1:]:
            html += "<tr>\n"
            for c in row:
                html += f"<td>{c}</td>\n"
            html += "</tr>\n"
        html += "</tbody>\n</table>\n"
    else:
        # Single row = no header
        html += "<tbody>\n<tr>\n"
        for c in rows[0]:
            html += f"<td>{c}</td>\n"
        html += "</tr>\n</tbody>\n</table>\n"
    return html


def generate_html(lang_key, md_text):
    v = VERSIONS[lang_key]
    body = md_to_html_body(md_text)
    clean_title = v["title"].replace("<br>", " ")

    css = f"""
  @page {{
    size: A4;
    margin: 12mm 14mm 16mm 14mm;
    @bottom-center {{
      content: "{v['page_footer']} – Pág. " counter(page);
      font-size: 7.5pt;
      color: #888;
      font-family: "Segoe UI", Arial, sans-serif;
    }}
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: "Segoe UI", Arial, sans-serif; font-size: 8.5pt; line-height: 1.35; color: #1a1a1a; }}
  .page-break {{ page-break-before: always; }}

  /* title page */
  .title-page {{
    text-align: center;
    padding-top: 60px;
    page-break-after: always;
  }}
  .title-page .shield {{ font-size: 60pt; margin-bottom: 8px; }}
  .title-page h1 {{
    font-size: 24pt; color: #c00; margin-bottom: 6px;
    letter-spacing: 1px; line-height: 1.15;
  }}
  .title-page h2 {{ font-size: 12pt; color: #444; font-weight: normal; margin-bottom: 8px; }}
  .title-page .tagline {{ font-size: 10pt; color: #666; margin-bottom: 30px; font-style: italic; }}
  .title-page .badge {{
    display: inline-block; background: #c00; color: #fff;
    padding: 6px 24px; font-size: 10pt; font-weight: bold;
    border-radius: 4px; margin-bottom: 30px; letter-spacing: 1px;
  }}
  .title-page .author {{ font-size: 9pt; color: #555; margin-top: 20px; }}
  .title-page .role {{ font-size: 8.5pt; color: #888; margin-top: 3px; }}
  .title-page .quote {{ font-style: italic; color: #888; margin-top: 35px; font-size: 9pt; }}
  .title-page .footer-info {{ margin-top: 40px; font-size: 8pt; color: #aaa; line-height: 1.6; }}
  .title-divider {{ width: 60%; margin: 16px auto; border: none; border-top: 1.5px solid #ddd; }}
  .title-divider.thick {{ border-top: 3px solid #c00; width: 40%; }}

  /* headings */
  h2 {{
    font-size: 11pt; color: #c00;
    border-bottom: 1.5px solid #c00; padding-bottom: 2px;
    margin-top: 10px; margin-bottom: 4px;
    page-break-after: avoid;
  }}
  h3 {{ font-size: 9.5pt; color: #333; margin-top: 7px; margin-bottom: 3px; page-break-after: avoid; }}
  h4 {{ font-size: 9pt; color: #555; margin-top: 5px; margin-bottom: 2px; }}

  /* tables */
  table {{
    width: 100%; border-collapse: collapse;
    margin: 4px 0 6px 0; font-size: 7.5pt;
    page-break-inside: avoid;
  }}
  th {{ background: #c00; color: #fff; padding: 2px 5px; text-align: left; font-weight: 600; }}
  td {{ padding: 2px 5px; border: 1px solid #ccc; vertical-align: top; }}
  tr:nth-child(even) td {{ background: #fafafa; }}

  /* lists */
  ul, ol {{ margin: 3px 0 5px 18px; }}
  li {{ margin-bottom: 1px; }}
  .checklist-item {{ margin: 1px 0; font-size: 8pt; }}

  /* code */
  pre {{ background: #f5f5f5; border: 1px solid #ddd; border-radius: 3px; padding: 5px 8px; font-size: 7.5pt; overflow-x: auto; white-space: pre-wrap; }}
  code {{ background: #f4f4f4; padding: 1px 3px; border-radius: 2px; font-size: 7.5pt; font-family: "Courier New", monospace; }}

  /* section colors */
  .section-red {{ border-left: 3px solid #c62828; padding-left: 8px; margin-top: 6px; }}
  .section-yellow {{ border-left: 3px solid #f57f17; padding-left: 8px; margin-top: 6px; }}
  .section-green {{ border-left: 3px solid #2e7d32; padding-left: 8px; margin-top: 6px; }}
  .section-orange {{ border-left: 3px solid #bf360c; padding-left: 8px; margin-top: 6px; }}
  .section-blue {{ border-left: 3px solid #1565c0; padding-left: 8px; margin-top: 6px; }}
  .section-purple {{ border-left: 3px solid #7b1fa2; padding-left: 8px; margin-top: 6px; }}

  hr {{ border: none; border-top: 1px solid #ddd; margin: 8px 0; }}

  blockquote {{
    background: #f9f9f9; border-left: 3px solid #ccc;
    padding: 4px 10px; margin: 4px 0; font-style: italic; color: #555; font-size: 8pt;
  }}

  @media print {{
    body {{ font-size: 8pt; }}
    h2, h3, h4 {{ page-break-after: avoid; }}
  }}
"""

    return f"""<!DOCTYPE html>
<html lang="{v["lang"]}">
<head>
<meta charset="UTF-8">
<meta name="robots" content="noindex,nofollow">
<title>{clean_title} – DHL Tiel (v0.1)</title>
<style>
{css}
</style>
</head>
<body>

<div class="title-page">
  <div class="shield">🛡️</div>
  <hr class="title-divider thick">
  <h1>{v["title"]}</h1>
  <h2>{v["subtitle"]}</h2>
  <hr class="title-divider">
  <div class="tagline">{v["tagline"]}</div>
  <div class="badge">{v["version_text"]}</div>
  <div class="author"><strong>{v["author"]}</strong></div>
  <div class="role">{v["role"]}</div>
  <div class="quote">{v["quote"]}</div>
  <div class="footer-info">
    {v["date_location"]}<br>
    <span class="lock">🔒 {v["disclaimer"]}</span>
  </div>
</div>

{body}

</body>
</html>"""


# ============================================================
#  MAIN
# ============================================================
if __name__ == "__main__":
    base = "/home/sacharuna/.openclaw/workspace/BONT"
    sources = {
        "es": f"{base}/manual-v0.1.md",
        "en": f"{base}/manual-v0.1-en.md",
        "nl": f"{base}/manual-v0.1-nl.md",
    }

    for lang_key, src_path in sources.items():
        md = read_md(src_path)
        html = generate_html(lang_key, md)
        out_path = f"{base}/manual-v0.1-{lang_key}.html"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

        lines = html.count("\n")
        pages_est = max(1, len(html) // 2500)  # rough estimate
        print(f"{lang_key.upper()}: {len(html)/1024:.0f} KB, {lines} lines, est. ~{pages_est} pages")

    print("\n✅ DONE. All 3 HTMLs regenerated v2.")

#!/usr/bin/env python3
import re

def read_md(path):
    with open(path) as f:
        return f.read()

es_md = read_md("/home/sacharuna/dev/Bont/manual-v0.1.md")
en_md = read_md("/home/sacharuna/dev/Bont/manual-v0.1-en.md")
nl_md = read_md("/home/sacharuna/dev/Bont/manual-v0.1-nl.md")
ro_md = read_md("/home/sacharuna/dev/Bont/manual-v0.1-ro.md")

versions = {
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
        "page_footer": "Manual del Guerrero BONT \u2013 v0.1 (Borrador no oficial)",
    },
    "en": {
        "lang": "en",
        "title": 'THE<br>"BONT WARRIOR" MANUAL',
        "subtitle": "DHL TIEL",
        "tagline": "World-Class Logistics: From Operator to Process Master",
        "version_text": "VERSION 0.1 \u2014 PERSONAL DRAFT",
        "author": "Boris Orlando Antequera Vargas",
        "role": "BONT Operator with interest in development and process optimization",
        "quote": "\"Shared knowledge is multiplied efficiency.\"",
        "date_location": "May 2026 \u2014 DHL Tiel, BONT Section",
        "disclaimer": "Personal use. Not official. Not distributed by DHL.",
        "page_footer": "BONT Warrior Manual \u2013 v0.1 (Unofficial draft)",
    },
    "nl": {
        "lang": "nl",
        "title": 'HET<br>"BONT KRIJGER" HANDBOEK',
        "subtitle": "DHL TIEL",
        "tagline": "Wereldklasse Logistiek: Van Operator tot Processmeester",
        "version_text": "VERSIE 0.1 \u2014 PERSOONLIJK CONCEPT",
        "author": "Boris Orlando Antequera Vargas",
        "role": "BONT-Operator met interesse in ontwikkeling en procesoptimalisatie",
        "quote": "\"Gedeelde kennis is vermenigvuldigde effici\u00ebntie.\"",
        "date_location": "Mei 2026 \u2014 DHL Tiel, BONT Sectie",
        "disclaimer": "Persoonlijk gebruik. Niet officieel. Niet verspreid door DHL.",
        "page_footer": "BONT Krijger Handboek \u2013 v0.1 (Niet-officieel concept)",
    },
    "ro": {
        "lang": "ro",
        "title": 'MANUALUL<br>"R\u0102ZBOINICULUI BONT"',
        "subtitle": "DHL TIEL",
        "tagline": "Ligistics de Clas\u0103 Mondial\u0103: De la Operator la Maestru al Procesului",
        "version_text": "VERSIUNEA 0.1 \u2014 PROIECT PERSONAL",
        "author": "Boris Orlando Antequera Vargas",
        "role": "Operator BONT cu interes \u00een dezvoltare \u0219i optimizare procese",
        "quote": "\"Cuno\u0219tin\u021bele \u00eemp\u0103rt\u0103\u0219ite \u00eenseamn\u0103 eficien\u021b\u0103 multiplicat\u0103.\"",
        "date_location": "Mai 2026 \u2014 DHL Tiel, Sec\u021bia BONT",
        "disclaimer": "Uz personal. Neoficial. Nu este distribuit de DHL.",
        "page_footer": "Manualul R\u0103zboinicului BONT \u2013 v0.1 (Proiect neoficial)",
    }
}


def md_body_to_html(md_text):
    lines = md_text.split("\n")
    result = []
    in_table = False
    table_rows = []
    in_ul = False
    in_ol = False
    in_code = False

    # Find start after front-matter (h1, h2, ---)
    start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("---") and i > 1:
            start = i + 1
            break

    i = start
    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.strip().startswith("```"):
            if in_code:
                result.append("</code></pre>\n")
                in_code = False
            else:
                result.append("<pre><code>\n")
                in_code = True
            i += 1
            continue
        if in_code:
            result.append(line.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;") + "\n")
            i += 1
            continue

        # Close table if needed
        if in_table:
            if not line.startswith("|"):
                in_table = False
                html_t = "<table>\n"
                for idx, row in enumerate(table_rows):
                    if idx == 0:
                        html_t += "<thead><tr>\n"
                        for c in row:
                            html_t += f"<th>{c.strip()}</th>\n"
                        html_t += "</tr></thead>\n<tbody>\n"
                    else:
                        html_t += "<tr>\n"
                        for c in row:
                            html_t += f"<td>{c.strip()}</td>\n"
                        html_t += "</tr>\n"
                if len(table_rows) > 1:
                    html_t += "</tbody>\n</table>\n"
                else:
                    html_t = html_t.replace("<thead>","").replace("</thead>","").replace("<tbody>","").replace("</tbody>","")
                    html_t = html_t.replace("<table>","<table>\n<tbody>\n").replace("</table>","\n</tbody>\n</table>\n")
                result.append(html_t)
                table_rows = []

        # Table detection
        if line.startswith("|"):
            parts = [p.strip() for p in line.split("|") if p.strip()]
            # Skip separator rows
            if all(p.replace("-","").replace(":","").strip() == "" for p in parts):
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

        # Horizontal rule
        if line.strip() == "---":
            result.append("<hr>\n")
            i += 1
            continue

        # Headers
        hm = re.match(r"^(#{1,3})\s+(.+)$", line)
        if hm:
            level = len(hm.group(1))
            content = hm.group(2)
            is_cat = "CATEGOR" in content.upper() or "CATEGORIE" in content.upper()
            cclass = ""
            if "🔴" in content and is_cat:
                cclass = ' class="section-red"'
            elif "🟡" in content and is_cat:
                cclass = ' class="section-yellow"'
            elif "🟢" in content and is_cat:
                cclass = ' class="section-green"'
            elif "🟠" in content and is_cat:
                cclass = ' class="section-orange"'
            elif "🔵" in content and is_cat:
                cclass = ' class="section-blue"'
            elif "🟣" in content and (is_cat or "Categorie" in content or "Categoria" in content):
                cclass = ' class="section-purple"'

            if level == 2:
                result.append('<div class="page-break"></div>\n')
            result.append(f"<h{level}{cclass}>{content}</h{level}>\n")
            i += 1
            continue

        # Checklist
        cm = re.match(r"^- \[([ x])\]\s+(.*)", line)
        if cm:
            chk = "☑ " if cm.group(1) == "x" else "☐ "
            result.append(f'<p class="checklist-item">{chk}{cm.group(2)}</p>\n')
            i += 1
            continue

        # Unordered list
        um = re.match(r"^-\s+(.*)", line)
        if um:
            if not in_ul:
                result.append("<ul>\n")
                in_ul = True
            result.append(f"<li>{um.group(1)}</li>\n")
            i += 1
            continue
        if in_ul:
            result.append("</ul>\n")
            in_ul = False

        # Ordered list
        om = re.match(r"^\d+\.\s+(.*)", line)
        if om:
            if not in_ol:
                result.append("<ol>\n")
                in_ol = True
            result.append(f"<li>{om.group(1)}</li>\n")
            i += 1
            continue
        if in_ol:
            result.append("</ol>\n")
            in_ol = False

        # Empty line
        if line.strip() == "":
            i += 1
            continue

        # Blockquote
        if line.startswith(">"):
            txt = line[1:].strip()
            result.append(f"<blockquote>{txt}</blockquote>\n")
            i += 1
            continue

        # Bold-only line
        bm = re.match(r"^\*\*(.+)\*\*$", line)
        if bm:
            result.append(f"<p><strong>{bm.group(1)}</strong></p>\n")
            i += 1
            continue

        # Regular paragraph
        result.append(f"<p>{line}</p>\n")
        i += 1

    # Close any remaining open tags
    if in_table and table_rows:
        html_t = "<table>\n"
        for idx, row in enumerate(table_rows):
            if idx == 0:
                html_t += "<thead><tr>\n"
                for c in row:
                    html_t += f"<th>{c.strip()}</th>\n"
                html_t += "</tr></thead>\n<tbody>\n"
            else:
                html_t += "<tr>\n"
                for c in row:
                    html_t += f"<td>{c.strip()}</td>\n"
                html_t += "</tr>\n"
        if len(table_rows) > 1:
            html_t += "</tbody>\n</table>\n"
        else:
            html_t = "<table>\n<tbody>\n<tr>\n"
            for c in table_rows[0]:
                html_t += f"<td>{c.strip()}</td>\n"
            html_t += "</tr>\n</tbody>\n</table>\n"
        result.append(html_t)
    if in_ul:
        result.append("</ul>\n")
    if in_ol:
        result.append("</ol>\n")

    return "".join(result)


def generate_html(lang_key, md_text):
    v = versions[lang_key]
    body = md_body_to_html(md_text)

    css_styles = """
  @page {
    size: A4;
    margin: 18mm 16mm 22mm 16mm;
    @bottom-center {
      content: \"""" + v["page_footer"] + """ – Pág. \" counter(page);
      font-size: 8pt;
      color: #888;
      font-family: \"Segoe UI\", Arial, sans-serif;
    }
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: \"Segoe UI\", Arial, sans-serif; font-size: 9.5pt; line-height: 1.45; color: #1a1a1a; }
  .page-break { page-break-before: always; }
  .title-page { text-align: center; padding-top: 80px; page-break-after: always; }
  .title-page .shield { font-size: 72pt; margin-bottom: 10px; }
  .title-page h1 { font-size: 28pt; color: #c00; margin-bottom: 8px; letter-spacing: 1px; line-height: 1.15; }
  .title-page h2 { font-size: 14pt; color: #444; font-weight: normal; margin-bottom: 10px; }
  .title-page .tagline { font-size: 11pt; color: #666; margin-bottom: 40px; font-style: italic; }
  .title-page .badge { display: inline-block; background: #c00; color: #fff; padding: 7px 28px; font-size: 11pt; font-weight: bold; border-radius: 4px; margin-bottom: 40px; letter-spacing: 1px; }
  .title-page .author { font-size: 10pt; color: #555; margin-top: 30px; }
  .title-page .role { font-size: 9pt; color: #888; margin-top: 4px; }
  .title-page .quote { font-style: italic; color: #888; margin-top: 50px; font-size: 10pt; }
  .title-page .footer-info { margin-top: 60px; font-size: 8.5pt; color: #aaa; line-height: 1.6; }
  .title-page .footer-info .lock { font-size: 10pt; margin-top: 8px; }
  .title-divider { width: 60%; margin: 20px auto; border: none; border-top: 1.5px solid #ddd; }
  .title-divider.thick { border-top: 3px solid #c00; width: 40%; }
  h2 { font-size: 13pt; color: #c00; border-bottom: 2px solid #c00; padding-bottom: 3px; margin-top: 16px; margin-bottom: 6px; page-break-after: avoid; }
  h3 { font-size: 11pt; color: #333; margin-top: 10px; margin-bottom: 4px; page-break-after: avoid; }
  h4 { font-size: 10pt; color: #555; margin-top: 8px; margin-bottom: 3px; }
  table { width: 100%; border-collapse: collapse; margin: 6px 0 10px 0; font-size: 8.5pt; page-break-inside: avoid; }
  th { background: #c00; color: #fff; padding: 4px 6px; text-align: left; font-weight: 600; }
  td { padding: 3px 6px; border: 1px solid #ccc; vertical-align: top; }
  tr:nth-child(even) td { background: #fafafa; }
  ul, ol { margin: 4px 0 6px 20px; }
  li { margin-bottom: 2px; }
  .checklist-item { margin: 2px 0; font-size: 9pt; }
  pre { background: #f5f5f5; border: 1px solid #ddd; border-radius: 4px; padding: 8px; font-size: 8pt; overflow-x: auto; }
  code { background: #f4f4f4; padding: 1px 4px; border-radius: 2px; font-size: 8.5pt; font-family: \"Courier New\", monospace; }
  hr { border: none; border-top: 1px solid #ddd; margin: 14px 0; }
  blockquote { background: #f9f9f9; border-left: 4px solid #ccc; padding: 6px 12px; margin: 6px 0; font-style: italic; color: #555; }
  .section-red { border-left: 4px solid #c62828; padding-left: 10px; }
  .section-yellow { border-left: 4px solid #f57f17; padding-left: 10px; }
  .section-green { border-left: 4px solid #2e7d32; padding-left: 10px; }
  .section-orange { border-left: 4px solid #bf360c; padding-left: 10px; }
  .section-blue { border-left: 4px solid #1565c0; padding-left: 10px; }
  .section-purple { border-left: 4px solid #7b1fa2; padding-left: 10px; }
  @media print { body { font-size: 9pt; } }
"""

    html_parts = []
    html_parts.append('<!DOCTYPE html>\n')
    html_parts.append(f'<html lang="{v["lang"]}">\n')
    html_parts.append('<head>\n')
    html_parts.append('<meta charset="UTF-8">\n')
    clean_title = v["title"].replace("<br>", " ")
    html_parts.append(f'<title>{clean_title} \u2013 DHL Tiel (v0.1)</title>\n')
    html_parts.append('<style>\n')
    html_parts.append(css_styles)
    html_parts.append('</style>\n')
    html_parts.append('</head>\n')
    html_parts.append('<body>\n')

    # Title page
    html_parts.append('<div class="title-page">\n')
    html_parts.append('  <div class="shield">\U0001f6e1\ufe0f</div>\n')
    html_parts.append('  <hr class="title-divider thick">\n')
    html_parts.append(f'  <h1>{v["title"]}</h1>\n')
    html_parts.append(f'  <h2>{v["subtitle"]}</h2>\n')
    html_parts.append('  <hr class="title-divider">\n')
    html_parts.append(f'  <div class="tagline">{v["tagline"]}</div>\n')
    html_parts.append(f'  <div class="badge">{v["version_text"]}</div>\n')
    html_parts.append(f'  <div class="author"><strong>{v["author"]}</strong></div>\n')
    html_parts.append(f'  <div class="role">{v["role"]}</div>\n')
    html_parts.append(f'  <div class="quote">{v["quote"]}</div>\n')
    html_parts.append('  <div class="footer-info">\n')
    html_parts.append(f'    {v["date_location"]}<br>\n')
    html_parts.append(f'    <span class="lock">\U0001f512 {v["disclaimer"]}</span>\n')
    html_parts.append('  </div>\n')
    html_parts.append('</div>\n')

    html_parts.append(body)

    html_parts.append('\n</body>\n')
    html_parts.append('</html>\n')

    return "".join(html_parts)


for lang_key, md in [("es", es_md), ("en", en_md), ("nl", nl_md), ("ro", ro_md)]:
    out = f"/home/sacharuna/dev/Bont/manual-v0.1-{lang_key}.html"
    html = generate_html(lang_key, md)
    with open(out, "w") as f:
        f.write(html)
    print(f"{lang_key.upper()}: {len(html)/1024:.0f} KB, {html.count(chr(10))} lines")

print("\nDONE \U0001f389 All 4 HTMLs regenerated with PURPLE CATEGORY included.")

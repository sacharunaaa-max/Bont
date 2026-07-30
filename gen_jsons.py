#!/usr/bin/env python3
"""Generate JSON data files for all 10 languages."""
import json, os, re

BASE = "/home/sacharuna/dev/Bont"
OUT = f"{BASE}/webapp/data"
os.makedirs(OUT, exist_ok=True)

LANG_FILES = {
    "es": ("manual-v0.1.md", False),
    "en": ("manual-v0.1-en.md", False),
    "nl": ("manual-v0.1-nl.md", False),
    "pl": ("manual-v0.1-pl.md", False),
    "ro": ("manual-v0.1-ro.md", False),
    "bg": ("manual-v0.1-bg.md", False),
    "ar": ("manual-v0.1-ar.md", True),
    "fa": ("manual-v0.1-fa.md", True),
    "uk": ("manual-v0.1-uk.md", False),
    "pt": ("manual-v0.1-pt.md", False),
}

def detect_tier(t):
    u = t.upper()
    if "REGLA" in u or "GOLDEN" in u or "GULDEN" in u or "REGLAS" in u: return "rule"
    if "GLOSARIO" in u or "GLOSSARY" in u or "WOORDEN" in u: return "glossary"
    if "CHECKLIST" in u: return "checklist"
    if "FLUJO" in u or "FLOW" in u or "STROOMDIAGRAM" in u: return "flow"
    if "ÍNDICE" in u or "INDEX" in u: return "index"
    if "🔴" in u and ("CATEGOR" in u or "CATEGORIE" in u): return "red"
    if "🟡" in u and ("CATEGOR" in u or "CATEGORIE" in u): return "yellow"
    if "🟢" in u and ("CATEGOR" in u or "CATEGORIE" in u): return "green"
    if "🟠" in u and ("CATEGOR" in u or "CATEGORIE" in u): return "orange"
    if "🔵" in u and ("CATEGOR" in u or "CATEGORIE" in u): return "blue"
    if "🟣" in u and ("CATEGOR" in u or "CATEGORIE" in u): return "purple"
    if "FAQ" in u or "PREGUNTA" in u or "QUESTIONS" in u or "VRAGEN" in u: return "faq"
    if "CONTACTO" in u or "CONTACT" in u or "ZONA" in u: return "contacts"
    if "ESCENARIO" in u or "SCENARIO" in u or "SCENARIO" in u: return "scenario"
    if "COMPROMISO" in u or "COMMITMENT" in u or "TOEWIJDING" in u or "DECLARACIÓN" in u or "DECLARATION" in u or "VERKLARING" in u: return "commitment"
    if "CONTROL" in u and ("VERSIÓN" in u or "VERSION" in u or "VERSIE" in u or "DOCUMENT" in u): return "version"
    if "MULTILINGÜE" in u or "MULTILINGUAL" in u or "INTERNACIONAL" in u or "INTERNATIONAL" in u or "INTERNATIONAAL" in u: return "multilingual"
    if "VISIÓN" in u or "VISION" in u or "VISIE" in u or "MÓVIL" in u or "MOBILE" in u or "APP" in u: return "vision"
    if "TARJETAS" in u or "POCKET" in u or "ZAKKAART" in u or "BOLSILLO" in u: return "pocket"
    return "other"

def parse_md(md_text):
    lines = md_text.split("\n")
    sections = []
    cur_title = ""
    cur_content = []
    started = False
    for line in lines:
        m = re.match(r"^##\s+(.+)$", line)
        if m:
            if started and cur_title:
                sec_id = re.sub(r'[^a-z0-9]+', '-', cur_title.lower()).strip('-')
                sections.append({
                    "id": sec_id[:60],
                    "title": cur_title,
                    "tier": detect_tier(cur_title),
                    "content": "\n".join(cur_content).strip()
                })
            cur_title = m.group(1)
            cur_content = []
            started = True
        elif started:
            cur_content.append(line)
    if cur_title:
        sec_id = re.sub(r'[^a-z0-9]+', '-', cur_title.lower()).strip('-')
        sections.append({
            "id": sec_id[:60],
            "title": cur_title,
            "tier": detect_tier(cur_title),
            "content": "\n".join(cur_content).strip()
        })
    return sections

for lang, (filename, rtl) in LANG_FILES.items():
    path = f"{BASE}/{filename}"
    with open(path, encoding="utf-8") as f:
        md = f.read()
    sections = parse_md(md)
    # Get title from h1
    title_m = re.search(r"^#\s+(.+)$", md, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else "BONT"
    data = {
        "lang": lang,
        "title": title,
        "rtl": rtl,
        "sections": sections
    }
    out = f"{OUT}/{lang}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    kb = os.path.getsize(out) / 1024
    sec_count = len(sections)
    print(f"{lang}: {kb:.0f} KB, {sec_count} sections")

print("\n✅ Done. 10 JSONs created.")

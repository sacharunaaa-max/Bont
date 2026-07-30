#!/usr/bin/env python3
"""
BONT App Builder — Genera index.html + data/*.json para la webapp
"BONT · Soluciones rápidas"
"""

import json, os, re

BASE = "/home/sacharuna/dev/Bont"
OUT = f"{BASE}/webapp"
DATA = f"{OUT}/data"

os.makedirs(DATA, exist_ok=True)

# Language definitions
LANGUAGES = {
    "es": {"name": "Español", "flag": "🇪🇸", "nativeName": "Español", "rtl": False, "file": "manual-v0.1.md"},
    "en": {"name": "English", "flag": "🇬🇧", "nativeName": "English", "rtl": False, "file": "manual-v0.1-en.md"},
    "nl": {"name": "Nederlands", "flag": "🇳🇱", "nativeName": "Nederlands", "rtl": False, "file": "manual-v0.1-nl.md"},
    "pl": {"name": "Polski", "flag": "🇵🇱", "nativeName": "Polski", "rtl": False, "file": "manual-v0.1-pl.md"},
    "ro": {"name": "Română", "flag": "🇷🇴", "nativeName": "Română", "rtl": False, "file": "manual-v0.1-ro.md"},
    "bg": {"name": "Български", "flag": "🇧🇬", "nativeName": "Български", "rtl": False, "file": "manual-v0.1-bg.md"},
    "ar": {"name": "العربية", "flag": "🇸🇦", "nativeName": "العربية", "rtl": True, "file": "manual-v0.1-ar.md"},
    "fa": {"name": "فارسی", "flag": "🇮🇷", "nativeName": "فارسی", "rtl": True, "file": "manual-v0.1-fa.md"},
    "uk": {"name": "Українська", "flag": "🇺🇦", "nativeName": "Українська", "rtl": False, "file": "manual-v0.1-uk.md"},
    "pt": {"name": "Português", "flag": "🇵🇹", "nativeName": "Português", "rtl": False, "file": "manual-v0.1-pt.md"},
}

def detect_tier(h2_text):
    t = h2_text.upper()
    if "REGLA" in t or "GOLDEN" in t or "GULDEN" in t or "REGLAS" in t: return "rule"
    if "GLOSARIO" in t or "GLOSSARY" in t or "WOORDEN" in t: return "glossary"
    if "CHECKLIST" in t: return "checklist"
    if "FLUJO" in t or "FLOW" in t or "STROOM" in t: return "flow"
    if "ÍNDICE" in t or "INDEX" in t: return "index"
    if "🔴" in t and ("CATEGOR" in t or "CATEGORIE" in t): return "red"
    if "🟡" in t and ("CATEGOR" in t or "CATEGORIE" in t): return "yellow"
    if "🟢" in t and ("CATEGOR" in t or "CATEGORIE" in t): return "green"
    if "🟠" in t and ("CATEGOR" in t or "CATEGORIE" in t): return "orange"
    if "🔵" in t and ("CATEGOR" in t or "CATEGORIE" in t): return "blue"
    if "🟣" in t and ("CATEGOR" in t or "CATEGORIE" in t): return "purple"
    if "FAQ" in t or "PREGUNTA" in t or "QUESTIONS" in t or "VRAGEN" in t: return "faq"
    if "CONTACTO" in t or "CONTACT" in t or "ZONA" in t: return "contacts"
    if "ESCENARIO" in t or "SCENARIO" in t: return "scenario"
    if "COMPROMISO" in t or "COMMITMENT" in t or "TOEWIJDING" in t or "DECLARACIÓN" in t or "DECLARATION" in t: return "commitment"
    if "CONTROL" in t or "VERSIÓN" in t or "VERSION" in t or "VERSIE" in t: return "version"
    if "MULTILINGÜE" in t or "MULTILINGUAL" in t or "INTERNACIONAL" in t or "INTERNATIONAL" in t: return "multilingual"
    if "VISIÓN" in t or "VISION" in t or "VISIE" in t or "MÓVIL" in t or "MOBILE" in t: return "vision"
    if "TARJETAS" in t or "POCKET" in t or "ZAKKAART" in t: return "pocket"
    return "other"

def parse_sections(md_text):
    """Split MD into sections by h2 headers."""
    lines = md_text.split("\n")
    sections = []
    current_title = ""
    current_content = []
    started = False

    for line in lines:
        hm = re.match(r"^#{2}\s+(.+)$", line)
        if hm:
            if started and current_title:
                tier = detect_tier(current_title)
                section_id = re.sub(r'[^a-z0-9]+', '-', current_title.lower()).strip('-')
                sections.append({
                    "id": section_id,
                    "title": current_title,
                    "tier": tier,
                    "content": "\n".join(current_content).strip()
                })
            current_title = hm.group(1)
            current_content = []
            started = True
        elif started:
            current_content.append(line)

    # Last section
    if current_title:
        tier = detect_tier(current_title)
        section_id = re.sub(r'[^a-z0-9]+', '-', current_title.lower()).strip('-')
        sections.append({
            "id": section_id,
            "title": current_title,
            "tier": tier,
            "content": "\n".join(current_content).strip()
        })

    return sections

def build_json(lang_key, lang_info):
    md_path = f"{BASE}/{lang_info['file']}"
    with open(md_path, encoding="utf-8") as f:
        md_text = f.read()

    # Extract title
    title_match = re.search(r"^#\s+(.+)$", md_text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "BONT"

    sections = parse_sections(md_text)

    data = {
        "lang": lang_key,
        "nativeName": lang_info["nativeName"],
        "rtl": lang_info["rtl"],
        "title": title,
        "sections": sections
    }

    return data

# ============================================================
#  BUILD THE INDEX.HTML
# ============================================================
def build_index_html():
    lang_selector_items = ""
    for lk, li in LANGUAGES.items():
        lang_selector_items += f"""
      <button class="lang-btn" data-lang="{lk}" onclick="switchLang('{lk}')">
        <span class="lang-flag">{li['flag']}</span>
        <span class="lang-name">{li['name']}</span>
      </button>"""

    # Build the error categories for the "soluciones rápidas" screen
    # These are the color-coded error categories
    quick_categories = [
        {"emoji": "🔴", "title_es": "Error de carga física", "desc_es": "Problemas con pallets, LPNs, carga dañada o mal colocada"},
        {"emoji": "🟡", "title_es": "Error de escáner / sistema", "desc_es": "Códigos 20, 38, «No inventory found» y otros errores del sistema"},
        {"emoji": "🟢", "title_es": "Problema con etiquetas / impresora", "desc_es": "Smart Scanner, etiquetas dañadas, impresora no responde"},
        {"emoji": "🟠", "title_es": "Emergencia o error humano", "desc_es": "Leer mal, carga en zona incorrecta, accidentes"},
    ]

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex,nofollow">
<title>BONT · Soluciones rápidas</title>
<style>
  :root {{
    --dhl-red: #c00;
    --dhl-dark: #1a1a1a;
    --dhl-gray: #555;
    --dhl-light: #f5f5f5;
    --bg: #fff;
    --bg-alt: #f9f9f9;
    --text: #1a1a1a;
    --text-muted: #777;
    --border: #e0e0e0;
    --shadow: 0 2px 8px rgba(0,0,0,0.08);
    --radius: 10px;
    --sidebar-w: 260px;
    --header-h: 60px;
    --tier-red: #c62828;
    --tier-yellow: #f57f17;
    --tier-green: #2e7d32;
    --tier-orange: #bf360c;
    --tier-blue: #1565c0;
    --tier-purple: #7b1fa2;
  }}
  .dark {{
    --bg: #121212;
    --bg-alt: #1e1e1e;
    --text: #e0e0e0;
    --text-muted: #999;
    --border: #333;
    --shadow: 0 2px 8px rgba(0,0,0,0.3);
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    transition: background .3s, color .3s;
    overflow-x: hidden;
  }}

  /* ===== HEADER ===== */
  .header {{
    position: fixed; top: 0; left: 0; right: 0; height: var(--header-h);
    background: var(--bg);
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 16px; z-index: 100;
    backdrop-filter: blur(8px);
  }}
  .header-left {{
    display: flex; align-items: center; gap: 10px;
  }}
  .header-logo {{
    font-size: 18px; font-weight: 800; color: var(--dhl-red);
    letter-spacing: -0.5px;
  }}
  .header-logo small {{
    font-weight: 400; color: var(--text-muted); font-size: 11px;
    letter-spacing: 0;
  }}
  .header-right {{
    display: flex; align-items: center; gap: 8px;
  }}

  /* ===== LANGUAGE SELECTOR ===== */
  .lang-toggle {{
    position: relative;
  }}
  .lang-current {{
    display: flex; align-items: center; gap: 6px;
    background: var(--bg-alt); border: 1px solid var(--border);
    padding: 6px 12px; border-radius: 8px; cursor: pointer;
    font-size: 13px; color: var(--text);
  }}
  .lang-dropdown {{
    display: none;
    position: absolute; top: 100%; right: 0; margin-top: 4px;
    background: var(--bg); border: 1px solid var(--border);
    border-radius: 10px; box-shadow: var(--shadow);
    min-width: 200px; z-index: 200;
    max-height: 300px; overflow-y: auto;
  }}
  .lang-dropdown.show {{ display: block; }}
  .lang-btn {{
    display: flex; align-items: center; gap: 8px;
    width: 100%; padding: 10px 14px; border: none; background: none;
    cursor: pointer; font-size: 13px; color: var(--text);
    text-align: left; transition: background .15s;
  }}
  .lang-btn:hover {{ background: var(--bg-alt); }}
  .lang-btn.active {{ background: var(--bg-alt); font-weight: 600; }}
  .lang-btn .lang-flag {{ font-size: 18px; }}
  .lang-btn .lang-name {{ flex: 1; }}

  /* ===== THEME TOGGLE ===== */
  .theme-btn {{
    background: none; border: 1px solid var(--border); border-radius: 8px;
    padding: 6px 10px; cursor: pointer; font-size: 16px; color: var(--text);
  }}

  /* ===== LAYOUT ===== */
  .app {{ margin-top: var(--header-h); display: flex; min-height: calc(100vh - var(--header-h)); }}

  /* ===== SIDEBAR ===== */
  .sidebar {{
    width: var(--sidebar-w); background: var(--bg-alt);
    border-right: 1px solid var(--border); padding: 16px 0;
    position: fixed; top: var(--header-h); left: 0; bottom: 0;
    overflow-y: auto; z-index: 50;
  }}
  .sidebar-section {{
    padding: 8px 16px; cursor: pointer;
    display: flex; align-items: center; gap: 8px;
    font-size: 12.5px; color: var(--text); text-decoration: none;
    border-left: 3px solid transparent; transition: all .15s;
  }}
  .sidebar-section:hover {{ background: var(--bg); }}
  .sidebar-section.active {{ background: var(--bg); font-weight: 600; }}
  .sidebar-section[data-tier="rule"] {{ border-left-color: var(--dhl-red); }}
  .sidebar-section[data-tier="red"] {{ border-left-color: var(--tier-red); }}
  .sidebar-section[data-tier="yellow"] {{ border-left-color: var(--tier-yellow); }}
  .sidebar-section[data-tier="green"] {{ border-left-color: var(--tier-green); }}
  .sidebar-section[data-tier="orange"] {{ border-left-color: var(--tier-orange); }}
  .sidebar-section[data-tier="blue"] {{ border-left-color: var(--tier-blue); }}
  .sidebar-section[data-tier="purple"] {{ border-left-color: var(--tier-purple); }}
  .sidebar-divider {{
    height: 1px; background: var(--border); margin: 8px 16px;
  }}
  .sidebar-title {{
    padding: 12px 16px 4px; font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted);
  }}

  /* ===== MAIN CONTENT ===== */
  .main {{
    margin-left: var(--sidebar-w); flex: 1;
    padding: 24px 32px 80px; max-width: 900px;
  }}
  .content-section {{
    display: none;
  }}
  .content-section.active {{
    display: block;
    animation: fadeIn .3s ease;
  }}
  @keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(8px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}

  /* ===== SECTION STYLES (shared with rendered markdown) ===== */
  .section {{
    padding: 0 0 0 0;
  }}
  .section h2 {{
    font-size: 20px; font-weight: 700; margin-bottom: 12px;
    padding-bottom: 8px; border-bottom: 2px solid var(--border);
  }}
  .section h3 {{ font-size: 16px; font-weight: 600; margin: 16px 0 8px; }}
  .section p {{ margin: 6px 0; line-height: 1.5; font-size: 14px; }}
  .section ul, .section ol {{ margin: 6px 0 6px 20px; }}
  .section li {{ margin-bottom: 3px; line-height: 1.5; font-size: 14px; }}
  .section pre {{ background: var(--bg-alt); border: 1px solid var(--border); border-radius: 6px; padding: 10px 14px; font-size: 13px; overflow-x: auto; margin: 8px 0; }}
  .section code {{ background: var(--bg-alt); padding: 2px 5px; border-radius: 3px; font-size: 13px; }}
  .section blockquote {{ border-left: 3px solid var(--dhl-red); background: var(--bg-alt); padding: 10px 14px; margin: 8px 0; font-size: 13px; color: var(--text-muted); }}
  .section hr {{ border: none; border-top: 1px solid var(--border); margin: 16px 0; }}
  .section table {{ width: 100%; border-collapse: collapse; margin: 8px 0; font-size: 13px; }}
  .section th {{ background: var(--dhl-red); color: #fff; padding: 8px 10px; text-align: left; }}
  .section td {{ padding: 6px 10px; border: 1px solid var(--border); }}
  .section tr:nth-child(even) td {{ background: var(--bg-alt); }}

  /* ===== SOLUCIONES RÁPIDAS ===== */
  .quick-grid {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
    margin-top: 8px;
  }}
  .quick-card {{
    background: var(--bg); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 18px; cursor: pointer;
    transition: all .2s; position: relative; overflow: hidden;
  }}
  .quick-card:hover {{
    box-shadow: var(--shadow); transform: translateY(-2px);
  }}
  .quick-card .qc-emoji {{ font-size: 28px; margin-bottom: 6px; }}
  .quick-card .qc-title {{ font-size: 15px; font-weight: 700; margin-bottom: 4px; }}
  .quick-card .qc-desc {{ font-size: 12px; color: var(--text-muted); line-height: 1.4; }}
  .quick-card .qc-bar {{
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
  }}
  .quick-card[data-tier="red"] {{ border-top: 3px solid var(--tier-red); }}
  .quick-card[data-tier="yellow"] {{ border-top: 3px solid var(--tier-yellow); }}
  .quick-card[data-tier="green"] {{ border-top: 3px solid var(--tier-green); }}
  .quick-card[data-tier="orange"] {{ border-top: 3px solid var(--tier-orange); }}

  /* ===== CÓDIGOS EXPRÉS ===== */
  .codes-grid {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
  }}
  .code-card {{
    background: var(--bg); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 16px;
  }}
  .code-card .cc-label {{
    font-size: 11px; font-weight: 700; text-transform: uppercase;
    color: var(--text-muted); letter-spacing: 0.5px; margin-bottom: 4px;
  }}
  .code-card .cc-code {{
    font-size: 18px; font-weight: 700; color: var(--dhl-red);
    font-family: "Courier New", monospace;
  }}
  .code-card .cc-desc {{ font-size: 12px; color: var(--text-muted); margin-top: 2px; }}

  /* ===== SEARCH ===== */
  .search-box {{
    position: relative; margin-bottom: 16px;
  }}
  .search-box input {{
    width: 100%; padding: 10px 14px 10px 36px;
    border: 1px solid var(--border); border-radius: 8px;
    background: var(--bg-alt); color: var(--text);
    font-size: 14px; outline: none;
  }}
  .search-box input:focus {{ border-color: var(--dhl-red); }}
  .search-box .search-icon {{
    position: absolute; left: 12px; top: 50%; transform: translateY(-50%);
    font-size: 14px; color: var(--text-muted);
  }}

  /* ===== SCROLLBAR ===== */
  ::-webkit-scrollbar {{ width: 6px; }}
  ::-webkit-scrollbar-track {{ background: transparent; }}
  ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}

  /* ===== RESPONSIVE ===== */
  @media (max-width: 768px) {{
    .sidebar {{ display: none; }}
    .main {{ margin-left: 0; padding: 16px; }}
    .quick-grid {{ grid-template-columns: 1fr; }}
    .codes-grid {{ grid-template-columns: 1fr; }}
    .lang-dropdown {{ min-width: 160px; }}
  }}

  /* ===== LOADING ===== */
  .loading {{
    display: flex; align-items: center; justify-content: center;
    padding: 80px 0; color: var(--text-muted);
  }}
  .loading .spinner {{
    width: 32px; height: 32px; border: 3px solid var(--border);
    border-top-color: var(--dhl-red); border-radius: 50%;
    animation: spin .8s linear infinite; margin-right: 10px;
  }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
</style>
</head>
<body>

<div class="header">
  <div class="header-left">
    <span style="font-size:24px;">🛡️</span>
    <span class="header-logo">BONT <small>· Soluciones rápidas</small></span>
    <button class="theme-btn" onclick="toggleTheme()" title="Modo oscuro">🌙</button>
  </div>
  <div class="header-right">
    <div class="lang-toggle" id="langToggle">
      <div class="lang-current" onclick="toggleLang()">
        <span id="langFlag">🇪🇸</span>
        <span id="langLabel">Español</span>
        <span style="font-size:10px;margin-left:4px;">▾</span>
      </div>
      <div class="lang-dropdown" id="langDropdown">
        {lang_selector_items}
      </div>
    </div>
  </div>
</div>

<div class="app">
  <div class="sidebar" id="sidebar">
    <div class="sidebar-title">Secciones</div>
    <div id="sidebarContent"></div>
  </div>
  <div class="main" id="mainContent">
    <div class="loading"><div class="spinner"></div> Cargando...</div>
  </div>
</div>

<script>
// ===== CONFIG =====
const LANGS = {json.dumps({k: {"name": v["name"], "flag": v["flag"], "rtl": v["rtl"]} for k,v in LANGUAGES.items()}, ensure_ascii=False)};

let currentLang = localStorage.getItem("bont-lang") || "es";
let currentView = "soluciones"; // soluciones | codigos | guia
let allData = {{}};
let allSections = [];

// ===== MARKDOWN RENDER (minimal) =====
function renderMD(text) {{
  let html = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    // headers
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    // bold
    .replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>')
    // inline code
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // images (skip actual files, keep text)
    .replace(/!\\[([^\\]]*)\\]\\([^)]+\\)/g, '<span class="img-placeholder">[$1]</span>')
    // links
    .replace(/\\[([^\\]]+)\\]\\([^)]+\\)/g, '$1')
    // unordered list
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    // ordered list
    .replace(/^(\\d+)\\.\\s+(.+)$/gm, '<li value="$1">$2</li>')
    // tables (basic)
    .replace(/^\\|(.+)\\|$/gm, function(m) {{
      var cells = m.split('|').filter(c => c.trim());
      if (cells[0] && cells[0].match(/^[-:]+$/)) return '<tr class="sep">';
      return '<td>' + cells.join('</td><td>') + '</td>';
    }})
    // paragraphs
    .replace(/\\n\\n/g, '</p><p>')
    // code blocks
    .replace(/```(\\w*)\\n([\\s\\S]*?)```/g, '<pre><code>$2</code></pre>')
    // blockquotes
    .replace(/^>\\s(.+)$/gm, '<blockquote>$1</blockquote>');

  html = '<p>' + html + '</p>';
  // Fix list wrapping
  html = html.replace(/<p>(<li[^>]*>.*?<\\/li>(\\n?<li[^>]*>.*?<\\/li>)*)<\\/p>/g, '<ul>$1</ul>');
  // Wrap consecutive <li> in <ul> if not already
  html = html.replace(/(<li[^>]*>.*?<\\/li>(\\s*<li[^>]*>.*?<\\/li>)*)/g, function(m) {{
    if (!m.includes('<ul>')) return '<ul>' + m + '</ul>';
    return m;
  }});
  // Remove empty <p></p>
  html = html.replace(/<p><\\/p>/g, '');
  // checklist
  html = html.replace(/- \\[ \\] /g, '☐ ');
  html = html.replace(/- \\[x\\] /g, '☑ ');

  return html;
}}

// ===== LOAD LANGUAGE DATA =====
async function loadLang(lang) {{
  if (allData[lang]) {{
    renderView(lang);
    return;
  }}
  try {{
    const resp = await fetch(`data/${{lang}}.json`);
    if (!resp.ok) throw new Error("Not found");
    const data = await resp.json();
    allData[lang] = data;
    renderView(lang);
  }} catch(e) {{
    document.getElementById("mainContent").innerHTML =
      '<div class="loading" style="color:var(--dhl-red);">❌ Error al cargar idioma</div>';
  }}
}}

// ===== RENDER VIEW =====
function renderView(lang) {{
  const data = allData[lang];
  if (!data) return;
  allSections = data.sections;

  // Render sidebar
  renderSidebar(data);

  // Show main content
  renderRoute();
}}

function renderSidebar(data) {{
  const sb = document.getElementById("sidebarContent");
  let html = '';
  data.sections.forEach(s => {{
    if (s.tier === 'other') return;
    if (s.tier === 'flow' || s.tier === 'index') return;
    if (s.tier === 'multilingual' || s.tier === 'vision' || s.tier === 'pocket') return;
    const title = s.title.replace(/^[🔴🟡🟢🟠🔵🟣🌟📚🏹🧭📋❓📞🛡️🌍📱🃏📜💡™️]+\s*/g, '');
    html += `<div class="sidebar-section" data-tier="${{s.tier}}" onclick="scrollToSection('${{s.id}}')">${{title}}</div>`;
    if (s.tier === 'purple' || s.tier === 'faq' || s.tier === 'scenario') {{
      html += '<div class="sidebar-divider"></div>';
    }}
  }});
  sb.innerHTML = html;
}}

function renderRoute() {{
  const data = allData[currentLang];
  if (!data) return;

  const main = document.getElementById("mainContent");
  main.innerHTML = '';

  // We show all sections in one scrollable page
  // But we add "SOLUCIONES RÁPIDAS" as the landing introduction
  let html = '';

  // === SOLUCIONES RÁPIDAS (landing) ===
  html += '<div class="content-section active" id="soluciones-intro">';
  html += '<h2 style="font-size:22px;font-weight:700;margin-bottom:4px;">🔧 ¿Qué necesitas resolver?</h2>';
  html += '<p style="color:var(--text-muted);font-size:14px;margin-bottom:16px;">Selecciona el tipo de problema para ir directo a la solución</p>';

  // Error categories based on data
  const catTiers = ['red', 'yellow', 'green', 'orange'];
  const catMeta = {{
    red: {{emoji: '🔴', title: data.sections.find(s => s.tier==='red')?.title.replace(/^[🔴🟡🟢🟠🔵🟣🌟📚🏹🧭📋❓📞🛡️🌍📱🃏📜💡™️]+\s*/g,'') || 'Problemas físicos de carga', desc: 'LPNs, pallets, carga dañada'}},
    yellow: {{emoji: '🟡', title: data.sections.find(s => s.tier==='yellow')?.title.replace(/^[🔴🟡🟢🟠🔵🟣🌟📚🏹🧭📋❓📞🛡️🌍📱🃏📜💡™️]+\s*/g,'') || 'Errores de escáner', desc: 'Códigos 20, 38, errores del sistema'}},
    green: {{emoji: '🟢', title: data.sections.find(s => s.tier==='green')?.title.replace(/^[🔴🟡🟢🟠🔵🟣🌟📚🏹🧭📋❓📞🛡️🌍📱🃏📜💡™️]+\s*/g,'') || 'Etiquetas e impresora', desc: 'Smart Scanner, etiquetas, impresión'}},
    orange: {{emoji: '🟠', title: data.sections.find(s => s.tier==='orange')?.title.replace(/^[🔴🟡🟢🟠🔵🟣🌟📚🏹🧭📋❓📞🛡️🌍📱🃏📜💡™️]+\s*/g,'') || 'Emergencias', desc: 'Errores humanos, accidentes'}},
  }};

  html += '<div class="quick-grid">';
  catTiers.forEach(t => {{
    const meta = catMeta[t];
    html += `<div class="quick-card" data-tier="${{t}}" onclick="scrollToSection('${{data.sections.find(s => s.tier===t)?.id}}')">
      <div class="qc-bar" style="background:var(--tier-${{t}})"></div>
      <div class="qc-emoji">${{meta.emoji}}</div>
      <div class="qc-title">${{meta.title}}</div>
      <div class="qc-desc">${{meta.desc}}</div>
    </div>`;
  }});
  html += '</div>';

  // Purple & Blue quick cards
  html += '<div style="margin-top:16px;display:grid;grid-template-columns:1fr 1fr;gap:12px;" class="quick-grid-extra">';
  const blueSection = data.sections.find(s => s.tier==='blue');
  const purpleSection = data.sections.find(s => s.tier==='purple');
  if (purpleSection) {{
    html += `<div class="quick-card" onclick="scrollToSection('${{purpleSection.id}}')" style="border-top:3px solid var(--tier-purple)">
      <div class="qc-emoji">🟣</div>
      <div class="qc-title">Códigos de bolsillo</div>
      <div class="qc-desc">QR Personal, Location, Equipment, Turno de día</div>
    </div>`;
  }}
  if (blueSection) {{
    html += `<div class="quick-card" onclick="scrollToSection('${{blueSection.id}}')" style="border-top:3px solid var(--tier-blue)">
      <div class="qc-emoji">🔵</div>
      <div class="qc-title">Buenas prácticas</div>
      <div class="qc-desc">Nivel Leyenda — tips avanzados</div>
    </div>`;
  }}
  html += '</div>';
  html += '</div>';

  // === ALL SECTIONS ===
  html += '<hr style="margin:24px 0;">';
  html += '<h2 id="guia-titulo" style="font-size:20px;font-weight:700;margin-bottom:16px;">📖 Guía de soluciones</h2>';

  data.sections.forEach(s => {{
    if (s.tier === 'other' || s.tier === 'flow' || s.tier === 'index' ||
        s.tier === 'multilingual' || s.tier === 'vision' || s.tier === 'pocket') return;
    html += `<div class="section" id="${{s.id}}" data-tier="${{s.tier}}">`;
    html += `<h2>${{s.title}}</h2>`;
    html += `<div class="section-content">${{renderMD(s.content)}}</div>`;
    html += `</div>`;
  }});

  main.innerHTML = html;

  // Scroll to hash if present
  const hash = window.location.hash;
  if (hash) {{
    setTimeout(() => scrollToSection(hash.substring(1)), 100);
  }}
}}

function scrollToSection(id) {{
  const el = document.getElementById(id);
  if (el) {{
    el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    window.location.hash = id;
  }}
}}

function switchLang(lang) {{
  if (currentLang === lang) return;
  currentLang = lang;
  localStorage.setItem("bont-lang", lang);
  updateLangUI();
  loadLang(lang);
}}

function updateLangUI() {{
  const info = LANGS[currentLang];
  if (!info) return;
  document.getElementById("langFlag").textContent = info.flag;
  document.getElementById("langLabel").textContent = info.name;
  document.body.dir = info.rtl ? "rtl" : "ltr";
  // Update active button
  document.querySelectorAll(".lang-btn").forEach(b => {{
    b.classList.toggle("active", b.getAttribute("data-lang") === currentLang);
  }});
}}

function toggleLang() {{
  document.getElementById("langDropdown").classList.toggle("show");
}}

function toggleTheme() {{
  const isDark = document.body.classList.toggle("dark");
  localStorage.setItem("bont-theme", isDark ? "dark" : "light");
  const btn = document.querySelector(".theme-btn");
  btn.textContent = isDark ? "☀️" : "🌙";
}}

// Close dropdown when clicking outside
document.addEventListener("click", (e) => {{
  if (!e.target.closest("#langToggle")) {{
    document.getElementById("langDropdown").classList.remove("show");
  }}
}});

// Init
(function init() {{
  // Load theme
  const savedTheme = localStorage.getItem("bont-theme");
  if (savedTheme === "dark") {{
    document.body.classList.add("dark");
    document.querySelector(".theme-btn").textContent = "☀️";
  }}
  // Load language
  updateLangUI();
  loadLang(currentLang);
}})();
</script>
</body>
</html>"""

# ============================================================
#  MAIN
# ============================================================
if __name__ == "__main__":
    print("🔨 Building BONT webapp...")
    print(f"   Base: {BASE}")
    print(f"   Output: {OUT}")

    # Generate JSON data files
    for lang_key, lang_info in LANGUAGES.items():
        print(f"   Processing {lang_key} ({lang_info['name']})...")
        data = build_json(lang_key, lang_info)
        json_path = f"{DATA}/{lang_key}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        sections_count = len(data["sections"])
        kb = os.path.getsize(json_path) / 1024
        print(f"     ✅ {lang_key}: {kb:.0f} KB, {sections_count} sections")

    # Generate index.html
    print("   Generating index.html...")
    index_html = build_index_html()
    index_path = f"{OUT}/index.html"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    kb = os.path.getsize(index_path) / 1024
    print(f"     ✅ index.html: {kb:.0f} KB")

    print(f"\n✅ Done. Webapp ready at {OUT}/")
    print(f"   {OUT}/index.html")
    print(f"   {DATA}/ (10 language JSONs)")
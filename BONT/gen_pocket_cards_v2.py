#!/usr/bin/env python3
"""
Pocket Cards v2 — Diseñadas con CONTENIDO REAL del manual.
85×55mm, 3 idiomas, SOLO información útil de verdad.
"""

import os

PRINT_URL = "https://sacharunaaa-max.github.io/Bont/"

def gen_cards():
    out = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BONT · Pocket Cards v2</title>
<style>
  @page { size: 85mm 55mm; margin: 0; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: "Segoe UI", Arial, Helvetica, sans-serif;
    background: #ddd;
    padding: 8mm;
  }

  .page {
    max-width: 1000px;
    margin: 0 auto;
  }

  .sheet {
    display: grid;
    grid-template-columns: repeat(3, 85mm);
    gap: 4mm 8mm;
    justify-content: center;
    margin-bottom: 20px;
    page-break-inside: avoid;
  }

  .sheet-header {
    grid-column: 1 / -1;
    display: flex; align-items: center; gap: 6px;
    padding: 4px 10px; background: #c00; color: #fff;
    border-radius: 3px; font-size: 9pt; font-weight: 700;
    letter-spacing: 0.5px; text-transform: uppercase;
  }

  .card {
    width: 85mm; height: 55mm;
    position: relative;
    border-radius: 2px;
    overflow: hidden;
    page-break-inside: avoid;
    break-inside: avoid;
  }

  .card-front, .card-back {
    width: 100%; height: 100%;
    padding: 3mm 4mm;
    position: relative;
  }

  .card-front { background: #fff; border: 0.3mm solid #bbb; }
  .card-back { background: #fafafa; border: 0.3mm solid #bbb; }

  /* CUT MARKS */
  .card::before {
    content: '';
    position: absolute;
    top: -0.5mm; left: -0.5mm; right: -0.5mm; bottom: -0.5mm;
    border: 0.2mm dashed #aaa;
    border-radius: 3px;
    pointer-events: none;
    z-index: 10;
  }

  /* ===== FRONT ===== */
  .f-top {
    display: flex; align-items: center; gap: 2mm;
    margin-bottom: 1.2mm;
  }
  .f-icon { font-size: 8mm; line-height: 1; }
  .f-title {
    font-size: 8pt; font-weight: 800;
    text-transform: uppercase; letter-spacing: 0.3px;
    line-height: 1.1;
  }
  .f-sub {
    font-size: 5pt; color: #888;
    margin-top: 0.3mm; font-weight: 500;
  }

  .f-line { height: 0.3mm; border: none; margin: 1mm 0; }

  .f-row {
    display: flex; gap: 1mm;
    margin-bottom: 0.5mm;
    font-size: 5.8pt; line-height: 1.3; color: #333;
    align-items: flex-start;
  }
  .f-label {
    font-weight: 700; color: #fff;
    padding: 0.3mm 1.5mm; border-radius: 1.5px;
    white-space: nowrap; text-align: center;
    min-width: 8mm; font-size: 5.5pt;
    flex-shrink: 0;
  }
  .f-text { flex: 1; }
  .f-text strong { color: #111; }

  /* ===== BACK ===== */
  .b-title {
    font-size: 6.5pt; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.5px;
    margin-bottom: 0.8mm;
    border-bottom: 0.3mm solid #ddd;
    padding-bottom: 0.3mm;
  }
  .b-steps { list-style: none; padding: 0; }
  .b-step {
    display: flex; gap: 1.2mm; margin-bottom: 0.4mm;
    font-size: 5.7pt; line-height: 1.25; color: #333;
  }
  .b-num {
    font-weight: 700; min-width: 2.5mm;
    font-size: 6pt;
  }
  .b-note {
    font-size: 5pt; color: #888; margin-top: 0.5mm;
    font-style: italic;
  }

  /* Colors */
  .cr .f-title { color: #c62828; }
  .cr .f-line { background: #c62828; }
  .cr .f-label { background: #c62828; }
  .cr .b-title { color: #c62828; }
  .cr .b-num { color: #c62828; }

  .cy .f-title { color: #f57f17; }
  .cy .f-line { background: #f57f17; }
  .cy .f-label { background: #f57f17; }
  .cy .b-title { color: #f57f17; }
  .cy .b-num { color: #f57f17; }

  .cg .f-title { color: #2e7d32; }
  .cg .f-line { background: #2e7d32; }
  .cg .f-label { background: #2e7d32; }
  .cg .b-title { color: #2e7d32; }
  .cg .b-num { color: #2e7d32; }

  .co .f-title { color: #bf360c; }
  .co .f-line { background: #bf360c; }
  .co .f-label { background: #bf360c; }
  .co .b-title { color: #bf360c; }
  .co .b-num { color: #bf360c; }

  .cp .f-title { color: #7b1fa2; }
  .cp .f-line { background: #7b1fa2; }
  .cp .f-label { background: #7b1fa2; }
  .cp .b-title { color: #7b1fa2; }
  .cp .b-num { color: #7b1fa2; }

  .cgold .f-title { color: #c00; }
  .cgold .f-line { background: #c00; }
  .cgold .f-label { background: #c00; }
  .cgold .b-title { color: #c00; }
  .cgold .b-num { color: #c00; }

  .b-box {
    background: #fff5f5; border-left: 1mm solid #c00;
    padding: 0.8mm 1.5mm; margin-bottom: 1mm;
    font-size: 6pt; font-style: italic; color: #333;
    line-height: 1.3;
  }

  /* Print */
  @media print {
    body { background: white; padding: 0; }
    .sheet { gap: 0; margin-bottom: 0; }
    .card::before { display: none; }
    .card-front, .card-back { border-width: 0.1mm; }
    @page { margin: 0; }
  }
</style>
</head>
<body>
<div class="page">
"""

    # ================================================================
    # CONTENT DEFINITIONS
    # ================================================================
    # Each: (front_title, front_sub, items[(label, text)], back_title, back_steps[str])
    # Colors: cr=red, cy=yellow, cg=green, co=orange, cp=purple, cgold=rule

    ES = [
        # 1 - RED
        ("cr", "🔴", "Problemas físicos de carga",
         "RCG · Pallet · Krat",
         [
             ("📏 Altura", "Máximo 2.3 m. Si ves que sobrepasa, redistribuye."),
             ("⬆️ Flechas", "La flecha siempre hacia arriba. Sin flecha = frágil."),
             ("🎩 Sombrero", "Caja grande NO va sobre pequeña. Base firme."),
             ("🔧 Tuberías", "Siempre al fondo/lateral del RCG. Nunca sobre cajas."),
             ("📋 Etiquetas", "Krats con etiqueta visible hacia fuera."),
         ],
         "🔴 Carga física — Claves",
         [
             "Altura máx: 2.3 m. Si un RCG/pallet parece inestable, redistribuye.",
             "Flechas SIEMPRE hacia arriba. Si no tiene flecha, tratar como frágil.",
             "El efecto sombrero evítalo: base más grande que la parte superior.",
             "Las tuberías van al fondo o lateral del RCG. No sobre cajas de cartón.",
             "Etiquetas de krats visibles hacia fuera para que se puedan escanear.",
             "¿Producto sobresale del RCG? Reubica dentro o usa otro RCG.",
             "¿RCG/pallet dañado? Reubica la carga y etiqueta de nuevo.",
         ]),

        # 2 - YELLOW
        ("cy", "🟡", "Errores de escáner / sistema",
         "Mensajes comunes",
         [
             ('"No inventory found"', "El producto no tiene ubicación. Usa INVENTORY DSP."),
             ('"SSCC wrong/missing"', "Código no válido. Usa Smart Scanner (INBOUND o SURPLUS)."),
             ('"Different pallet number"', "Escaneaste el RCG/pallet equivocado."),
             ('"INVENTORY invalid"', "Error grave. Lleva el producto a Teamleader."),
             ("Escáner no reacciona", "Ajusta distancia. Limpia etiqueta. Aparta producto."),
         ],
         "🟡 Solución rápida de errores",
         [
             '"No inventory found" → INVENTORY DSP en Blue Yonder. Busca código.',
             "SSCC wrong/missing → Smart Scanner → INBOUND. Si dice NOT FOUND, pasa a SURPLUS.",
             "Different pallet → Reubica el producto en el contenedor correcto.",
             "Inventory invalid → Lleva el producto a Teamleader o Troubleshooter.",
             "Escáner no responde → 1) Distancia 2) Limpiar 3) Apartar 4) Probar manual.",
             "Si el sistema sigue bloqueado → DONE → reiniciar → reportar.",
         ]),

        # 3 - GREEN
        ("cg", "🟢", "Smart Scanner / Etiquetas",
         "INBOUND · SURPLUS · Impresora",
         [
             ("INBOUND", "Escanea SSCC. Elige tipo. Si dice NOT FOUND → SURPLUS."),
             ("SURPLUS", "Escanea código inferior + superior. Si ANOTHER POSITION → INBOUND."),
             ("🔙 ANOTHER POSITION", "Vuelve a INBOUND y escanea de nuevo."),
             ("🖨️ LPN perdida", "BY → CHANGE POSITION → anota LPN → Smart Printer → LPN PRINTING."),
             ("🖨️ Sticker cierre", "Smart Scanner → PRINTING → SSCC INTERGAMMA. Imprime 2 copias."),
         ],
         "🟢 Smart Scanner paso a paso",
         [
             "Método INBOUND: Escanea código SSCC → elige tipo (KRT, COL...)",
             "Si dice NOT FOUND → cambia a SURPLUS. Escanea inf + sup.",
             "Si dice ANOTHER POSITION → vuelve a INBOUND y reintenta.",
             "Protocolo A (LPN perdida): BY → 3 puntos → CHANGE POSITION → anota LPN.",
             "Luego: Smart Scanner → PRINTING → LPN PRINTING → mete código.",
             "Protocolo C (sticker cierre): PRINTING → SSCC INTERGAMMA → 2 copias.",
         ]),

        # 4 - ORANGE
        ("co", "🟠", "Emergencias / Errores",
         "Derrames · Confusiones · Accidentes",
         [
             ("💧 Derrame", "No pares. Ve al kit de arena. Limpia de afuera hacia adentro."),
             ("📦 Confusión RCG", "Verifica destino en pantalla. Reubica producto en el correcto."),
             ("❌ Escanear sin poner", "No lo hagas. El sistema lo da por colocado y otro operario falla."),
             ("👀 Producto perdido", "Escanea para ver destino. Usa INVENTORY DSP si no sabes."),
             ("🚨 Accidente", "STOP. Avisa Teamleader. No muevas nada."),
         ],
         "🟠 Protocolo de emergencia",
         [
             "Derrame: No detener flujo. Kit de arena → esparcir → limpiar afuera→adentro.",
             "Residuos de derrame: Depósitar en contenedores especiales.",
             "Confusión de contenedor: Ver pantalla. Comparar números. Reubicar.",
             "Escaneaste sin colocar: Sistema ya registró. Si no hay espacio, avisa TL.",
             "Producto mal ubicado: Escanea. Si puedes, colócalo. Si no, INVENTORY DSP.",
             "Accidente → STOP → Avisar supervisor → No mover nada.",
         ]),

        # 5 - PURPLE
        ("cp", "🟣", "Códigos de bolsillo",
         "Lo que siempre debes tener",
         [
             ("1️⃣ QR Personal", "Identificación única. Login en Blue Yonder y Smart Scanner."),
             ("2️⃣ Location", "Área de trabajo. Ej: BNT09."),
             ("3️⃣ Equipment", "Identifica tu equipo (hand en BONT)."),
             ("4️⃣ Turno día", "Código del turno laboral actual."),
             ("📍 Zonas", "PND-A · PND-P · T3-STGE · BNT09"),
         ],
         "🟣 ¿Para qué sirve cada código?",
         [
             "QR Personal → Iniciar sesión en SMAR T7 y Blue Yonder.",
             "Location → Indica al sistema dónde estás trabajando.",
             "Equipment → Asigna tu equipo a la sesión.",
             "Turno de día → Registra el turno actual en el sistema.",
             "Smart Scanner: Solo necesita QR Personal.",
             "Blue Yonder: Necesita los 4 códigos en secuencia.",
         ]),

        # 6 - GOLDEN RULE
        ("cgold", "⭐", "Regla de Oro + Checklist",
         "Tu mantra diario",
         [],
         "⭐ Regla de Oro",
         [
             '"Si algo se ve mal, está mal. No lo ignores. Verifícalo."',
         ]),
    ]

    def label(s, cls):
        return f'<span class="f-label">{s}</span>'

    def card_html(cls, emoji, title, sub, items, btitle, bsteps, lang_label, idx, side):
        fi = "".join(f'<div class="f-row">{label(it[0], cls.replace("c",""))}<span class="f-text">{it[1]}</span></div>' for it in items)
        bs = "".join(f'<li class="b-step"><span class="b-num">{n+1}.</span><span>{s}</span></li>' for n,s in enumerate(bsteps))
        return f'''<div class="card {cls}">
  <div class="card-{side}">
    <span style="position:absolute;top:0.3mm;right:0.8mm;font-size:4.5pt;color:#bbb;font-weight:600;">{lang_label} {side.upper()} {idx}</span>
    {"" if side=="back" else f'''<div class="f-top"><span class="f-icon">{emoji}</span><div><div class="f-title">{title}</div><div class="f-sub">{sub}</div></div></div>
    <hr class="f-line">{fi}'''}
    {"" if side=="front" else f'''<div class="b-title">{btitle}</div>
    <ol class="b-steps">{bs}</ol>'''}
  </div>
</div>'''

    langs = [
        ("es", "ES", "ESPAÑOL 🇪🇸", ES),
        ("en", "EN", "ENGLISH 🇬🇧", None),
        ("nl", "NL", "NEDERLANDS 🇳🇱", None),
    ]

    # ===== SPANISH =====
    out += '<div class="sheet">\n<div class="sheet-header">🛡️ BONT · Pocket Cards — ESPAÑOL 🇪🇸</div>\n'
    for i, card in enumerate(ES):
        out += card_html(*card, "ES", i+1, "front")
    # Same backs reversed order for duplex printing
    for i, card in enumerate(ES):
        out += card_html(*card, "ES", i+1, "back")
    out += '</div>\n'

    # ===== ENGLISH =====
    EN = [
        ("cr", "🔴", "Physical load issues",
         "RCG · Pallet · Krat",
         [
             ("📏 Height", "Max 2.3 m. If it looks unstable, redistribute."),
             ("⬆️ Arrows", "Always pointing up. No arrow = fragile."),
             ("🎩 Hat effect", "Big box NOT on small one. Stable base."),
             ("🔧 Pipes", "Always at back/side of RCG. Never on boxes."),
             ("📋 Labels", "Krat labels visible facing out."),
         ],
         "🔴 Physical load — Keys",
         [
             "Max height: 2.3 m. If RCG/pallet looks unstable, redistribute.",
             "Arrows always UP. No arrow = treat as fragile.",
             "Hat effect: base must be ≥ top. Heavy at bottom.",
             "Pipes go at back or side of RCG. NOT on cardboard boxes.",
             "Krat labels visible facing out for scanning.",
             "Product sticking out of RCG? Move inside or use another RCG.",
             "Damaged RCG/pallet? Relocate load and relabel.",
         ]),

        ("cy", "🟡", "Scanner / System errors",
         "Common messages",
         [
             ('"No inventory found"', "Product has no location. Use INVENTORY DSP."),
             ('"SSCC wrong/missing"', "Invalid code. Use Smart Scanner (INBOUND or SURPLUS)."),
             ('"Different pallet"', "You scanned the wrong RCG/pallet."),
             ('"INVENTORY invalid"', "Serious error. Take product to Teamleader."),
             ("Scanner no response", "Adjust distance. Clean label. Set aside."),
         ],
         "🟡 Quick error solution",
         [
             '"No inventory found" → INVENTORY DSP in Blue Yonder. Search code.',
             "SSCC wrong/missing → Smart Scanner → INBOUND. NOT FOUND? Switch to SURPLUS.",
             "Different pallet → Move product to correct container.",
             "Inventory invalid → Take product to Teamleader or Troubleshooter.",
             "Scanner no response → 1) Distance 2) Clean 3) Set aside 4) Try manual.",
             "System still blocked → DONE → restart → report.",
         ]),

        ("cg", "🟢", "Smart Scanner / Labels",
         "INBOUND · SURPLUS · Printer",
         [
             ("INBOUND", "Scan SSCC. Choose type. NOT FOUND? Switch to SURPLUS."),
             ("SURPLUS", "Scan lower + upper code. ANOTHER POSITION? Back to INBOUND."),
             ("🔙 ANOTHER POSITION", "Go back to INBOUND and scan again."),
             ("🖨️ Lost LPN", "BY → CHANGE POSITION → note LPN → Smart Printer → LPN PRINTING."),
             ("🖨️ Close sticker", "Smart Scanner → PRINTING → SSCC INTERGAMMA. Print 2 copies."),
         ],
         "🟢 Smart Scanner step by step",
         [
             "INBOUND: Scan SSCC code → choose type (KRT, COL...)",
             "If it says NOT FOUND → switch to SURPLUS. Scan low + high.",
             "If it says ANOTHER POSITION → back to INBOUND and retry.",
             "Protocol A (lost LPN): BY → 3 dots → CHANGE POSITION → note LPN.",
             "Then: Smart Scanner → PRINTING → LPN PRINTING → enter code.",
             "Protocol C (close sticker): PRINTING → SSCC INTERGAMMA → 2 copies.",
         ]),

        ("co", "🟠", "Emergencies / Errors",
         "Spills · Mix-ups · Accidents",
         [
             ("💧 Spill", "Don't stop. Get spill kit. Clean outside→in."),
             ("📦 Container mix-up", "Check destination on screen. Relocate product."),
             ("❌ Scan without placing", "Don't. System marks it as placed, another operator fails."),
             ("👀 Lost product", "Scan to see destination. Use INVENTORY DSP."),
             ("🚨 Accident", "STOP. Call Teamleader. Don't move anything."),
         ],
         "🟠 Emergency protocol",
         [
             "Spill: Don't stop flow. Spill kit → sand → clean outside→in.",
             "Spill waste: Dispose in special containers.",
             "Container mix-up: Check screen. Compare numbers. Relocate.",
             "Scanned without placing: System registered it. If no space, tell TL.",
             "Misplaced product: Scan. If possible, place it. If not, INVENTORY DSP.",
             "Accident → STOP → Call supervisor → Don't move anything.",
         ]),

        ("cp", "🟣", "Pocket codes",
         "Always keep these handy",
         [
             ("1️⃣ Personal QR", "Unique ID. Login in Blue Yonder and Smart Scanner."),
             ("2️⃣ Location", "Work area. E.g.: BNT09."),
             ("3️⃣ Equipment", "Identifies your equipment (hand in BONT)."),
             ("4️⃣ Day turn", "Current shift code."),
             ("📍 Zones", "PND-A · PND-P · T3-STGE · BNT09"),
         ],
         "🟣 What is each code for?",
         [
             "Personal QR → Log in to SMAR T7 and Blue Yonder.",
             "Location → Tells the system where you're working.",
             "Equipment → Assigns your equipment to the session.",
             "Day turn → Registers current shift in the system.",
             "Smart Scanner: Only needs Personal QR.",
             "Blue Yonder: Needs all 4 codes in sequence.",
         ]),

        ("cgold", "⭐", "Golden Rule + Checklist",
         "Your daily mantra",
         [],
         "⭐ Golden Rule",
         [
             '"If something looks wrong, it is wrong. Don\'t ignore it. Verify it."',
         ]),
    ]

    out += '<div class="sheet">\n<div class="sheet-header">🛡️ BONT · Pocket Cards — ENGLISH 🇬🇧</div>\n'
    for i, card in enumerate(EN):
        out += card_html(*card, "EN", i+1, "front")
    for i, card in enumerate(EN):
        out += card_html(*card, "EN", i+1, "back")
    out += '</div>\n'

    # ===== DUTCH =====
    NL = [
        ("cr", "🔴", "Fysieke laadproblemen",
         "RCG · Pallet · Krat",
         [
             ("📏 Hoogte", "Max 2.3 m. Onstabiel? Herverdeel."),
             ("⬆️ Pijlen", "Pijl altijd omhoog. Geen pijl = breekbaar."),
             ("🎩 Hoed-effect", "Grote doos NIET op kleine. Stevige basis."),
             ("🔧 Buizen", "Altijd achter/zij RCG. Nooit op dozen."),
             ("📋 Labels", "Krat labels zichtbaar naar buiten."),
         ],
         "🔴 Fysiek laden — Sleutels",
         [
             "Max hoogte: 2.3 m. Onstabiele RCG/pallet? Herverdeel.",
             "Pijlen altijd OMHOOG. Geen pijl = behandelen als breekbaar.",
             "Hoed-effect: basis ≥ bovenkant. Zwaar onderaan.",
             "Buizen achter of zijkant RCG. NIET op kartonnen dozen.",
             "Krat labels zichtbaar naar buiten voor scannen.",
             "Product steekt uit RCG? Verplaats of gebruik andere RCG.",
             "Beschadigde RCG/pallet? Verplaats lading en herlabel.",
         ]),

        ("cy", "🟡", "Scanner / Systeemfouten",
         "Veelvoorkomende meldingen",
         [
             ('"No inventory found"', "Product heeft geen locatie. Gebruik INVENTORY DSP."),
             ('"SSCC wrong/missing"', "Ongeldige code. Gebruik Smart Scanner (INBOUND of SURPLUS)."),
             ('"Different pallet"', "Je scande de verkeerde RCG/pallet."),
             ('"INVENTORY invalid"', "Ernstige fout. Breng product naar Teamleader."),
             ("Scanner reageert niet", "Pas afstand. Maak label schoon. Leg apart."),
         ],
         "🟡 Snelle foutoplossing",
         [
             '"No inventory found" → INVENTORY DSP in Blue Yonder. Zoek code.',
             "SSCC wrong/missing → Smart Scanner → INBOUND. NOT FOUND? Naar SURPLUS.",
             "Different pallet → Verplaats product naar juiste container.",
             "Inventory invalid → Breng naar Teamleader of Troubleshooter.",
             "Scanner reageert niet → 1) Afstand 2) Schoonmaken 3) Apart leggen 4) Handmatig.",
             "Systeem nog steeds geblokkeerd → DONE → herstarten → melden.",
         ]),

        ("cg", "🟢", "Smart Scanner / Labels",
         "INBOUND · SURPLUS · Printer",
         [
             ("INBOUND", "Scan SSCC. Kies type. NOT FOUND? Naar SURPLUS."),
             ("SURPLUS", "Scan onder + boven code. ANOTHER POSITION? Terug naar INBOUND."),
             ("🔙 ANOTHER POSITION", "Ga terug naar INBOUND en scan opnieuw."),
             ("🖨️ LPN kwijt", "BY → CHANGE POSITION → noteer LPN → Smart Printer → LPN PRINTING."),
             ("🖨️ Sluitsticker", "Smart Scanner → PRINTING → SSCC INTERGAMMA. Print 2 exemplaren."),
         ],
         "🟢 Smart Scanner stap voor stap",
         [
             "INBOUND: Scan SSCC → kies type (KRT, COL...)",
             "Zegt NOT FOUND? Naar SURPLUS. Scan laag + hoog.",
             "Zegt ANOTHER POSITION? Terug naar INBOUND en opnieuw.",
             "Protocol A (LPN kwijt): BY → 3 punten → CHANGE POSITION → noteer LPN.",
             "Dan: Smart Scanner → PRINTING → LPN PRINTING → voer code in.",
             "Protocol C (sluitsticker): PRINTING → SSCC INTERGAMMA → 2 ex.",
         ]),

        ("co", "🟠", "Noodgevallen / Fouten",
         "Morsen · Verwarring · Ongelukken",
         [
             ("💧 Morsen", "Niet stoppen. Pak morsset. Reinig buiten→binnen."),
             ("📦 Container verwarring", "Controleer bestemming op scherm. Verplaats product."),
             ("❌ Scannen zonder plaatsen", "Niet doen. Systeem markeert als geplaatst."),
             ("👀 Product kwijt", "Scan om bestemming te zien. Gebruik INVENTORY DSP."),
             ("🚨 Ongeluk", "STOP. Bel Teamleader. Verplaats niks."),
         ],
         "🟠 Noodprotocol",
         [
             "Morsen: Niet stoppen. Morsset → zand → reinigen buiten→binnen.",
             "Morsafval: Deponeren in speciale containers.",
             "Container verwarring: Scherm checken. Nummers vergelijken. Verplaatsen.",
             "Gescaand zonder plaatsen: Systeem heeft geregistreerd. Geen ruimte? TL.",
             "Verkeerd geplaatst product: Scannen. Plaatsen indien mogelijk. Zo niet, DSP.",
             "Ongeluk → STOP → Bel supervisor → Verplaats niks.",
         ]),

        ("cp", "🟣", "Zakcodes",
         "Altijd bij de hand",
         [
             ("1️⃣ Persoonlijke QR", "Unieke ID. Inloggen Blue Yonder en Smart Scanner."),
             ("2️⃣ Locatie", "Werkgebied. Bijv.: BNT09."),
             ("3️⃣ Equipment", "Identificeert je apparatuur (hand in BONT)."),
             ("4️⃣ Dagdienst", "Huidige dienstcode."),
             ("📍 Zones", "PND-A · PND-P · T3-STGE · BNT09"),
         ],
         "🟣 Waar dient elke code voor?",
         [
             "Persoonlijke QR → Inloggen SMAR T7 en Blue Yonder.",
             "Locatie → Vertelt systeem waar je werkt.",
             "Equipment → Koppelt apparatuur aan sessie.",
             "Dagdienst → Registreert huidige dienst in systeem.",
             "Smart Scanner: Alleen Persoonlijke QR nodig.",
             "Blue Yonder: Alle 4 codes in volgorde nodig.",
         ]),

        ("cgold", "⭐", "Gouden Regel + Checklist",
         "Je dagelijkse mantra",
         [],
         "⭐ Gouden Regel",
         [
             '"Als iets er verkeerd uitziet, is het verkeerd. Negeer het niet. Controleer het."',
         ]),
    ]

    out += '<div class="sheet">\n<div class="sheet-header">🛡️ BONT · Pocket Cards — NEDERLANDS 🇳🇱</div>\n'
    for i, card in enumerate(NL):
        out += card_html(*card, "NL", i+1, "front")
    for i, card in enumerate(NL):
        out += card_html(*card, "NL", i+1, "back")
    out += '</div>\n'

    # ===== FOOTER =====
    out += f'''
<div style="text-align:center;padding:10px;font-size:7pt;color:#888;margin-top:10px;">
  📱 Escanea para la app: <a href="{PRINT_URL}" style="color:#c00;">{PRINT_URL}</a>
</div>
</div>
</body>
</html>'''

    path = "/home/sacharuna/.openclaw/workspace/BONT/pocket-cards.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)

    size = os.path.getsize(path) / 1024
    print(f"✅ Pocket Cards v2 generadas: {size:.0f} KB")
    print(f"   {len(ES)} tarjetas × 3 idiomas = {len(ES)*3} pares (anverso+reverso)")

if __name__ == "__main__":
    gen_cards()

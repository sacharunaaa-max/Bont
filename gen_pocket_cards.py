#!/usr/bin/env python3
"""
Generate pocket cards HTML for 3 languages (ES, EN, NL)
Cards are 85x55mm (credit card size), designed for front pocket.
6 cards per language = 18 cards total.
"""

import os

QR_B64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAADIAQMAAACXljzdAAAABlBMVEX///+ZmZmqRC6mAAAAAXRSTlMAQObYZgAAABxJREFUeF7twQEBAAAAgiD5R1oOYKANAAAAPAwJEgABkcdNcAAAAABJRU5ErkJggg=="

CARDS = {}

# ===== SPANISH =====
CARDS["es"] = [
    {
        "id": 1, "emoji": "🔴", "tier": "red",
        "front_title": "Problemas físicos de carga",
        "front_sub": "LPN · SSCC · RCG · Pallet · Krat",
        "front_items": [
            ("LPN", "Etiqueta dañada / ilegible: No se puede leer → imprimir nueva etiqueta"),
            ("SSCC", "Código incorrecto: Verificar en Blue Yonder → reimprimir"),
            ("RCG", "Código no reconocido: Escanear manualmente en INVENTORY DSP"),
            ("Pallet", "Dañado / inestable: Reubicar en pallet nuevo. Reetiquetar."),
            ("Krat", "Caja dañada: Reemplazar. Revisar contenido."),
        ],
        "back_title": "🔴 Solución rápida",
        "back_steps": [
            "LPN dañada/ilegible → SMAR T7 → IMPRIMIR NUEVA ETIQUETA.",
            "SSCC rechazado → Ver código en Blue Yonder. Si no coincide, cambiar LPN/SSCC.",
            "RCG no lee → INVENTORY DSP → escaneo manual o rotación de pallet.",
            "Pallet/Krat dañado → Reubicar carga en pallet nuevo. Reetiquetar.",
            "¿Sigue sin funcionar? → Llamar a Teamleader o Troubleshooter.",
        ],
    },
    {
        "id": 2, "emoji": "🟡", "tier": "yellow",
        "front_title": "Errores de escáner / sistema",
        "front_sub": "Código 20 · 38 · No inventory",
        "front_items": [
            ("C 20", "No inventory found: LPN no registrada en surtido. Verificar."),
            ("C 38", "Wrong slot location: Ubicación incorrecta."),
            ("INBOUND", "Pendiente de inbound: Esperar. Preguntar Recepción."),
            ("SCANNER", "No enciende / pantalla negra: Batería. Conectar 5 min."),
            ("SURPLUS", "Rollo pallet sin ubicación. Mover a surtido masivo."),
        ],
        "back_title": "🟡 Solución rápida",
        "back_steps": [
            '"No inventory found" → Ver LPN en BY. Si no aparece, INVENTORY DSP → DONE.',
            "Cód 20 / LPN no válida → SSCC no leído bien. Reintentar. Si falla, entrada manual.",
            "Cód 38 / Wrong location → Ver slot en BY. CHANGE POSITION a ubicación correcta.",
            '"ANOTHER POSITION" → Picking cursando en otra ubicación. Esperar.',
            "Blue Yonder no responde → Cerrar sesión. Volver a entrar. Esperar 30 seg.",
        ],
    },
    {
        "id": 3, "emoji": "🟢", "tier": "green",
        "front_title": "Smart Scanner / Etiquetas",
        "front_sub": "SMAR T7 · Impresora Zebra",
        "front_items": [
            ("1QR", "QR Personal → Escanea tu QR en SMAR T7 para iniciar sesión"),
            ("2LC", "Location → Escanea código de ubicación. Ej: BNT09"),
            ("3EQ", "Equipment → Escanea EPT/EPTXL asignado"),
            ("4TR", "Turno de día → Escanea código de turno"),
            ("PRN", "Impresora no responde: Ver papel/cinta. Encender/apagar."),
        ],
        "back_title": "🟢 Smart Scanner — Secuencia",
        "back_steps": [
            "Paso 1: QR Personal (identificación)",
            "Paso 2: Código Location (dónde estás)",
            "Paso 3: Código Equipment (qué usas)",
            "Paso 4: Turno de día",
            "Zebra: Ver papel → Ver cinta → Apagar/encender → Prueba → Reportar",
        ],
    },
    {
        "id": 4, "emoji": "🟠", "tier": "orange",
        "front_title": "Emergencias / Error humano",
        "front_sub": "Carga mal puesta · Producto caído",
        "front_items": [
            ("STOP", "Producto caído/roto: No tocar. Avisar Teamleader."),
            ("MOVE", "Carga en ubicación incorrecta: CHANGE POSITION."),
            ("CPT", "Leer mal código (CPT8000): No es error. Revisar manualmente."),
            ("ACC", "Accidente: STOP. Avisar supervisor. No mover nada."),
            ("LOCK", "Scanner bloquea proceso: DONE → reiniciar."),
        ],
        "back_title": "🟠 Protocolo de emergencia",
        "back_steps": [
            "DETENER — Para lo que estás haciendo",
            "AVISAR — Teamleader / Supervisor / GC",
            "NO MODIFICAR — No muevas nada hasta que llegue el responsable",
            "DOCUMENTAR — Toma nota (foto si aplica)",
            "Error ubicación: CHANGE POSITION → escanear actual → nueva → confirmar",
        ],
    },
    {
        "id": 5, "emoji": "🟣", "tier": "purple",
        "front_title": "Códigos exprés",
        "front_sub": "Smart Scanner · Blue Yonder",
        "front_items": [
            ("1QR", "QR Personal — Identificación única del operador"),
            ("2LC", "Location — Código de ubicación. Ej: BNT09"),
            ("3EQ", "Equipment — EPT / EPTXS / EPTXL asignado"),
            ("4TR", "Turno de día — Código del turno actual"),
            ("ZNS", "Zonas: PND-A · PND-P · T3-STGE · BNT09"),
        ],
        "back_title": "🟣 ¿Para qué sirve?",
        "back_steps": [
            "QR Personal → Iniciar sesión en SMAR T7. Identifica al operador.",
            "Location → Indica al sistema DÓNDE estás trabajando.",
            "Equipment → Asigna el equipo (EPT/EPTXL) a tu sesión.",
            "Turno de día → Registra el turno en el sistema.",
            "Smart Scanner: solo QR Personal | Blue Yonder: 4 códigos",
        ],
    },
    {
        "id": 6, "emoji": "⭐", "tier": "rule",
        "front_title": "Regla de Oro + Checklist",
        "front_sub": "Tu mantra diario",
        "mantra": '"Si algo se ve mal, está mal."',
        "front_items": [
            ("1", "Verificar equipo (scanner, EPT)"),
            ("2", "Iniciar sesión en sistema"),
            ("3", "Revisar tareas asignadas"),
            ("4", "Confirmar zona y turno"),
        ],
        "back_title": "⭐ Regla de Oro",
        "back_quote": "Si algo se ve mal, está mal. No lo ignores. Verifícalo.",
        "back_steps_title": "🏹 Checklist inicio de turno",
        "back_steps": [
            "Encender Smart Scanner (SMAR T7)",
            "Escanear QR Personal → iniciar sesión",
            "Escanear Location (tu zona)",
            "Escanear Equipment (EPT asignado)",
            "Escanear Turno de día",
            "Revisar en Blue Yonder tus tareas",
        ],
    },
]

# ===== ENGLISH =====
CARDS["en"] = [
    {
        "id": 1, "emoji": "🔴", "tier": "red",
        "front_title": "Physical load issues",
        "front_sub": "LPN · SSCC · RCG · Pallet · Krat",
        "front_items": [
            ("LPN", "Damaged / illegible label: Can't read → print new label"),
            ("SSCC", "Wrong code: Verify in Blue Yonder → reprint"),
            ("RCG", "Unrecognized code: Scan manually via INVENTORY DSP"),
            ("Pallet", "Damaged / unstable: Move to new pallet. Relabel."),
            ("Krat", "Damaged crate: Replace. Check contents."),
        ],
        "back_title": "🔴 Quick solution",
        "back_steps": [
            "Damaged LPN/illegible → SMAR T7 → PRINT NEW LABEL.",
            "SSCC rejected → Check code in BY. If mismatch, change LPN/SSCC.",
            "RCG won't scan → INVENTORY DSP → manual scan or rotate pallet.",
            "Damaged pallet/crate → Relocate to new pallet. Relabel.",
            "Still not working? → Call Teamleader or Troubleshooter.",
        ],
    },
    {
        "id": 2, "emoji": "🟡", "tier": "yellow",
        "front_title": "Scanner / System errors",
        "front_sub": "Code 20 · 38 · No inventory",
        "front_items": [
            ("C 20", "No inventory found: LPN not registered. Verify."),
            ("C 38", "Wrong slot location: Incorrect location."),
            ("INB", "Pending inbound: Wait for arrival. Ask Receiving."),
            ("SCN", "Won't turn on / black screen: Battery. Charge 5 min."),
            ("SRP", "SURPLUS: Pallet roll without location. Move to mass."),
        ],
        "back_title": "🟡 Quick solution",
        "back_steps": [
            '"No inventory found" → Check LPN in BY. DSP → DONE.',
            "Code 20 / invalid LPN → SSCC not read well. Retry or manual entry.",
            "Code 38 / Wrong location → Check slot in BY. CHANGE POSITION.",
            '"ANOTHER POSITION" → Picking active elsewhere. Wait.',
            "Blue Yonder unresponsive → Log out. Re-enter. Wait 30 sec.",
        ],
    },
    {
        "id": 3, "emoji": "🟢", "tier": "green",
        "front_title": "Smart Scanner / Labels",
        "front_sub": "SMAR T7 · Zebra Printer",
        "front_items": [
            ("1QR", "Personal QR → Scan your QR at SMAR T7 to log in"),
            ("2LC", "Location → Scan location code. E.g. BNT09"),
            ("3EQ", "Equipment → Scan assigned EPT/EPTXL"),
            ("4TR", "Day turn → Scan turn code"),
            ("PRN", "Printer not responding: Check paper/ribbon. On/Off."),
        ],
        "back_title": "🟢 Smart Scanner — Sequence",
        "back_steps": [
            "Step 1: Personal QR (identification)",
            "Step 2: Location code (where you are)",
            "Step 3: Equipment code (what you use)",
            "Step 4: Day turn code",
            "Zebra: Paper → Ribbon → Power cycle → Test → Report",
        ],
    },
    {
        "id": 4, "emoji": "🟠", "tier": "orange",
        "front_title": "Emergencies / Human error",
        "front_sub": "Wrong location · Fallen product",
        "front_items": [
            ("STOP", "Fallen/broken product: Don't touch. Call Teamleader."),
            ("MOVE", "Load in wrong location: CHANGE POSITION."),
            ("CPT", "Misread code (CPT8000): Not an error. Check manually."),
            ("ACC", "Accident: STOP. Call supervisor. Don't move anything."),
            ("LOCK", "Scanner blocks process: DONE → restart."),
        ],
        "back_title": "🟠 Emergency protocol",
        "back_steps": [
            "STOP — Stop what you're doing",
            "NOTIFY — Teamleader / Supervisor / GC",
            "DO NOT MODIFY — Don't move anything",
            "DOCUMENT — Take notes (photo if possible)",
            "Location error: CHANGE POSITION → scan current → new → confirm",
        ],
    },
    {
        "id": 5, "emoji": "🟣", "tier": "purple",
        "front_title": "Quick codes",
        "front_sub": "Smart Scanner · Blue Yonder",
        "front_items": [
            ("1QR", "Personal QR — Unique operator identification"),
            ("2LC", "Location — Location code. E.g. BNT09"),
            ("3EQ", "Equipment — Assigned EPT / EPTXS / EPTXL"),
            ("4TR", "Day turn — Current shift code"),
            ("ZNS", "Zones: PND-A · PND-P · T3-STGE · BNT09"),
        ],
        "back_title": "🟣 What's each code for?",
        "back_steps": [
            "Personal QR → Log in to SMAR T7. Identifies the operator.",
            "Location → Tells the system WHERE you're working.",
            "Equipment → Assigns the EPT/EPTXL to your session.",
            "Day turn → Registers the shift in the system.",
            "Smart Scanner: Personal QR only | Blue Yonder: all 4 codes",
        ],
    },
    {
        "id": 6, "emoji": "⭐", "tier": "rule",
        "front_title": "Golden Rule + Checklist",
        "front_sub": "Your daily mantra",
        "mantra": '"If something looks wrong, it is wrong."',
        "front_items": [
            ("1", "Check equipment (scanner, EPT)"),
            ("2", "Log into the system"),
            ("3", "Review assigned tasks"),
            ("4", "Confirm zone and shift"),
        ],
        "back_title": "⭐ Golden Rule",
        "back_quote": "If something looks wrong, it is wrong. Don't ignore it. Verify it.",
        "back_steps_title": "🏹 Shift start checklist",
        "back_steps": [
            "Turn on Smart Scanner (SMAR T7)",
            "Scan Personal QR → log in",
            "Scan Location (your zone)",
            "Scan Equipment (assigned EPT)",
            "Scan Day turn",
            "Check Blue Yonder for tasks",
        ],
    },
]

# ===== DUTCH =====
CARDS["nl"] = [
    {
        "id": 1, "emoji": "🔴", "tier": "red",
        "front_title": "Fysieke laadproblemen",
        "front_sub": "LPN · SSCC · RCG · Pallet · Krat",
        "front_items": [
            ("LPN", "Beschadigd / onleesbaar label: Niet leesbaar → nieuw label printen"),
            ("SSCC", "Verkeerde code: Controleren in Blue Yonder → herprinten"),
            ("RCG", "Code niet herkend: Handmatig scannen via INVENTORY DSP"),
            ("Pallet", "Beschadigd / instabiel: Verplaatsen naar nieuwe pallet. Herlabelen."),
            ("Krat", "Beschadigde krat: Vervangen. Inhoud controleren."),
        ],
        "back_title": "🔴 Snelle oplossing",
        "back_steps": [
            "Beschadigde LPN → SMAR T7 → NIEUW LABEL PRINTEN.",
            "SSCC afgewezen → Code checken in BY. Wijzig LPN/SSCC indien nodig.",
            "RCG leest niet → INVENTORY DSP → handmatig scannen of pallet draaien.",
            "Pallet/Krat beschadigd → Verplaatsen naar nieuwe pallet. Herlabelen.",
            "Werkt het nog niet? → Bel Teamleader of Troubleshooter.",
        ],
    },
    {
        "id": 2, "emoji": "🟡", "tier": "yellow",
        "front_title": "Scanner / Systeemfouten",
        "front_sub": "Code 20 · 38 · No inventory",
        "front_items": [
            ("C 20", "No inventory found: LPN niet geregistreerd. Controleren."),
            ("C 38", "Wrong slot location: Verkeerde locatie."),
            ("INB", "Inbound in afwachting: Wachten. Vraag Ontvangst."),
            ("SCN", "Scanner gaat niet aan: Batterij. 5 min opladen."),
            ("SRP", "SURPLUS: Rolpallet zonder locatie. Naar massasurplus."),
        ],
        "back_title": "🟡 Snelle oplossing",
        "back_steps": [
            '"No inventory found" → LPN in BY checken. INVENTORY DSP → DONE.',
            "Code 20 / ongeldige LPN → SSCC niet goed gelezen. Opnieuw of handmatig.",
            "Code 38 / Verkeerde locatie → Slot checken in BY. CHANGE POSITION.",
            '"ANOTHER POSITION" → Picking actief elders. Wachten.',
            "Blue Yonder reageert niet → Uitloggen. Opnieuw inloggen. 30 sec wachten.",
        ],
    },
    {
        "id": 3, "emoji": "🟢", "tier": "green",
        "front_title": "Smart Scanner / Labels",
        "front_sub": "SMAR T7 · Zebra Printer",
        "front_items": [
            ("1QR", "Persoonlijke QR → Scan QR op SMAR T7 om in te loggen"),
            ("2LC", "Locatie → Scan locatiecode. Bijv. BNT09"),
            ("3EQ", "Equipment → Scan toegewezen EPT/EPTXL"),
            ("4TR", "Dagdienst → Scan dienstcode"),
            ("PRN", "Printer reageert niet: Controleer papier/lint. Aan/uit."),
        ],
        "back_title": "🟢 Smart Scanner — Volgorde",
        "back_steps": [
            "Stap 1: Persoonlijke QR (identificatie)",
            "Stap 2: Locatiecode (waar je bent)",
            "Stap 3: Equipmentcode (wat je gebruikt)",
            "Stap 4: Dagdienstcode",
            "Zebra: Papier → Lint → Aan/uit → Test → Melden",
        ],
    },
    {
        "id": 4, "emoji": "🟠", "tier": "orange",
        "front_title": "Noodgevallen / Menselijke fout",
        "front_sub": "Verkeerde locatie · Product gevallen",
        "front_items": [
            ("STOP", "Gevallen/beschadigd product: Niet aanraken. Bel Teamleader."),
            ("MOVE", "Lading op verkeerde locatie: CHANGE POSITION."),
            ("CPT", "Code verkeerd gelezen (CPT8000): Geen fout. Handmatig checken."),
            ("ACC", "Ongeluk: STOP. Bel supervisor. Niks verplaatsen."),
            ("LOCK", "Scanner blokkeert proces: DONE → herstarten."),
        ],
        "back_title": "🟠 Noodprotocol",
        "back_steps": [
            "STOPPEN — Stop waar je mee bezig bent",
            "MELDEN — Teamleader / Supervisor / GC",
            "NIET WIJZIGEN — Verplaats niks tot verantwoordelijke komt",
            "DOCUMENTEREN — Noteer wat er gebeurde (foto indien mogelijk)",
            "Locatiefout: CHANGE POSITION → scan huidig → nieuw → bevestigen",
        ],
    },
    {
        "id": 5, "emoji": "🟣", "tier": "purple",
        "front_title": "Snelle codes",
        "front_sub": "Smart Scanner · Blue Yonder",
        "front_items": [
            ("1QR", "Persoonlijke QR — Unieke operatoridentificatie"),
            ("2LC", "Locatie — Locatiecode. Bijv. BNT09"),
            ("3EQ", "Equipment — Toegewezen EPT / EPTXS / EPTXL"),
            ("4TR", "Dagdienst — Huidige dienstcode"),
            ("ZNS", "Zones: PND-A · PND-P · T3-STGE · BNT09"),
        ],
        "back_title": "🟣 Waar dient elke code voor?",
        "back_steps": [
            "Persoonlijke QR → Inloggen op SMAR T7. Identificeert de operator.",
            "Locatie → Vertelt het systeem WAAR je werkt.",
            "Equipment → Koppelt EPT/EPTXL aan je sessie.",
            "Dagdienst → Registreert de dienst in het systeem.",
            "Smart Scanner: alleen Persoonlijke QR | Blue Yonder: alle 4 codes",
        ],
    },
    {
        "id": 6, "emoji": "⭐", "tier": "rule",
        "front_title": "Gouden Regel + Checklist",
        "front_sub": "Je dagelijkse mantra",
        "mantra": '"Als iets er verkeerd uitziet, is het verkeerd."',
        "front_items": [
            ("1", "Controleer apparatuur (scanner, EPT)"),
            ("2", "Log in op het systeem"),
            ("3", "Bekijk toegewezen taken"),
            ("4", "Bevestig zone en dienst"),
        ],
        "back_title": "⭐ Gouden Regel",
        "back_quote": "Als iets er verkeerd uitziet, is het verkeerd. Negeer het niet. Controleer het.",
        "back_steps_title": "🏹 Dienststart checklist",
        "back_steps": [
            "Smart Scanner aanzetten (SMAR T7)",
            "Persoonlijke QR scannen → inloggen",
            "Locatie scannen (je zone)",
            "Equipment scannen (toegewezen EPT)",
            "Dagdienst scannen",
            "Taken controleren in Blue Yonder",
        ],
    },
]


def gen_badge(text, color):
    return f'<span class="cf-item-badge" style="background:{color}">{text}</span>'


def gen_card(card, lang, idx):
    colors = {"red": "#c62828", "yellow": "#f57f17", "green": "#2e7d32",
              "orange": "#bf360c", "purple": "#7b1fa2", "rule": "#c00"}
    color = colors.get(card["tier"], "#c00")
    tier_color = f"t-{card['tier']}"

    front_items = "".join(
        f'<div class="cf-item">{gen_badge(i[0], color)}<span class="cf-item-text"><strong>{i[1].split(":")[0] if ":" in i[1] else ""}</strong>{"".join(i[1].split(":")[1:])}</span></div>'
        for i in card["front_items"]
    )

    back_steps = "".join(
        f'<li class="cb-step"><span class="cb-num">{n+1}</span><span>{s}</span></li>'
        for n, s in enumerate(card["back_steps"])
    )

    # Add mantra/quote for card 6
    extra_front = ""
    extra_back = ""
    if "mantra" in card:
        extra_front = f'<div style="text-align:center;margin:2mm 0 1.5mm;font-size:7pt;font-weight:700;color:#c00;font-style:italic;">{card["mantra"]}</div>'
    if "back_quote" in card:
        extra_back = f'<div style="font-size:6.5pt;line-height:1.4;color:#333;margin-bottom:1.5mm;font-style:italic;background:#fff5f5;padding:1mm;border-left:1mm solid #c00;">{card["back_quote"]}</div>'
    if "back_steps_title" in card:
        extra_back += f'<div class="cb-title" style="margin-top:1mm;">{card["back_steps_title"]}</div>'

    return f'''<div class="card {tier_color}">
    <div class="card-front">
      <span class="card-label">{lang.upper()} F{idx+1}</span>
      <div class="cf-header">
        <div class="cf-emoji">{card["emoji"]}</div>
        <div class="cf-titles">
          <div class="cf-title">{card["front_title"]}</div>
          <div class="cf-sub">{card["front_sub"]}</div>
        </div>
      </div>
      <hr class="cf-divider" style="background:{color}">
      {extra_front}{front_items}
    </div>
  </div>
  <div class="card {tier_color}">
    <div class="card-back">
      <span class="card-label">{lang.upper()} B{idx+1}</span>
      <div class="cb-title">{card["back_title"]}</div>
      {extra_back}<ol class="cb-steps">{back_steps}</ol>
    </div>
  </div>'''


def gen_lang_sheet(lang, label, flag):
    cards_html = "".join(gen_card(c, lang, i) for i, c in enumerate(CARDS[lang]))
    return f'''<div class="sheet">
  <div class="sheet-title">{flag} BONT · Pocket Cards — {label}</div>
  {cards_html}
</div>'''


html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BONT · Pocket Cards v0.1</title>
<style>
  @page {{ size: 85mm 55mm; margin: 0; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: "Segoe UI", Arial, sans-serif; background: #e0e0e0; padding: 20px; }}

  .sheet {{
    display: grid;
    grid-template-columns: repeat(3, 85mm);
    gap: 8mm;
    justify-content: center;
    margin-bottom: 30px;
  }}
  .sheet-title {{
    grid-column: 1 / -1;
    font-size: 14px; font-weight: 700; color: #c00;
    text-align: center; padding: 8px; background: #fff;
    border-radius: 6px; letter-spacing: 1px;
  }}

  .card {{
    width: 85mm; height: 55mm;
    position: relative; overflow: hidden;
    border-radius: 3px; break-inside: avoid;
  }}
  .card-front, .card-back {{
    width: 100%; height: 100%; padding: 4mm 5mm;
    box-sizing: border-box; font-size: 0; position: relative;
  }}
  .card-front {{ background: #fff; border: 0.5px solid #ccc; }}
  .card-back  {{ background: #f9f9f9; border: 0.5px solid #ccc; }}

  .card::before {{
    content: '';
    position: absolute;
    top: -1mm; left: -1mm; right: -1mm; bottom: -1mm;
    border: 0.3mm dashed #999; border-radius: 4px;
    pointer-events: none; z-index: 10;
  }}
  .card-label {{
    position: absolute; top: 0.5mm; right: 1mm;
    font-size: 5px; color: #999; font-weight: 600; z-index: 5;
  }}
  .cf-header {{ display: flex; align-items: center; gap: 2mm; margin-bottom: 1.5mm; }}
  .cf-emoji {{ font-size: 10mm; line-height: 1; }}
  .cf-titles {{ flex: 1; }}
  .cf-title {{ font-size: 7.5pt; font-weight: 800; text-transform: uppercase; letter-spacing: 0.3px; line-height: 1.15; }}
  .cf-sub {{ font-size: 5.5pt; color: #888; font-weight: 500; margin-top: 0.5mm; }}
  .cf-divider {{ height: 0.5mm; border: none; margin: 1.5mm 0; }}
  .cf-item {{ display: flex; align-items: flex-start; gap: 1.5mm; margin-bottom: 0.8mm; }}
  .cf-item-badge {{ font-size: 6.5pt; font-weight: 700; color: #fff; padding: 0.5mm 2mm; border-radius: 2px; white-space: nowrap; min-width: 12mm; text-align: center; }}
  .cf-item-text {{ font-size: 6pt; line-height: 1.3; color: #333; flex: 1; }}
  .cf-item-text strong {{ color: #111; }}

  .cb-title {{ font-size: 6.5pt; font-weight: 700; color: #c00; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 1mm; border-bottom: 0.3mm solid #ddd; padding-bottom: 0.5mm; }}
  .cb-steps {{ list-style: none; padding: 0; }}
  .cb-step {{ display: flex; gap: 1.5mm; margin-bottom: 0.6mm; font-size: 5.8pt; line-height: 1.3; color: #333; }}
  .cb-num {{ font-weight: 700; color: #c00; min-width: 3mm; font-size: 6pt; }}
  .cb-strong {{ font-weight: 700; color: #111; }}

  @media print {{
    body {{ background: white; padding: 0; }}
    .sheet {{ margin: 0; gap: 0; }}
    @page {{ margin: 0; }}
    .card::before {{ display: none; }}
  }}
</style>
</head>
<body>

{gen_lang_sheet("es", "Español", "🇪🇸")}
{gen_lang_sheet("en", "English", "🇬🇧")}
{gen_lang_sheet("nl", "Nederlands", "🇳🇱")}

</body>
</html>'''

out_path = "/home/sacharuna/dev/Bont/pocket-cards.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Pocket cards generadas: {out_path}")
print(f"   {os.path.getsize(out_path)/1024:.0f} KB")
print("   3 idiomas × 6 tarjetas (anverso+reverso) = 18 tarjetas")

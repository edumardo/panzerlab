"""Build the canonical decomposition skeleton (manifests + content.json) for
Nm 261/237 (Maybach HL 120 TRM Ersatzteil-Liste).

Overwrites: manifest.json, sections/*/manifest.json, sections/*/pages/*/manifest.json,
sections/*/pages/*/content.json, frontmatter/manifest.json, frontmatter/pages/*/manifest.json,
frontmatter/pages/*/content.json, index/contents.json.
Never touches source.jpg / source_display.jpg / assets/.
Idempotent: re-running regenerates the same files from the data tables below.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC_ID = "nm261-237"
DOC_PREFIX = "nm261237"

LANGS = ["de", "en-GB", "es-ES"]


def page_id(n: int) -> str:
    return f"{DOC_PREFIX}-page-{n:03d}"


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Explicit page map: page -> (section, pdf_spread, side)
# ---------------------------------------------------------------------------
PAGE_MAP = {
    1: ("FrontMatter", 2, "right"),
    2: ("FrontMatter", 3, "left"),
    3: ("FrontMatter", 3, "right"),
    4: ("A01", 4, "left"),
    5: ("A01", 4, "right"),
    6: ("A02", 5, "left"),
    7: ("A02", 5, "right"),
    8: ("A03", 6, "left"),
    9: ("A03", 6, "right"),
    10: ("A04", 7, "left"),
    11: ("A04", 7, "right"),
    12: ("A05", 8, "left"),
    13: ("A05", 8, "right"),
    14: ("A06", 9, "left"),
    15: ("A06", 9, "right"),
    16: ("A07", 10, "left"),
    17: ("A07", 10, "right"),
    18: ("A08", 11, "left"),
    19: ("A08", 11, "right"),
    20: ("A09", 12, "left"),
    21: ("A09", 12, "right"),
}

SECTION_TITLES = {
    "FrontMatter": {"de": None, "en-GB": None, "es-ES": None},
    "A01": {
        "de": "Brennstoffpumpe, Druckölfilter, Elektrische Apparate (Tafel 1)",
        "en-GB": "Fuel pump, pressure oil filter, electrical equipment (Plate 1)",
        "es-ES": "Bomba de combustible, filtro de aceite a presión, equipo eléctrico (Lámina 1)",
    },
    "A02": {
        "de": "Kurbelgehäuse (Tafel 2)",
        "en-GB": "Crankcase (Plate 2)",
        "es-ES": "Cárter del cigüeñal (Lámina 2)",
    },
    "A03": {
        "de": "Kurbelgehäuse (Fortsetzung), Motorlagerung (Tafel 3)",
        "en-GB": "Crankcase (continued), engine mounting (Plate 3)",
        "es-ES": "Cárter del cigüeñal (continuación), bancada del motor (Lámina 3)",
    },
    "A04": {
        "de": "Ölbehälter, Ölkühler, Ölpumpen — Ausführung „A“ (Tafel 4)",
        "en-GB": "Oil tank, oil cooler, oil pumps — version “A” (Plate 4)",
        "es-ES": "Depósito de aceite, radiador de aceite, bombas de aceite — versión «A» (Lámina 4)",
    },
    "A05": {
        "de": "Ölbehälter, Ölkühler, Ölpumpen — Ausführung „B“ (Tafel 5)",
        "en-GB": "Oil tank, oil cooler, oil pumps — version “B” (Plate 5)",
        "es-ES": "Depósito de aceite, radiador de aceite, bombas de aceite — versión «B» (Lámina 5)",
    },
    "A06": {
        "de": "Saug- und Auspuffrohr mit Vergaser (Tafel 6)",
        "en-GB": "Intake and exhaust manifold with carburettor (Plate 6)",
        "es-ES": "Colector de admisión y escape con carburador (Lámina 6)",
    },
    "A07": {
        "de": "Schwingungsdämpfer, Schwungkraft-Anlasser, Triebwerk (Tafel 7)",
        "en-GB": "Vibration damper, inertia starter, engine gear train (Plate 7)",
        "es-ES": "Amortiguador de vibraciones, motor de arranque por inercia, tren motor (Lámina 7)",
    },
    "A08": {
        "de": "Wasserpumpe mit Antrieb, Zylinderkopf (Tafel 8)",
        "en-GB": "Water pump with drive, cylinder head (Plate 8)",
        "es-ES": "Bomba de agua con accionamiento, culata (Lámina 8)",
    },
    "A09": {
        "de": "Zylinderkopf (Fortsetzung), Zubehörteile und Werkzeuge (Tafel 9)",
        "en-GB": "Cylinder head (continued), accessories and tools (Plate 9)",
        "es-ES": "Culata (continuación), accesorios y herramientas (Lámina 9)",
    },
}

# ---------------------------------------------------------------------------
# Row data for fully-transcribed sections (FrontMatter, A01, A02).
# Each row: (number, de, en-GB, es-ES, quantity, part_no)
# ---------------------------------------------------------------------------

A01_PAGE005_ROWS = [
    (1, "Solex-Brennstoffpumpe, links", "Solex fuel pump, left", "Bomba de combustible Solex, izquierda", 1, "224956/0 (A)"),
    (1, "Solex-Brennstoffpumpe, rechts", "Solex fuel pump, right", "Bomba de combustible Solex, derecha", 1, "224957/0 (A)"),
    (2, "Solex-Brennstoffpumpe, links", "Solex fuel pump, left", "Bomba de combustible Solex, izquierda", 1, "230451/0 (B)"),
    (2, "Solex-Brennstoffpumpe, rechts", "Solex fuel pump, right", "Bomba de combustible Solex, derecha", 1, "223048/0 (B)"),
    (3, "Isolierflansch", "Insulating flange", "Brida aislante", 2, "312403/1"),
    (4, "Dichtung", "Gasket", "Junta", 2, "81919"),
    (5, "Einschraubstutzen für Rohr 10×8 Ø", "Screw-in union for 10×8 mm pipe", "Racor roscado para tubo de 10×8 Ø", 2, "358075/0"),
    (6, "Ermeto-Dichtkegel für Rohr 10×8 Ø", "Ermeto sealing cone for 10×8 mm pipe", "Cono de estanqueidad Ermeto para tubo de 10×8 Ø", 2, "313512/0"),
    (7, "Überwurfmutter für Rohr 10×8 Ø", "Union nut for 10×8 mm pipe", "Tuerca de racor para tubo de 10×8 Ø", 2, "313511/0"),
    (8, "Einschraubstutzen für Rohr 8×6 Ø", "Screw-in union for 8×6 mm pipe", "Racor roscado para tubo de 8×6 Ø", 2, "358080/0"),
    (9, "Ermeto-Dichtkegel für Rohr 8×6 Ø", "Ermeto sealing cone for 8×6 mm pipe", "Cono de estanqueidad Ermeto para tubo de 8×6 Ø", 2, "313713/0"),
    (10, "Überwurfmutter für Rohr 8×6 Ø", "Union nut for 8×6 mm pipe", "Tuerca de racor para tubo de 8×6 Ø", 2, "358079/0"),
    (11, "Verbindungsleitung der Brennstoffpumpen", "Connecting line between the fuel pumps", "Tubería de unión de las bombas de combustible", 1, "223854/2"),
    (12, "Anschlußstück", "Connector piece", "Pieza de conexión", 1, "223835/3"),
    (13, "Dichtkegel", "Sealing cone", "Cono de estanqueidad", 1, "E 3069"),
    (14, "Überwurfmutter", "Union nut", "Tuerca de racor", 1, "E 3068"),
    (15, "EC-Spaltfilter", "EC gap-type oil filter", "Filtro de ranuras EC", 1, "224964/1 (A)"),
    (16, "EC-Spaltfilter", "EC gap-type oil filter", "Filtro de ranuras EC", 1, "227741/0 (B)"),
    (17, "Kugelpfanne mit Zusatzsicherung", "Ball socket with additional locking", "Rótula con seguro adicional", 1, "10 K 1802 u. E. 5665"),
    (18, "Sicherungsblech", "Locking plate", "Chapa de seguridad", 4, "E 3184"),
    (19, "Dichtkegel", "Sealing cone", "Cono de estanqueidad", 1, "E 7087"),
    (20, "Überwurfmutter", "Union nut", "Tuerca de racor", 1, "E 7087"),
    (21, "Dichtung für Ölzulauf", "Gasket for oil inlet", "Junta para entrada de aceite", 1, "303075/1"),
    (22, "Dichtung für Ölrücklauf", "Gasket for oil return", "Junta para retorno de aceite", 1, "301381"),
    (23, "Lichtmaschine", "Dynamo", "Dínamo", 1, "218728/2 (A)"),
    (24, "Lichtmaschine", "Dynamo", "Dínamo", 1, "226579/0 (B)"),
    (25, "Anlasser", "Starter motor", "Motor de arranque", 1, "228334/0"),
    (26, "Magnetzünder", "Magneto", "Magneto", 1, "226177/0"),
    (27, "Zündkerze", "Spark plug", "Bujía", 12, "W 225 T 22"),
    (28, "Dichtring für Zündkerze", "Sealing ring for spark plug", "Anillo de estanqueidad para bujía", 12, "C14×20 Din 7603"),
    (29, "Magnetzünder-Gehäuse", "Magneto housing", "Carcasa del magneto", 1, "313098/2"),
    (30, "Verschlußschraube", "Screw plug", "Tornillo tapón", 1, "AM 30×1,5 Din 7604"),
    (31, "Dichtring", "Sealing ring", "Anillo de estanqueidad", 1, "C 30×36 Din 7603"),
    (32, "Gummischnur 5×6 cm 157 lg.", "Rubber cord, 5×6 mm section, 157 mm long", "Cordón de goma 5×6 mm, 157 mm de largo", 1, "309079/0"),
    (33, "Konsole", "Bracket", "Ménsula", 1, "222524/0"),
    (34, "Gewindebuchse", "Threaded bushing", "Casquillo roscado", 4, "50018"),
    (35, "Bügel für Lichtmaschine", "Clip for dynamo", "Abrazadera para la dínamo", 2, "88607/2"),
    (36, "Bügel für Anlasser", "Clip for starter motor", "Abrazadera para el motor de arranque", 2, "312231/4"),
    (37, "Reglerkasten", "Regulator box", "Caja del regulador", 1, "220202/1"),
    (38, "Riemenscheibe mit 2 Rillen", "Belt pulley with 2 grooves", "Polea con 2 canales", 1, "308547/1 (A)"),
    (39, "Riemenscheibe mit 3 Rillen", "Belt pulley with 3 grooves", "Polea con 3 canales", 1, "308381/0 (B)"),
    (40, "Sicherungsblech", "Locking plate", "Chapa de seguridad", 4, "E 3184"),
    (41, "Antriebsrad", "Drive gear", "Rueda de arrastre", 1, "227998/0"),
    (42, "Bolzen", "Bolt", "Perno", 1, "88606"),
    (43, "Stellscheibe", "Adjusting shim", "Arandela de ajuste", 1, "88574/2"),
    (44, "Stiftschraube", "Stud bolt", "Espárrago", 2, "316104/0 (B)"),
    (45, "Sterngriff", "Star grip", "Empuñadura de estrella", 2, "E 32280 (B)"),
    (46, "Abschirmblech", "Shielding plate", "Chapa de blindaje", 1, "315962/0"),
    (47, "Kabeldeckel links, komplett", "Cable cover, left, complete", "Tapa de cables, izquierda, completa", 1, "228025/2"),
    (47, "Kabeldeckel rechts, komplett", "Cable cover, right, complete", "Tapa de cables, derecha, completa", 1, "228026/2"),
    (48, "Buna-Gummischnur 5Ø 1592 lg.", "Buna rubber cord, 5 mm dia., 1592 mm long", "Cordón de goma Buna, 5 mm Ø, 1592 mm de largo", 2, "223386/1"),
    (49, "Sechskantschraube", "Hex bolt", "Tornillo hexagonal", 4, "312600/2"),
    (50, "Sicherungsring", "Locking ring", "Anillo de seguridad", 4, "308154/1"),
    (51, "Satz Kabel rechts, komplett", "Cable set, right, complete", "Juego de cables, derecho, completo", 1, "226912/0"),
    (51, "Satz Kabel links, komplett", "Cable set, left, complete", "Juego de cables, izquierdo, completo", 1, "226913/0"),
    (52, "Kabelstecker", "Cable plug", "Conector de cable", 12, "223435/1"),
    (53, "Kabelnummernschild 1M–6M", "Cable number tag, 1M–6M", "Placa de numeración de cables 1M–6M", 2, "54060–65"),
    (54, "Kabelnummernschild 7M–12M", "Cable number tag, 7M–12M", "Placa de numeración de cables 7M–12M", 2, "67680–85"),
    (55, "Kabelleitung Plus 30", "Cable lead, positive 30", "Cable positivo 30", 1, "223331/0"),
    (56, "Kabelleitung Minus 31", "Cable lead, negative 31", "Cable negativo 31", 2, "223332/0"),
    (57, "Rohrschelle", "Pipe clamp", "Abrazadera de tubo", 1, "223333/0"),
    (58, "Kabelleitung", "Cable lead", "Cable", 2, "229942/1"),
    (59, "Entstörschlauch, komplett", "Radio-suppression hose, complete", "Manguera antiparasitaria, completa", 2, "316048/0"),
    (60, "Gewindestutzen", "Threaded stub", "Racor roscado", 2, "301777"),
    (61, "Gummitülle 10 InnenØ", "Rubber grommet, 10 mm inner dia.", "Pasacables de goma, 10 mm Ø interior", 4, "301778"),
]

A02_PAGE007_ROWS = [
    (1, "Kurbelgehäuse", "Crankcase", "Cárter del cigüeñal", 1, "221695/3"),
    (2, "vorderer Abschlußdeckel, komplett", "Front end cover, complete", "Tapa de cierre delantera, completa", 1, "220960/7"),
    (3, "Vierkantschraube", "Square-head bolt", "Tornillo de cabeza cuadrada", 2, "319498/0"),
    (4, "Sicherungsblech", "Locking plate", "Chapa de seguridad", 6, "E 3162"),
    (5, "Gummiring", "Rubber ring", "Anillo de goma", 1, "318481/0"),
    (6, "Zylinderbuchse", "Cylinder liner", "Camisa de cilindro", 12, "305640"),
    (7, "Dichtungsring", "Sealing ring", "Anillo de junta", 24, "306448/2"),
    (8, "Ölfangblech", "Oil deflector plate", "Chapa colectora de aceite", 12, "309143/2"),
    (9, "Wasserablaßstopfen", "Water drain plug", "Tapón de vaciado de agua", 2, "88571/1"),
    (10, "Dichtring", "Sealing ring", "Anillo de estanqueidad", 2, "C 18×22 Din 7603"),
    (11, "Überwurfmutter", "Union nut", "Tuerca de racor", 1, "A 16 M 26×1,5 Din 7606 (A)"),
    (12, "Dichtkegel", "Sealing cone", "Cono de estanqueidad", 1, "B 16 Din 7608 (A)"),
    (13, "Einschraubstutzen", "Screw-in union", "Racor roscado", 1, "A 16 Din 7611 (A)"),
    (14, "Dichtring", "Sealing ring", "Anillo de estanqueidad", 1, "C 26×32 Din 7603"),
    (15, "Kernlochstopfen", "Core-hole plug", "Tapón de agujero de macho", 1, "E 6530 (B)"),
    (16, "Lasche", "Strap", "Presilla", 1, "88573/2"),
    (17, "Winkel", "Angle bracket", "Escuadra", 1, "88590"),
    (18, "Düse", "Nozzle", "Tobera", 1, "305506/5"),
    (19, "Dichtring", "Sealing ring", "Anillo de estanqueidad", 1, "A 20×24 Din 7603 Cu"),
    (20, "Sicherungsblech", "Locking plate", "Chapa de seguridad", 8, "E 3184"),
    (21, "Deckel mit Öse, vorne", "Cover with eyelet, front", "Tapa con argolla, delantera", 1, "306751/1"),
    (22, "Dichtung, vorne", "Gasket, front", "Junta, delantera", 1, "306752/0"),
    (23, "Deckel ohne Öse, hinten", "Cover without eyelet, rear", "Tapa sin argolla, trasera", 1, "314802/1"),
    (24, "Dichtung hinten", "Gasket, rear", "Junta, trasera", 1, "306754/0"),
    (25, "Aufhängeöse", "Suspension eyelet", "Argolla de suspensión", 1, "304889/1"),
    (26, "Unterlegscheibe", "Washer, as required", "Arandela, según necesidad", None, "319040/0"),
    (27, "Zwischenrad", "Idler gear", "Engranaje intermedio", 1, "227879/0"),
    (28, "Zwischenradbolzen", "Idler gear pin", "Perno del engranaje intermedio", 1, "313353/0"),
    (29, "Kegelrollenlager", "Taper roller bearing", "Rodamiento de rodillos cónicos", 2, "VKF 30206"),
    (30, "Ausgleichscheibe", "Shim washer", "Arandela de compensación", 5, "89891/1"),
    (31, "Flansch", "Flange", "Brida", 1, "307769/1"),
    (32, "Dichtung", "Gasket", "Junta", 1, "307770/0"),
    (33, "Anlaufzapfen", "Thrust pin", "Espiga de tope", 1, "220960/7"),
    (34, "Füllstück", "Filler piece", "Pieza de relleno", 1, "88594/2"),
    (35, "Ausgleichscheibe", "Shim washer", "Arandela de compensación", 1, "88597/1"),
    (36, "Buchse", "Bushing", "Casquillo", 1, "309170/0"),
    (37, "Bundbuchse", "Flanged bushing", "Casquillo con collar", 2, "300053"),
    (38, "Buchse", "Bushing", "Casquillo", 1, "303828"),
    (39, "Buchse", "Bushing", "Casquillo", 1, "303829"),
    (40, "Sicherungsblech", "Locking plate", "Chapa de seguridad", 1, "303830"),
    (41, "Verschlußschraube", "Screw plug", "Tornillo tapón", 4, "77109/1"),
    (42, "Dichtring", "Sealing ring", "Anillo de estanqueidad", 5, "AM 18×1,5 Din 7604"),
    (43, "Schlitzstopfen", "Slotted plug", "Tapón ranurado", 1, "A 18×22 Din 7603 Cu"),
    (44, "Rückzugfeder", "Return spring", "Muelle de retorno", 2, "M 18×1,5 Kr 1022"),
    (45, "Federöse", "Spring eyelet", "Argolla del muelle", 1, "309075/0"),
    (46, "Brennstoff-Überlauf-Ventil, komplett", "Fuel overflow valve, complete", "Válvula de rebose de combustible, completa", 1, "309076/0"),
    (47, "Ermeto-Dichtkegel", "Ermeto sealing cone", "Cono de estanqueidad Ermeto", 1, "226573/2"),
    (48, "Ermeto-Überwurfmutter", "Ermeto union nut", "Tuerca de racor Ermeto", 3, "E 7737"),
    (49, "Ermeto-Schraubstutzen", "Ermeto screw union", "Racor roscado Ermeto", 3, "E 7738"),
    (50, "Dichtring", "Sealing ring", "Anillo de estanqueidad", 2, "C 18×22 Din 7603"),
    (51, "T-Stück", "T-piece", "Pieza en T", 1, "312641/1"),
    (52, "Rohrleitung", "Pipe", "Tubería", 1, "226574/1"),
    (53, "Einschraubnippel", "Screw-in nipple", "Racor roscado (niple)", 1, "E 3084"),
    (54, "Dichtring", "Sealing ring", "Anillo de estanqueidad", 1, "C 14×18 Din 7603"),
    (55, "Einschraubnippel", "Screw-in nipple", "Niple roscado", 1, "E 3084"),
    (56, "Dichtring", "Sealing ring", "Anillo de estanqueidad", 1, "C 18×22 Din 7603"),
    (57, "Rohrleitung", "Pipe", "Tubería", 1, "228782/0"),
    (58, "Verschlußschraube", "Screw plug", "Tornillo tapón", 1, "AM 12×1,5 Din 7604"),
    (59, "Dichtring", "Sealing ring", "Anillo de estanqueidad", 1, "C 12×16 Din 7603"),
]

DIAGRAM_GROUPS = {
    4: [
        {"de": "Brennstoffpumpe", "en-GB": "Fuel pump", "es-ES": "Bomba de combustible", "numbers": [1, 14]},
        {"de": "Druckölfilter", "en-GB": "Pressure oil filter", "es-ES": "Filtro de aceite a presión", "numbers": [15, 22]},
        {"de": "Elektrische Apparate", "en-GB": "Electrical equipment", "es-ES": "Equipo eléctrico", "numbers": [23, 62]},
    ],
    6: [
        {"de": "Kurbelgehäuse", "en-GB": "Crankcase", "es-ES": "Cárter del cigüeñal", "numbers": [1, 59]},
    ],
}


def localised_text(de: str, en: str, es: str) -> dict:
    return {
        "de": {"plain": de, "runs": [{"text": de, "bold": False}]},
        "en-GB": {"plain": en, "runs": [{"text": en, "bold": False}]},
        "es-ES": {"plain": es, "runs": [{"text": es, "bold": False}]},
    }


def make_row_paragraphs(page_num: int, rows: list) -> list:
    paragraphs = []
    for i, (num, de, en, es, qty, part_no) in enumerate(rows, start=1):
        paragraphs.append({
            "id": f"{DOC_PREFIX}-p{page_num:03d}-row{i:03d}",
            "number": num,
            "text": localised_text(de, en, es),
            "quantity": qty,
            "maybach_part_no": part_no,
        })
    return paragraphs


def make_diagram_figures(page_num: int) -> list:
    figures = []
    for i, group in enumerate(DIAGRAM_GROUPS.get(page_num, []), start=1):
        figures.append({
            "id": f"{DOC_PREFIX}-p{page_num:03d}-fig{i:02d}",
            "numbers": group["numbers"],
            "captions": {
                "de": {"plain": group["de"]},
                "en-GB": {"plain": group["en-GB"]},
                "es-ES": {"plain": group["es-ES"]},
            },
        })
    return figures


FULLY_TRANSCRIBED_PAGES = {5: A01_PAGE005_ROWS, 7: A02_PAGE007_ROWS}
DIAGRAM_PAGES_DONE = {4, 6}

FRONTMATTER_CONTENT = {
    1: {
        "type": "text",
        "titles": {
            "de": "Titelseite",
            "en-GB": "Title page",
            "es-ES": "Página de título",
        },
        "paragraphs": [
            {"id": f"{DOC_PREFIX}-p001-title", "text": localised_text(
                "MAYBACH-MOTOR HL 120 TRM — ERSATZTEIL-LISTE",
                "MAYBACH ENGINE HL 120 TRM — SPARE-PARTS LIST",
                "MOTOR MAYBACH HL 120 TRM — LISTA DE PIEZAS DE REPUESTO")},
            {"id": f"{DOC_PREFIX}-p001-note", "text": localised_text(
                "Beachten: Ausführung „A“ oder Ausführung „B“",
                "Note: version “A” or version “B”",
                "Atención: versión «A» o versión «B»")},
            {"id": f"{DOC_PREFIX}-p001-publisher", "text": localised_text(
                "Maybach-Motorenbau G.m.b.H. / Friedrichshafen a.B.",
                "Maybach-Motorenbau G.m.b.H. / Friedrichshafen a.B. (manufacturer)",
                "Maybach-Motorenbau G.m.b.H. / Friedrichshafen a.B. (fabricante)")},
            {"id": f"{DOC_PREFIX}-p001-contact", "text": localised_text(
                "Fernsprecher: 651 / Telegramme: Maybachmotor / Fernschreibnummer: 06958",
                "Telephone: 651 / Telegrams: Maybachmotor / Teleprinter number: 06958",
                "Teléfono: 651 / Telegramas: Maybachmotor / Número de télex: 06958")},
        ],
    },
    2: {
        "type": "figures",
        "titles": {
            "de": "HL 120 TRM — Werkfotos Ausführung A und B",
            "en-GB": "HL 120 TRM — factory photographs, versions A and B",
            "es-ES": "HL 120 TRM — fotografías de fábrica, versiones A y B",
        },
        "figures": [
            {"id": f"{DOC_PREFIX}-p002-fig01", "captions": {
                "de": {"plain": "Ausführung „A“, Lichtmaschinenseite"},
                "en-GB": {"plain": "Version “A”, dynamo side"},
                "es-ES": {"plain": "Versión «A», lado de la dínamo"}}},
            {"id": f"{DOC_PREFIX}-p002-fig02", "captions": {
                "de": {"plain": "Ausführung „A“, Ölkühlerseite"},
                "en-GB": {"plain": "Version “A”, oil-cooler side"},
                "es-ES": {"plain": "Versión «A», lado del radiador de aceite"}}},
            {"id": f"{DOC_PREFIX}-p002-fig03", "captions": {
                "de": {"plain": "Ausführung „B“, Lichtmaschinenseite"},
                "en-GB": {"plain": "Version “B”, dynamo side"},
                "es-ES": {"plain": "Versión «B», lado de la dínamo"}}},
            {"id": f"{DOC_PREFIX}-p002-fig04", "captions": {
                "de": {"plain": "Ausführung „B“, Ölkühlerseite"},
                "en-GB": {"plain": "Version “B”, oil-cooler side"},
                "es-ES": {"plain": "Versión «B», lado del radiador de aceite"}}},
        ],
    },
    3: {
        "type": "index",
        "titles": {
            "de": "Achtung! Inhaltsverzeichnis",
            "en-GB": "Attention! Table of contents",
            "es-ES": "¡Atención! Índice",
        },
        "paragraphs": [
            {"id": f"{DOC_PREFIX}-p003-notice", "text": localised_text(
                "Achtung! Wichtig! zur Vermeidung von Lieferungsverzögerungen! Bei Ersatzteil-Bestellungen ist unbedingt die Motornummer mit anzugeben, beispielsweise: sendet Teil-Nr. 49738, Motor 7035",
                "Attention! Important, to avoid delivery delays! Spare-part orders must always state the engine number, for example: send part no. 49738, engine 7035",
                "¡Atención! ¡Importante para evitar retrasos en la entrega! Los pedidos de piezas de repuesto deben indicar siempre el número de motor, por ejemplo: enviar pieza n.º 49738, motor 7035")},
        ],
    },
}


def build_page(page_num: int) -> None:
    section, spread, side = PAGE_MAP[page_num]
    is_frontmatter = section == "FrontMatter"
    base_dir = ROOT / ("frontmatter" if is_frontmatter else f"sections/{section}") / "pages" / f"{page_num:03d}"

    prev_id = page_id(page_num - 1) if page_num > 1 else None
    next_id = page_id(page_num + 1) if page_num < max(PAGE_MAP) else None

    if is_frontmatter:
        fm = FRONTMATTER_CONTENT[page_num]
        page_type = fm["type"]
        titles = fm["titles"]
        paragraphs = fm.get("paragraphs", [])
        figures = fm.get("figures", [])
        transcription_status = "validated"
        translation_status = "validated"
    elif page_num in FULLY_TRANSCRIBED_PAGES:
        titles = SECTION_TITLES[section]
        page_type = "text"
        paragraphs = make_row_paragraphs(page_num, FULLY_TRANSCRIBED_PAGES[page_num])
        figures = []
        transcription_status = "validated"
        translation_status = "validated"
    elif page_num in DIAGRAM_PAGES_DONE:
        titles = SECTION_TITLES[section]
        page_type = "figures"
        paragraphs = []
        figures = make_diagram_figures(page_num)
        transcription_status = "validated"
        translation_status = "validated"
    else:
        titles = SECTION_TITLES[section]
        page_type = "unclassified"
        paragraphs = []
        figures = []
        transcription_status = "pending"
        translation_status = "pending"

    content = {
        "schema_version": 1,
        "id": page_id(page_num),
        "document_id": DOC_ID,
        "page": page_num,
        "section": section,
        "type": page_type,
        "titles": titles,
        "source": {
            "image": "source.jpg",
            "pdf_spread": spread,
            "side": side,
            "status": "extracted_clean",
        },
        "navigation": {"previous": prev_id, "next": next_id},
        "paragraphs": paragraphs,
        "figures": figures,
        "status": {
            "transcription": transcription_status,
            "en-GB": translation_status,
            "es-ES": translation_status,
            "figures": "not_applicable" if page_type != "figures" else transcription_status,
        },
    }
    write_json(base_dir / "content.json", content)

    manifest = {
        "page": page_num,
        "section": section,
        "pdf_spread": spread,
        "side": side,
        "source_scan": "source.jpg",
        "content": "content.json",
        "source_scan_status": "extracted_clean",
        "transcription_status": transcription_status,
        "translation_en_status": translation_status,
        "translation_es_status": translation_status,
        "figures": [{"number": f["numbers"][0] if "numbers" in f else None} for f in figures] if figures else [],
    }
    write_json(base_dir / "manifest.json", manifest)
    return manifest


def main():
    global_pages = []
    for page_num in sorted(PAGE_MAP):
        manifest = build_page(page_num)
        global_pages.append(manifest)

    # Section manifests
    section_ranges = {}
    for page_num, (section, _, _) in PAGE_MAP.items():
        lo, hi = section_ranges.get(section, (page_num, page_num))
        section_ranges[section] = (min(lo, page_num), max(hi, page_num))

    for section, (lo, hi) in section_ranges.items():
        section_dir = ROOT / ("frontmatter" if section == "FrontMatter" else f"sections/{section}")
        write_json(section_dir / "manifest.json", {
            "id": section,
            "pages": list(range(lo, hi + 1)),
            "titles": SECTION_TITLES[section],
            "output": {"cover": False, "header": False, "footer": False},
            "layout": "A4_portrait_facsimile_then_translation",
        })

    # Global manifest
    write_json(ROOT / "manifest.json", {
        "document": "Nm 261/237",
        "source_pdf_pages": 15,
        "book_pages": [1, max(PAGE_MAP)],
        "languages": ["de", "en-GB", "es-ES"],
        "sections": {s: [lo, hi] for s, (lo, hi) in section_ranges.items()},
        "pages": global_pages,
    })

    # index/contents.json mirrors the printed Inhaltsverzeichnis (TOC), page 3
    toc_groups = [
        ("Brennstoffpumpe", "Fuel pump", "Bomba de combustible", "1", "A01"),
        ("Drucköfilter", "Pressure oil filter", "Filtro de aceite a presión", "1", "A01"),
        ("Elektrische Apparate", "Electrical equipment", "Equipo eléctrico", "1", "A01"),
        ("Kurbelgehäuse", "Crankcase", "Cárter del cigüeñal", "2 u. 3", "A02–A03"),
        ("Motorlagerung", "Engine mounting", "Bancada del motor", "3", "A03"),
        ("Ölbehälter (Ausführung A)", "Oil tank (version A)", "Depósito de aceite (versión A)", "4", "A04"),
        ("Ölkühler (Ausführung A)", "Oil cooler (version A)", "Radiador de aceite (versión A)", "4", "A04"),
        ("Ölpumpen (Ausführung A)", "Oil pumps (version A)", "Bombas de aceite (versión A)", "4", "A04"),
        ("Ölbehälter (Ausführung B)", "Oil tank (version B)", "Depósito de aceite (versión B)", "5", "A05"),
        ("Ölkühler (Ausführung B)", "Oil cooler (version B)", "Radiador de aceite (versión B)", "5", "A05"),
        ("Ölpumpen (Ausführung B)", "Oil pumps (version B)", "Bombas de aceite (versión B)", "5", "A05"),
        ("Saug- und Auspuffrohr mit Vergaser", "Intake and exhaust manifold with carburettor", "Colector de admisión y escape con carburador", "6", "A06"),
        ("Schwingungsdämpfer", "Vibration damper", "Amortiguador de vibraciones", "7", "A07"),
        ("Schwungkraft-Anlasser", "Inertia starter", "Motor de arranque por inercia", "7", "A07"),
        ("Triebwerk", "Engine gear train", "Tren motor", "7", "A07"),
        ("Zylinderkopf", "Cylinder head", "Culata", "8 u. 9", "A08–A09"),
        ("Zubehörteile und Werkzeuge", "Accessories and tools", "Accesorios y herramientas", "9", "A09"),
    ]
    write_json(ROOT / "index" / "contents.json", {
        "schema_version": 1,
        "document_id": DOC_ID,
        "source_page": 3,
        "entries": [
            {"group_de": g[0], "group_en": g[1], "group_es": g[2], "tafel": g[3], "section": g[4]}
            for g in toc_groups
        ],
    })

    print(f"Built {len(global_pages)} pages across {len(section_ranges)} sections.")


if __name__ == "__main__":
    main()

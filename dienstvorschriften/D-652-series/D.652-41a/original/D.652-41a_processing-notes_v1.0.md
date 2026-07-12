# D 652/41a — Bilingual translation project: processing notes

**Purpose:** working record of how the translated editions of Wehrmacht manual **D 652/41a** were
produced, so the job can be reprocessed or extended later. Two editions exist, both **Version 1.0**:
- **DE-EN** — original German + English (British spelling).
- **DE-ES** — original German + Spanish (Castilian / español de España).

Compiled for Eduardo Delgado Díaz — Asociación de Amigos del Museo Histórico Militar de Cartagena (AAMMILCAR).

---

## 1. Source document

- **Manual:** D 652/41a — *7,5 cm Sturmgeschütz 40 (Ausf. F/8 u. G) und 10,5 cm Sturmhaubitze 42 (Ausf. G) — Gerätbeschreibung und Bedienungsanweisung zum Fahrgestell*. Dated Berlin, 1 May 1943 (Oberkommando des Heeres / Heereswaffenamt).
- Covers **only the chassis (Fahrgestell)**. The superstructure is a separate manual (D 652/43b). The chassis is essentially the Panzer III Ausf. J chassis.
- **Source scan file:** `100.-StuG-StuH-652-42a_compressed_bushmakow.pdf` — original from **https://bushmakow.com/**
- **Typeface:** Antiqua (NOT Fraktur) — normal Latin type, so visual transcription is straightforward.

### PDF geometry (important)
- **65 PDF pages.** Each PDF page is one **two-page book spread** (left printed page + right printed page), A4 landscape.
- Image-only PDF (no text layer). Interior scans ≈ **150 ppi**; cover ≈ 300 ppi.
- **Watermark** ("Dmitry Bushmakow Restoration") sits in *separate overlay objects*. Extracting the base raster with `pdfimages` yields **clean, watermark-free** page images. This is the key trick used throughout.

### Page-number mapping
For PDF page *p*: **left printed page = 2p − 4**, **right printed page = 2p − 3**.
- Text runs on printed pages up to **69** (page 70 is a blank verso).
- **Plates (G. Bilder) begin at printed page 71 = the right half of PDF page 37.**
- Plate spreads: from **PDF page 38 onward each PDF sheet is ONE full plate** that crosses the gutter (do NOT split these).

---

## 2. Document structure (what is where)

Printed-page ranges and the section data files that cover them (EN → _es for Spanish):

| Part | Content | Printed pages | Data file (EN / ES) |
|------|---------|---------------|---------------------|
| Front matter | Cover, Inhalt (contents), Vorbemerkungen, A. Technische Angaben, B. Beschreibung §1–2 | cover, 3–8 | sec0.js / sec0_es.js |
| B. Beschreibung §3–4 | Panzerwanne, Motor | 9–14 | sec1.js / sec1_es.js |
| B. Beschreibung §5–9 | Hauptkupplung, Wechselgetriebe, Kegel-/Lenkgetriebe, Stütz-/Lenkbremse, Kraftübertragung | 15–23 | sec2.js / sec2_es.js |
| B. Beschreibung §10–17 | Seitenvorgelege, Laufwerk, Gestänge, Elektrik, Schalttafel, Werkzeug, Hilfsgerät, Schanzzeug | 24–31 | sec3.js / sec3_es.js |
| C. Schmieren §18–19 + D. Aus-/Einbau §20–24 (start) | Lubrication + removal/installation | 32–45 | sec4a.js / sec4a_es.js |
| D. §24 (cont.)–§28 | Steering, brakes, final drive, suspension, track | 46–62 | sec4b.js / sec4b_es.js |
| E. Sondervorschriften §29–30 + F. Fahrvorschrift §31–32 | Special instructions + driving instructions | 63–69 | sec5.js / sec5_es.js |
| G. Bilder | 31 plates (Bild 1–31) | 71+ | sec6.js + sec6b.js / sec6_es.js + sec6b_es.js |

**Full table of contents (translated):** A. Technical data (7); B. Description (8): 1 General, 2 Main components, 3 Hull, 4 Engine [a Lubrication/oil filter, b Cooling, c Carburettor/air filter, d Starter, e Fuel storage], 5 Main clutch & cardan shaft, 6 Gearbox, 7 Bevel drive/steering gear/cardan shafts, 8 Support & steering brake, 9 Power transmission for steering, 10 Final drive, 11 Running gear [a sprocket/idler/return rollers, b road wheels/torsion bars, c shock absorbers, d track], 12 Linkages, 13 Electrical, 14 Switchboard/bulkhead, 15 Tools, 16 Auxiliary equipment, 17 Entrenching tools; C. Lubrication (32): 18 in service, 19 during assembly; D. Removal/installation/operation (35): 20 Hull, 21 Engine [a–d], 22 Cardan shaft, 23 Clutch & gearbox, 24 Bevel drive/steering gear/side shafts/steering brake, 25 Adjust/service brakes, 26 Power transmission for steering, 27 Final drive, 28 Running gear [a–d]; E. Special instructions (63): 29 Seals, 30 Remote thermometer; F. Driving (65): 31 General, 32 Overcoming obstacles; G. Plates (71).

---

## 3. Plates — sheet → Bild map (verified)

31 plates on 28 PDF sheets (38–65). **Three sheets are rotated 90° and carry TWO plates each.**

| PDF sheet | Bild | Title (DE) | Notes |
|-----------|------|-----------|-------|
| 38 | 1 | Ansicht des Fahrgestells | |
| 39 | 2 | Antriebsplan | |
| 40 | 3 | Kühlanlage | |
| 41 | **4 + 5** | Luftfilter / Kraftstofflagerung u. -förderung | rotated double |
| 42 | 6 | Hauptkupplung | |
| 43 | 7 | Wechselgetriebe | gear ratios + tooth counts (left as-is) |
| 44 | 8 | Lenkgetriebe | |
| 45 | 9 | Schnitt durch Kegeltrieb | |
| 46 | **10 + 11** | Lenkgetriebe Geradeausfahrt / Lenken | rotated double |
| 47 | 12 | Stützbremse | |
| 48 | 13 | Lenkbremse | |
| 49 | 14 | Seitenvorgelege | |
| 50 | 15 | Triebrad | |
| 51 | 16 | Leitrad mit Kettenspanner | rotated |
| 52 | 17 | Laufwerk | |
| 53 | 18 | Laufwerk | rotated |
| 54 | 19 | Stoßdämpfer | rotated |
| 55 | 20 | Schaltplan | rotated; wiring diagram, wire codes left as-is |
| 56 | 21 | Schmier- und Pflegeplan | numbered diagram, points 1–36 |
| 57 | 22 | Schmier- und Pflegeanweisung | rotated; the lubrication TABLE — fully translated (36 rows) in both editions |
| 58 | **23 + 24** | Einstellbild Stützbremse / Lenkbremse | rotated double |
| 59 | 25 | Gestänge zur Stütz- und Lenkbremse | |
| 60 | 26 | Lenkgetriebe m. Stützbremse, Ausbau | 9-step workshop seq.; DB-tool numbers |
| 61 | 27 | Lenkgetriebe m. Stützbremse, Einbau | 8 steps |
| 62 | 28 | Lenkgetriebe Einbau; Lenkbremse Aus-/Einbau | 8 steps |
| 63 | 29 | Seitenvorgelege, Aus- und Einbau | rotated; steps 1–4b |
| 64 | 30 | Laufwerk, Ausbau | 4 steps |
| 65 | 31 | Laufwerk, Einbau | sub-figures 1–4 |

**Rotated doubles:** sheets **41, 46, 58**. Bild 21 (diagram) and Bild 22 (its table) are the lubrication pair. Bild 26–31 are workshop removal/installation sequences whose callouts are mostly **special-tool numbers "DB xxx/x" (Sonderwerkzeug)** and "Schlüssel" (spanner) — kept as printed.

---

## 4. Decisions log

### Shared
1. **Bilingual layout:** clean (watermark-free) scan on the left, translation on the right. Landscape A4; 2-column table (image 6100 DXA, text 7858 DXA). Flowing layout with green top/bottom borders between page blocks (no forced page breaks in text sections).
2. **Terminology style:** translated term with the German original in parentheses in prose — e.g. "the chassis (Fahrgestell)" / "el chasis (Fahrgestell)". German kept with proper umlauts (ß, ä, ö, ü) everywhere, including plate keys.
3. **Plates:** each plate kept whole (they cross the gutter). Key = **glossary of the printed German callouts translated** (no numbers drawn onto the drawing — scan left pristine). 2 pages per plate: full plate image, then key. Rotated plates left **as-scanned** with a note.
4. **Bild 22 table:** fully transcribed & translated (36 lubrication points, intervals 250/500/2000 km + special cases, lubricant, count, operation, 2 footnotes) in BOTH editions.
5. **Bild 7 & Bild 20:** left as image + short key only (gear ratios/tooth counts and wiring codes NOT transcribed into a table — by decision).
6. **File-size control:** embedded scans are **downsampled to JPEG** in `mimg/` (text pages capped ~1000 px, plates ~1300 px, quality 82). Keeps each master ≈ 20 MB / PDF ≈ 24 MB instead of ~150 MB, with no visible loss. Standalone Sec6 (EN) still uses full-res PNG (≈ 61 MB).
7. **Title-page credit (both editions, Version 1.0):** "Compiled by / Compilado por Eduardo Delgado Díaz (edelgadodiaz@gmail.com, https://github.com/edumardo/panzerlab) — Asociación de Amigos del Museo Histórico Militar de Cartagena (AAMMILCAR, aammilcar@gmail.com)" + "Original file / Fichero original: https://bushmakow.com/" + "Version / Versión 1.0".

### English (DE-EN)
- **British spelling** (armour, tyre, gearbox, colour…).

### Spanish (DE-ES) — added later
- **Separate DE-ES edition** (not trilingual): keeps the 2-column scan+translation layout uncluttered; audiences differ (EN for international sharing, ES for the association).
- **Translated from the German original, cross-checked against the finished English** edition (avoids relay-translation drift).
- **Castilian (Spain).** Decimals with comma (11,9 litros). **PS → CV.** Key terms: Sturmgeschütz→cañón de asalto; Sturmhaubitze→obús de asalto; Panzerwanne→casco blindado; Wechselgetriebe→caja de cambios; Gelenkwelle→árbol de transmisión (cardán); Kegeltrieb→par cónico; Lenkgetriebe→mecanismo de dirección; Stützbremse→freno de apoyo; Lenkbremse→freno de dirección; Seitenvorgelege→reductora final; Laufwerk→tren de rodaje; Laufrolle→rueda de rodadura; Stützrolle→rodillo de retorno; Leitrad→rueda tensora; Triebrad→rueda motriz; Stabfeder→barra de torsión; Schwingarm→brazo oscilante; Gleiskette→cadena (oruga).
- Builders take Spanish labels via env vars: `PAGELABEL="Página original"`, `KEYTITLE="Clave / Legende — …"` (set inside `master_es.js`).

### Interpretation caveats (both editions)
- **Bild 22, point 3:** original "Schwingungsdämpferbolzen" interpreted as the shock-absorber (damper) bolts.
- **Bild 22, points 35 & 36:** carry the warning that no grease/oil must reach the brake shoes or inner drum face of the steering brake.
- Faithful visual transcription used instead of OCR (German-language OCR unavailable in the environment; visual transcription higher-fidelity here anyway).

---

## 5. File inventory

### Deliverables (canonical names)
- **English:** `D.652-41a_en_v1.0.docx` / `.pdf` — 135 pages.
- **Spanish:** `D.652-41a_es_v1.0.docx` / `.pdf` — 138 pages.
- **EN by-section set:** `D.652-41a_en_Sec1_v1.0.docx` … `D.652-41a_en_Sec5_v1.0.docx`, plus `D.652-41a_en_Sec6_v1.0.docx` (≈ 61 MB, full-res plates).
- (ES by-section set: not built yet — can be generated the same way from the *_es.js data if wanted.)

### Build scripts (Node.js + `docx` npm library)
- `make_bilingual.js` — reusable builder for text sections. Exports `buildSection(data,out)`, `pageRow`, `txtBlocksToParas`. Block types: `h`{de,en}, `p`{text}, `b`{text,lvl}, `note`{text}, `tbl`{cols,header,rows}. Reads images from `pages_clean/`; if `process.env.MIMG` set, prefers the matching `.jpg` in that dir. Page-label bar text = `process.env.PAGELABEL` || "Original page".
- `make_plate.js` — reusable builder for plates. Exports `buildPlates(data,out)`, `platePages`. Plate fields: `bild,titleDe,titleEn,img,w,h,key[{de,en}],notes[],tableData{...}`. `tableData` renders a full translated table after the key (used for Bild 22). Key-bar title = `process.env.KEYTITLE` || English default. Also honours `MIMG`.
- Text-section data: `sec0.js`…`sec5.js` (EN) and `sec0_es.js`…`sec5_es.js` (ES); each exports `{ data }` and self-builds only when run directly (`require.main===module`).
- Plate data: `sec6.js`/`sec6b.js` (EN), `sec6_es.js`/`sec6b_es.js` (ES). `sec6_build.js` concatenates and builds the standalone EN Sec6.
- Masters: `master.js` → `D.652-41a_en_v1.0.docx`; `master_es.js` → `D.652-41a_es_v1.0.docx`. Each sets `MIMG` (+ ES sets `PAGELABEL`/`KEYTITLE`), assembles title page + front matter + Sec1–5 + all plates, continuous pagination.
- `sec6_sample.js` — single-plate sample (Bild 1) used to validate the plate format. `buildES_phase1.js` — Spanish Phase-1 validation doc (front matter + Sec1). `build_docx.js` — original portrait sample (superseded).

### Image pipeline (Python + Pillow)
- `extract.py` — extracts clean base images per PDF page via `pdfimages`, splits into L/R halves → `pages_clean/` (full res) and `read/` (≤1400 px).
- `recrop.py` — re-crops printed pages from `full_clean/sheetNN.png` with overlap (LEFT_R=0.53 / RIGHT_L=0.47) to fix cut-off text at the gutter.
- All of these scripts, the data files, the working image dirs and `node_modules/` live inside the **`D.652-41a/`** subfolder (the document's processing home); the finished deliverables and this guide sit one level up, at the outputs root. Run regeneration from inside `D.652-41a/`.
- Directories (inside `D.652-41a/`): `full_clean/` = full-res spreads sheet01–65 (plates use these). `pages_clean/` = split printed pages `pNNN.png` + covers `pdf01_R.png` etc. `read/` = ≤1400 px reading copies. `mimg/` = downsampled JPEGs (+PNGs) for the masters.

---

## 6. How to reprocess / regenerate

Environment: Node.js with `docx` installed locally; Python 3 with Pillow; `pdfimages`/`pdftoppm`/`pdftotext` (poppler); LibreOffice (`soffice`) for PDF export. Source PDF read-only in `uploads/`.

```bash
cd D.652-41a                  # scripts, working dirs and node_modules live here

# (once) extract clean, watermark-free page images
python3 extract.py            # -> pages_clean/, read/
python3 recrop.py 1 65        # -> re-crop printed pages from full_clean/

# (once, for the masters) downsample to JPEG into mimg/
#   text pages pNNN.png cap ~1000 px, plates sheetNN.png cap ~1300 px, quality 82

# rebuild a text section standalone (writes its own .docx)
node sec1.js                  # EN …  (ES data files have no standalone build wired yet)

# rebuild the standalone EN plates document
node sec6_build.js            # -> D.652-41a_en_Sec6_v1.0.docx

# rebuild the masters
node master.js                # -> D.652-41a_en_v1.0.docx
node master_es.js             # -> D.652-41a_es_v1.0.docx

# export any docx to PDF (write to a NEW name; this FS sometimes blocks overwriting)
soffice --headless --convert-to pdf --outdir . <file>.docx
```

### Gotchas learned
- **Bump the version string** on the title page in `master.js` / `master_es.js` for each new release.
- Credits/version live only in the title-page block of each master script.
- Writing large JS with the editor sometimes truncates — the section/builder files were written via shell heredocs; always `node --check <file>` before building.
- This filesystem sometimes refuses to delete/overwrite files ("Operation not permitted"/EACCES) — write PDFs to fresh names and retry a failed build once.
- Editing images: text scans display at 350 px, plates at ~860 px, but full resolution is embedded (JPEG in the masters), so zoom stays crisp.
- To build an ES by-section set, add a guarded `buildSection(data, "…_es.docx")` call (with `PAGELABEL` set) to each `secN_es.js`, mirroring the EN files.

---

*End of processing notes — keep alongside the source PDF and the build scripts for any future revision.*
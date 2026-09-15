"""Title-page content for D.652-41a, rendered with the series-wide
render_title_page from D-652-series/scripts/title_page.py.

See that module's docstring for the field shapes and styling rules.

The org_line date and issuing body are taken from the document's own
colophon on book page 73 ("Berlin, den 1. 5. 43 / Oberkommando des Heeres /
Heereswaffenamt"), not from metadata.md alone.
"""

from __future__ import annotations

TITLE_PAGE_SPEC = {
    "designation": "D 652/41a",
    "model_lines": [
        "7,5 cm Sturmgeschütz 40 (Ausf. F/8 u. G)",
        "10,5 cm Sturmhaubitze 42 (Ausf. G)",
    ],
    "subtitle_en": "Equipment description and operating instructions for the chassis",
    "subtitle_es": "Descripción del material e instrucciones de manejo del chasis",
    "subtitle_de": "Gerätbeschreibung und Bedienungsanweisung zum Fahrgestell",
    "edition_line": (
        "Complete bilingual edition — full facsimile of the original German "
        "with English and Spanish translation"
    ),
    "edition_line_es": (
        "Edición bilingüe completa — facsímil íntegro del original alemán "
        "con traducción al inglés y al español"
    ),
    "org_line": "Heereswaffenamt · Berlin, 1 May 1943",
    "credit_line": (
        "Compiled by Eduardo Delgado Díaz (edelgadodiaz@gmail.com, "
        "https://github.com/edumardo/panzerlab) · Asociación de Amigos del "
        "Museo Histórico Militar de Cartagena (AAMMILCAR, aammilcar@gmail.com)"
    ),
    "source_line": "Original file: https://bushmakow.com/library/",
    "version_line": "Version 1.1",
}

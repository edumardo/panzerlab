"""Title-page content for D.652-50b, rendered with the series-wide
render_title_page from D-652-series/scripts/title_page.py.

See that module's docstring for the field shapes and styling rules.
"""

from __future__ import annotations

TITLE_PAGE_SPEC = {
    "designation": "D 652/50b",
    "model_lines": [
        "Panzerkampfwagen III (Ausf. H–L) · Panzerbefehlswagen (Ausf. H–K)",
        "Gepanzerte Selbstfahrlafette / StuG (Ausf. A, B, D, E)",
    ],
    "subtitle_en": "Preliminary repair instructions for the power train",
    "subtitle_es": "Instrucciones provisionales de reparación del tren de potencia",
    "subtitle_de": "Vorläufige Instandsetzungsanleitung für das Triebwerk",
    "edition_line": (
        "Complete bilingual edition — full facsimile of the original German "
        "with English and Spanish translation"
    ),
    "edition_line_es": (
        "Edición bilingüe completa — facsímil íntegro del original alemán "
        "con traducción al inglés y al español"
    ),
    "org_line": "Heereswaffenamt · Berlin, 1 February 1943",
    "credit_line": (
        "Compiled by Eduardo Delgado Díaz (edelgadodiaz@gmail.com, "
        "https://github.com/edumardo/panzerlab) · Asociación de Amigos del "
        "Museo Histórico Militar de Cartagena (AAMMILCAR, aammilcar@gmail.com)"
    ),
    "source_line": "Original file: https://bushmakow.com/library/",
    "version_line": "Version 1.0",
}

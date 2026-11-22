"""Hook MkDocs : vérifie les recettes et affiche leurs bandeaux d'infos.

Le format attendu est décrit dans docs-recettes/FORMAT.md.
"""

import logging
import re

log = logging.getLogger("mkdocs.hooks.recettes")

CATEGORIES = ("plats/", "desserts/")
NOMBRES = ("masse", "energie", "proteines", "glucides", "lipides")
OBLIGATOIRES = ("title", "cuisson") + NOMBRES
SECTIONS = ("Ingrédients", "Schéma", "Instructions", "Notes")

DUREE = re.compile(r"^(\d+ h( \d{1,2} min)?|\d+ min)$")
INGREDIENT = re.compile(r"^- \[ \] \*\*[^*]+\*\* \S")
ETAPE = re.compile(r"^\d+\. \*\*[^*]+\*\*")


def _renseigne(meta, cle):
    return meta.get(cle) not in (None, "")


def _est_nombre(valeur):
    return isinstance(valeur, (int, float)) and not isinstance(valeur, bool) and valeur >= 0


def _verifier(meta, markdown):
    problemes = []

    for cle in OBLIGATOIRES:
        if not _renseigne(meta, cle):
            problemes.append(f"champ obligatoire manquant : {cle}")
    for cle in NOMBRES:
        if _renseigne(meta, cle) and not _est_nombre(meta[cle]):
            problemes.append(f"{cle} doit être un nombre positif : {meta[cle]!r}")
    if _renseigne(meta, "masse") and _est_nombre(meta["masse"]) and meta["masse"] == 0:
        problemes.append("masse doit être supérieure à 0")
    for cle in ("cuisson", "preparation"):
        if _renseigne(meta, cle) and not DUREE.match(str(meta[cle])):
            problemes.append(
                f"durée invalide pour {cle} : {meta[cle]!r} (attendu : 20 min, 1 h, 1 h 30 min)"
            )

    sections = []
    section = None
    dans_code = False
    for ligne in markdown.splitlines():
        if ligne.startswith("```"):
            dans_code = not dans_code
        elif dans_code:
            continue
        elif ligne.startswith("# "):
            problemes.append("pas de titre H1 dans le corps : le titre vient du front matter")
        elif ligne.startswith("## "):
            section = ligne[3:].strip()
            sections.append(section)
        elif section == "Ingrédients" and ligne.strip() and not ligne.startswith("### "):
            if not INGREDIENT.match(ligne):
                problemes.append(f"ingrédient mal formé : {ligne!r}")
        elif section == "Instructions" and re.match(r"^\d+\. ", ligne):
            if not ETAPE.match(ligne):
                problemes.append(f"étape sans verbe d'action en gras : {ligne!r}")

    attendues = [s for s in SECTIONS if s in sections]
    if "Ingrédients" not in sections or "Instructions" not in sections:
        problemes.append("sections obligatoires : Ingrédients et Instructions")
    elif sections != attendues:
        problemes.append(
            f"sections attendues dans l'ordre : Ingrédients, [Schéma], Instructions, [Notes] "
            f"(trouvé : {', '.join(sections)})"
        )

    return problemes


def _nombre(valeur):
    if isinstance(valeur, float) and not valeur.is_integer():
        return f"{valeur:.1f}".replace(".", ",")
    return f"{int(valeur):,}".replace(",", " ")


def _carte(libelle, valeur, icone=None):
    icone_md = f":material-{icone}:{{ .lg .middle }} " if icone else ""
    return f"- {icone_md}**{libelle}**\n\n    ---\n\n    {valeur}\n\n"


def _grille(cartes):
    return (
        f'<div class="grid cards infos" style="--n: {len(cartes)}" markdown>\n\n'
        + "".join(cartes)
        + "</div>\n\n"
    )


def _bandeau(meta):
    temps = []
    if _renseigne(meta, "preparation"):
        temps.append(_carte("Préparation", meta["preparation"], "clock-outline"))
    temps.append(_carte("Cuisson", meta["cuisson"], "fire"))
    temps.append(_carte("Masse totale", f"{_nombre(meta['masse'])} g", "scale-balance"))

    macros = [
        _carte("Énergie", f"{_nombre(meta['energie'])} kcal"),
        _carte("Protéines", f"{_nombre(meta['proteines'])} g"),
        _carte("Glucides", f"{_nombre(meta['glucides'])} g"),
        _carte("Lipides", f"{_nombre(meta['lipides'])} g"),
    ]
    legende = '<p class="infos-legende">Valeurs nutritionnelles pour toute la recette</p>\n\n'
    return _grille(temps) + _grille(macros) + legende


def on_page_markdown(markdown, page, config, files):
    if not page.file.src_uri.startswith(CATEGORIES):
        return markdown

    for probleme in _verifier(page.meta, markdown):
        log.warning("%s : %s", page.file.src_uri, probleme)

    infos_ok = _renseigne(page.meta, "cuisson") and all(
        _renseigne(page.meta, cle) and _est_nombre(page.meta[cle]) for cle in NOMBRES
    )
    return _bandeau(page.meta) + markdown if infos_ok else markdown

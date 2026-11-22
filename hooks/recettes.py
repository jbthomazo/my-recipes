"""Hook MkDocs : vérifie les recettes et affiche leur bandeau d'infos.

Le format attendu est décrit dans docs-recettes/FORMAT.md.
"""

import logging
import re

log = logging.getLogger("mkdocs.hooks.recettes")

CATEGORIES = ("plats/", "desserts/")
OBLIGATOIRES = ("title", "portions", "preparation", "cuisson")
SECTIONS = ("Ingrédients", "Schéma", "Instructions", "Notes")

DUREE = re.compile(r"^(\d+ h( \d{1,2} min)?|\d+ min)$")
INGREDIENT = re.compile(r"^- \[ \] \*\*[^*]+\*\* \S")
ETAPE = re.compile(r"^\d+\. \*\*[^*]+\*\*")


def _renseigne(meta, cle):
    return meta.get(cle) not in (None, "")


def _verifier(meta, markdown):
    problemes = []

    for cle in OBLIGATOIRES:
        if not _renseigne(meta, cle):
            problemes.append(f"champ obligatoire manquant : {cle}")
    if _renseigne(meta, "portions") and not isinstance(meta["portions"], int):
        problemes.append(f"portions doit être un nombre entier : {meta['portions']!r}")
    for cle in ("preparation", "cuisson"):
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


def _carte(icone, libelle, valeur):
    return f"- :material-{icone}:{{ .lg .middle }} **{libelle}**\n\n    ---\n\n    {valeur}\n\n"


def _bandeau(meta):
    portions = meta["portions"]
    personnes = f"{portions} personne{'s' if portions > 1 else ''}"
    return (
        '<div class="grid cards infos" markdown>\n\n'
        + _carte("clock-outline", "Préparation", meta["preparation"])
        + _carte("fire", "Cuisson", meta["cuisson"])
        + _carte("silverware-fork-knife", "Portions", personnes)
        + "</div>\n\n"
    )


def on_page_markdown(markdown, page, config, files):
    if not page.file.src_uri.startswith(CATEGORIES):
        return markdown

    for probleme in _verifier(page.meta, markdown):
        log.warning("%s : %s", page.file.src_uri, probleme)

    infos = ("portions", "preparation", "cuisson")
    if all(_renseigne(page.meta, cle) for cle in infos) and isinstance(page.meta["portions"], int):
        return _bandeau(page.meta) + markdown
    return markdown

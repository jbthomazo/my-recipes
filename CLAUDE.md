# Carnet de recettes

Site de recettes personnel : MkDocs avec le thème Material, en français, publié sur GitHub Pages.

## Avant d'ajouter ou de modifier une recette

Lire `docs-recettes/FORMAT.md`. C'est la spec du format, et sa section « Règles pour Claude » donne la procédure. Elle prime sur toute habitude de mise en forme.

## Structure du repo

- `docs/` : contenu du site (`plats/`, `desserts/`, `index.md`)
- `docs-recettes/` : spec du format, non publiée sur le site
- `hooks/recettes.py` : vérifie les recettes au build et génère leur bandeau (préparation, cuisson, portions)
- `overrides/` : surcharges du thème
- `requirements.txt` : dépendances Python, les seules installées par le déploiement
- `.github/workflows/deploy.yml` : à chaque push sur `main`, `mkdocs gh-deploy`

## Conventions

- Contenu du site et messages de commit en français, courts.
- Par défaut : travailler sur une branche et proposer la PR. Pousser directement sur `main` seulement si on le demande explicitement.
- Ne pas ajouter de dépendance sans demander : le déploiement n'installe que `requirements.txt`.
- Pas de photos dans les recettes.

## Vérifier

`mkdocs build` : aucun avertissement du hook sur les fichiers modifiés.

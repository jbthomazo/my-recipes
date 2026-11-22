# Format des recettes

Cette spec est la référence : toute recette ajoutée ou modifiée la suit à la lettre. Le hook `hooks/recettes.py` affiche un avertissement au build quand une recette s'en écarte.

Principes : lisible d'un coup d'œil sur téléphone, le moins de mots possible, chaque information écrite à un seul endroit, rien d'inventé.

Exemple complet : `docs/desserts/cookies-de-mathilde.md`.

## Emplacement

- `docs/<categorie>/<slug>.md`, avec `<categorie>` = `plats` ou `desserts`
- slug : minuscules, sans accents, mots séparés par des tirets (`poulet-curry`)
- une recette = un fichier, sans photo

## Gabarit

````markdown
---
title: Nom de la recette
cuisson: 35 min
masse: 1000
energie: 1500
proteines: 130
glucides: 60
lipides: 70
preparation: 20 min
tags: [volaille, rapide]
---

## Ingrédients

- [ ] **600 g** de blanc de poulet
- [ ] **2** oignons
- [ ] **2 c. à soupe** de curry en poudre
- [ ] **au goût** sel

### Pour la sauce

- [ ] **20 cl** de crème

## Schéma

```mermaid
flowchart TD
    classDef ing fill:#eceff1,stroke:#90a4ae,color:#263238
    classDef act fill:#e0f2f1,stroke:#00897b,color:#004d40
    classDef heat fill:#fbe9e7,stroke:#e64a19,color:#bf360c

    I1(["beurre, sucres"]):::ing --> A1["Crémer"]:::act
    A1 --> A2["Mélanger"]:::act
    I2(["œuf, farine, pépites"]):::ing --> A2
    A2 --> A3["Former les boules"]:::act
    A3 --> A4["Cuire"]:::heat
    F(["four"]):::heat --> A4
    A4 --> A5["Refroidir"]:::act
```

## Instructions

1. **Couper** le poulet en dés.
2. **Faire revenir** 5 min à feu vif.
3. **Ajouter** la crème, **laisser mijoter** 20 min.

!!! tip "Astuce"
    Phrase courte.

## Notes

Phrase courte.
````

Les valeurs de l'en-tête et le schéma du gabarit sont des exemples de forme : le contenu vient de la recette. Les sections `Schéma` et `Notes` sont optionnelles, les autres obligatoires, dans cet ordre.

## Règles

### En-tête (front matter)

| Champ | Obligatoire | Format |
|---|---|---|
| `title` | oui | nom court de la recette |
| `cuisson` | oui | `20 min`, `1 h`, `1 h 30 min` ; `0 min` s'il n'y a pas de cuisson |
| `masse` | oui | nombre, en g : masse totale de la recette |
| `energie` | oui | nombre, en kcal, pour toute la recette |
| `proteines` | oui | nombre, en g, pour toute la recette |
| `glucides` | oui | nombre, en g, pour toute la recette |
| `lipides` | oui | nombre, en g, pour toute la recette |
| `preparation` | non | même format que `cuisson` |
| `tags` | non | liste en minuscules, sans accents |

Pas de portions : la masse et les valeurs nutritionnelles sont celles de toute la recette. Pour une part : valeur × masse de la part ÷ masse totale.

Le titre de la page vient de `title` : pas de `# Titre` dans le corps. Les bandeaux (temps, masse, valeurs nutritionnelles) sont générés automatiquement sous le titre : ne jamais les écrire dans le corps.

### Masse et valeurs nutritionnelles

- masse : somme des ingrédients en g, avant cuisson. Les unités non pondérales sont converties avec des poids usuels (1 œuf ≈ 50 g, 1 c. à café de levure ≈ 4 g…)
- valeurs : pour chaque ingrédient, valeur Ciqual (ANSES) pour 100 g × quantité ÷ 100, puis somme. Énergie arrondie à la dizaine, macros au gramme
- les ingrédients à contribution négligeable (levure, sel, épices, eau) comptent dans la masse mais pas dans les valeurs
- si la source donne la masse ou les valeurs, les utiliser telles quelles
- si elles sont estimées : une phrase dans `Notes` indique la méthode et les hypothèses (poids de l'œuf…)

### Ingrédients

- une ligne par ingrédient, dans l'ordre d'utilisation : `- [ ] **quantité** nom`
- quantité en gras : nombre + unité métrique (`g`, `kg`, `ml`, `cl`, `l`, `c. à soupe`, `c. à café`, `pincée`), nombre seul pour ce qui se compte (`**2** œufs`), ou `**au goût**`
- après l'unité : « de » ou « d' » (`**600 g** de blanc de poulet`)
- sous-titres `###` seulement si la recette a des groupes (sauce, pâte…)

### Schéma (optionnel)

- ajouté si la recette a au moins 5 étapes ou des étapes en parallèle, sinon omis
- mêmes étapes que les instructions, dans le même ordre
- cases d'action : un verbe, sans complément ; durée ou température seulement si elles figurent dans la source
- ingrédients : nom exact de la liste, sans quantité, regroupés par étape d'entrée ; chaque ingrédient de la liste apparaît exactement une fois
- chaleur (four, poêle…) : entrée de l'étape de cuisson
- couleurs : copier les trois lignes `classDef` du gabarit (`ing` neutre, `act` action, `heat` chaleur)

### Instructions

- liste numérotée, une action par étape
- chaque étape commence par le verbe d'action à l'infinitif, en gras
- phrases courtes, forme impersonnelle (pas de « tu » ni de « vous »)
- températures en °C, durées en min

### Encadrés et notes

- `!!! tip "Astuce"` ou `!!! warning "Attention"`, placés après la liste d'instructions, 3 au maximum
- `Notes` : variantes, conservation, points à vérifier, en quelques phrases

## Règles pour Claude

1. Lire cette spec et `CLAUDE.md` avant toute modification d'une recette.
2. Extraire de la source (texte, notes, photo) : titre, catégorie, cuisson, ingrédients, étapes, et masse ou valeurs nutritionnelles si elles y figurent.
3. Ne jamais inventer une quantité, un temps, une température, un ingrédient ou une étape. Si une information obligatoire manque : poser une seule question groupée avant d'écrire. Si une information optionnelle manque : l'omettre. Exception : la masse et les valeurs nutritionnelles se calculent selon la section dédiée, sans poser de question.
4. Normaliser : unités métriques, verbes à l'infinitif, ordre d'utilisation des ingrédients, texte en français.
5. Calculer la masse et les valeurs avec un script, pas de tête.
6. Créer `docs/<categorie>/<slug>.md` à partir du gabarit, puis :
   - ajouter la page dans `nav` de `mkdocs.yml`, par ordre alphabétique dans sa catégorie
   - ajouter son lien dans `docs/index.md`, au même endroit
7. Si un schéma est ajouté : vérifier que chaque ingrédient de la liste y apparaît une fois, et que les étapes sont celles des instructions.
8. Lancer `mkdocs build` : aucun avertissement du hook ne doit concerner le fichier ajouté.
9. Suivre les conventions de commit et de branche de `CLAUDE.md`.

Les deux ajouts manuels de l'étape 6 disparaîtront si le menu et l'accueil deviennent automatiques.

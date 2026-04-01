# Analyse Exploratoire des Données (EDA) sur le dataset Ames Housing

## Description du projet

Ce projet est un exercice pratique d’**Analyse Exploratoire des Données (EDA)** appliqué au dataset **Ames Housing**. L’objectif est de maîtriser les fondamentaux de l’EDA, de la visualisation et du feature engineering sur un jeu de données immobilier réel.

## Le dataset : Ames Housing

Le fichier `AmesHousing.csv` contient des données sur la vente de maisons individuelles à **Ames, Iowa (USA)** entre **2006 et 2010**.

| Caractéristique | Détail |
|-----------------|--------|
| Nombre d’observations | ~2930 maisons (sources courantes) ; **dans ce dépôt**, le fichier fourni compte environ **2197** lignes |
| Nombre de variables | **82** colonnes |
| Variable cible | `SalePrice` (prix de vente en dollars) |
| Types de variables | Quantitatives continues, discrètes, qualitatives nominales et ordinales |

## Objectifs d’apprentissage

À la fin de cet exercice, vous serez capable de :

- **Comprendre la structure des données** — Explorer les dimensions, types de colonnes et premières lignes
- **Évaluer la qualité des données** — Identifier les valeurs manquantes, doublons, types inappropriés
- **Calculer des statistiques descriptives** — Indicateurs classiques (moyenne, écart-type) **et** robustes (médiane, MAD, IQR)
- **Visualiser les distributions** — Histogrammes, boxplots, diagrammes en barres avec annotations
- **Détecter les valeurs aberrantes** — Comparer la méthode IQR et le z-score modifié
- **Formuler des hypothèses métier** — Transformer des observations en hypothèses testables

## Variables ciblées (exercice E1)

L’exercice se concentre sur **5 variables clés** :

| Variable | Description | Type |
|----------|-------------|------|
| `Gr Liv Area` | Surface habitable (pieds carrés) | Quantitative continue |
| `SalePrice` | Prix de vente (dollars) | Quantitative continue |
| `Lot Area` | Surface du terrain (pieds carrés) | Quantitative continue |
| `Year Built` | Année de construction | Quantitative discrète |
| `Overall Qual` | Note globale de qualité (1 à 10) | Ordinale |

## Structure de l’exercice (notebook E1)

Le notebook **E1** est organisé en **6 sections** progressives :

1. **Section 1 — Imports et chargement** — Bibliothèques, chargement du CSV, `head()`
2. **Section 2 — Aperçu général et qualité** — Structure, manquants, doublons, sous-ensemble cible
3. **Section 3 — Statistiques univariées** — Classiques, robustes, skew/kurtosis, tableau récap
4. **Section 4 — Visualisations** — Histogrammes + boxplots, barres, analyse comparative
5. **Section 5 — Détection d’outliers** — IQR, z-score modifié, comparaison et graphique
6. **Section 6 — Hypothèses métier** — Trois hypothèses testables structurées

## Concepts clés du cours

### Statistiques classiques vs robustes

| Mesure | Classique | Robuste |
|--------|-----------|---------|
| Centralité | Moyenne | Médiane |
| Dispersion | Écart-type | MAD, IQR |
| Détection d’outliers | Z-score | Z-score modifié |

Les statistiques **robustes** résistent mieux aux valeurs extrêmes que les classiques.

### Asymétrie (skewness)

- **Positive (> 0)** : queue à droite, souvent moyenne > médiane
- **Négative (< 0)** : queue à gauche, souvent moyenne < médiane
- **Nulle (≈ 0)** : distribution plutôt symétrique

### Aplatissement (kurtosis)

- **Leptokurtique (> 0)** : queues épaisses, plus de valeurs extrêmes
- **Mésokurtique (≈ 0)** : proche de la loi normale
- **Platykurtique (< 0)** : queues fines

### Section 5 — z-score modifié (rappel)

\[
Z_{\text{modifié}} = 0{,}6745 \times \frac{x - \text{médiane}}{\text{MAD}}
\]

Seuil de détection courant : **> 3,5**.

## Prérequis techniques

```sh
pip install pandas numpy matplotlib seaborn scipy
```

*(Le projet utilise aussi `requirements.txt` avec les versions du dépôt.)*

## Structure du dépôt

```
EDA_Vis_FEng/
├── README.md                              # Ce fichier (guide + fiches mémo)
├── requirements.txt                       # Dépendances Python
├── AmesHousing.csv                      # Dataset Ames Housing
├── E1 - Analyse Exploratoire des Données.ipynb    # EDA : énoncé + travail
├── E2 - Visualisation univariées et bivariées.ipynb
├── E3 - Analyse Multivariées et Corrélation.ipynb
├── E4 - Détection d'anomalies.ipynb
├── images/                              # Captures de figures (si présentes)
└── .venv/                               # Environnement virtuel (local, optionnel)
```

Les notebooks **E2–E4** prolongent l’EDA (visualisations bivariées, corrélations multivariées, anomalies).

---

## Sommaire

### Projet et environnement

- [Structure du dépôt](#structure-du-dépôt)
- [Environnement virtuel (venv)](#environnement-virtuel-venv)
- [Lancer le projet](#lancer-le-projet)

### Fiches Python / pandas

- [Ceci est une docstring](#ceci-est-une-docstring)
- [`describe(include='all')`](#describeincludeall)
- [Colonnes `str` → `category`](#colonnes-str--devraient-être-category)
- [La différence entre `NaN` et `None`](#la-différence-entre-nan-et-none)
- [Lecture simple de `describe()` + skew + kurtosis](#lecture-simple-de-describe--skew--kurtosis)
- [`df.select_dtypes(include='number')`](#dfselect_dtypesincludenumber)
- [Skewness (rappel simple)](#skewness-rappel-simple)
- [`bins` (histogramme)](#bins-histogramme)
- [`plt.tight_layout()`](#plttight_layout)
- [`fig.tight_layout()`](#figtight_layout)
- [`plt.subplots(1, 2, figsize=(12, 4))`](#pltsubplots1-2-figsize12-4)
- [`sns.boxplot(...)` (explication rapide)](#snsboxplot-explication-rapide)
- [`pd.DataFrame.from_dict(..., orient='index')`](#pddataframefrom_dict-orientindex)

### Visualisation et résultats

- [Résultats (images)](#resultats-images)
- [Lecture approfondie du skew](#lecture-approfondie-du-skew)
- [Heatmap (corrélations)](#heatmap-corrélations)
- [`jitter=True` dans `sns.stripplot()`](#jittertrue-dans-snsstripplot)

### Statistiques avancées

- [Corrélation partielle](#corrélation-partielle)
- [E3 S5.1 : corrélation partielle NumPy (`E3` notebook, lignes 1–10)](#e3-s51-partial-corr-numpy)
- [KDE supervisée](#kde-supervisée)
- [Ticks sur l'axe des x (Year Built)](#ticks-sur-laxe-des-x-year-built)
- [Explication : `qual_counts`](#explication--qual_counts)

## Environnement virtuel (venv)

Depuis le dossier du projet :

```sh
cd /Users/romain/Desktop/EDA_Vis_FEng
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Sous Windows (PowerShell) : `.\.venv\Scripts\Activate.ps1` puis les mêmes commandes `pip`.

## `"""Ceci est une docstring"""`

🧠 A quoi ca sert ?

➡️ Expliquer :
- ce que fait une fonction
- ses parametres
- ce qu'elle retourne

📌 Exemple

```python
def moyenne(liste):
    """
    Calcule la moyenne d'une liste de nombres.

    Parametres :
    liste (list) : liste de nombres

    Retour :
    float : moyenne des valeurs
    """
    return sum(liste) / len(liste)
```

🔍 Comment y acceder ?

```python
help(moyenne)
```

ou

```python
moyenne.__doc__
```

## Lancer le projet

Une fois le venv créé et les dépendances installées (voir [Environnement virtuel (venv)](#environnement-virtuel-venv)) :

```sh
cd /Users/romain/Desktop/EDA_Vis_FEng
source .venv/bin/activate
jupyter notebook
```

Ouvrez ensuite les notebooks `E1` à `E4` et exécutez-les avec **Restart & Run All** pour valider le parcours complet.

Alternative (sans interface graphique) :

```sh
jupyter nbconvert --to notebook --execute "E1 - Analyse Exploratoire des Données.ipynb" --inplace
```

## `describe(include='all')`

Avec `include='all'`, tu obtiens :

📊 **Colonnes numériques :**
- `mean` (moyenne)
- `std` (écart-type)
- `min` / `max`
- quartiles (`25%`, `50%`, `75%`)

🏷️ **Colonnes catégorielles (texte) :**
- `count` (nombre de valeurs)
- `unique` (nombre de valeurs différentes)
- `top` (valeur la plus fréquente)
- `freq` (fréquence de la plus fréquente)

## Colonnes `str` → devraient être `category`

Toutes ces colonnes sont du texte répétitif (catégories), donc mieux en `category` :

**Exemples :**
- MS Zoning
- Street
- Neighborhood
- House Style
- Kitchen Qual
- Sale Condition
- etc.

👉 **Pourquoi c’est mieux ?**
- moins de mémoire
- plus rapide pour ML
- logique métier (ce ne sont pas des phrases)

## La différence entre `NaN` et `None`

Il est essentiel de comprendre la distinction entre `NaN` et `None` en Python. `NaN` est une représentation en virgule flottante de "Not a Number" (pas un nombre), principalement utilisée dans les calculs numériques. `None`, quant à lui, est un objet Python représentant l'absence de valeur, similaire au `null` dans d'autres langages. Alors que `NaN` est utilisé dans les calculs mathématiques ou scientifiques, `None` est plus polyvalent et indique l'absence de données.

## Lecture simple de `describe()` + `skew` + `kurtosis`

Parfait, tu as affiche un `describe()` + `skew` + `kurtosis`. Voici une lecture simple et directe.

### 1) Ce qui est affiche (ordre)

Tes blocs correspondent a :
- `mean` (moyenne)
- `std` (ecart-type)
- `min`
- `max`
- `median` (50%)
- `Q1` (25%)
- `Q3` (75%)
- `skew`
- `kurtosis`

### 2) Interpretation simple, variable par variable

**Gr Liv Area (surface)**
- Moyenne ~ 1507
- Mediane ~ 1452 (proches)
- `skew = 1.37` (asymetrie positive)
- Conclusion: quelques grandes maisons tirent la moyenne vers le haut.

**SalePrice (prix)**
- Moyenne ~ 182k
- Mediane ~ 163k (moyenne > mediane)
- `skew = 1.77` (forte asymetrie positive)
- `kurtosis ~ 5.48` (beaucoup d'outliers)
- Conclusion: distribution tiree vers le haut, avec quelques maisons tres cheres.
- Typique: transformation log recommandee.

**Lot Area (terrain)**
- Moyenne ~ 10k
- Mediane ~ 9488
- `skew = 12.85` (tres eleve)
- `kurtosis ~ 270` (extreme)
- Conclusion: variable ultra desequilibree, avec des terrains geants qui dominent la distribution.

Transformation utile :
```python
df["Lot Area"] = np.log1p(df["Lot Area"])
```

**Year Built**
- Moyenne ~ 1972
- Mediane ~ 1975 (proches)
- `skew = -0.65` (legerement negatif)
- Conclusion: distribution globalement correcte.

**Overall Qual**
- Moyenne ~ 6.1
- Mediane = 6
- `skew ~ 0.16` (quasi symetrique)
- `kurtosis ~ 0.096` (proche normal)
- Conclusion: variable propre, pas de transformation necessaire.

### 3) Resume rapide

| Variable | Skew | Kurtosis | Interpretation |
|---|---:|---:|---|
| Gr Liv Area | 1.37 | 4.89 | un peu asymetrique |
| SalePrice | 1.77 | 5.48 | asymetrie + outliers |
| Lot Area | 12.85 | 270 | extremement desequilibree |
| Year Built | -0.65 | -0.40 | OK |
| Overall Qual | 0.16 | 0.09 | tres stable |

### 4) A retenir (ML)

- A corriger en priorite: `SalePrice`, `Lot Area`
- A laisser tel quel: `Year Built`, `Overall Qual`

Regle simple:
- `|skew| > 1` -> asymetrie importante
- `kurtosis > 3` -> presence forte d'outliers

## `df.select_dtypes(include='number')`

🧠 Ca veut dire :

➡️ On garde uniquement les colonnes numeriques

📌 Exemple

Si ton DataFrame contient :

| colonne | type |
|---|---|
| SalePrice | int |
| Lot Area | float |
| Neighborhood | object |

👉 Resultat :

`df.select_dtypes(include='number')`

➡️ Garde :
- SalePrice
- Lot Area

❌ Ignore :
- Neighborhood (texte)

## Skewness (rappel simple)

👉 La skewness mesure l'asymetrie

`df.skew()`

🧠 Interpretation
- ~ 0 -> symetrique
- > 0 -> valeurs extremes vers la droite
- < 0 -> valeurs extremes vers la gauche

📌 Exemple

`df["SalePrice"].skew()`

➡️ 1.7 -> il y a des maisons tres cheres qui tirent vers le haut

⚡ Resume

| Element | Role |
|---|---|
| `include='number'` | selectionne les colonnes numeriques |
| `skew()` | mesure l'asymetrie |

🚀 En une ligne

`df.select_dtypes(include='number').skew()`

👉 Tu obtiens la skewness de toutes tes variables numeriques

## `bins` (histogramme)

`bins` = nombre de barres (ou intervalles) dans l'histogramme.

🧠 Concretement

Un histogramme decoupe tes donnees en groupes (intervalles) :

- `bins=10` → 10 barres
- `bins=30` → 30 barres
- `bins=100` → tres detaille

## `plt.tight_layout()`

Quand on cree plusieurs sous-graphiques, par exemple:

```python
fig, axes = plt.subplots(2, 2)
```

on observe souvent:
- les titres qui se chevauchent
- les labels coupes
- des graphiques trop serres

Solution:

```python
plt.tight_layout()
```

`tight_layout()`:
- ajuste automatiquement les marges
- evite les chevauchements
- rend la figure plus propre et lisible

## `fig.tight_layout()`

`fig.tight_layout()` ajuste automatiquement les espaces dans la figure pour eviter que:
- les titres se chevauchent
- les labels soient coupes
- les graphiques se superposent

## `plt.subplots(1, 2, figsize=(12, 4))`

`plt.subplots(1, 2)` signifie:
- 1 ligne
- 2 colonnes

Donc: 2 graphiques cotes a cotes.

### `fig`

`fig` est la figure globale:
- le canvas principal
- il contient tous les graphiques

### `axes`

`axes` correspond aux zones de dessin (les sous-graphiques).

Dans ce cas:
- `axes[0]` = premier graphique (a gauche)
- `axes[1]` = deuxieme graphique (a droite)

### `figsize=(12, 4)`

`figsize` definit la taille de la figure:
- largeur = 12
- hauteur = 4

## `sns.boxplot(...)` (explication rapide)

```python
sns.boxplot(x=df_subset[col], ax=axes[1], color=palette[1])
axes[1].set_title(f"Boxplot - {col}")
```

### 1) `sns.boxplot(...)`

- fonction de Seaborn
- elle cree un boxplot (boite a moustaches)

### 2) `x=df_subset[col]`

- donnees utilisees: une colonne de ton DataFrame
- exemple: `SalePrice`
- tu analyses une seule variable

### 3) `ax=axes[1]` (important)

- `axes[1]` = deuxieme sous-graphique
- donc le boxplot est dessine a droite (dans une mise en page `1x2`)

### 4) `color=palette[1]`

- couleur du graphique
- `palette` est une liste de couleurs
- `[1]` = deuxieme couleur

### Ligne suivante: titre

`axes[1].set_title(f"Boxplot - {col}")` ajoute le titre du deuxieme graphique.

Exemple:
- `Boxplot - SalePrice`

## `pd.DataFrame.from_dict(..., orient='index')`

`pd.DataFrame.from_dict(data, orient='index')` permet de construire un DataFrame a partir d'un dictionnaire en utilisant les cles comme index (lignes), ce qui est pratique pour un tableau recapitulatif de statistiques.

## Resultats (images)

Figure resultat (section 3.4) :

![results_section_3_4](images/results_section_3_4.png)

Figure resultat (section 4.1) :

![results_section_4_1](images/results_section_4_1.png)

Figure resultat (section 4.2) :

![results_section_4_2](images/results_section_4_2.png)

Overall Qual est la note de qualité globale du logement dans Ames Housing.

Lecture rapide :

- Overall Qual = 3 -> qualite plutot faible
- Overall Qual = 6 -> moyenne/correcte
- Overall Qual = 9 -> qualite tres elevee

On peut la traiter comme numerique ordonnee (souvent OK) ou comme categorie ordonnee selon le modele utilise.

## Lecture approfondie du skew

Le skew (asymetrie) mesure uniquement la forme de la distribution.

👉 Donc :
- skew eleve = distribution tres desequilibree
- ca ne dit rien directement sur l'impact sur le prix

Regarde tes resultats :

- Gr Liv Area -> skew = 1.370
- SalePrice -> skew = 1.779
- Lot Area -> skew = 12.854 (!!)

👉 Interpretation :

🔹 Gr Liv Area
- asymetrie moderee a droite
- quelques grandes maisons

🔹 SalePrice
- asymetrie a droite
- quelques maisons tres cheres

🔹 Lot Area
- skew enorme (12.8)
- ca veut dire :
  - enormement de petits terrains
  - + quelques terrains gigantesques (outliers)

3. Le vrai probleme du skew eleve

Un skew eleve indique :

👉 presence d'outliers (valeurs extremes)

Dans ton cas :

Lot Area -> quelques terrains enormes
qui tirent la moyenne vers le haut

📌 On le voit :

- mean = 10268
- median = 9488

👉 la moyenne > mediane -> classique skew a droite

⚠️ 4. Pourquoi c'est dangereux en ML

Un skew eleve peut :

- biaiser la moyenne
- perturber les modeles (regression, etc.)
- donner trop d'importance a quelques valeurs extremes

 5. Impact sur le prix : comment savoir vraiment ?

👉 Pour savoir si une variable impacte le prix, il faut :

✔ correlation

```python
df["Lot Area"].corr(df["SalePrice"])
```

✔ modele (regression)
✔ scatter plot

👉 PAS le skew

 6. Interpretation 

La variable Lot Area presente une tres forte asymetrie (skew=12.8), ce qui indique la presence d'outliers importants. Cela peut biaiser l'analyse et necessiter une transformation (log) avant modelisation. Cependant, le skew ne permet pas de conclure sur son impact direct sur le prix, qui doit etre evalue via la correlation ou un modele.

 

 7. Ce que tu devrais faire ensuite

👉 Tres important pour ton projet :

✔ transformation log

```python
df["Lot Area"] = np.log1p(df["Lot Area"])
```

✔ ou supprimer outliers

 Resume simple

| Concept | Signification |
|---|---|
| Skew eleve | distribution desequilibree |
| Skew eleve | presence d'outliers |
| Skew eleve | pas egal impact sur prix |
| Impact sur prix | correlation / modele |

## Heatmap (corrélations)

Avec `annot=True` (recommandé) :

```python
sns.heatmap(corr, annot=True)
```

👉 Tu vois :
- les couleurs
- les valeurs exactes

🎯 Options utiles avec `annot`

✔ format des nombres

```python
sns.heatmap(corr, annot=True, fmt=".2f")
```

👉 2 chiffres apres la virgule (plus propre)

✔ taille du texte

```python
sns.heatmap(corr, annot=True, annot_kws={"size": 8})
```

✔ meilleure lisibilite

```python
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
```

### Lecture rapide des paramètres

`corr = df.corr()`
- calcule la correlation entre variables numeriques
- renvoie des valeurs entre `-1` et `1`

`annot=True`
- affiche les valeurs dans chaque case
- indispensable pour lire les chiffres exacts

`fmt=".2f"`
- format des nombres
- `.2f` = 2 chiffres apres la virgule

`cmap="coolwarm"`
- palette de couleurs
- bleu = correlation negative
- rouge = correlation positive
- blanc = proche de `0`

`center=0`
- force le centre de la palette a `0`
- negatif -> bleu, positif -> rouge, `0` -> blanc
- evite des couleurs trompeuses

## `jitter=True` dans `sns.stripplot()`

`jitter=True` ajoute une petite dispersion aleatoire sur l'axe categoriel pour eviter que les points se superposent.

Sans jitter:
- plusieurs observations ayant la meme categorie (ex: `Overall Qual = 6`) tombent exactement au meme endroit
- on sous-estime visuellement la densite des points

Avec jitter:
- les points sont legerement decales horizontalement
- la distribution par categorie est plus lisible

Exemple:

```python
sns.stripplot(
    data=df,
    x="Overall Qual",
    y="SalePrice",
    alpha=0.3,
    jitter=True,
    size=2
)
```

Conseil pratique: combine `boxplot` + `stripplot(jitter=True)` pour voir a la fois le resume statistique (boite) et les observations individuelles.

## Corrélation partielle

```python
result = pg.partial_corr(data=dt, x="X", y="Y", covar="Z")
```

👉 avec :
- `dt` = ton DataFrame
- `"X"` = variable 1
- `"Y"` = variable 2
- `"Z"` = variable a controler

### C'est quoi une correlation partielle ?

👉 C'est une correlation en supprimant l'effet d'une autre variable.

🔥 Intuition

👉 Tu veux savoir :

"Est-ce que X influence Y independamment de Z ?"

### Exemple simple (immobilier)

- `X` = surface (`Gr Liv Area`)
- `Y` = prix (`SalePrice`)
- `Z` = localisation

👉 probleme :

- surface et prix sont lies
- MAIS localisation influence aussi le prix

❌ correlation normale

```python
corr(X, Y)
```

👉 melange tout.

✅ correlation partielle

```python
corr(X, Y | Z)
```

👉 enleve l'effet de `Z`.

### Ce que fait `pg.partial_corr`

👉 La librairie Pingouin :

```python
pg.partial_corr(data=dt, x="X", y="Y", covar="Z")
```

👉 retourne :

| colonne | signification |
|---|---|
| `r` | correlation partielle |
| `p-val` | significativite |
| `CI95%` | intervalle de confiance |

### Comment ca marche (idee)

👉 mathematiquement :

- on enleve `Z` de `X` -> residu `X'`
- on enleve `Z` de `Y` -> residu `Y'`
- on correle `X'` et `Y'`

C'est la correlation « pure ».

### Pourquoi c'est puissant

👉 Ca evite :

- faux liens
- biais (Simpson)
- variables cachees

### Exemple concret

```python
result = pg.partial_corr(
    data=df,
    x="Gr Liv Area",
    y="SalePrice",
    covar="Overall Qual"
)

print(result)
```

👉 question :

"Est-ce que la surface influence encore le prix si on fixe la qualite ?"

### Resume

| element | role |
|---|---|
| `x` | variable 1 |
| `y` | variable 2 |
| `covar` | variable a controler |
| resultat | correlation sans biais |

👉 "La correlation partielle mesure la relation entre deux variables en controlant l'effet d'une ou plusieurs variables supplementaires. Elle permet d'isoler une relation directe en eliminant les variables confondantes."

<a id="e3-s51-partial-corr-numpy"></a>

## E3 S5.1 — corrélation partielle NumPy (`E3` notebook, lignes 1–10)

**Intitulé de référence :** E3 S5.1 : [`E3 - Analyse Multivariées et Corrélation.ipynb`](./E3%20-%20Analyse%20Multivariées%20et%20Corrélation.ipynb) (1–10) — fonction `partial_corr_one_covar`.

La cellule concernée définit `partial_corr_one_covar` (en-tête + corps, typiquement les premières lignes de la cellule). Même idée que la [corrélation partielle](#corrélation-partielle) avec Pingouin : on enlève l’effet **linéaire** de `covar` sur `x` et sur `y`, puis on corrèle les **résidus**.

```python
def partial_corr_one_covar(data: pd.DataFrame, x: str, y: str, covar: str):
    z = data[[covar]].values.astype(float)
    z = np.column_stack([np.ones(len(z)), z])
    xv = data[x].values.astype(float)
    yv = data[y].values.astype(float)
    bx, *_ = np.linalg.lstsq(z, xv, rcond=None)
    by, *_ = np.linalg.lstsq(z, yv, rcond=None)
    rx = xv - z @ bx
    ry = yv - z @ by
    return stats.pearsonr(rx, ry)
```

### Opérateur `@`

En NumPy, **`@` est le produit matriciel** (équivalent pratique à `np.dot` pour des tableaux bien dimensionnés).

- **`z @ bx`** : valeurs prédites de `xv` par une régression linéaire sur les colonnes de `z` (constante + `covar`), avec coefficients `bx`.
- **`xv - z @ bx`** : **résidus** de `x` après retrait de cette partie linéaire. Idem pour `y` avec `by`, `ry`.

### `np.linalg.lstsq(z, xv, rcond=None)`

**`lstsq`** (*least squares*) cherche les coefficients **`bx`** qui minimisent \(\lVert z \cdot bx - xv \rVert^2\) : régression des moindres carrés de `xv` sur `z` (intercept + `covar`).

Le motif **`bx, *_ = ...`** ne garde que le premier élément du retour (le vecteur de coefficients) et ignore le reste (résidus, rang, singular values selon la version de NumPy).

### `rcond=None`

**`rcond`** fixe le seuil lié au **conditionnement** / au **rang** de la matrice (valeurs singulières trop petites traitées comme nulles).

Avec **`rcond=None`**, NumPy applique la politique **par défaut** (souvent liée à la précision machine) pour stabiliser le calcul quand `z` est presque singulière ou mal conditionnée.

### Synthèse

| Élément | Rôle |
|--------|------|
| `z` | Matrice du modèle : colonne de **1** + **`covar`** |
| `lstsq` | Estime l’effet linéaire de `covar` sur `x` puis sur `y` |
| `@` | Applique le modèle pour obtenir les **résidus** `rx`, `ry` |
| `rcond=None` | Comportement numérique par défaut pour la résolution |
| `pearsonr(rx, ry)` | Corrélation de Pearson des résidus = corrélation partielle (linéaire, une covariable) |

## KDE supervisée

Une courbe **KDE supervisee**, c'est simplement une KDE (Kernel Density Estimation) ou tu separes les donnees par classe (label) pour comparer leurs distributions.

### 1) Rappel: KDE (non supervisee)

Une KDE est une version lissee d'un histogramme:
- au lieu de barres, on obtient une courbe
- elle montre la distribution des donnees

### 2) KDE supervisee = par classe

Ici, \"supervisee\" veut dire que tu utilises la target (`y`) pour tracer une courbe par groupe.

Exemples:
- prix des maisons selon `SaleCondition`
- revenu selon une classe
- variable selon fraude / non fraude

Exemple code:

```python
plt.figure(figsize=(8, 5))
sns.kdeplot(data=df, x="SalePrice", hue="Sale Condition", fill=True, common_norm=False, alpha=0.3)
plt.title("KDE supervisee de SalePrice par Sale Condition")
plt.tight_layout()
plt.show()
```

## Ticks sur l'axe des x (Year Built)

`axes[0].set_xticks(x_year[::tick_step])`

`tick_step` :
Les annees ne se chevauchent plus, car on affiche "une annee sur n" sur l'axe x de `Year Built`.

## Explication : `qual_counts`

```python
qual_counts = df_subset["Overall Qual"].value_counts().sort_index()
```

Cette ligne :
- selectionne la colonne `Overall Qual`
- compte le nombre d'occurrences de chaque note (`value_counts`)
- trie les resultats par valeur de note (`sort_index`)

Tu obtiens une serie `note -> effectif`, pratique pour tracer un diagramme en barres ordonne.


#!/usr/bin/env python3
"""Génère E1bis … E5bis — focus localisation (Neighborhood, MSZoning, Condition1/2) vs SalePrice."""
import json
import textwrap
import uuid

NB_META = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.12.0"},
}


def _src_lines(s: str):
    lines = s.splitlines()
    return [ln + "\n" for ln in lines[:-1]] + ([lines[-1] + "\n"] if lines else [])


def md(s: str):
    return {
        "cell_type": "markdown",
        "id": str(uuid.uuid4())[:12],
        "metadata": {},
        "source": _src_lines(textwrap.dedent(s).strip()),
    }


def code(s: str):
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": str(uuid.uuid4())[:12],
        "metadata": {},
        "outputs": [],
        "source": _src_lines(textwrap.dedent(s).strip()),
    }


def write_nb(path: str, cells: list):
    nb = {
        "cells": cells,
        "metadata": NB_META,
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)


# Colonnes canoniques (après suppression des espaces dans les noms)
LOC_BLOCK = """
# Variables étudiées (jeu réduit « localisation »)

| Colonne (pandas) | Rôle |
|------------------|------|
| `Neighborhood` | Quartier à Ames |
| `MSZoning` | Zonage (usage du sol) |
| `Condition1` | Proximité / condition 1 (route, voie ferrée, etc.) |
| `Condition2` | Proximité / condition 2 |
| `SalePrice` | Prix de vente (cible) |

```python
COLS_LOC = ["Neighborhood", "MSZoning", "Condition1", "Condition2", "SalePrice"]
```
"""

# --------------------------------------------------------------------------- E1bis
cells_e1 = [
    md(
        """
        # Exercice 1.1 bis : EDA — **impact de la localisation sur le prix**

        Variante du notebook E1 : même méthodologie d’analyse exploratoire, appliquée à un **sous-jeu centré sur la localisation** (quartier, zonage, conditions de proximité) et le prix de vente.
        """
    ),
    md(
        """
        ## Contexte

        Le dataset **Ames Housing** décrit des ventes de maisons à Ames (Iowa). Ici, on isole les variables qui décrivent **où** se situe le bien et **quel environnement** l’entoure, pour mesurer leur lien avec `SalePrice`.

        """
        + LOC_BLOCK
    ),
    md(
        """
        ## Objectifs d’apprentissage

        - Structurer une EDA sur un sous-ensemble de variables métier (localisation).
        - Décrire `SalePrice` et les distributions des modalités de localisation.
        - Détecter des valeurs atypiques sur le prix (IQR, z-score modifié).
        - Formuler des hypothèses sur l’effet du quartier et du zonage sur le prix.
        """
    ),
    md(
        """
        ### Section 1 — Imports et chargement

        **À faire :**
        - Charger `AmesHousing.csv`, harmoniser les noms de colonnes (suppression des espaces).
        - Construire `df_loc = df[COLS_LOC].copy()`.
        - Afficher les dimensions, les 5 premières lignes et les types.
        """
    ),
    code(
        """
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        from scipy import stats

        sns.set_theme(style="whitegrid")

        df = pd.read_csv("AmesHousing.csv")
        df.columns = df.columns.str.replace(" ", "")

        COLS_LOC = ["Neighborhood", "MSZoning", "Condition1", "Condition2", "SalePrice"]
        df_loc = df[COLS_LOC].copy()

        print(df_loc.shape)
        print(df_loc.dtypes)
        print(df_loc.head())
        """
    ),
    md(
        """
        ### Section 2 — Aperçu général et qualité des données

        **À faire :**
        - Pour chaque colonne : nombre de valeurs manquantes et proportion.
        - Vérifier les doublons complets sur les 5 colonnes.
        - Les modalités rares (ex. quartiers) peuvent poser problème plus tard : notez les effectifs par `Neighborhood`.
        """
    ),
    code(
        """
        miss = df_loc.isna().mean() * 100
        print("Pourcentage de manquants par colonne :")
        print(miss.round(2))

        print("Doublons complets :", df_loc.duplicated().sum())

        print("\\nEffectifs par quartier (top 15) :")
        print(df_loc["Neighborhood"].value_counts().head(15))
        """
    ),
    md(
        """
        ### Section 3 — Statistiques descriptives univariées

        **À faire :**
        - `describe()` sur `SalePrice` ; skewness et kurtosis.
        - Tableaux de fréquences pour `Neighborhood`, `MSZoning`, `Condition1`, `Condition2` (tri par fréquence décroissante).
        """
    ),
    code(
        """
        print(df_loc["SalePrice"].describe())
        print("Skew SalePrice :", df_loc["SalePrice"].skew())
        print("Kurtosis SalePrice :", df_loc["SalePrice"].kurtosis())

        for col in ["Neighborhood", "MSZoning", "Condition1", "Condition2"]:
            print("\\n---", col, "---")
            print(df_loc[col].value_counts())
        """
    ),
    md(
        """
        ### Section 4 — Visualisations et symétrie du prix

        **À faire :**
        - Histogramme + KDE de `SalePrice` ; Q-Q plot (normalité grossière).
        - Graphiques adaptés aux variables qualitatives : barres des effectifs pour le zonage et les conditions.
        - Graphique montrant la **médiane de `SalePrice` par `Neighborhood`** (barres horizontales, triées).
        """
    ),
    code(
        """
        fig, ax = plt.subplots(1, 2, figsize=(12, 4))
        sns.histplot(df_loc["SalePrice"], kde=True, ax=ax[0])
        ax[0].set_title("Distribution de SalePrice")
        stats.probplot(df_loc["SalePrice"], dist="norm", plot=ax[1])
        ax[1].set_title("Q-Q plot (référence normale)")
        plt.tight_layout()
        plt.show()

        fig, axes = plt.subplots(1, 3, figsize=(14, 4))
        for ax, col in zip(axes, ["MSZoning", "Condition1", "Condition2"]):
            df_loc[col].value_counts().head(12).plot(kind="bar", ax=ax, rot=45)
            ax.set_title(col)
        plt.tight_layout()
        plt.show()

        med_nbh = df_loc.groupby("Neighborhood")["SalePrice"].median().sort_values()
        med_nbh.plot(kind="barh", figsize=(8, 10), title="Prix médian par quartier")
        plt.xlabel("SalePrice (médiane)")
        plt.tight_layout()
        plt.show()
        """
    ),
    md(
        """
        ### Section 5 — Détection d’outliers sur le prix (IQR et z-score modifié)

        **À faire :**
        - Sur `SalePrice` global : seuils IQR (1,5 × IQR) et comptage des points extrêmes.
        - z-score modifié (MAD) ou `scipy.stats.median_abs_deviation` — repérer les observations extrêmes.
        - Optionnel : même logique par **groupe `Neighborhood`** (prix « anormal » par rapport au quartier).
        """
    ),
    code(
        """
        s = df_loc["SalePrice"]
        q1, q3 = s.quantile([0.25, 0.75])
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        mask_iqr = (s < low) | (s > high)
        print(f"IQR : bornes [{low:.0f}, {high:.0f}], outliers : {mask_iqr.sum()}")

        med = s.median()
        mad = stats.median_abs_deviation(s, scale="normal")
        z_mod = 0.6745 * (s - med) / (mad if mad > 0 else np.nan)
        mask_z = np.abs(z_mod) > 3.5
        print(f"z modifié (>|3,5|) : {mask_z.sum()} observations")
        """
    ),
    md(
        """
        ### Section 6 — Hypothèses métier (localisation)

        **À rédiger en Markdown :**
        - H1 : les **quartiers** diffèrent significativement en prix médian.
        - H2 : le **zonage** `MSZoning` est associé à des niveaux de prix distincts.
        - H3 : certaines **conditions de proximité** (`Condition1` / `Condition2`) sont liées à des prix plus bas (nuisances).

        Indiquez comment vous pourriez tester ces hypothèses (tests, modèles) dans les prochains exercices.
        """
    ),
]

# --------------------------------------------------------------------------- E2bis
cells_e2 = [
    md(
        """
        # Exercice 1.2 bis : Visualisations univariées et bivariées — localisation vs prix

        Même logique que E2, appliquée à `df_loc` (quartier, zonage, conditions, `SalePrice`).
        """
    ),
    md("## Section 1: Imports et configuration"),
    code(
        """
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns

        sns.set_theme(style="whitegrid")

        df = pd.read_csv("AmesHousing.csv")
        df.columns = df.columns.str.replace(" ", "")
        COLS_LOC = ["Neighborhood", "MSZoning", "Condition1", "Condition2", "SalePrice"]
        df_loc = df[COLS_LOC].copy()
        """
    ),
    md(
        """
        ## Section 2: Visualisations univariées — variable continue (`SalePrice`)

        **À faire :** histogramme, KDE, boxplot vertical du prix.
        """
    ),
    code(
        """
        fig, axes = plt.subplots(1, 3, figsize=(14, 4))
        sns.histplot(df_loc["SalePrice"], kde=True, ax=axes[0])
        sns.boxplot(y=df_loc["SalePrice"], ax=axes[1])
        sns.ecdfplot(df_loc["SalePrice"], ax=axes[2])
        axes[0].set_title("Histogramme + KDE")
        axes[1].set_title("Boxplot")
        axes[2].set_title("Fonction de répartition empirique")
        plt.tight_layout()
        plt.show()
        """
    ),
    md(
        """
        ## Section 3: Visualisations univariées — variables qualitatives de localisation

        **À faire :** diagrammes en barres des effectifs pour chaque variable (limiter aux modalités les plus fréquentes si besoin).
        """
    ),
    code(
        """
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        for ax, col in zip(axes.ravel(), ["Neighborhood", "MSZoning", "Condition1", "Condition2"]):
            vc = df_loc[col].value_counts().head(20)
            vc.plot(kind="bar", ax=ax, rot=45)
            ax.set_title(col)
        plt.tight_layout()
        plt.show()
        """
    ),
    md(
        """
        ## Section 4: Visualisations bivariées — prix vs localisation

        **À faire :**
        - Boxplots ou violin plots de `SalePrice` par `Neighborhood` (rotation des labels).
        - Même idée pour `MSZoning`, `Condition1`, `Condition2`.
        - Strip plot ou `sns.swarmplot` (échantillon si trop lourd) pour voir la dispersion.
        """
    ),
    code(
        """
        plt.figure(figsize=(14, 6))
        order = df_loc.groupby("Neighborhood")["SalePrice"].median().sort_values().index
        sns.boxplot(data=df_loc, x="Neighborhood", y="SalePrice", order=order)
        plt.xticks(rotation=90)
        plt.title("SalePrice par quartier (ordonné par médiane croissante)")
        plt.tight_layout()
        plt.show()

        fig, axes = plt.subplots(1, 3, figsize=(14, 5))
        for ax, col in zip(axes, ["MSZoning", "Condition1", "Condition2"]):
            sns.boxplot(data=df_loc, x=col, y="SalePrice", ax=ax)
            ax.tick_params(axis="x", rotation=45)
            ax.set_title(col)
        plt.tight_layout()
        plt.show()
        """
    ),
    md(
        """
        ## Section 5: Exercice « Bad Viz »

        **À faire :** produire **volontairement** un graphique trompeur ou illisible (ex. barres sans échelle log pour des prix très skewés, ou quartiers illisibles sans rotation), puis le corriger dans la cellule suivante avec un court commentaire.
        """
    ),
    code(
        """
        # Mauvais : échelle écrasée, labels illisibles
        plt.figure(figsize=(4, 2))
        sns.boxplot(data=df_loc, x="Neighborhood", y="SalePrice")
        plt.title("Bad viz (volontaire)")
        plt.show()

        # Corrigé
        plt.figure(figsize=(14, 6))
        sns.boxplot(data=df_loc, x="Neighborhood", y="SalePrice", order=order)
        plt.xticks(rotation=90)
        plt.title("Version lisible")
        plt.tight_layout()
        plt.show()
        """
    ),
]

# --------------------------------------------------------------------------- E3bis
cells_e3 = [
    md(
        """
        # Exercice 1.3 bis : Analyse multivariée — corrélation et structure (localisation)

        Variante de E3 : les prédicteurs sont surtout **catégoriels**. On les encode (one-hot) pour construire des corrélations avec `SalePrice`, analyser la multicolinéarité sur les indicatrices, et explorer des corrélations partielles.
        """
    ),
    md("## Section 1: Imports et préparation"),
    code(
        """
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        from sklearn.preprocessing import OneHotEncoder

        df = pd.read_csv("AmesHousing.csv")
        df.columns = df.columns.str.replace(" ", "")
        COLS_LOC = ["Neighborhood", "MSZoning", "Condition1", "Condition2", "SalePrice"]
        df_loc = df[COLS_LOC].dropna().copy()

        X_cat = df_loc[["Neighborhood", "MSZoning", "Condition1", "Condition2"]]
        y = df_loc["SalePrice"]

        ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
        X_dum = pd.DataFrame(
            ohe.fit_transform(X_cat),
            columns=ohe.get_feature_names_out(X_cat.columns),
            index=df_loc.index,
        )
        df_num = pd.concat([X_dum, y.rename("SalePrice")], axis=1)
        print(df_num.shape)
        print(df_num.iloc[:, :8].head())
        # Les 8 premières colonnes = début des Neighborhood_* (ordre alphabétique) ; pas forcément le quartier de la ligne.
        s0 = df_num.iloc[0].drop("SalePrice", errors="ignore")
        print("Indicatrices à 1 pour la ligne 0 :")
        print(s0[s0 == 1])
        """
    ),
    md(
        """
        ## Section 2: Matrice de corrélation (Pearson) — `SalePrice` vs indicatrices

        **À faire :** heatmap des corrélations entre `SalePrice` et les colonnes dummy (afficher un sous-ensemble : par ex. les 30 corrélations les plus fortes en valeur absolue).
        """
    ),
    code(
        """
        corr = df_num.corr()["SalePrice"].drop("SalePrice").sort_values(key=np.abs, ascending=False)
        top = corr.head(30)
        plt.figure(figsize=(6, 10))
        sns.heatmap(top.to_frame("corr avec SalePrice"), annot=True, fmt=".2f", cmap="RdBu_r", center=0)
        plt.title("Top corrélations (valeur absolue)")
        plt.tight_layout()
        plt.show()
        """
    ),
    md(
        """
        ## Section 3: Nuages de dispersion / pair plot restreint

        **À faire :** comme il y a trop de dummy, tracez `SalePrice` en fonction d’un **code numérique de quartier** (LabelEncoder) en colorant par `MSZoning`, ou utilisez `sns.scatterplot` avec `Neighborhood` en `hue` sur un échantillon de quartiers.
        """
    ),
    code(
        """
        from sklearn.preprocessing import LabelEncoder

        le = LabelEncoder()
        df_loc["Neighborhood_code"] = le.fit_transform(df_loc["Neighborhood"])
        sample_nbh = df_loc["Neighborhood"].value_counts().head(8).index
        sub = df_loc[df_loc["Neighborhood"].isin(sample_nbh)]

        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=sub,
            x="Neighborhood_code",
            y="SalePrice",
            hue="MSZoning",
            alpha=0.5,
        )
        plt.title("Prix vs code quartier (8 quartiers les plus fréquents), couleur = zonage")
        plt.tight_layout()
        plt.show()
        """
    ),
    md(
        """
        ## Section 4: Multicolinéarité (VIF) sur un sous-ensemble d’indicatrices

        **À faire :** calculer le VIF sur les **k premières colonnes** dummy + constante (ex. `statsmodels`), ou sur un groupe réduit pour éviter matrices singulières. Interpréter : fortes dépendances entre indicatrices du même bloc (normal).
        """
    ),
    code(
        """
        try:
            from statsmodels.stats.outliers_influence import variance_inflation_factor
            import statsmodels.api as sm

            k = min(25, X_dum.shape[1])
            X_vif = sm.add_constant(X_dum.iloc[:, :k])
            vifs = [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]
            vif_df = pd.DataFrame({"feature": X_vif.columns, "VIF": vifs})
            print(vif_df.sort_values("VIF", ascending=False).head(15))
        except ImportError:
            print("Installez statsmodels : pip install statsmodels")
        """
    ),
    md(
        """
        ## Section 5: Corrélation partielle (proxy)

        **À faire :** avec `pingouin` si disponible, corrélation partielle entre `SalePrice` et une variable encodée en numérique simple, en contrôlant une autre (ex. effet `MSZoning` numérisé). Sinon, expliquer la limite des indicatrices multiples.
        """
    ),
    code(
        """
        try:
            import pingouin as pg

            df_loc["MSZ_num"] = LabelEncoder().fit_transform(df_loc["MSZoning"])
            df_loc["Cond1_num"] = LabelEncoder().fit_transform(df_loc["Condition1"])
            # corrélation partielle : prix vs cond1 en contrôlant MSZoning
            pc = pg.partial_corr(
                data=df_loc,
                x="SalePrice",
                y="Cond1_num",
                covar="MSZ_num",
                method="spearman",
            )
            print(pc)
        except ImportError:
            print("pip install pingouin pour la corrélation partielle")
        """
    ),
    md(
        """
        ## Section 7 (optionnelbis) : Synthèse

        Résumez : quelles modalités de localisation sont les plus associées à des prix élevés ou bas d’après les corrélations et les graphiques ?
        """
    ),
]

# --------------------------------------------------------------------------- E4bis
cells_e4 = [
    md(
        """
        # Exercice 1.4 bis : Détection d’anomalies — contexte « localisation »

        On cherche des ventes **atypiques** : prix extrême par rapport au quartier, ou combinaisons rares localisation / prix. Même plan méthodologique que E4, adapté à `df_loc`.
        """
    ),
    md("## Section 1.1 — Préparation"),
    code(
        """
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        from sklearn.preprocessing import LabelEncoder, StandardScaler
        from sklearn.ensemble import IsolationForest
        from sklearn.cluster import DBSCAN
        from scipy import stats

        df = pd.read_csv("AmesHousing.csv")
        df.columns = df.columns.str.replace(" ", "")
        COLS_LOC = ["Neighborhood", "MSZoning", "Condition1", "Condition2", "SalePrice"]
        df_loc = df[COLS_LOC].dropna().copy()

        le_n = LabelEncoder()
        df_loc["Neighborhood_code"] = le_n.fit_transform(df_loc["Neighborhood"])
        """
    ),
    md("## Section 1.2 — IQR et z-score modifié sur `SalePrice`"),
    code(
        """
        s = df_loc["SalePrice"]
        q1, q3 = s.quantile([0.25, 0.75])
        iqr = q3 - q1
        mask_iqr = (s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)

        med = s.median()
        mad = stats.median_abs_deviation(s, scale="normal")
        z = 0.6745 * (s - med) / mad
        mask_z = np.abs(z) > 3.5
        df_loc["flag_iqr"] = mask_iqr
        df_loc["flag_z"] = mask_z
        print("IQR outliers :", mask_iqr.sum(), "| z-mod outliers :", mask_z.sum())
        """
    ),
    md("## Section 1.3 — Isolation Forest (prix + code quartier)"),
    code(
        """
        X_if = df_loc[["SalePrice", "Neighborhood_code"]].values
        iso = IsolationForest(random_state=42, contamination=0.05)
        pred_iso = iso.fit_predict(X_if)
        df_loc["iso"] = pred_iso
        print("Anomalies IF :", (pred_iso == -1).sum())
        """
    ),
    md("## Section 1.4 — DBSCAN (features normalisées)"),
    code(
        """
        sc = StandardScaler()
        X_db = sc.fit_transform(df_loc[["SalePrice", "Neighborhood_code"]])
        db = DBSCAN(eps=0.5, min_samples=10)
        df_loc["dbscan"] = db.fit_predict(X_db)
        print("Clusters / bruit DBSCAN :", np.unique(df_loc["dbscan"], return_counts=True))
        """
    ),
    md("## Section 1.5 — Tableau comparatif et scatter"),
    code(
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        sca = ax.scatter(
            df_loc["Neighborhood_code"],
            df_loc["SalePrice"],
            c=np.where(df_loc["iso"] == -1, 2, 0),
            cmap="coolwarm",
            alpha=0.5,
            s=12,
        )
        ax.set_xlabel("Neighborhood (code)")
        ax.set_ylabel("SalePrice")
        ax.set_title("Prix vs quartier — couleur liée à Isolation Forest")
        plt.colorbar(sca, ax=ax)
        plt.tight_layout()
        plt.show()
        """
    ),
    md("## Section 2: LOF (optionnel)"),
    code(
        """
        try:
            from sklearn.neighbors import LocalOutlierFactor

            X_lof = StandardScaler().fit_transform(df_loc[["SalePrice", "Neighborhood_code"]])
            lof = LocalOutlierFactor(n_neighbors=30, contamination=0.05)
            df_loc["lof"] = lof.fit_predict(X_lof)
            print("LOF outliers :", (df_loc["lof"] == -1).sum())
        except Exception as e:
            print(e)
        """
    ),
    md("## Section 3: Stratégies (Markdown à compléter)"),
    md(
        """
        - Liste d’actions possibles : garder, investiguer, caper le prix, segmenter par quartier.
        - Log-transform du prix pour réduire l’asymétrie avant clustering.
        """
    ),
    md("## Section 4: Great Expectations (optionnel)"),
    md(
        """
        Si vous utilisez GX : attentes sur `SalePrice` > 0, modalités connues pour `Neighborhood`, etc.
        """
    ),
    md("## Section 5: Bilan critique"),
    md(
        """
        Un prix « anormal » peut être une **erreur** ou une **vente atypique légitime** (très grande maison dans un quartier modeste) : la localisation seule n’explique pas tout.
        """
    ),
]

# --------------------------------------------------------------------------- E5bis
cells_e5 = [
    md(
        """
        # Exercice 1.5 bis : Feature engineering — prédire le prix à partir de la localisation

        Variante de E5 : **X** = uniquement les variables de localisation (et dérivées), **y** = `SalePrice`.
        Même principes : split train/test, encodage adapté, pipeline, comparaison baseline vs modèle enrichi.
        """
    ),
    md(
        """
        ## Règle : pas de fuite de données

        `fit` sur le train uniquement pour toute transformation.
        """
    ),
    md("## Section 1: Imports, chargement, split"),
    code(
        """
        import numpy as np
        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import OneHotEncoder, TargetEncoder
        from sklearn.impute import SimpleImputer
        from sklearn.linear_model import Lasso, Ridge
        from sklearn.metrics import root_mean_squared_error

        df = pd.read_csv("AmesHousing.csv")
        df.columns = df.columns.str.replace(" ", "")
        COLS_LOC = ["Neighborhood", "MSZoning", "Condition1", "Condition2", "SalePrice"]

        X = df[COLS_LOC[:-1]]
        y = df["SalePrice"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )
        print(X_train.shape, X_test.shape)

        cat_cols = list(X_train.columns)

        def make_ohe_prep():
            ohe_pipe = Pipeline(
                steps=[
                    ("imp", SimpleImputer(strategy="most_frequent")),
                    (
                        "ohe",
                        OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                    ),
                ]
            )
            return ColumnTransformer([("cat", ohe_pipe, cat_cols)], remainder="drop")

        """
    ),
    md("## Section 2: Encodage (OHE pour les nominaux)"),
    code(
        """
        base = Pipeline(
            [
                ("prep", make_ohe_prep()),
                ("model", Lasso(alpha=1.0, max_iter=20000)),
            ]
        )
        base.fit(X_train, y_train)
        pred_b = base.predict(X_test)
        rmse_b = root_mean_squared_error(y_test, pred_b)
        print("RMSE baseline (OHE + Lasso) :", round(rmse_b, 2))
        """
    ),
    md("## Section 3: Cible log + même pipeline"),
    code(
        """
        y_tr_log = np.log1p(y_train)

        base_log = Pipeline(
            [
                ("prep", make_ohe_prep()),
                ("model", Ridge(alpha=10.0)),
            ]
        )
        base_log.fit(X_train, y_tr_log)
        pred_log = np.expm1(base_log.predict(X_test))
        rmse_log = root_mean_squared_error(y_test, pred_log)
        print("RMSE avec log1p sur y + Ridge :", round(rmse_log, 2))
        """
    ),
    md("## Section 4: Modèle enrichi — Target Encoding sur `Neighborhood` + OHE sur le reste"),
    code(
        """
        te_nbh = TargetEncoder(random_state=42, target_type="continuous")

        transformers = [
            ("te_nbh", te_nbh, ["Neighborhood"]),
            (
                "ohe_rest",
                Pipeline(
                    [
                        ("imp", SimpleImputer(strategy="most_frequent")),
                        (
                            "ohe",
                            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                        ),
                    ]
                ),
                ["MSZoning", "Condition1", "Condition2"],
            ),
        ]

        prep_fe = ColumnTransformer(transformers)

        pipe_fe = Pipeline(
            [
                ("prep", prep_fe),
                ("model", Ridge(alpha=10.0)),
            ]
        )

        pipe_fe.fit(X_train, y_tr_log)
        pred_fe = np.expm1(pipe_fe.predict(X_test))
        rmse_fe = root_mean_squared_error(y_test, pred_fe)
        print("RMSE pipeline FE (TE Neighborhood + OHE + log y) :", round(rmse_fe, 2))
        print("Comparaison RMSE (même échelle $) : baseline OHE+Lasso", round(rmse_b, 2), "| OHE+Ridge+log y", round(rmse_log, 2))
        """
    ),
    md(
        """
        ## Synthèse

        | Modèle | RMSE ($) |
        |--------|----------|
        | Lasso + OHE (y en dollars) | *voir sortie* |
        | Ridge + OHE + `log1p(y)` | *voir sortie* |
        | Ridge + TE `Neighborhood` + OHE reste + `log1p(y)` | *voir sortie* |

        Interprétez : la localisation seule explique une part limitée de la variance du prix ; comparez aux modèles utilisant toutes les variables du dataset complet.
        """
    ),
]

if __name__ == "__main__":
    base = "/Users/romain/Desktop/EDA_Vis_FEng"
    # Noms courts (E1bis … E5bis) + titres descriptifs en doublon
    write_nb(f"{base}/E1bis.ipynb", cells_e1)
    write_nb(f"{base}/E2bis.ipynb", cells_e2)
    write_nb(f"{base}/E3bis.ipynb", cells_e3)
    write_nb(f"{base}/E4bis.ipynb", cells_e4)
    write_nb(f"{base}/E5bis.ipynb", cells_e5)
    print("5 notebooks bis générés (E1bis.ipynb … E5bis.ipynb).")

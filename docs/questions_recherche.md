# Questions de recherche / use cases métier – Google Trends & IA

## 1. Contexte

Nous analysons l'évolution de l'intérêt des internautes pour l'intelligence artificielle
à partir des données **Google Trends** sur plusieurs mots-clés liés à l'IA, par exemple :

- `ia`
- `chatgpt`
- `deep_learning`
- (et éventuellement d'autres termes à venir)

Chaque point de données représente un **indice d'intérêt (0-100)** normalisé par Google,
pour une période donnée (par exemple par mois).

---

## 2. Questions principales

### Q1 – Comment l'intérêt pour l'IA évolue-t-il dans le temps ?
- **Données utilisées** : toutes les catégories (`ia`, `chatgpt`, `deep_learning`, …).
- **Métrique principale** : `metric_1` = indice d'intérêt Google Trends.
- **Visualisation** : courbe de l'indice d'intérêt (par mot-clé) en fonction du temps.
- **Insight attendu** :
  - Montée brutale de certains termes (`chatgpt`) à partir de fin 2022 / 2023.
  - Tendances longues sur `ia` vs termes plus récents comme `chatgpt`.

### Q2 – Quels mots-clés liés à l'IA sont les plus recherchés ?
- **Données utilisées** : agrégation par `category` (mot-clé).
- **Métriques** :
  - `metric_1` moyen par mot-clé.
  - éventuellement max / min.
- **Visualisation** : diagramme en barres comparant les moyens par mot-clé.
- **Insight attendu** :
  - Comparaison de popularité entre `ia`, `chatgpt`, `deep_learning`, etc.

### Q3 – Y a-t-il une saisonnalité ou des périodes clés ?
- **Données utilisées** : `event_time`, `metric_1`, `category`.
- **Métrique** :
  - moyenne de `metric_1` par mois / trimestre.
- **Visualisation** :
  - courbe ou heatmap (plus tard) par période.
- **Insight attendu** :
  - pics lors de sorties médiatiques (lancement de modèles, annonces IA, etc.).

---

## 3. Interprétation des colonnes techniques

Dans la table `fact_event` actuelle :

- `event_time` : date / période Google Trends (par exemple début de mois).
- `metric_1` : **indice d'intérêt Google Trends** (0–100) pour un mot-clé.
- `metric_2` : placeholder pour une métrique secondaire (peut devenir, par exemple,
  un indice lissé, un score de volatilité ou un autre indicateur).
- `category` : mot-clé Google Trends (`ia`, `chatgpt`, `deep_learning`, ...).
- `source_id` : identifiant de la source de données (1 = CSV Google Trends IA).
- `raw_reference` : référence vers la donnée brute dans la couche raw (fichier, index…).

---

## 4. Pistes d’extension (IA / ML)

- Prédire l'évolution de l'intérêt pour un mot-clé (série temporelle simple).
- Détecter automatiquement des “changepoints” (sauts brusques d'intérêt).
- Comparer plusieurs pays / régions si on introduit cette dimension.


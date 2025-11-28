# Architecture du projet DataLake

> À compléter avec votre groupe.

## 1. Vue d'ensemble

- **Couche ingestion** : scripts batch (Python) pour récupérer les données depuis plusieurs sources (CSV, API, scraping, ...).
- **Couche persistance** : Data Lake (fichiers `raw` / `processed`) + base relationnelle (PostgreSQL) pour l'analyse.
- **Couche insight** : dashboard interactif (Streamlit) + notebooks éventuels.

## 2. Schéma logique (exemple à adapter)

- `ingestion` écrit :
  - fichiers bruts (`raw`) dans `data/raw/`
  - logs éventuels

- `persistence` :
  - lit `data/raw/*`
  - nettoie / transforme
  - écrit les données consolidées dans les tables :
    - `dim_source`
    - `fact_event`

- `insight` :
  - lit depuis PostgreSQL
  - fournit :
    - filtres
    - visualisations
    - édition / insertion simple

## 3. Technologies retenues

- Langage principal : **Python**
- Base de données : **PostgreSQL**
- Dashboard : **Streamlit**
- Orchestration batch : scripts manuels (ou Airflow / cron si vous souhaitez aller plus loin)

Expliquez ici **pourquoi** vous avez choisi ces technologies (contexte pédagogique, contraintes, préférences de l'équipe, etc.).

# Projet Big Data / DataLake – Skeleton

Ce dépôt contient une **architecture type** pour le TP *Architecture Big Data : Ingestion, Persistance, Traitement et Insights des Données*.

L'idée est de vous fournir une base de travail :
- une séparation claire des **3 couches** : ingestion, persistance, insight,
- des exemples de scripts Python prêts à adapter,
- un `docker-compose` minimal pour une base PostgreSQL,
- un exemple de dashboard **Streamlit**.

> ⚠️ Tout est **à adapter** à votre sujet, vos jeux de données et vos choix technologiques.

---

## Structure

```bash
bigdata_datalake_tp/
├── README.md
├── docker-compose.yml
├── requirements.txt
├── config/
│   └── config_example.yaml
├── ingestion/
│   ├── ingest_csv_batch.py
│   └── ingest_api_batch.py
├── persistence/
│   ├── create_tables.sql
│   └── load_to_warehouse.py
├── insight/
│   └── dashboard_streamlit.py
└── docs/
    ├── architecture.md
    └── questions_recherche.md
```

---

## 1. Installation rapide

```bash
python -m venv .venv
source .venv/bin/activate  # sous Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Lancez la base de données :

```bash
docker-compose up -d
```

---

## 2. Flux de bout en bout (exemple)

1. **Ingestion (batch)**
   - `ingestion/ingest_csv_batch.py` : récupère un fichier CSV (local ou distant) et le stocke en **raw**.
   - `ingestion/ingest_api_batch.py` : appelle une API et stocke la réponse JSON en **raw**.

   Les données brutes sont stockées, par exemple, sous :
   - `data/raw/csv/...`
   - `data/raw/api/...`

2. **Persistance / ETL**
   - `persistence/load_to_warehouse.py` :
     - lit les données `raw`,
     - fait un nettoyage / normalisation simple,
     - insère les données dans PostgreSQL (ou autre base) via les tables définies dans `create_tables.sql`.

3. **Insight / Dashboard**
   - `insight/dashboard_streamlit.py` :
     - lit les données dans PostgreSQL,
     - propose quelques filtres,
     - affiche des graphes simples,
     - permet (exemple) d'insérer ou d'éditer une ligne.

Lancement :

```bash
# 1. ingestion
python ingestion/ingest_csv_batch.py
python ingestion/ingest_api_batch.py

# 2. ETL -> base
python persistence/load_to_warehouse.py

# 3. Dashboard
streamlit run insight/dashboard_streamlit.py
```

---

## 3. À faire par votre groupe

- Choisir **au moins deux sources** (CSV, API, scraping, etc.).
- Adapter les scripts d'ingestion pour vos vraies sources.
- Concevoir un **schéma de tables** cohérent dans `create_tables.sql`.
- Définir vos **questions d'analyse** dans `docs/questions_recherche.md` et réaliser les graphes / rapports associés.
- Compléter `docs/architecture.md` avec votre schéma final et vos choix techniques.

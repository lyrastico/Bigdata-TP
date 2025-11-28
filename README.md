# 🧠 Big Data – DataLake IA (Google Trends & Actualités)

Projet réalisé dans le cadre du module **Architecture Big Data – DataLake**.  
L’objectif est de construire un pipeline complet d’ingestion, de persistance et de visualisation autour du thème :

# 🎯 Analyse de l’évolution de l’intérêt mondial pour l’Intelligence Artificielle

Ce projet combine deux sources de données **hétérogènes** :

1. **Google Trends (CSV)** – intérêt du public pour :  
   - “ia”  
   - “deep learning”  
   - “chatgpt”

2. **Google News RSS (XML / RSS)** – nombre d’articles publiés sur **“intelligence artificielle”**

Ces données sont ingérées en batch, stockées dans une couche raw, transformées puis envoyées dans un Data Warehouse Postgres, et visualisées via Streamlit.

---

# 📌 Sujet du projet

L’objectif est de construire une architecture DataLake comprenant :

- Ingestion (CSV + RSS)  
- Nettoyage et transformation  
- Stockage raw + Data Warehouse  
- Dashboard Insight interactif  

Le thème choisi :  
> Étudier l’évolution de l’intérêt mondial pour l’Intelligence Artificielle, ainsi que son niveau de médiatisation, puis explorer d’éventuelles corrélations.

---

# 🔎 Sources de données utilisées

## 1. Google Trends (CSV)

Google Trends fournit un score hebdomadaire (0–100) indiquant à quel point un terme est recherché.  
Mots-clés utilisés :

- `ia`
- `deep learning`
- `chatgpt`

Exemple de CSV :

```
Semaine, deep learning
2020-11-22, 15
2020-11-29, 16
```

Ce sont des données historiques permettant d’analyser les tendances du public.

---

## 2. Google News RSS (Actualités IA)

Flux RSS Google News :  
`https://news.google.com/rss/search?q=intelligence+artificielle`

Chaque article contient :

- un titre  
- une date de publication  
- une source média  

Les données sont nettoyées puis agrégées **par semaine**, donnant :

| event_time | metric_1 | category |
|------------|----------|----------|
| 2025-11-17 | 42       | news_ia  |
| 2025-11-24 | 18       | news_ia  |

---

# 🧩 Pourquoi combiner ces deux sources ?

Parce qu’ensemble, elles permettent d’étudier l’écosystème IA :

### 🔵 Google Trends → intérêt du public  
### 🟠 Google News → médiatisation dans les médias  

Cela permet de voir :

- si les pics de recherche correspondent aux pics d’actualité  
- l’impact médiatique de ChatGPT  
- la différence entre intérêt général (IA) et intérêt technique (deep learning)

---

# 🏗️ Architecture du projet

```
             +----------------------+
             | Google Trends (CSV)  |
             +----------+-----------+
                        |
                        v
                ingest_csv_batch.py
                        |
                +-------+-------+
                |     Raw       |
                +-------+-------+
                        |
             +----------+-----------+
             | Google News (RSS)    |
             +----------+-----------+
                        |
                        v
               ingest_news_batch.py
                        |
                        v
           +------------+-------------+
           | ETL → Postgres (DW)      |
           +------------+-------------+
                        |
                        v
                  Dashboard Insight
                 (Streamlit, filters)
```

---

# 🚀 Installation & Lancement

## 1. Cloner

```powershell
git clone https://github.com/lyrastico/Bigdata-TP.git
cd Bigdata-TP
```

## 2. Installer Python

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 3. Lancer Postgres (Docker)

```powershell
docker-compose up -d
```

Créer les tables :

```powershell
Get-Content .\persistence\create_tables.sql | docker exec -i datalake_postgres psql -U datalake_user -d datalake_db
```

## 4. Ingestion

### Google Trends

```powershell
python ingestion\ingest_csv_batch.py
```

### Actualités IA

```powershell
python ingestion\ingest_news_batch.py
```

## 5. ETL vers Postgres

```powershell
python persistence\load_to_warehouse.py
```

## 6. Dashboard

```powershell
streamlit run insight\dashboard_streamlit.py
```

---

# ♻️ Réinitialiser complètement les données

## 1. Vider Postgres

```powershell
docker exec -it datalake_postgres psql -U datalake_user -d datalake_db
```

Dans psql :

```sql
TRUNCATE TABLE fact_event, dim_source RESTART IDENTITY;
\q
```

## 2. Supprimer Raw & Processed

```powershell
Remove-Item data\raw\* -Force
Remove-Item data\processed\* -Force
```

## 3. Re-ingérer

```powershell
python ingestion\ingest_csv_batch.py
python ingestion\ingest_news_batch.py
python persistence\load_to_warehouse.py
```

---

# 👥 Auteurs

Projet réalisé dans le cadre du module Big Data – DataLake (IPSSI).

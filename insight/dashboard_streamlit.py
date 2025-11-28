import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import yaml


def load_config(path: str = "config/config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@st.cache_resource
def get_engine(cfg):
    db = cfg["database"]
    url = (
        f"postgresql://{db['user']}:{db['password']}@{db['host']}:"
        f"{db['port']}/{db['db']}"
    )
    return create_engine(url, future=True)


def load_fact_event(engine):
    query = """
    SELECT id, source_id, event_time, metric_1, metric_2, category, raw_reference
    FROM fact_event
    ORDER BY event_time ASC;
    """
    return pd.read_sql(query, engine)


def main():
    st.set_page_config(page_title="DataLake IA – Trends & News", layout="wide")

    st.title("📊 DataLake IA – Google Trends & Actualités")
    st.write(
        "Analyse de l’intérêt pour l’intelligence artificielle à partir de "
        "**Google Trends** (3 mots-clés) et d’un **flux RSS d’actualités IA**."
    )

    config = load_config()
    engine = get_engine(config)

    df = load_fact_event(engine)
    if df.empty:
        st.warning("Aucune donnée dans `fact_event` pour l'instant. Lance l'ingestion + ETL.")
        return

    df["event_time"] = pd.to_datetime(df["event_time"], errors="coerce")
    df = df.dropna(subset=["event_time"])
    df = df.sort_values("event_time")

    # Séparation par source
    df_trends = df[df["source_id"] == 1].copy()
    df_news = df[df["source_id"] == 2].copy()

    # ============================
    #  PARTIE 1 : GOOGLE TRENDS
    # ============================
    st.header("📈 Google Trends – Intérêt pour l’IA")

    if df_trends.empty:
        st.info("Aucune donnée Google Trends (source_id = 1).")
    else:
        st.sidebar.header("🎛 Filtres Google Trends")

        all_categories = sorted(df_trends["category"].dropna().unique().tolist())
        selected_categories = st.sidebar.multiselect(
            "Mots-clés à afficher",
            options=all_categories,
            default=all_categories,
        )

        min_date = df_trends["event_time"].min().date()
        max_date = df_trends["event_time"].max().date()

        date_range = st.sidebar.date_input(
            "Période d’analyse (Trends)",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date, end_date = min_date, max_date

        filtered_df = df_trends.copy()

        if selected_categories:
            filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]

        filtered_df = filtered_df[
            (filtered_df["event_time"].dt.date >= start_date)
            & (filtered_df["event_time"].dt.date <= end_date)
        ]

        if filtered_df.empty:
            st.warning("Aucune donnée Trends pour ces filtres (catégories + dates).")
        else:
            st.subheader("🧾 Indicateurs de synthèse (Trends)")

            col_a, col_b, col_c = st.columns(3)

            with col_a:
                st.metric("Nombre total de points (Trends)", len(filtered_df))

            with col_b:
                st.metric("Nombre de mots-clés", len(filtered_df["category"].unique()))

            with col_c:
                avg_global = filtered_df["metric_1"].mean()
                st.metric("Intérêt moyen (Trends)", f"{avg_global:.1f}")

            st.markdown("### 📈 Évolution de l’intérêt dans le temps (Google Trends)")
            st.caption("`metric_1` = indice d'intérêt Google Trends (0–100). Une ligne par mot-clé.")

            pivot_df = (
                filtered_df.pivot_table(
                    index="event_time",
                    columns="category",
                    values="metric_1",
                    aggfunc="mean",
                )
                .sort_index()
            )
            st.line_chart(pivot_df)

            st.markdown("### 📊 Comparaison de l’intérêt moyen par mot-clé (Trends)")
            st.caption("Moyenne de `metric_1` sur la période filtrée.")

            mean_df = (
                filtered_df.groupby("category", dropna=True)["metric_1"]
                .mean()
                .sort_values(ascending=False)
                .reset_index()
            )
            mean_df = mean_df.set_index("category")

            st.bar_chart(mean_df)

            st.markdown("### 🔎 Aperçu des données Trends filtrées")
            st.dataframe(
                filtered_df[["event_time", "category", "metric_1"]]
                .sort_values(["event_time", "category"])
                .reset_index(drop=True)
                .head(200)
            )

    st.markdown("---")

    # ============================
    #  PARTIE 2 : NEWS IA (RSS)
    # ============================
    st.header("📰 Actualités IA – Flux RSS")

    if df_news.empty:
        st.info("Aucune donnée d’actualités IA (source_id = 2). "
                "Lance `ingest_news_batch.py` puis `load_to_warehouse.py`.")
    else:
        # On suppose que metric_1 = nb d'articles par semaine, category = "news_ia"
        df_news = df_news.sort_values("event_time")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Semaines avec des news", len(df_news))
        with col2:
            total_articles = df_news["metric_1"].sum()
            st.metric("Nombre total d’articles IA (approx.)", int(total_articles))

        st.markdown("### 📊 Volume d’articles IA par semaine")
        st.caption("`metric_1` = nombre d’articles IA trouvés dans le flux RSS (agrégés par semaine).")

        news_series = df_news.set_index("event_time")["metric_1"]
        st.bar_chart(news_series)

        st.markdown("### 🔎 Aperçu des agrégations news")
        st.dataframe(
            df_news[["event_time", "category", "metric_1"]]
            .sort_values("event_time")
            .reset_index(drop=True)
        )


if __name__ == "__main__":
    main()

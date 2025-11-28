from pathlib import Path

import pandas as pd
import yaml
from sqlalchemy import create_engine


def load_config(path: str = "config/config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_engine(cfg):
    db = cfg["database"]
    url = (
        f"postgresql://{db['user']}:{db['password']}@{db['host']}:"
        f"{db['port']}/{db['db']}"
    )
    return create_engine(url, future=True)


def load_raw_parquets(raw_dir: Path, pattern: str) -> pd.DataFrame:
    files = sorted(raw_dir.glob(pattern))
    if not files:
        print(f"[WARN] Aucun fichier raw ne correspond à {pattern}")
        return pd.DataFrame()

    print(f"[INFO] Fichiers raw trouvés pour {pattern}:")
    for fp in files:
        print(f"  - {fp}")

    dfs = [pd.read_parquet(fp) for fp in files]
    df = pd.concat(dfs, ignore_index=True)
    print(f"[INFO] Total lignes raw ({pattern}) : {len(df)}")
    return df


def prepare_fact_df(df: pd.DataFrame, source_id: int) -> pd.DataFrame:

    expected_cols = ["event_time", "metric_1", "metric_2", "category"]
    for col in expected_cols:
        if col not in df.columns:
            print(f"[WARN] Colonne manquante: {col} -> création à None.")
            df[col] = None

    df["event_time"] = pd.to_datetime(df["event_time"], errors="coerce")
    df = df.dropna(subset=["event_time"])

    df["source_id"] = source_id
    df["raw_reference"] = df.index.astype(str)

    fact_df = df[["source_id", "event_time", "metric_1", "metric_2", "category", "raw_reference"]]
    return fact_df


def main():
    config = load_config()
    raw_dir = Path(config["paths"]["raw_dir"])
    engine = get_engine(config)

    df_trends_raw = load_raw_parquets(raw_dir, "csv_example_raw_*.parquet")
    fact_trends = pd.DataFrame()
    if not df_trends_raw.empty:
        fact_trends = prepare_fact_df(df_trends_raw, source_id=1)

    df_news_raw = load_raw_parquets(raw_dir, "news_ai_raw_*.parquet")
    fact_news = pd.DataFrame()
    if not df_news_raw.empty:
        fact_news = prepare_fact_df(df_news_raw, source_id=2)

    fact_all = pd.concat([fact_trends, fact_news], ignore_index=True)

    if fact_all.empty:
        print("[WARN] Rien à insérer dans fact_event.")
        return

    with engine.begin() as conn:
        fact_all.to_sql("fact_event", conn, if_exists="append", index=False)
        print(f"[OK] {len(fact_all)} lignes insérées dans fact_event.")


if __name__ == "__main__":
    main()

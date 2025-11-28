from pathlib import Path
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import xml.etree.ElementTree as ET

import pandas as pd
import requests
import yaml


def load_config(path: str = "config/config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    # Chargement config
    config = load_config()
    raw_dir = Path(config["paths"]["raw_dir"])
    raw_dir.mkdir(parents=True, exist_ok=True)

    news_conf = config["sources"]["news_ai"]
    url = news_conf["url"]

    print(f"[INFO] Récupération du flux RSS : {url}")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    # Parsing XML du RSS
    root = ET.fromstring(resp.content)

    items = []
    for item in root.iter("item"):
        title = item.findtext("title")
        pub_date_str = item.findtext("pubDate")

        if not pub_date_str:
            continue

        try:
            pub_dt = parsedate_to_datetime(pub_date_str)  # datetime avec timezone
        except Exception:
            continue

        items.append(
            {
                "title": title,
                "event_time": pub_dt,
            }
        )

    if not items:
        print("[WARN] Aucun item trouvé dans le flux RSS.")
        return

    df = pd.DataFrame(items)

    # Normalisation : on travaille en date de début de semaine (lundi)
    # -> to_period('W-MON') = semaine commençant le lundi
    df["week_start"] = df["event_time"].dt.to_period("W-MON").dt.start_time
    # On convertit en date sans heure pour éviter les axes chelous dans les graphes
    df["week_start"] = df["week_start"].dt.date

    # Agrégation : nombre d'articles par semaine
    agg = df.groupby("week_start").size().reset_index(name="article_count")

    # On construit la structure commune pour le DataLake
    agg = agg.rename(columns={"week_start": "event_time"})
    agg["metric_1"] = agg["article_count"]          # nb d'articles par semaine
    agg["metric_2"] = None                          # placeholder
    agg["category"] = "news_ia"                     # catégorie spéciale
    agg = agg[["event_time", "metric_1", "metric_2", "category"]]

    print(f"[INFO] Semaines agrégées : {len(agg)}")

    # Nom de fichier avec timestamp propre (timezone-aware)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = raw_dir / f"news_ai_raw_{ts}.parquet"
    agg.to_parquet(out_path, index=False)

    print(f"[OK] Données news IA (agrégées par semaine) sauvegardées en raw : {out_path}")


if __name__ == "__main__":
    main()

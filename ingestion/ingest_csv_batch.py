import re
from datetime import datetime
from io import StringIO
from pathlib import Path

import pandas as pd
import yaml


def load_config(path: str = "config/config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def read_trends_csv(csv_path: Path) -> pd.DataFrame:
    """
    Lit un CSV Google Trends du type :

    Catégorie : ...
    <ligne vide>
    Semaine,deep learning: (Dans tous les pays)
    2020-11-22,15
    2020-11-29,15
    ...

    -> On détecte la première ligne contenant une date AAAA-MM-JJ
       et on lit à partir de là, sans header.
    """
    with open(csv_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    data_start = None
    date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")

    for i, line in enumerate(lines):
        if date_pattern.search(line):
            data_start = i
            break

    if data_start is None:
        raise ValueError(
            f"Impossible de trouver une ligne de données avec une date dans {csv_path}"
        )

    # On reconstruit un CSV à partir de la 1ère ligne de data
    data_str = "".join(lines[data_start:])
    df = pd.read_csv(StringIO(data_str), sep=",", header=None)

    if df.shape[1] < 2:
        raise ValueError(
            f"Le fichier {csv_path} ne contient pas au moins 2 colonnes (date + valeur) après la ligne {data_start}."
        )

    # On ne garde que les 2 premières colonnes : date, valeur
    df = df.iloc[:, :2]
    df.columns = ["event_time", "metric_1"]

    return df


def main():
    config = load_config()

    raw_dir = Path(config["paths"]["raw_dir"])
    raw_dir.mkdir(parents=True, exist_ok=True)

    input_dir = Path("./data/input")

    # Fichiers CSV + catégorie associée
    files = [
        ("ai.csv", "ia"),
        ("deep learning.csv", "deep_learning"),
        ("chatgpt.csv", "chatgpt"),
    ]

    all_dfs = []

    for filename, category in files:
        csv_path = input_dir / filename
        if not csv_path.exists():
            print(f"[WARN] Fichier introuvable, on ignore : {csv_path}")
            continue

        print(f"[INFO] Lecture de {csv_path}")
        df = read_trends_csv(csv_path)

        if df.empty:
            print(f"[WARN] Fichier vide, on ignore : {csv_path}")
            continue

        # Conversion des dates
        df["event_time"] = pd.to_datetime(df["event_time"], errors="coerce")
        df = df.dropna(subset=["event_time"])

        # Ajout des autres colonnes
        df["metric_2"] = None  # placeholder pour plus tard si tu veux une autre métrique
        df["category"] = category

        df["metric_1"] = pd.to_numeric(df["metric_1"], errors="coerce")
        df = df.dropna(subset=["metric_1"])

        print(f"[INFO] Lignes gardées pour {category} : {len(df)}")
        all_dfs.append(df)

    if not all_dfs:
        print("[ERROR] Aucun CSV valide trouvé, rien à ingérer.")
        return

    final_df = pd.concat(all_dfs, ignore_index=True)

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_path = raw_dir / f"csv_example_raw_{ts}.parquet"

    final_df.to_parquet(out_path, index=False)
    print(f"[OK] Données Trends combinées en raw : {out_path}")
    print(f"[INFO] Lignes totales : {len(final_df)}")


if __name__ == "__main__":
    main()

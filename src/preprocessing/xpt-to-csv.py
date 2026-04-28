# import pyreadstat # Does not work
from pathlib import Path
import pandas as pd

# df = pd.read_sas(
#     "../../data/raw/CDS/DEMO_G.xpt",
#     format="xport"
# )
# print(df.head())
# df = pd.read_sas(DEMO_G.xpt, format="xport")
# print(df.head())

# cds-xpt-convert.py location
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent

raw_dir = PROJECT_ROOT / "data" / "raw" / "CDS"
preprocessed_dir = PROJECT_ROOT / "data" / "preprocessed" / "CDS"
preprocessed_dir.mkdir(parents=True, exist_ok=True)

for xpt_path in raw_dir.glob("*.xpt"):
    cds_data = xpt_path.stem
    df = pd.read_sas(str(xpt_path), format="xport")

    out_path = preprocessed_dir / f"{cds_data}.csv"
    df.to_csv(out_path, index=False)
    print(f"Converted {xpt_path.name} -> {out_path}")

    
# datasets = {}

# for file in data_dir.glob("*.xpt"):
#     datasets[file.stem] = pd.read_sas(file, format="xport")

# print(datasets.keys())
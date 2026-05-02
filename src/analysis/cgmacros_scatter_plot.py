from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CGMACROS_ROOT = (
    PROJECT_ROOT
    / "data"
    / "sample"
    / "cgmacros-scientific-dataset-nutrition-diet-monitoring-1.0.0"
    / "CGMacros_dateshifted365"
    / "CGMacros"
)

def get_bio_data():

    bio = pd.read_csv(CGMACROS_ROOT / "bio.csv")

    bio.columns = bio.columns.str.strip()

    if "Collection time PDL (Lab)" in bio.columns:
        bio["Collection time PDL (Lab)"] = pd.to_datetime(
            bio["Collection time PDL (Lab)"],
            errors="coerce"
        )
    return bio
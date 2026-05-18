from pathlib import Path
import pandas as pd

ROOT = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "raw"
    / "PhysioNet"
    / "cgmacros-scientific-dataset-nutrition-diet-monitoring-1.0.0"
    / "cgmacros-scientific-dataset-nutrition-diet-monitoring-1.0.0"
    / "CGMacros"
    / "_dateshifted365"
    / "CGMacros"
)
# Unnamed:0 is only in the first CGMacros
def load_participant(participant_id: int) -> pd.DataFrame:
    folder = ROOT / f"CGMacros-{participant_id:03d}"
    csv_path = folder / f"CGMacros-{participant_id:03d}.csv"

    df = pd.read_csv(csv_path)
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])
    if "Image path" in df.columns:
        df = df.drop(columns=["Image path"])

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df.sort_values("Timestamp")
from pathlib import Path
import pandas as pd
import numpy as np

# ROOT = Path(r"C:\Users\cymos\Akasi\data\sample\cgmacros-scientific-dataset-nutrition-diet-monitoring-1.0.0\CGMacros_dateshifted365\CGMacros")
# I am used to working on my university's OpenLab that I memorized how file directories are stored via Linux. 
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ROOT = (
    PROJECT_ROOT
    / "data"
    / "sample"
    / "cgmacros-scientific-dataset-nutrition-diet-monitoring-1.0.0"
    / "CGMacros_dateshifted365"
    / "CGMacros"
)
BIO_PATH = ROOT / "bio.csv"
PREPROCESS_PATH = PROJECT_ROOT / "data" / "preprocessed"

PARTICIPANTS = list(range(1, 46)) # All participants
# PARTICIPANTS = [2,5,6,8,10,12,14,15,16,23,26,29,31,33,35,38,39,42,43,45,46] #Match age range of 35-55
AGE_LO, AGE_HI = 35, 55

def to_numeric(s):
    return pd.to_numeric(s, errors="coerce")

# May not need
def time_in_range(g, lo=70, hi=180):
    g = g.dropna() # Remove null values
    if len(g) == 0:
        return np.nan
    return ((g >= lo) & (g <= hi)).mean()

def build_features_for_timeseries(ts, prefix):
    g = to_numeric(ts[f"{prefix} GL"])
    return {
        f"{prefix}_mean": g.mean(),
        f"{prefix}_median": g.median(),
        f"{prefix}_std": g.std(),
        f"{prefix}_min": g.min(),
        f"{prefix}_max": g.max(),
        f"{prefix}_range": g.max() - g.min(),
        f"{prefix}_tir_70_180": time_in_range(g, 70, 180),
        f"{prefix}_t_below_70": time_in_range(g, 0, 70),
        f"{prefix}_t_above_180": time_in_range(g, 180, 10000),
    }

def main():
    bio = pd.read_csv(BIO_PATH)

    # Keep lowercase naming convention
    bio = bio.rename(columns={
        "Gender": "gender"
    })

    bio["Age__num"] = to_numeric(bio["Age"])

    # cohort filter [ages 35-50]
    # Already added age
    bio = bio[(bio["Age__num"] >= AGE_LO) & (bio["Age__num"] <= AGE_HI)].copy()
    bio = bio[bio["subject"].isin(PARTICIPANTS)].copy()

    # Build map of data based on consistent file naming
    folder_id_map = {}
    for p in ROOT.iterdir():
        if p.is_dir() and p.name.startswith("CGMacros-"):
            try:
                sid = int(p.name.split("-")[-1])
                folder_id_map[sid] = p
            except:
                pass

    print("Found CGMacros folders:", len(folder_id_map))
    print("Folder ids example:", sorted(folder_id_map.keys())[:20])

    feature_rows = []

    for _, row in bio.iterrows(): # Literally iterate through rows
        sid = int(row["subject"])

        # ERROR: Folder not found circument
        if sid not in folder_id_map:
            print(f"No folder for subject {sid}")
            continue

        folder = folder_id_map[sid]
        expected = folder / f"{folder.name}.csv"
        if expected.exists():
            ts_path = expected
        else:
            csvs = list(folder.glob("*.csv"))
            if not csvs:
                print(f"No csv found for subject {sid}: {folder}")
                continue
            ts_path = csvs[0]

        ts = pd.read_csv(ts_path)

        # Sort by timestamp
        if "Timestamp" in ts.columns:
            ts["Timestamp"] = pd.to_datetime(ts["Timestamp"], errors="coerce")
            ts = ts.sort_values("Timestamp")

        feats = {}

        # Data was separated by Libre vs Dexcom sensors
        if "Libre GL" in ts.columns:
            feats.update(build_features_for_timeseries(ts, "Libre"))
        if "Dexcom GL" in ts.columns:
            feats.update(build_features_for_timeseries(ts, "Dexcom"))

        feats["subject"] = sid
        feats["age"] = float(row["Age__num"])
        feats["gender"] = row["gender"]

        feature_rows.append(feats)

    feat_df = pd.DataFrame(feature_rows)
    out = PREPROCESS_PATH / "cgmacros-time-series-res.csv"
    feat_df.to_csv(out, index=False)
    print(f"Saved: {out}  shape={feat_df.shape}")

if __name__ == "__main__":
    main()
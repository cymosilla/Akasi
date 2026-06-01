import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "UTM-1-3Campaign"
    / "cardiovascular"
    / "BRSMCF_Campaign_1_Echocardiography"
)

CF_AVG_FILE = RAW_DATA_PATH / "BRSMCF_Campaign_1_Echocardiography_CF_Avg.csv"

PRIMARY_METRICS = {
    "LVM": {"name": "Left Ventricular Mass", "unit": "g"},
    "SV pre": {"name": "Stroke Volume", "unit": "mL"},
    "CO pre": {"name": "Cardiac Output", "unit": "L/min"},
    "LV vol": {"name": "Left Ventricular Volume", "unit": "mL"},
    "EF pre": {"name": "Ejection Fraction", "unit": "%"},
    "LVDD": {"name": "Left Ventricular Diameter (Diastole)", "unit": "cm"},
}


def load_cf_avg():
    df = pd.read_csv(CF_AVG_FILE)

    # basic cleaning
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Recorded_Value"] = pd.to_numeric(df["Recorded_Value"], errors="coerce")
    return df


def get_PRIMARYl():
    # Remove later? Was for debugging
    labels = {}
    for code, meta in PRIMARY_METRICS.items():
        labels[code] = f"{meta['name']} ({meta['unit']})"
    return labels


def filter_metric(df: pd.DataFrame, metric_code: str) -> pd.DataFrame:
    # filter and sort so later code works
    x = df[df["Test"] == metric_code].copy()
    x = x.sort_values(["Subject", "BR_Day"])
    return x


def long_sum(metric_df: pd.DataFrame) -> pd.DataFrame:
    out = []

    # group by subject and compute baseline/final/min/max
    for subject, group in metric_df.groupby("Subject"):
        group = group.sort_values("BR_Day")

        baseline = group.iloc[0]["Recorded_Value"]
        final = group.iloc[-1]["Recorded_Value"]

        # % change
        if baseline != 0:
            pct_change = ((final - baseline) / baseline) * 100
            pct_change = round(pct_change, 2)
        else:
            pct_change = None

        out.append(
            {
                "Subject": subject,
                "Baseline": round(baseline, 2),
                "Final": round(final, 2),
                "% Change": pct_change,
                "Min": round(group["Recorded_Value"].min(), 2),
                "Max": round(group["Recorded_Value"].max(), 2),
            }
        )

    return pd.DataFrame(out)
import pandas as pd
import numpy as np
from pathlib import Path
import sklearn
from sklearn.linear_model import BayesianRidge
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "UTM-1-3Campaign"
    / "cardiovascular"
    / "BRSMCF_Campaign_1_Echocardiography"
)

CF_AVG_FILE = (
    RAW_DATA_PATH
    / "BRSMCF_Campaign_1_Echocardiography_CF_Avg.csv"
)

PRIMARY_METRICS = {
    "LVM": {"name": "Left Ventricular Mass","unit": "g",},
    "SV pre": {"name": "Stroke Volume","unit": "mL",},
    "CO pre": {"name": "Cardiac Output","unit": "L/min",},
    "LV vol": {"name": "Left Ventricular Volume","unit": "mL",},
    "EF pre": {"name": "Ejection Fraction","unit": "%",},
    "LVDD": {"name": "Left Ventricular Diameter (Diastole)","unit": "cm",},
}

# Should've had a helper file
def load_cf_avg():

    df = pd.read_csv(CF_AVG_FILE)
    df["Date"] = pd.to_datetime(df["Date"],errors="coerce",)
    df["Recorded_Value"] = pd.to_numeric(df["Recorded_Value"],errors="coerce",)
    return df


def fit_bayesian_metric(
    metric_code: str,
):

    df = load_cf_avg()

    metric_df = df[df["Test"] == metric_code].copy().dropna(subset=["BR_Day","Recorded_Value",])

    X = metric_df[["BR_Day"]].values

    y = metric_df["Recorded_Value"].values

    model = BayesianRidge()
   
    # Dev error by 3, due to accidental deletion of data. Reverted 
    # print("metric:", metric_code)
    # print("rows:", len(metric_df))
    # print("X shape:", X.shape)
    # print("y shape:", y.shape)

    # print("X sample:")
    # print(X[:5])

    # print("y sample:")
    # print(y[:5])

    model.fit(X, y)
    y_pred, y_std = model.predict(X,return_std=True)
    metric_df["Prediction"] = y_pred
    metric_df["Lower_95"] = y_pred - 1.96 * y_std
    metric_df["Upper_95"] = y_pred + 1.96 * y_std

    return 0
from pathlib import Path
import pandas as pd

ROOT = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "raw"
    / "PhysioNet"
    / "cgmacros-scientific-dataset-nutrition-diet-monitoring-1.0.0"
    / "cgmacros-scientific-dataset-nutrition-diet-monitoring-1.0.0"
    / "CGMacros_dateshifted365"
    / "CGMacros"
)
# Filtration start
def get_subjects(age_range = None, genders=None,):
    bio = pd.read_csv(ROOT / "bio.csv")
    if age_range is not None:
        bio = bio[
            bio["Age"].between(age_range[0],age_range[1])]
        
    if genders:
            bio = bio[bio["Gender"].isin(genders)]

    return sorted(bio["subject"].astype(int).tolist())

# def load_bio():

# For every individual in the study, there will be a graph
def load_subject(subject: int) -> pd.DataFrame:
    folder = ROOT / f"CGMacros-{subject:03d}"
    csv_path = folder / f"CGMacros-{subject:03d}.csv"

    # Remove Unnamed: 0 & Image path for graphs
    # Unnamed:0 is only in the first CGMacros
    df = pd.read_csv(csv_path)
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])
    if "Image path" in df.columns:
        df = df.drop(columns=["Image path"])

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df.sort_values("Timestamp").reset_index(drop=True)

# Meals-only
def extract_meals(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df[df["Meal Type"].notna()]
        .copy()
        .sort_values("Timestamp")
    )

# From start to end, for Streamlit's slider system
def date_filter(df: pd.DataFrame, start_date, end_date,):
    mask = (df["Timestamp"].dt.date >= start_date) & (df["Timestamp"].dt.date <= end_date)
    return df.loc[mask].copy()

# def prepare_timeseries_data(subject: int) -> dict: # Dictionary may not work for timestamps
def prepare_timeseries_data(subject: int, start_date=None, end_date=None):
    df = load_subject(subject)
    if (start_date is not None and end_date is not None):
        df = date_filter(df,start_date, end_date,)
    meals = extract_meals(df)
    return {
        "glucose": df[["Timestamp", "Libre GL", "Dexcom GL"]].copy(),
        "heart_rate": df[["Timestamp", "HR"]].copy(),
        "activity": df[["Timestamp", "METs", "Calories (Activity)"]].copy(),
        "meals": meals[
            [
                "Timestamp",
                "Meal Type",
                "Calories",
                "Carbs",
                "Protein",
                "Fat",
                "Fiber",
            ]
        ].copy(),

        "heart_rate": df[["Timestamp","HR",]].copy(),
        "activity": df[["Timestamp","METs", "Calories (Activity)",]].copy(),

        "meals": meals[
            [
                "Timestamp",
                "Meal Type",
                "Calories",
                "Carbs",
                "Protein",
                "Fat",
                "Fiber",
            ]
        ].copy(),
    }
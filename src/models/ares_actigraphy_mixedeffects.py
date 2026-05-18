"""
ARES Bed Rest Study
Actigraphy Mixed Effects Model

(From readme)
Parameter	Units	Range
Sleep latency	HH:mm	No Range
Sleep duration	HH:mm	No Range
Sleep efficiency	%	(0 to 100)
Comments		No Units	No Range

Outcome:
    Sleep Efficiency (%)

Fixed Effects:
    BR_Day
    Test_Phase

Random Effect:
    Subject

Question to answer: Sleep efficiency, what's eaffected by it?
"""

from pathlib import Path

import pandas as pd
# import seaborn as sns # GLMM https://github.com/junpenglao/GLMM-in-Python/blob/master/Playground.py 
import statsmodels.formula.api as smf # Extension to scipy
# Documentation: https://www.statsmodels.org/stable/example_formulas.html

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "UTM-1-3Campaign"
    / "BRSMACT_Campaign_1_Actigraphy"
    / "BRSMACT_Campaign_1_Actigraphy"
)

MAIN_FILE = ( DATA_DIR / "BRSMACT_Campagin_1_Actigraphy.csv" )

QUERY_FILE = ( DATA_DIR / "BRSMACT_Campagin_1_Actigraphy_Query_Result.csv" )

ANALYSIS_DIR = (PROJECT_ROOT / "data" / "analyzed")

# Some of this code was templated from an earlier project I did for preprocessing.

def parse_sleep_time(x):
    # Conversion of time
    if pd.isna(x): # Some cells are empty for comments
        return None

    s = str(x).strip() # Strip of zero values

    if not s:
        return None
    # Track hrs/mins
    if ":" in s:
        hrs, mins = s.split(":")
        return int(hrs) + int(mins) / 60 
    return float(s)

# This dataset was created in 2002, but due to an error, it was marked as 2004 (according to the readme).
def force_year_2002(series):
    dates = pd.to_datetime(series, errors="coerce")
    mask = dates.notna()
    dates.loc[mask] = (
        dates.loc[mask]
        .apply(
            lambda d: d.replace(year=2002)
        )
    )
    return dates

def load_data():
    frames = []
    for file in (MAIN_FILE, QUERY_FILE):
        df = pd.read_csv(file)
        df["source_file"] = file.name
        frames.append(df)
        # return pd.concat(frames, ignore_index=True)
    # XXX: Comment this out for later, shows rows of data
    # print(
    #     f"Loaded rows: {len(df)}"
    # )
    return df

def clean_data(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    # print("\nColumns:") # XXX: Remove before submission
    # print(df.columns.tolist())
    df["Date"] = force_year_2002(df["Date"])
    df["sleep_latency_hr"] = df["Sleep_latency"].apply(parse_sleep_time)
    df["sleep_duration_hr"] = df["Sleep_duration"].apply(parse_sleep_time)
    df["sleep_efficiency"] = pd.to_numeric(df["Sleep_efficiency"], errors="coerce")
    df["BR_Day"] = pd.to_numeric(df["BR_Day"], errors="coerce")
    df["Test_Phase"] = df["Test_Phase"].astype("category")
    # Under comments, every row has a chance of having some sort of medicine.
    comments = df["Comments"].fillna("").astype(str)
    # Concentration
    df["ambien"] = comments.str.contains("ambien", case=False, na=False).astype(int)
    # Drowsiness,
    df["diphenhydramine"] = comments.str.contains("diphenhydramine", case=False, na=False).astype(int)
    df["any_sleep_med"] = ((df["ambien"] == 1) | ( df["diphenhydramine"] == 1)).astype(int)
    return df

def fit_sleep_efficiency_model(df):
    model_df = df.dropna(
        subset=["sleep_efficiency", "BR_Day", "Subject",]
    )
    model = smf.mixedlm(
        formula=(
            "sleep_efficiency "
            "~ BR_Day "
            "+ Test_Phase "
            "+ any_sleep_med"
        ),
        data=model_df,
        groups=model_df["Subject"]
    )
    results = model.fit(
        method="lbfgs"
    )
    return results

def main():
    df = load_data()
    df = clean_data(df)

    print("\nSubjects:")
    print(df["Subject"].value_counts())
    results = fit_sleep_efficiency_model(df)
    coef_table = pd.DataFrame(
        {
            "coefficient": results.params,
            "std_error": results.bse,
            "z_value": results.tvalues,
            "p_value": results.pvalues,
            "ci_lower": results.conf_int()[0],
            "ci_upper": results.conf_int()[1],
        }
    )
    coef_table.index.name = "term"
    output_file = (ANALYSIS_DIR / "ares-actigraphy-mixedeffects.csv" )
    coef_table.to_csv(output_file)
    print(f"Saved: {output_file}")

    # print("/n" + results.summary())

if __name__ == "__main__":
    main()
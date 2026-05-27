import pandas as pd
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "UTM-1-3Campaign"
    / "immunity"
    / "BRSMIMMUNE_CFT70"
)

def test():
    df = pd.read_csv(RAW_DATA_PATH / "BRSMIMMUNE_CFT70_avgs_All.csv")
    # print(df.columns.tolist())
    # for c in df.columns:
    #     print(c, df[c].nunique()) 
    # df.head(20)
    print(df.groupby(
    ["GroupLabel", "Statistic", "Test_Phase", "BR_Day", "Unit"]).size().value_counts())

test()
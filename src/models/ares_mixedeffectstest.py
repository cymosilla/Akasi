from pathlib import Path
import re
import pandas as pd
import numpy as np

# According to the readme file, this study was done in 2002, but the files are in 2004 due to a rounding error by their system.
def shift_to_2002(date_series):
    dt = pd.to_datetime(date_series, errors="coerce")  # parses m/d/yyyy
    # subtract exactly 2 years
    return dt - pd.DateOffset(years=2)

# df["Date"] = shift_to_2002(df["Date"])


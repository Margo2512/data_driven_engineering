import numpy as np
import pandas as pd


def transform_data_types(df: pd.DataFrame) -> pd.DataFrame:
    df["education"] = df["education"].round().astype("Int64").astype("category")
    df["sex"] = df["sex"].astype("category")
    df["is_smoking"] = np.where(df["is_smoking"] == "YES", True, False)
    df["cigsPerDay"] = df["cigsPerDay"].astype("Int64")
    df["BPMeds"] = df["BPMeds"].astype("Int64")
    df["totChol"] = df["totChol"].astype("Int64")
    df["heartRate"] = df["heartRate"].astype("Int64")
    df["glucose"] = df["glucose"].astype("Int64")
    df["TenYearCHD"] = np.where(df["TenYearCHD"] == 1, True, False)

    return df

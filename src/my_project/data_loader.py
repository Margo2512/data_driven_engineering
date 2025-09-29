import pandas as pd
import numpy as np

FILE_ID = "1ZAaB3w-ssykhQXt8ikc9w4RM3seucxpQ"
file_url = f"https://drive.google.com/uc?id={FILE_ID}"
raw_data = pd.read_csv(file_url)
print(raw_data.head(10))
print(raw_data.dtypes)
# print(raw_data.info())

raw_data["education"] = raw_data["education"].round().astype("Int64").astype("category")
# raw_data['education'] = raw_data['education'].apply(lambda x: np.round(x)).astype('Int64').astype('category')
raw_data["sex"] = raw_data["sex"].astype("category")
raw_data["is_smoking"] = np.where(raw_data["is_smoking"] == "YES", True, False)
raw_data["cigsPerDay"] = raw_data["cigsPerDay"].astype("Int64")
raw_data["BPMeds"] = raw_data["BPMeds"].astype("Int64")
raw_data["totChol"] = raw_data["totChol"].astype("Int64")
raw_data["heartRate"] = raw_data["heartRate"].astype("Int64")
raw_data["glucose"] = raw_data["glucose"].astype("Int64")
raw_data["TenYearCHD"] = np.where(raw_data["TenYearCHD"] == 1, True, False)

print(raw_data.head(5))
print(raw_data.dtypes)
raw_data.to_csv("df.csv")

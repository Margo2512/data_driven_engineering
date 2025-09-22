import pandas as pd

FILE_ID = "1ZAaB3w-ssykhQXt8ikc9w4RM3seucxpQ"
file_url = f"https://drive.google.com/uc?id={FILE_ID}"
raw_data = pd.read_csv(file_url)
print(raw_data.head(10))

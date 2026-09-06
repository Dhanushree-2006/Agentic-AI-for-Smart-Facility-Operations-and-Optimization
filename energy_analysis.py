import pandas as pd

# Load the energy dataset
data = pd.read_csv("data/energydata_complete.csv")

# Show basic information
print("Dataset loaded successfully!")
print("Number of rows:", len(data))
print("Number of columns:", len(data.columns))

# Show column names
print("\nColumns:")
print(data.columns.tolist())

# Show first 5 records
print("\nFirst 5 records:")
print(data.head())
import pandas as pd

INPUT_FILE = "data/Facility Management Unified Classification Database (FMUCD).csv"
OUTPUT_FILE = "data/cost_data.csv"

print("Preparing Cost Dataset...")
print("==========================")

chunksize = 100000
first_chunk = True
cost_id = 1
total_rows = 0

for chunk in pd.read_csv(INPUT_FILE, chunksize=chunksize):

    # Keep records with required information
    chunk = chunk[
        chunk["WOID"].notna()
        & chunk["TotalCost"].notna()
        & chunk["WOStartDate"].notna()
    ].copy()

    # Convert cost to numeric
    chunk["TotalCost"] = pd.to_numeric(
        chunk["TotalCost"],
        errors="coerce"
    )

    # Keep only actual positive costs
    chunk = chunk[chunk["TotalCost"] > 0]

    # Create project-ready cost dataset
    cost_data = pd.DataFrame()

    cost_data["cost_id"] = range(
        cost_id,
        cost_id + len(chunk)
    )

    cost_data["report_id"] = chunk["WOID"].astype(str)

    cost_data["category"] = (
        chunk["SystemDescription"]
        .fillna("Other")
        .astype(str)
    )

    cost_data["amount"] = chunk["TotalCost"]

    cost_data["report_date"] = pd.to_datetime(
        chunk["WOStartDate"],
        errors="coerce"
    ).dt.date

    cost_data = cost_data.dropna(
        subset=["amount", "report_date"]
    )

    # Save the processed records
    cost_data.to_csv(
        OUTPUT_FILE,
        mode="w" if first_chunk else "a",
        header=first_chunk,
        index=False
    )

    total_rows += len(cost_data)
    cost_id += len(cost_data)
    first_chunk = False

    print(f"Processed {total_rows:,} positive-cost records...")

print("\nCost dataset created successfully!")
print(f"Total positive cost records: {total_rows:,}")
print(f"Output file: {OUTPUT_FILE}")
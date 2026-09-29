import pandas as pd

rooms = {
    "Room 1": "data/combined_Room1.csv",
    "Room 2": "data/combined_Room2.csv",
    "Room 3": "data/combined_Room3.csv",
    "Room 4": "data/combined_Room4.csv",
    "Room 5": "data/combined_Room5.csv"
}

results = []

print("FACILITY OCCUPANCY AGENT")
print("========================")

for room_name, file_path in rooms.items():

    df = pd.read_csv(file_path)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    total_records = len(df)

    present_records = (df["occupant_presence"] == 1).sum()

    occupancy_rate = (present_records / total_records) * 100

    average_occupants = df["occupant_count"].mean()

    maximum_occupants = df["occupant_count"].max()

    results.append({
        "Room": room_name,
        "Records": total_records,
        "Average Occupants": round(average_occupants, 2),
        "Maximum Occupants": int(maximum_occupants),
        "Occupancy Rate (%)": round(occupancy_rate, 2)
    })

occupancy_summary = pd.DataFrame(results)
def classify_utilization(rate):
    
    if rate < 30:
        return "Under-utilized"
    elif rate <= 70:
        return "Moderately utilized"
    else:
        return "Highly utilized"


occupancy_summary["Utilization Status"] = occupancy_summary[
    "Occupancy Rate (%)"
].apply(classify_utilization)
def detect_occupancy_level(rate):
    if rate > 100:
        return "Potential Overcrowding"
    elif rate >= 70:
        return "High Occupancy"
    else:
        return "Normal"


occupancy_summary["Occupancy Alert"] = occupancy_summary[
    "Occupancy Rate (%)"
].apply(detect_occupancy_level)
print("\nAI OCCUPANCY INSIGHTS")
print("====================")

for _, row in occupancy_summary.iterrows():

    if row["Utilization Status"] == "Under-utilized":
        print(
            f"{row['Room']}: Under-utilized. "
            f"Consider optimizing space usage or reallocating activities."
        )

    elif row["Occupancy Alert"] == "High Occupancy":
        print(
            f"{row['Room']}: High occupancy detected. "
            f"Consider monitoring capacity and space availability."
        )

    elif row["Occupancy Alert"] == "Potential Overcrowding":
        print(
            f"{row['Room']}: Potential overcrowding detected. "
            f"Immediate capacity monitoring is recommended."
        )

    else:
        print(
            f"{row['Room']}: Occupancy is within the normal utilization range."
        )

print("\nROOM-WISE OCCUPANCY")
print(occupancy_summary.to_string(index=False))

print("\nOccupancy Agent completed successfully.")
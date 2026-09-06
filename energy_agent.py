import pandas as pd

# Load dataset
data = pd.read_csv("data/energydata_complete.csv")

# Convert timestamp
data["date"] = pd.to_datetime(data["date"])

# Rename important columns for our Energy Agent
energy_data = data.rename(columns={
    "date": "timestamp",
    "Appliances": "electricity_kwh",
    "lights": "lighting_power_kwh",
    "T1": "temperature",
    "T_out": "outside_temperature"
})

# Add prototype facility information
energy_data["building_id"] = "Building_A"
energy_data["floor"] = 1

# Display selected data
print("\nENERGY AGENT DATA")
print("-" * 50)

print(energy_data[
    [
        "timestamp",
        "building_id",
        "floor",
        "electricity_kwh",
        "lighting_power_kwh",
        "temperature",
        "outside_temperature"
    ]
].head(10))


# Basic energy analysis
print("\nENERGY ANALYSIS")
print("-" * 50)

print("Average electricity consumption:",
      round(energy_data["electricity_kwh"].mean(), 2))

print("Maximum electricity consumption:",
      energy_data["electricity_kwh"].max())

print("Average lighting consumption:",
      round(energy_data["lighting_power_kwh"].mean(), 2))

print("Average indoor temperature:",
      round(energy_data["temperature"].mean(), 2))

print("Average outside temperature:",
      round(energy_data["outside_temperature"].mean(), 2))


# Detect high energy consumption
threshold = energy_data["electricity_kwh"].quantile(0.90)

high_energy = energy_data[
    energy_data["electricity_kwh"] > threshold
]

print("\nHIGH ENERGY EVENTS")
print("-" * 50)

print("High-energy threshold:", round(threshold, 2))
print("Number of high-energy events:", len(high_energy))

print("\nEnergy Agent Recommendation:")

if len(high_energy) > 0:
    print("⚠️ High energy consumption detected.")
    print("Recommendation: Investigate lighting, HVAC and equipment usage during peak periods.")
else:
    print("✅ No abnormal energy consumption detected.")
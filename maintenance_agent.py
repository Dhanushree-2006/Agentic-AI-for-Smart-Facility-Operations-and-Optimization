import pandas as pd
data = pd.read_csv("data/maintenance_data.csv")
data["timestamp"] = pd.to_datetime(data["timestamp"])


# MAINTENANCE AGENT

print("\n🔧 MAINTENANCE AGENT")
print("-" * 50)

print("Dataset loaded successfully!")
print("Total records:", len(data))
print("Total machines:", data["machine_id"].nunique())


# 1. EQUIPMENT HEALTH MONITORING

print("\n🏭 EQUIPMENT HEALTH MONITORING")
print("-" * 50)

avg_vibration = data["vibration_rms"].mean()
avg_temperature = data["temperature_motor"].mean()

print("Average vibration:", round(avg_vibration, 2))
print("Average motor temperature:", round(avg_temperature, 2))



# 2. MAINTENANCE PREDICTION


print("\n🔮 MAINTENANCE PREDICTION")
print("-" * 50)

high_risk = data[
    (data["rul_hours"] < 24) |
    (data["failure_within_24h"] == 1)
]

print("Machines requiring attention:", len(high_risk))


# 3. ABNORMAL BEHAVIOR DETECTION


print("\n⚠️ ABNORMAL BEHAVIOR DETECTION")
print("-" * 50)

vibration_threshold = data["vibration_rms"].quantile(0.90)
temperature_threshold = data["temperature_motor"].quantile(0.90)

abnormal = data[
    (data["vibration_rms"] > vibration_threshold) |
    (data["temperature_motor"] > temperature_threshold)
]

print("High vibration threshold:", round(vibration_threshold, 2))
print("High temperature threshold:", round(temperature_threshold, 2))
print("Abnormal equipment records:", len(abnormal))


# 4. ASSET LIFECYCLE MONITORING


print("\n🔄 ASSET LIFECYCLE")
print("-" * 50)

lifecycle = data.groupby("machine_id")["hours_since_maintenance"].max()

print("Machines monitored:", len(lifecycle))
print("Maximum hours since maintenance:",
      round(lifecycle.max(), 2))

# 5. WORK ORDER GENERATION


print("\n📋 MAINTENANCE WORK ORDERS")
print("-" * 50)

if len(high_risk) > 0:

    machine = high_risk.iloc[0]

    print("Machine:", machine["machine_id"])
    print("Machine Type:", machine["machine_type"])
    print("Priority: HIGH")
    print("Action: Schedule preventive maintenance")
    print("Reason: Low remaining useful life or failure risk")

else:

    print("No urgent maintenance work orders required.")


# 6. DOWNTIME REDUCTION


print("\n⏱️ DOWNTIME REDUCTION")
print("-" * 50)

if len(high_risk) > 0:

    print("⚠️ Preventive maintenance recommended.")
    print("Early maintenance can reduce the risk of unexpected equipment downtime.")

else:

    print("✅ Equipment risk is currently low.")


# -----------------------------
# AGENT SUMMARY
# -----------------------------

print("\n🤖 MAINTENANCE AGENT SUMMARY")
print("-" * 50)

print("Observe → Analyze → Predict → Recommend")

print("\nMaintenance Agent completed successfully.")
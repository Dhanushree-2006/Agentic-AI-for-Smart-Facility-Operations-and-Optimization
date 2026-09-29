import pandas as pd

# LOAD SECURITY DATA

DATA_PATH = "data/insider_threat_clean_dataset.csv"

df = pd.read_csv(DATA_PATH)

print("SECURITY INTELLIGENCE AGENT")
print("===========================")

print(f"\nTotal Security Activities: {len(df):,}")

# SECURITY ACTIVITY ANALYSIS


malicious_count = (
    df["is_malicious"] == 1
).sum()

normal_count = (
    df["is_malicious"] == 0
).sum()

late_exit_count = (
    df["late_exit_flag"] == 1
).sum()

weekend_entry_count = (
    df["entry_during_weekend"] == 1
).sum()

total_entries = df["num_entries"].sum()


print("\nSECURITY SUMMARY")
print("----------------")

print(f"Normal Activities       : {normal_count:,}")
print(f"Malicious Activities    : {malicious_count:,}")
print(f"Late Exit Activities    : {late_exit_count:,}")
print(f"Weekend Entry Activities: {weekend_entry_count:,}")
print(f"Total Entries           : {total_entries:,}")


# MALICIOUS ACTIVITY RATE


malicious_rate = (
    malicious_count / len(df)
) * 100

print(
    f"\nMalicious Activity Rate : "
    f"{malicious_rate:.2f}%"
)


# CAMPUS SECURITY ANALYSIS

campus_analysis = (
    df.groupby("employee_campus")
    .agg(
        Total_Activities=("is_malicious", "count"),
        Malicious_Activities=("is_malicious", "sum"),
        Total_Entries=("num_entries", "sum")
    )
    .reset_index()
)

campus_analysis["Malicious_Rate"] = (
    campus_analysis["Malicious_Activities"]
    / campus_analysis["Total_Activities"]
) * 100


print("\nCAMPUS SECURITY ANALYSIS")
print("------------------------")

print(
    campus_analysis.to_string(index=False)
)


# DEPARTMENT SECURITY ANALYSIS


department_analysis = (
    df.groupby("employee_department")
    .agg(
        Total_Activities=("is_malicious", "count"),
        Malicious_Activities=("is_malicious", "sum"),
        Total_Entries=("num_entries", "sum")
    )
    .reset_index()
)

department_analysis["Malicious_Rate"] = (
    department_analysis["Malicious_Activities"]
    / department_analysis["Total_Activities"]
) * 100


# LATE EXIT ANALYSIS


late_exit_rate = (
    late_exit_count / len(df)
) * 100


# WEEKEND ACCESS ANALYSIS


weekend_entry_rate = (
    weekend_entry_count / len(df)
) * 100


# SECURITY RISK DETECTION


print("\nSECURITY RISK DETECTION")
print("-----------------------")

if malicious_rate > 5:

    print(
        "🔴 HIGH SECURITY RISK: "
        "Malicious activity rate is elevated."
    )

elif malicious_rate > 1:

    print(
        "🟠 MEDIUM SECURITY RISK: "
        "Suspicious activity requires monitoring."
    )

else:

    print(
        "🟢 LOW SECURITY RISK: "
        "Overall malicious activity is low."
    )


# AI SECURITY INSIGHTS


print("\nAI SECURITY INSIGHTS")
print("--------------------")

highest_risk_campus = campus_analysis.loc[
    campus_analysis["Malicious_Rate"].idxmax(),
    "employee_campus"
]

highest_risk_rate = campus_analysis[
    "Malicious_Rate"
].max()


print(
    f"Highest-risk campus: {highest_risk_campus} "
    f"({highest_risk_rate:.2f}% malicious activity)"
)


print(
    f"Late-exit activity represents "
    f"{late_exit_rate:.2f}% of monitored activities."
)


print(
    f"Weekend entry activity represents "
    f"{weekend_entry_rate:.2f}% of monitored activities."
)


# SECURITY RECOMMENDATIONS


print("\nAI SECURITY RECOMMENDATIONS")
print("---------------------------")

if malicious_count > 0:

    print(
        "1. Investigate employees associated with "
        "malicious activity."
    )

if late_exit_count > 0:

    print(
        "2. Monitor repeated late-exit behavior "
        "for security risks."
    )

if weekend_entry_count > 0:

    print(
        "3. Review unusual weekend access activity."
    )

print(
    "4. Continuously monitor campus and "
    "department-level security patterns."
)

print(
    "5. Trigger security alerts when "
    "high-risk behavior is detected."
)


print("\nSecurity Agent completed successfully.")
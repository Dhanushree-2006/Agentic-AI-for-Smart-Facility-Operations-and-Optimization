import streamlit as st
import pandas as pd
from auth import create_database, create_user, check_login

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="FacilityOps AI",
    page_icon="🏢",
    layout="wide"
)
create_database()

# -----------------------------
# LOGIN SYSTEM
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# -----------------------------
# LOGIN PAGE
# -----------------------------
if not st.session_state.logged_in:

    st.title("🏢 FacilityOps AI")
    st.subheader("🔐 Facility Operations Login")

    st.write("Login to access the Facility Intelligence Dashboard.")

    username = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin@facility.com" and password == "admin123":
            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("❌ Invalid email or password")


# -----------------------------
# DASHBOARD
# -----------------------------
else:

    # Load data
    data = pd.read_csv("data/energydata_complete.csv")
    data["date"] = pd.to_datetime(data["date"])

    # Rename columns
    data = data.rename(columns={
        "Appliances": "energy_consumption",
        "lights": "lighting_power",
        "T1": "temperature",
        "T_out": "outside_temperature"
    })

    # -----------------------------
    # SIDEBAR
    # -----------------------------
    st.sidebar.title("🏢 FacilityOps AI")
    st.sidebar.write("Facility Intelligence Platform")

    page = st.sidebar.radio(
    "Navigation",
    [
        "Energy Dashboard",
        "Energy Agent",
        "Maintenance Agent"
    ]
)
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # -----------------------------
    # ENERGY DASHBOARD
    # -----------------------------
    if page == "Energy Dashboard":

        st.title("⚡ Energy Intelligence Dashboard")
        st.caption("AI-powered facility energy monitoring")

        avg_energy = data["energy_consumption"].mean()
        max_energy = data["energy_consumption"].max()
        avg_temp = data["temperature"].mean()
        avg_lighting = data["lighting_power"].mean()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Average Energy",
            f"{avg_energy:.2f}"
        )

        col2.metric(
            "Peak Energy",
            f"{max_energy:.0f}"
        )

        col3.metric(
            "Avg Temperature",
            f"{avg_temp:.2f} °C"
        )

        col4.metric(
            "Lighting Usage",
            f"{avg_lighting:.2f}"
        )

        st.divider()

        st.subheader("📈 Energy Consumption")

        chart_data = data[
            ["date", "energy_consumption"]
        ].set_index("date").head(500)

        st.line_chart(chart_data)

        st.subheader("🌡️ Temperature Monitoring")

        temperature_data = data[
            ["date", "temperature", "outside_temperature"]
        ].set_index("date").head(500)

        st.line_chart(temperature_data)

    # -----------------------------
    # ENERGY AGENT
    # -----------------------------
    elif page == "Energy Agent":

        st.title("🤖 Energy Agent")

        st.write(
            "The Energy Agent analyzes facility energy consumption "
            "and identifies abnormal usage patterns."
        )

        threshold = data["energy_consumption"].quantile(0.90)

        high_energy = data[
            data["energy_consumption"] > threshold
        ]

        st.subheader("🔍 Energy Analysis")

        col1, col2 = st.columns(2)

        col1.metric(
            "High Energy Threshold",
            f"{threshold:.2f}"
        )

        col2.metric(
            "High Energy Events",
            len(high_energy)
        )

        st.divider()

        st.subheader("⚠️ AI Recommendation")

        if len(high_energy) > 0:

            st.warning(
                "High energy consumption detected."
            )

            st.write(
                "💡 Recommendation: Investigate HVAC, "
                "lighting and equipment usage during peak "
                "energy periods."
            )

        else:

            st.success(
                "No abnormal energy consumption detected."
            )

        st.divider()

        st.subheader("📊 High Energy Events")

        st.dataframe(
            high_energy[
                [
                    "date",
                    "energy_consumption",
                    "lighting_power",
                    "temperature",
                    "outside_temperature"
                ]
            ].head(20),
            use_container_width=True
        )
    # MAINTENANCE AGENT
    elif page == "Maintenance Agent":

        st.title("🔧 Maintenance Intelligence")
        st.caption("AI-powered equipment health and predictive maintenance")

        # Load maintenance data
        maintenance_data = pd.read_csv(
            "data/maintenance_data.csv"
        )

        maintenance_data["timestamp"] = pd.to_datetime(
            maintenance_data["timestamp"]
        )

        
        # KEY METRICS
        

        total_machines = maintenance_data["machine_id"].nunique()

        critical_records = maintenance_data[
            (maintenance_data["rul_hours"] < 24) |
            (maintenance_data["failure_within_24h"] == 1)
        ]

        critical_machines = critical_records[
            "machine_id"
        ].nunique()

        healthy_machines = total_machines - critical_machines

        abnormal_records = maintenance_data[
            (maintenance_data["vibration_rms"] >
             maintenance_data["vibration_rms"].quantile(0.90)) |
            (maintenance_data["temperature_motor"] >
             maintenance_data["temperature_motor"].quantile(0.90))
        ]

        abnormal_machines = abnormal_records[
            "machine_id"
        ].nunique()

        
        # DISPLAY METRICS
        

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Equipment",
            total_machines
        )

        col2.metric(
            "Healthy Equipment",
            healthy_machines
        )

        col3.metric(
            "Critical Equipment",
            critical_machines
        )

        col4.metric(
            "Abnormal Equipment",
            abnormal_machines
        )

        st.divider()

        
        # EQUIPMENT HEALTH
    

        st.subheader("🏭 Equipment Health Monitoring")

        health_data = maintenance_data.groupby(
            "machine_id"
        ).agg(
            machine_type=("machine_type", "first"),
            vibration=("vibration_rms", "mean"),
            motor_temperature=("temperature_motor", "mean"),
            RUL_hours=("rul_hours", "min"),
            hours_since_maintenance=(
                "hours_since_maintenance",
                "max"
            )
        ).reset_index()

        health_data["status"] = health_data.apply(
            lambda row:
            "🔴 Critical"
            if row["RUL_hours"] < 24
            else "🟡 Monitoring"
            if row["RUL_hours"] < 72
            else "🟢 Healthy",
            axis=1
        )

        st.dataframe(
            health_data,
            use_container_width=True
        )

        st.divider()

        # -----------------------------
        # MAINTENANCE ANALYTICS CHARTS
        # -----------------------------

        st.subheader("📊 Maintenance Analytics")

        # Get the latest reading for each machine
        latest_data = (
            maintenance_data
            .sort_values("timestamp")
            .groupby("machine_id")
            .tail(1)
        )

        # RUL chart
        st.write("🔮 Remaining Useful Life by Machine")

        rul_chart = latest_data[
            ["machine_id", "rul_hours"]
        ].set_index("machine_id")

        st.bar_chart(rul_chart)

        # Vibration chart
        st.write("📳 Machine Vibration Levels")

        vibration_chart = latest_data[
            ["machine_id", "vibration_rms"]
        ].set_index("machine_id")

        st.bar_chart(vibration_chart)
        st.divider()

        
        # AI RECOMMENDATION
        

        st.subheader("🤖 AI Maintenance Recommendation")

        if critical_machines > 0:

            st.warning(
                f"⚠️ {critical_machines} equipment unit(s) "
                "require maintenance attention."
            )

            st.write(
                "💡 Recommendation: Schedule preventive "
                "maintenance for equipment with low RUL "
                "or predicted failure within 24 hours."
            )

        else:

            st.success(
                "✅ No critical equipment detected."
            )

        st.divider()

        
        # WORK ORDERS
        

        st.subheader("📋 Maintenance Work Orders")

        work_orders = health_data[
            health_data["status"] == "🔴 Critical"
        ].copy()

        if len(work_orders) > 0:

            work_orders["Priority"] = "HIGH"
            work_orders["Action"] = (
                "Schedule Preventive Maintenance"
            )

            st.dataframe(
                work_orders[
                    [
                        "machine_id",
                        "machine_type",
                        "RUL_hours",
                        "Priority",
                        "Action"
                    ]
                ],
                use_container_width=True
            )

        else:

            st.success(
                "No urgent work orders required."
            )

        st.divider()

        
        # DOWNTIME REDUCTION
        

        st.subheader("⏱️ Downtime Risk Reduction")

        st.info(
            "The Maintenance Agent identifies equipment "
            "with high failure risk and recommends preventive "
            "maintenance to reduce the possibility of "
            "unexpected downtime."
        )
    
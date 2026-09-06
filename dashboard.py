import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="FacilityOps AI",
    page_icon="🏢",
    layout="wide"
)

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
        ["Energy Dashboard", "Energy Agent"]
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
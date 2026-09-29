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
        "Maintenance Agent",
        "Occupancy Dashboard",
        "Security Dashboard",
        "Cost Optimization Dashboard"
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
    # OCCUPANCY DASHBOARD

    elif page == "Occupancy Dashboard":

        st.title("👥 Occupancy Intelligence Dashboard")
        st.caption(
            "AI-powered room occupancy and space utilization"
        )

        # Load occupancy datasets
        rooms = {
            "Room 1": "data/combined_Room1.csv",
            "Room 2": "data/combined_Room2.csv",
            "Room 3": "data/combined_Room3.csv",
            "Room 4": "data/combined_Room4.csv",
            "Room 5": "data/combined_Room5.csv"
        }
        

        occupancy_results = []

        for room_name, file_path in rooms.items():

            room_data = pd.read_csv(file_path)

            total_records = len(room_data)

            present_records = (
                room_data["occupant_presence"] == 1
            ).sum()

            occupancy_rate = (
                present_records / total_records
            ) * 100

            average_occupants = (
                room_data["occupant_count"].mean()
            )

            maximum_occupants = (
                room_data["occupant_count"].max()
            )

            if occupancy_rate < 30:
                utilization = "Under-utilized"
            elif occupancy_rate <= 70:
                utilization = "Moderately utilized"
            else:
                utilization = "Highly utilized"

            if occupancy_rate >= 70:
                alert = "High Occupancy"
            else:
                alert = "Normal"

            occupancy_results.append({
                "Room": room_name,
                "Average Occupants": round(
                    average_occupants, 2
                ),
                "Maximum Occupants": int(
                    maximum_occupants
                ),
                "Occupancy Rate": round(
                    occupancy_rate, 2
                ),
                "Utilization": utilization,
                "Alert": alert
            })

        occupancy_df = pd.DataFrame(
            occupancy_results
        )
               
        # KEY METRICS
        

        total_rooms = len(occupancy_df)

        average_occupancy = (
            occupancy_df["Average Occupants"].mean()
        )

        under_utilized = (
            occupancy_df["Utilization"] ==
            "Under-utilized"
        ).sum()

        high_occupancy = (
            occupancy_df["Alert"] ==
            "High Occupancy"
        ).sum()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "🏢 Total Rooms",
            total_rooms
        )

        col2.metric(
            "👥 Average Occupants",
            f"{average_occupancy:.2f}"
        )

        col3.metric(
            "🟠 Under-utilized Rooms",
            under_utilized
        )

        col4.metric(
            "🔴 High Occupancy Rooms",
            high_occupancy
        )

        st.divider()
                
        # ROOM-WISE OCCUPANCY GRAPH
        

        st.subheader("📊 Room-wise Occupancy Rate")

        occupancy_chart = occupancy_df[
            ["Room", "Occupancy Rate"]
        ].set_index("Room")

        st.bar_chart(
            occupancy_chart
        )

        st.divider()
            
        # AVERAGE OCCUPANTS GRAPH
        

        st.subheader("👥 Average Occupants by Room")

        average_chart = occupancy_df[
            ["Room", "Average Occupants"]
        ].set_index("Room")

        st.bar_chart(
            average_chart
        )

        st.divider()
               
        # UTILIZATION STATUS
        

        st.subheader("📊 Room Utilization Status")

        utilization_counts = (
            occupancy_df["Utilization"]
            .value_counts()
        )

        st.bar_chart(
            utilization_counts
        )

        st.divider()
                
        # AI OCCUPANCY INSIGHTS
        

        st.subheader("🤖 AI Occupancy Insights")

        for _, row in occupancy_df.iterrows():

            if row["Utilization"] == "Under-utilized":

                st.warning(
                    f"⚠️ {row['Room']} is under-utilized "
                    f"with {row['Occupancy Rate']:.2f}% occupancy. "
                    f"Consider optimizing space usage."
                )

            elif row["Alert"] == "High Occupancy":

                st.error(
                    f"🔴 {row['Room']} has high occupancy "
                    f"({row['Occupancy Rate']:.2f}%). "
                    f"Monitor space availability."
                )

            else:

                st.success(
                    f"🟢 {row['Room']} is operating within "
                    f"the normal utilization range."
                )

        st.divider()
                
        # OCCUPANCY TREND
       

        st.subheader("📈 Occupancy Trend - Room 1")

        room1_data = pd.read_csv(
            "data/combined_Room1.csv"
        )

        room1_data["timestamp"] = pd.to_datetime(
            room1_data["timestamp"]
        )

        trend_data = (
            room1_data[
                ["timestamp", "occupant_count"]
            ]
            .set_index("timestamp")
            .resample("1h")
            .mean()
        )

        st.line_chart(
            trend_data
        )

        st.divider()
            
        # CO2 VS OCCUPANCY
        

        st.subheader("🌫️ CO₂ vs Occupancy - Room 1")

        co2_occupancy = (
            room1_data[
                ["timestamp", "indoor_co2", "occupant_count"]
            ]
            .set_index("timestamp")
            .resample("1h")
            .mean()
        )

        st.line_chart(
            co2_occupancy
        )

        st.divider()
            
        # ROOM UTILIZATION COMPARISON
        

        st.subheader("🏢 Room Utilization Comparison")

        utilization_chart = occupancy_df[
            ["Room", "Occupancy Rate"]
        ].set_index("Room")

        st.bar_chart(
            utilization_chart
        )

        st.divider()
        
        # OCCUPANCY SUMMARY
        
        st.subheader("🧠 Occupancy Intelligence Summary")

        busiest_room = occupancy_df.loc[
            occupancy_df["Occupancy Rate"].idxmax(),
            "Room"
        ]

        least_used_room = occupancy_df.loc[
            occupancy_df["Occupancy Rate"].idxmin(),
            "Room"
        ]

        st.info(
            f"🏢 **Busiest Room:** {busiest_room}  \n"
            f"🟠 **Least Utilized Room:** {least_used_room}  \n"
            f"📊 **Rooms Monitored:** {total_rooms}  \n"
            f"👥 **Average Occupants:** {average_occupancy:.2f}"
        )

        st.divider()
        
        # PEAK OCCUPANCY
        

        st.subheader("🔴 Peak Occupancy by Room")

        peak_occupancy = occupancy_df[
            ["Room", "Maximum Occupants"]
        ].set_index("Room")

        st.bar_chart(
            peak_occupancy
        )

        st.divider()
            
        # HOURLY OCCUPANCY PATTERN
        

        st.subheader("🕒 Hourly Occupancy Pattern - Room 1")

        hourly_occupancy = (
            room1_data
            .assign(
                hour=room1_data["timestamp"].dt.hour
            )
            .groupby("hour")["occupant_count"]
            .mean()
        )

        st.line_chart(
            hourly_occupancy
        )

        st.divider()
            
        # AI RECOMMENDATIONS
        

        st.subheader("💡 AI Space Optimization Recommendations")

        for _, row in occupancy_df.iterrows():

            if row["Utilization"] == "Under-utilized":
                st.warning(
                    f"🟠 {row['Room']}: Consider reallocating activities "
                    f"or optimizing the available space."
                )

            elif row["Utilization"] == "Highly utilized":
                st.error(
                    f"🔴 {row['Room']}: High utilization detected. "
                    f"Monitor space availability and capacity."
                )

            else:
                st.success(
                    f"🟢 {row['Room']}: Space utilization is within "
                    f"the normal range."
                )

        st.divider()

        # ROOM-WISE DETAILS


        st.subheader("📋 Room-wise Occupancy Details")

        st.dataframe(
            occupancy_df,
            use_container_width=True
        )

        st.divider()
            
        # FINAL OCCUPANCY DASHBOARD SUMMARY
        


        st.subheader("📊 Facility Occupancy Overview")

        col1, col2 = st.columns(2)

        with col1:
            busiest_room = occupancy_df.loc[
                occupancy_df["Occupancy Rate"].idxmax(),
                "Room"
            ]

            busiest_rate = occupancy_df["Occupancy Rate"].max()

            st.metric(
                "🔴 Busiest Room",
                busiest_room,
                f"{busiest_rate:.2f}% occupancy"
            )

        with col2:
            least_used_room = occupancy_df.loc[
                occupancy_df["Occupancy Rate"].idxmin(),
                "Room"
            ]

            least_used_rate = occupancy_df["Occupancy Rate"].min()

            st.metric(
                "🟠 Least Utilized Room",
                least_used_room,
                f"{least_used_rate:.2f}% occupancy"
            )

        st.divider()

        
        
    # SECURITY DASHBOARD
    # ============================================================

    elif page == "Security Dashboard":

        st.title("🔐 Security Intelligence Dashboard")

        st.caption(
            "AI-powered security monitoring, risk detection and "
            "access intelligence"
        )

        security_data = pd.read_csv(
            "data/insider_threat_clean_dataset.csv"
        )

        # SECURITY CALCULATIONS

        total_activities = len(security_data)

        malicious_activities = (
            security_data["is_malicious"] == 1
        ).sum()

        normal_activities = (
            security_data["is_malicious"] == 0
        ).sum()

        malicious_rate = (
            malicious_activities / total_activities
        ) * 100

        total_entries = security_data[
            "num_entries"
        ].sum()

        weekend_entries = (
            security_data["entry_during_weekend"] == 1
        ).sum()

        late_exit = (
            security_data["late_exit_flag"] == 1
        ).sum()

        # SECURITY RISK

        if malicious_rate > 5:
            risk_level = "HIGH"
        elif malicious_rate > 1:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # KEY METRICS

        st.subheader("🛡️ Security Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "🔐 Security Activities",
            f"{total_activities:,}"
        )

        col2.metric(
            "🔴 Malicious Activities",
            f"{malicious_activities:,}"
        )

        col3.metric(
            "📊 Malicious Rate",
            f"{malicious_rate:.2f}%"
        )

        col4.metric(
            "🚨 Risk Level",
            risk_level
        )

        st.divider()

        # ACCESS METRICS

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "🚪 Total Entries",
            f"{total_entries:,}"
        )

        col2.metric(
            "🟠 Weekend Entries",
            f"{weekend_entries:,}"
        )

        col3.metric(
            "🌙 Late Exits",
            f"{late_exit:,}"
        )

        st.divider()

        # CAMPUS ANALYSIS

        st.subheader("🏢 Campus-wise Security Analysis")

        campus_analysis = (
            security_data
            .groupby("employee_campus")
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

        st.dataframe(
            campus_analysis,
            use_container_width=True
        )

        # CAMPUS MALICIOUS ACTIVITY

        st.subheader("🔴 Malicious Activity by Campus")

        campus_chart = campus_analysis[
            [
                "employee_campus",
                "Malicious_Activities"
            ]
        ].set_index("employee_campus")

        st.bar_chart(campus_chart)

        st.divider()

        # CAMPUS MALICIOUS RATE

        st.subheader("📊 Malicious Activity Rate by Campus")

        campus_rate_chart = campus_analysis[
            [
                "employee_campus",
                "Malicious_Rate"
            ]
        ].set_index("employee_campus")

        st.bar_chart(campus_rate_chart)

        st.divider()

        # DEPARTMENT ANALYSIS

        st.subheader("🏢 Department-wise Security Analysis")

        department_analysis = (
            security_data
            .groupby("employee_department")
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

        st.dataframe(
            department_analysis,
            use_container_width=True
        )

        st.subheader("🔴 Malicious Activities by Department")

        department_chart = department_analysis[
            [
                "employee_department",
                "Malicious_Activities"
            ]
        ].set_index("employee_department")

        st.bar_chart(department_chart)

        st.divider()

        # WEEKEND ACCESS

        st.subheader("📅 Weekend Access Monitoring")

        weekend_normal = (
            security_data["entry_during_weekend"] == 0
        ).sum()

        weekend_activity = (
            security_data["entry_during_weekend"] == 1
        ).sum()

        weekend_chart = pd.DataFrame(
            {
                "Activities": [
                    weekend_normal,
                    weekend_activity
                ]
            },
            index=[
                "Regular Access",
                "Weekend Access"
            ]
        )

        st.bar_chart(weekend_chart)

        st.divider()

        # NORMAL VS MALICIOUS

        st.subheader("🛡️ Normal vs Malicious Activities")

        activity_chart = pd.DataFrame(
            {
                "Activities": [
                    normal_activities,
                    malicious_activities
                ]
            },
            index=[
                "Normal",
                "Malicious"
            ]
        )

        st.bar_chart(activity_chart)

        st.divider()

        # SECURITY RISK

        st.subheader("🚨 Security Risk Assessment")

        if risk_level == "HIGH":

            st.error(
                f"🔴 HIGH SECURITY RISK\n\n"
                f"Malicious activity rate is "
                f"{malicious_rate:.2f}%."
            )

        elif risk_level == "MEDIUM":

            st.warning(
                f"🟠 MEDIUM SECURITY RISK\n\n"
                f"Malicious activity rate is "
                f"{malicious_rate:.2f}%."
            )

        else:

            st.success(
                f"🟢 LOW SECURITY RISK\n\n"
                f"Malicious activity rate is "
                f"{malicious_rate:.2f}%."
            )

        st.divider()

        # AI SECURITY INSIGHTS

        st.subheader("🤖 AI Security Insights")

        highest_risk_campus = campus_analysis.loc[
            campus_analysis["Malicious_Rate"].idxmax(),
            "employee_campus"
        ]

        highest_risk_rate = campus_analysis[
            "Malicious_Rate"
        ].max()

        st.info(
            f"🏢 **Highest-risk campus:** "
            f"{highest_risk_campus} "
            f"({highest_risk_rate:.2f}% malicious activity)"
        )

        st.info(
            f"🔴 **Malicious activities detected:** "
            f"{malicious_activities:,}"
        )

        st.info(
            f"📅 **Weekend access activities:** "
            f"{weekend_entries:,}"
        )

        st.info(
            f"🌙 **Late-exit activities:** "
            f"{late_exit:,}"
        )

        st.divider()

        # AI RECOMMENDATIONS

        st.subheader("💡 AI Security Recommendations")

        if malicious_activities > 0:

            st.warning(
                "🔴 Investigate employees associated "
                "with malicious activity."
            )

        if weekend_entries > 0:

            st.warning(
                "🟠 Review unusual weekend access activity "
                "for potential security risks."
            )

        if late_exit > 0:

            st.warning(
                "🌙 Monitor repeated late-exit behavior."
            )

        st.success(
            "🏢 Continuously monitor campus and "
            "department-level security patterns."
        )

        st.success(
            "🚨 Trigger security alerts when "
            "high-risk behavior is detected."
        )

        st.divider()

        # SECURITY DATA

        st.subheader("📋 Security Activity Data")

        st.dataframe(
            security_data.head(100),
            use_container_width=True
        )
            # ============================================================
    # COST OPTIMIZATION DASHBOARD
    # ============================================================

    elif page == "Cost Optimization Dashboard":

        st.title("💰 Cost Optimization Dashboard")

        st.caption(
            "AI-powered facility cost monitoring, analysis and optimization"
        )

        # --------------------------------------------------------
        # LOAD COST DATA
        # --------------------------------------------------------

        cost_data = pd.read_csv(
            "data/cost_data.csv"
        )

        cost_data["report_date"] = pd.to_datetime(
            cost_data["report_date"],
            errors="coerce"
        )

        cost_data["amount"] = pd.to_numeric(
            cost_data["amount"],
            errors="coerce"
        )

        cost_data = cost_data.dropna(
            subset=["amount", "report_date"]
        )

        # --------------------------------------------------------
        # KEY METRICS
        # --------------------------------------------------------

        total_cost = cost_data["amount"].sum()

        total_records = len(cost_data)

        average_cost = cost_data["amount"].mean()

        highest_cost = cost_data["amount"].max()

        category_analysis = (
            cost_data
            .groupby("category")
            .agg(
                Total_Cost=("amount", "sum"),
                Average_Cost=("amount", "mean"),
                Number_of_Records=("amount", "count")
            )
            .reset_index()
            .sort_values(
                "Total_Cost",
                ascending=False
            )
        )

        highest_cost_category = (
            category_analysis.iloc[0]["category"]
        )

        highest_category_cost = (
            category_analysis.iloc[0]["Total_Cost"]
        )

        cost_concentration = (
            highest_category_cost / total_cost
        ) * 100

                # --------------------------------------------------------
        # EXECUTIVE COST OVERVIEW
        # --------------------------------------------------------

        st.subheader("👔 Executive Cost Overview")

        st.caption(
            "Management-level summary of facility expenditure, "
            "cost concentration and optimization risk"
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "💰 Total Facility Cost",
            f"{total_cost:,.2f}"
        )

        col2.metric(
            "📋 Cost Records",
            f"{total_records:,}"
        )

        col3.metric(
            "💵 Average Work Order Cost",
            f"{average_cost:,.2f}"
        )

        col4.metric(
            "🏢 Highest Cost Category",
            highest_cost_category
        )

        st.divider()

        # --------------------------------------------------------
        # EXECUTIVE COST RISK
        # --------------------------------------------------------

        st.subheader("🚨 Executive Cost Risk")

        risk_col1, risk_col2, risk_col3 = st.columns(3)

        with risk_col1:
            st.metric(
                "Cost Concentration",
                f"{cost_concentration:.2f}%"
            )

        with risk_col2:

            if cost_concentration >= 40:
                risk_level = "HIGH"

            elif cost_concentration >= 20:
                risk_level = "MEDIUM"

            else:
                risk_level = "LOW"

            st.metric(
                "Cost Risk Level",
                risk_level
            )

        with risk_col3:
            st.metric(
                "Highest Category Cost",
                f"{highest_category_cost:,.2f}"
            )

        if cost_concentration >= 40:

            st.error(
                f"🔴 HIGH COST CONCENTRATION\n\n"
                f"{highest_cost_category} accounts for "
                f"{cost_concentration:.2f}% of total facility cost. "
                f"Management attention is recommended for this category."
            )

        elif cost_concentration >= 20:

            st.warning(
                f"🟠 MEDIUM COST CONCENTRATION\n\n"
                f"{highest_cost_category} accounts for "
                f"{cost_concentration:.2f}% of total facility cost. "
                f"The category should be monitored for optimization opportunities."
            )

        else:

            st.success(
                "🟢 LOW COST CONCENTRATION\n\n"
                "Facility costs are distributed across multiple categories."
            )

        st.divider()

        # --------------------------------------------------------
        # EXECUTIVE INSIGHT
        # --------------------------------------------------------

        st.subheader("🧠 Executive AI Insight")

        st.info(
            f"💰 **Facility expenditure:** "
            f"{total_cost:,.2f}\n\n"
            f"🏢 **Primary cost driver:** "
            f"{highest_cost_category}\n\n"
            f"📊 **Cost concentration:** "
            f"{cost_concentration:.2f}% of total expenditure\n\n"
            f"🎯 **Management focus:** "
            f"Review {highest_cost_category} expenses and identify "
            f"potential cost optimization opportunities."
        )

        st.divider()

        # --------------------------------------------------------
        # CATEGORY-WISE COST
        # --------------------------------------------------------

        # --------------------------------------------------------
        # CATEGORY-WISE COST
        # --------------------------------------------------------

        st.subheader("📊 Cost by Category")

        category_chart = (
            category_analysis[
                ["category", "Total_Cost"]
            ]
            .set_index("category")
        )

        st.bar_chart(
            category_chart
        )

        st.divider()

        # --------------------------------------------------------
        # MONTHLY COST TREND
        # --------------------------------------------------------

        st.subheader("📈 Monthly Facility Cost Trend")

        cost_data["month"] = (
            cost_data["report_date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_cost = (
            cost_data
            .groupby("month")["amount"]
            .sum()
            .reset_index()
        )

        monthly_cost = monthly_cost.sort_values(
            "month"
        )

        monthly_chart = (
            monthly_cost
            .set_index("month")
        )

        st.line_chart(
            monthly_chart
        )

        st.divider()

        # --------------------------------------------------------
        # CATEGORY ANALYSIS TABLE
        # --------------------------------------------------------

        st.subheader("📋 Category-wise Cost Analysis")

        st.dataframe(
            category_analysis,
            use_container_width=True
        )

        st.divider()

        # --------------------------------------------------------
        # COST CONCENTRATION
        # --------------------------------------------------------

        st.subheader("⚠️ Cost Concentration Analysis")

        st.metric(
            "Highest Cost Category",
            highest_cost_category,
            f"{cost_concentration:.2f}% of total cost"
        )

        if cost_concentration >= 40:

            st.error(
                "🔴 High cost concentration detected. "
                "A large portion of facility expenses is "
                "concentrated in one category."
            )

        elif cost_concentration >= 20:

            st.warning(
                "🟠 Medium cost concentration detected. "
                "The highest-cost category should be monitored "
                "for optimization opportunities."
            )

        else:

            st.success(
                "🟢 Facility costs are relatively distributed "
                "across categories."
            )

        st.divider()
                # --------------------------------------------------------
        # SAVINGS OPPORTUNITY ENGINE
        # --------------------------------------------------------

        st.subheader("💡 Savings Opportunity Engine")

        st.caption(
            "Estimated cost-saving opportunities based on "
            "historical cost concentration"
        )

        # Determine optimization rate
        if cost_concentration >= 40:
            savings_rate = 0.15
        elif cost_concentration >= 20:
            savings_rate = 0.10
        else:
            savings_rate = 0.05

        estimated_saving = (
            highest_category_cost * savings_rate
        )

        # Savings metrics
        saving_col1, saving_col2, saving_col3 = st.columns(3)

        with saving_col1:
            st.metric(
                "🎯 Optimization Rate",
                f"{savings_rate * 100:.0f}%"
            )

        with saving_col2:
            st.metric(
                "💰 Potential Saving",
                f"{estimated_saving:,.2f}"
            )

        with saving_col3:
            st.metric(
                "🏢 Target Category",
                highest_cost_category
            )

        st.info(
            f"💡 The system identified a potential optimization "
            f"opportunity of **{estimated_saving:,.2f}** in "
            f"**{highest_cost_category}**."
        )

        st.warning(
            "⚠️ This is an estimated optimization opportunity "
            "based on a rule-based assumption, not actual realized savings."
        )

        st.divider()

        # --------------------------------------------------------
        # AI COST INSIGHTS
        # --------------------------------------------------------

        st.subheader("🤖 AI Cost Optimization Insights")

        st.info(
            f"💰 Total facility cost analyzed: "
            f"{total_cost:,.2f}"
        )

        st.info(
            f"🏢 Highest-cost category: "
            f"{highest_cost_category}"
        )

        st.info(
            f"📊 {highest_cost_category} represents "
            f"{cost_concentration:.2f}% of total facility cost."
        )

        # --------------------------------------------------------
        # AI RECOMMENDATIONS
        # --------------------------------------------------------

        st.subheader(
            "💡 AI Cost Optimization Recommendations"
        )

        if highest_cost_category == "HVAC":

            st.warning(
                "⚡ HVAC is the highest-cost category. "
                "Review HVAC operation, maintenance schedules "
                "and energy consumption for cost-saving opportunities."
            )

        else:

            st.warning(
                f"🔎 Review {highest_cost_category} expenses "
                "to identify major cost-saving opportunities."
            )

        st.success(
            "⚡ Use Energy Agent results to identify "
            "energy-related cost reduction opportunities."
        )

        st.success(
            "🔧 Use Maintenance Agent results to identify "
            "equipment-related maintenance cost opportunities."
        )

        st.success(
            "👥 Use Occupancy Agent results to identify "
            "space utilization and facility optimization opportunities."
        )

        st.success(
            "🔐 Use Security Agent results to monitor "
            "security-related operational activities."
        )

        st.success(
            "📈 Continuously monitor monthly facility costs "
            "and investigate significant increases."
        )

        st.divider()

        # --------------------------------------------------------
        # COST DATA
        # --------------------------------------------------------

        st.subheader("📋 Cost Activity Data")

        st.dataframe(
            cost_data.head(100),
            use_container_width=True
        )

        
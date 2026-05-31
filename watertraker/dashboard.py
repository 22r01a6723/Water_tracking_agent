import streamlit as st
import pandas as pd
import requests
from src.agent import WaterIntakeAgent

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Water Tracker", layout="wide")

agent = WaterIntakeAgent()

# ---------------- SESSION STATE ----------------
if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

# ---------------- BACKGROUND STYLE ----------------
st.markdown("""
<style>
.stApp {
    background-image: url("image.png");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.block-container {
    background-color: rgba(255,255,255,0.9);
    padding: 2rem;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HOME PAGE ----------------
if not st.session_state.tracker_started:
    st.title("💧 AI Water Tracker")
    st.markdown("Track hydration and get smart insights 💙")

    st.image("image.png", use_column_width=True)

    if st.button("🚀 Start Tracking"):
        st.session_state.tracker_started = True
        st.rerun()

# ---------------- DASHBOARD ----------------
else:
    st.title("📊 Hydration Dashboard")

    # ---------------- SIDEBAR INPUT ----------------
    st.sidebar.header("Log Water Intake")

    user_id = st.sidebar.text_input(
        "User ID",
        value=st.session_state.user_id,
        key="user_id_input"
    )

    user_id = user_id.strip().strip('"').strip("'")
    st.session_state.user_id = user_id

    intake_ml = st.sidebar.number_input(
        "Water Intake (ml)",
        min_value=0,
        step=100
    )

    if st.sidebar.button("Submit"):

        if user_id and intake_ml > 0:
            try:
                # Call FastAPI endpoint to log intake
                response = requests.post(
                    f"{API_BASE_URL}/log-intake",
                    json={"user_id": user_id, "intake_ml": intake_ml}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("Logged successfully 💧")
                    st.info(result.get("analysis", ""))
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"Failed to connect to API: {str(e)}")
        else:
            st.warning("Enter valid User ID and intake")

    # ---------------- HISTORY ----------------
    st.subheader("📅 Daily Water Consumption Trend")

    user_id = st.session_state.get("user_id")

    if user_id:
        try:
            # Call FastAPI endpoint to get history
            response = requests.get(f"{API_BASE_URL}/history/{user_id}")
            
            if response.status_code == 200:
                result = response.json()
                history = result.get("history", [])
                
                if history:
                    # Convert to DataFrame
                    data = history
                    df = pd.DataFrame(data, columns=["intake_ml", "date"])

                    df["date"] = pd.to_datetime(df["date"])
                    df["day"] = df["date"].dt.date

                    # ---------------- DAILY AGGREGATION ----------------
                    daily = df.groupby("day")["intake_ml"].sum().reset_index()
                    daily = daily.sort_values("day")

                    st.dataframe(daily)

                    # ---------------- TREND ANALYSIS ----------------
                    daily["change"] = daily["intake_ml"].diff()

                    # ---------------- AI INSIGHT ----------------
                    st.subheader("🤖 AI Hydration Insight")

                    if len(daily) >= 2:

                        avg_intake = daily["intake_ml"].mean()
                        last_day = daily["intake_ml"].iloc[-1]
                        prev_day = daily["intake_ml"].iloc[-2]

                        change_pct = ((last_day - prev_day) / prev_day) * 100 if prev_day != 0 else 0

                        if change_pct > 10:
                            msg = f"📈 Great improvement! Intake increased by {change_pct:.1f}% vs yesterday."
                        elif change_pct > 0:
                            msg = f"🙂 Slight increase of {change_pct:.1f}% from yesterday. Keep going!"
                        elif change_pct < -10:
                            msg = f"⚠️ Intake dropped by {abs(change_pct):.1f}%. Try to drink more water."
                        elif change_pct < 0:
                            msg = f"📉 Small decrease of {abs(change_pct):.1f}% from yesterday."
                        else:
                            msg = "➡️ Intake is consistent with yesterday."

                        # consistency check
                        std_dev = daily["intake_ml"].std()

                        if std_dev < 200:
                            msg += " 💧 Very consistent hydration pattern."
                        else:
                            msg += " 🔄 Hydration pattern is irregular."

                        st.info(msg)

                    else:
                        st.info("Log at least 2 days to get AI insights 🤖💧")

                    # ---------------- LINE CHART ----------------
                    st.subheader("📊 Trend Chart")
                    st.line_chart(daily.set_index("day")["intake_ml"])

                    # ---------------- METRICS ----------------
                    col1, col2, col3 = st.columns(3)

                    col1.metric("💧 Total Intake", f"{df['intake_ml'].sum()} ml")
                    col2.metric("📅 Days Tracked", len(daily))
                    col3.metric("📊 Avg per Day", f"{int(daily['intake_ml'].mean())} ml")

                else:
                    st.info("No data found 💧")
            else:
                st.error(f"Error fetching history: {response.status_code}")
        except Exception as e:
            st.error(f"Failed to connect to API: {str(e)}")

    else:
        st.warning("Enter User ID to view history")
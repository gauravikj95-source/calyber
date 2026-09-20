import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from predictions import (
    load_model, load_surge_patterns,
    predict_fare_forecast, predict_fairness_score, predict_wait_time,
    predict_cancellation_risk, predict_surge_timing, detect_anomaly,
    recommend_vehicle, compare_route, what_if_analysis
)
from components import (
    COLORS, kpi_card, kpi_row, comparison_card, fairness_badge,
    metric_row, callout, section_header, bar_chart, line_chart,
    donut_chart, dual_bar_chart, hero_header
)

st.set_page_config(
    page_title="Calyber",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_css():
    css_path = os.path.join(BASE_DIR, "styles.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown("<style>" + f.read() + "</style>", unsafe_allow_html=True)

load_css()

@st.cache_data
def load_data():
    trips = pd.read_csv(os.path.join(BASE_DIR, "pbi_trips.csv"))
    captive = pd.read_csv(os.path.join(BASE_DIR, "pbi_captive.csv"))
    weather = pd.read_csv(os.path.join(BASE_DIR, "pbi_weather.csv"))
    kpi = pd.read_csv(os.path.join(BASE_DIR, "pbi_kpi.csv"))
    demand = pd.read_csv(os.path.join(BASE_DIR, "pbi_demand.csv"))
    return trips, captive, weather, kpi, demand

@st.cache_resource
def load_trained_model():
    try:
        model_data = load_model(os.path.join(BASE_DIR, "demand_model.pkl"))
        load_surge_patterns(os.path.join(BASE_DIR, "surge_patterns.csv"))
        return model_data
    except Exception as e:
        return None

trips_df, captive_df, weather_df, kpi_df, demand_df = load_data()
model_data = load_trained_model()

if "section" not in st.session_state:
    st.session_state.section = "Overview"



nav_items = ["Overview", "Predict", "Decide", "Compare", "Data"]
cols = st.columns(len(nav_items))
for col, item in zip(cols, nav_items):
    with col:
        if st.button(item, key="nav_" + item, use_container_width=True):
            st.session_state.section = item
            st.rerun()

st.markdown("---")

# ============================================================
# OVERVIEW
# ============================================================
if st.session_state.section == "Overview":
    hero_header(
        "CALYBER",
        "Fair Pricing Intelligence for Mumbai Ride-Hailing",
        "Detecting unfair surge pricing from 54,132 trips using machine learning and fairness-aware policy design."
    )

    kpi_row([
        {"label": "Trips Analyzed", "value": "54,132", "color": COLORS["primary"]},
        {"label": "Avg Surge Premium", "value": "34.79%", "color": COLORS["warning"]},
        {"label": "Extreme Surge Trips", "value": "1,145", "color": COLORS["danger"]},
    ])

    st.markdown("##")
    callout(
        "The Problem",
        "Mumbai riders pay 34.79% above base fare on average. During storms, that jumps to 77.83%. Riders with no alternatives pay the most. This is systemic, not accidental."
    )

    st.markdown("##")
    section_header("What Calyber Does", "Three ways to understand the pricing problem")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### Predict")
        st.write("Forecast fares, wait times, cancellation risk, and fairness scores before you book.")
    with col2:
        st.markdown("### Decide")
        st.write("Compare vehicles, routes, and what-if scenarios to make an informed choice.")
    with col3:
        st.markdown("### Compare")
        st.write("See how the Calyber policy differs from the current system — fare by fare.")


# ============================================================
# PREDICT
# ============================================================
elif st.session_state.section == "Predict":
    section_header("Predict", "Six prediction tools powered by historical Mumbai data.")

    tabs = st.tabs(["Fare Forecast", "Fairness Score", "Wait Time", "Cancellation Risk", "Surge Timing", "Anomaly Detection"])

    with tabs[0]:
        st.markdown("### Fare Forecast")
        st.write("Predict your fare for the next 2 hours.")
        col1, col2 = st.columns([1, 1])
        with col1:
            distance = st.slider("Distance (km)", 1.0, 30.0, 7.0, 0.5)
            vehicle = st.selectbox("Vehicle type", ["Bike", "Auto", "Mini", "Sedan", "SUV", "Prime"], index=2)
            hour = st.slider("Current hour", 0, 23, 17)
            weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=3)
        with col2:
            if st.button("Predict Fare", key="predict_fare_btn"):
                result = predict_fare_forecast(pickup_zone="Andheri", drop_zone="BKC", distance_km=distance, vehicle_type=vehicle, current_hour=hour, weather=weather, day_of_week="Monday")
                st.session_state.fare_forecast_result = result
        if "fare_forecast_result" in st.session_state:
            r = st.session_state.fare_forecast_result
            st.markdown("---")
            kpi_row([
                {"label": "Fare Now", "value": "₹" + str(r["current_fare"]), "color": COLORS["primary"]},
                {"label": "Best Fare", "value": "₹" + str(r["best_fare"]), "color": COLORS["success"]},
                {"label": "Best Time", "value": r["best_time"], "color": COLORS["success"]},
                {"label": "Savings", "value": "₹" + str(r["savings"]), "color": COLORS["success"] if r["savings"] > 0 else COLORS["text_muted"]},
            ])
            forecast_df = pd.DataFrame(r["forecasts"])
            line_chart(forecast_df, "time_label", "fare", color=COLORS["primary"], height=320)

    with tabs[1]:
        st.markdown("### Fairness Score")
        st.write("Will this ride be fair?")
        col1, col2 = st.columns([1, 1])
        with col1:
            f_hour = st.slider("Hour", 0, 23, 18, key="fairness_hour")
            f_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=4, key="fairness_weather")
            f_captive = st.selectbox("Captive quartile", ["Low", "Medium", "High", "Extreme"], index=3, key="fairness_captive")
        with col2:
            if st.button("Calculate Fairness", key="fairness_btn"):
                result = predict_fairness_score(f_weather, f_hour, f_captive, "Mini")
                st.session_state.fairness_result = result
        if "fairness_result" in st.session_state:
            r = st.session_state.fairness_result
            st.markdown("---")
            col1, col2 = st.columns([1, 1])
            with col1:
                fairness_badge(r["grade"], r["label"], r["color"])
            with col2:
                metric_row([
                    {"label": "Surge", "value": str(r["surge"]) + "x"},
                    {"label": "Premium", "value": str(r["premium_pct"]) + "%", "color": r["color"]},
                ])
                st.markdown("##")
                st.write("Weather: " + r["weather"])
                st.write("Captive quartile: " + r["captive"])

    with tabs[2]:
        st.markdown("### Wait Time Forecast")
        w_hour = st.slider("Hour", 0, 23, 18, key="wait_hour")
        w_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=3, key="wait_weather")
        w_captive = st.selectbox("Captive quartile", ["Low", "Medium", "High", "Extreme"], index=2, key="wait_captive")
        if st.button("Predict Wait", key="wait_btn"):
            r = predict_wait_time(w_weather, w_hour, w_captive)
            kpi_row([
                {"label": "Predicted Wait", "value": str(r["wait_min"]) + " min", "color": COLORS["primary"]},
                {"label": "Range", "value": str(r["wait_range"][0]) + "–" + str(r["wait_range"][1]) + " min", "color": COLORS["text_muted"]},
            ])

    with tabs[3]:
        st.markdown("### Cancellation Risk")
        c_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=4, key="cancel_weather")
        c_traffic = st.selectbox("Traffic", ["Low", "Medium", "High", "Severe"], index=2, key="cancel_traffic")
        c_vehicle = st.selectbox("Vehicle", ["Bike", "Auto", "Mini", "Sedan", "SUV", "Prime"], index=3, key="cancel_vehicle")
        c_hour = st.slider("Hour", 0, 23, 18, key="cancel_hour")
        if st.button("Calculate Risk", key="cancel_btn"):
            r = predict_cancellation_risk(c_weather, c_traffic, c_vehicle, c_hour)
            kpi_row([
                {"label": "Cancellation Risk", "value": str(r["risk_pct"]) + "%", "color": r["color"]},
                {"label": "Level", "value": r["level"], "color": r["color"]},
            ])

    with tabs[4]:
        st.markdown("### Surge Timing")
        s_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=3, key="surge_weather")
        s_day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], key="surge_day")
        r = predict_surge_timing(s_weather, s_day)
        timeline_df = pd.DataFrame(r["timeline"])
        line_chart(timeline_df, "time_label", "surge", color=COLORS["warning"], height=320)
        kpi_row([
            {"label": "Peak Hour", "value": r["peak_hour"], "color": COLORS["danger"]},
            {"label": "Peak Surge", "value": str(r["peak_surge"]) + "x", "color": COLORS["danger"]},
            {"label": "Lowest Hour", "value": r["lowest_hour"], "color": COLORS["success"]},
            {"label": "Lowest Surge", "value": str(r["lowest_surge"]) + "x", "color": COLORS["success"]},
        ])

    with tabs[5]:
        st.markdown("### Anomaly Detection")
        st.write("Is your fare suspicious?")
        col1, col2 = st.columns([1, 1])
        with col1:
            actual_fare = st.number_input("Actual fare paid (₹)", 10.0, 5000.0, 420.0, 10.0)
            a_distance = st.slider("Distance (km)", 1.0, 30.0, 7.0, 0.5, key="anomaly_dist")
            a_vehicle = st.selectbox("Vehicle", ["Bike", "Auto", "Mini", "Sedan", "SUV", "Prime"], index=2, key="anomaly_vehicle")
            a_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=4, key="anomaly_weather")
            a_hour = st.slider("Hour", 0, 23, 18, key="anomaly_hour")
        with col2:
            if st.button("Check Fare", key="anomaly_btn"):
                r = detect_anomaly(actual_fare, a_distance, a_vehicle, a_weather, a_hour)
                st.session_state.anomaly_result = r
        if "anomaly_result" in st.session_state:
            r = st.session_state.anomaly_result
            st.markdown("---")
            kpi_row([
                {"label": "Status", "value": r["status"], "color": r["color"]},
                {"label": "Actual Fare", "value": "₹" + str(r["actual_fare"]), "color": COLORS["text"]},
                {"label": "Expected Fare", "value": "₹" + str(r["expected_fare"]), "color": COLORS["success"]},
                {"label": "Deviation", "value": str(r["deviation_pct"]) + "%", "color": r["color"]},
            ])


# ============================================================
# DECIDE
# ============================================================
elif st.session_state.section == "Decide":
    section_header("Decide", "Three tools to help you make the best choice.")

    tabs = st.tabs(["Vehicle Recommender", "Route Comparison", "What-If Explorer"])

    with tabs[0]:
        st.markdown("### Vehicle Recommender")
        v_distance = st.slider("Distance (km)", 1.0, 30.0, 7.0, 0.5, key="veh_dist")
        v_priority = st.radio("Priority", ["cheapest", "fastest", "fairest"], horizontal=True, key="veh_priority")
        v_hour = st.slider("Hour", 0, 23, 18, key="veh_hour")
        v_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=3, key="veh_weather")
        if st.button("Recommend", key="veh_btn"):
            r = recommend_vehicle(v_distance, v_priority, v_hour, v_weather)
            rec = r["recommended"]
            kpi_row([
                {"label": "Recommended", "value": rec["vehicle"], "color": COLORS["success"]},
                {"label": "Fare", "value": "₹" + str(rec["fare"]), "color": COLORS["primary"]},
                {"label": "Wait", "value": str(rec["wait"]) + " min", "color": COLORS["primary"]},
            ])
            st.markdown("### All options")
            options_df = pd.DataFrame(r["all_options"])
            st.dataframe(options_df, use_container_width=True)

    with tabs[1]:
        st.markdown("### Route Comparison")
        r_distance = st.slider("Distance (km)", 1.0, 30.0, 7.2, 0.1, key="route_dist")
        r_vehicle = st.selectbox("Vehicle", ["Bike", "Auto", "Mini", "Sedan", "SUV", "Prime"], index=2, key="route_vehicle")
        r_hour = st.slider("Hour", 0, 23, 18, key="route_hour")
        r_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=3, key="route_weather")
        if st.button("Compare", key="route_btn"):
            r = compare_route(r_distance, r_vehicle, r_hour, r_weather)
            kpi_row([
                {"label": "Predicted Fare", "value": "₹" + str(r["predicted_fare"]), "color": COLORS["primary"]},
                {"label": "Historical Average", "value": "₹" + str(r["historical_avg"]), "color": COLORS["text_muted"]},
                {"label": "Disparity", "value": str(r["disparity_pct"]) + "%", "color": r["color"]},
                {"label": "Status", "value": r["status"], "color": r["color"]},
            ])

    with tabs[2]:
        st.markdown("### What-If Explorer")
        w_distance = st.slider("Distance (km)", 1.0, 30.0, 7.0, 0.5, key="whatif_dist")
        w_vehicle = st.selectbox("Vehicle", ["Bike", "Auto", "Mini", "Sedan", "SUV", "Prime"], index=2, key="whatif_vehicle")
        w_hour = st.slider("Hour", 0, 23, 18, key="whatif_hour")
        w_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=4, key="whatif_weather")
        w_captive = st.selectbox("Captive quartile", ["Low", "Medium", "High", "Extreme"], index=3, key="whatif_captive")
        if st.button("Explore", key="whatif_btn"):
            r = what_if_analysis(w_distance, w_vehicle, w_hour, w_weather, w_captive)
            kpi_card("Current Fare", "₹" + str(r["current_fare"]), color=COLORS["danger"])
            st.markdown("### Scenarios")
            for s in r["scenarios"]:
                st.write(s["label"] + " — ₹" + str(s["fare"]) + " (" + str(s["change"]) + ")")


# ============================================================
# COMPARE
# ============================================================
elif st.session_state.section == "Compare":
    section_header("Compare", "See how Calyber changes the pricing.")

    tabs = st.tabs(["Policy Simulator", "Fairness Analysis"])

    with tabs[0]:
        st.markdown("### Policy Simulator")
        p_distance = st.slider("Distance (km)", 1.0, 30.0, 7.0, 0.5, key="policy_dist")
        p_vehicle = st.selectbox("Vehicle", ["Bike", "Auto", "Mini", "Sedan", "SUV", "Prime"], index=2, key="policy_vehicle")
        p_hour = st.slider("Hour", 0, 23, 18, key="policy_hour")
        p_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=4, key="policy_weather")
        p_captive = st.selectbox("Captive quartile", ["Low", "Medium", "High", "Extreme"], index=3, key="policy_captive")
        if st.button("Compare Policies", key="policy_btn"):
            from predictions import _calc_scenario
            baseline = _calc_scenario(p_distance, p_vehicle, p_hour, p_weather, p_captive, apply_policy=False)
            calyber = _calc_scenario(p_distance, p_vehicle, p_hour, p_weather, p_captive, apply_policy=True)
            comparison_card("Baseline (Current System)", "₹" + str(baseline["fare"]), "Calyber (Fair Policy)", "₹" + str(calyber["fare"]), savings=round(baseline["fare"] - calyber["fare"], 2))
            st.markdown("### Surge comparison")
            metric_row([
                {"label": "Baseline Surge", "value": str(baseline["surge"]) + "x", "color": COLORS["danger"]},
                {"label": "Calyber Surge", "value": str(calyber["surge"]) + "x", "color": COLORS["success"]},
            ])

    with tabs[1]:
        st.markdown("### Fairness Analysis")
        st.write("Where does the pricing system fail?")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Surge by Weather")
            bar_chart(weather_df, "Weather", "Baseline_Surge", color=COLORS["warning"], height=280)
        with col2:
            st.markdown("#### Surge by Captive Quartile")
            bar_chart(captive_df, "Captive_Quartile", "Baseline_Surge", color=COLORS["danger"], height=280)
        st.markdown("#### Baseline vs Calyber by Captive Quartile")
        dual_bar_chart(captive_df, "Captive_Quartile", "Baseline_Surge", "Calyber_Surge", height=320)
        callout("Key Finding", "Extreme captive riders pay 43.7% more surge than low captive riders. This is systemic.", color=COLORS["danger"])


# ============================================================
# DATA
# ============================================================
elif st.session_state.section == "Data":
    section_header("Data Explorer", "Explore 54,132 Mumbai trips.")

    col1, col2, col3 = st.columns(3)
    with col1:
        weather_filter = st.selectbox("Weather", ["All"] + list(trips_df["Weather_Condition"].unique()), key="data_weather")
    with col2:
        captive_filter = st.selectbox("Captive Quartile", ["All"] + list(trips_df["captive_quartile"].unique()), key="data_captive")
    with col3:
        vehicle_filter = st.selectbox("Vehicle", ["All"] + list(trips_df["Vehicle_Type"].unique()), key="data_vehicle")

    filtered = trips_df.copy()
    if weather_filter != "All":
        filtered = filtered[filtered["Weather_Condition"] == weather_filter]
    if captive_filter != "All":
        filtered = filtered[filtered["captive_quartile"] == captive_filter]
    if vehicle_filter != "All":
        filtered = filtered[filtered["Vehicle_Type"] == vehicle_filter]

    st.markdown("**Showing " + str(len(filtered)) + " of " + str(len(trips_df)) + " trips**")

    display_cols = ["Trip_ID", "Weather_Condition", "Vehicle_Type", "Distance_KM", "Surge_Multiplier", "Total_Fare", "captive_quartile", "fairness_band"]
    display_cols = [c for c in display_cols if c in filtered.columns]
    st.dataframe(filtered[display_cols].head(500), use_container_width=True, height=500)

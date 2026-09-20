app_content = r'''import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from predictions import (
    load_model, load_surge_patterns,
    predict_fare_forecast, predict_fairness_score, predict_wait_time,
    predict_cancellation_risk, predict_surge_timing, detect_anomaly,
    recommend_vehicle, compare_route, what_if_analysis, _calc_scenario
)
from components import (
    COLORS, hero_header, hero_card, section_label, section_header,
    kpi_card, kpi_row, card_label, result_card, comparison_card,
    fairness_badge, metric_row, callout, bar_chart, line_chart,
    donut_chart, dual_bar_chart
)

st.set_page_config(page_title="Calyber", layout="wide", initial_sidebar_state="collapsed")

def load_css():
    p = os.path.join(BASE_DIR, "styles.css")
    if os.path.exists(p):
        with open(p) as f:
            st.markdown("<style>" + f.read() + "</style>", unsafe_allow_html=True)
load_css()

@st.cache_data
def load_data():
    return (
        pd.read_csv(os.path.join(BASE_DIR, "pbi_trips.csv")),
        pd.read_csv(os.path.join(BASE_DIR, "pbi_captive.csv")),
        pd.read_csv(os.path.join(BASE_DIR, "pbi_weather.csv")),
        pd.read_csv(os.path.join(BASE_DIR, "pbi_kpi.csv")),
        pd.read_csv(os.path.join(BASE_DIR, "pbi_demand.csv"))
    )

@st.cache_resource
def load_model_data():
    try:
        m = load_model(os.path.join(BASE_DIR, "demand_model.pkl"))
        load_surge_patterns(os.path.join(BASE_DIR, "surge_patterns.csv"))
        return m
    except Exception:
        return None

trips_df, captive_df, weather_df, kpi_df, demand_df = load_data()
model_data = load_model_data()

if "section" not in st.session_state:
    st.session_state.section = "Overview"

# ============================================================
# NAVIGATION (minimal, outline buttons)
# ============================================================
nav_items = ["Overview", "Predict", "Decide", "Compare", "Data"]
nav_cols = st.columns(len(nav_items), gap="small")
for col, item in zip(nav_cols, items := nav_items):
    with col:
        if st.button(item, key="nav_" + item, use_container_width=True):
            st.session_state.section = item
            st.rerun()


# ============================================================
# OVERVIEW
# ============================================================
if st.session_state.section == "Overview":
    hero_header(
        "CALYBER",
        "Fair Pricing Intelligence for Mumbai Ride-Hailing",
        "Detecting unfair surge pricing from 54,132 trips using machine learning and fairness-aware policy design."
    )

    hero_card(
        "THE PROBLEM",
        "Mumbai riders pay 34.79% above base fare on average. During storms, that jumps to 77.83%.",
        "Riders with no alternatives pay the most. This is not an accident — it is a pattern embedded in the pricing algorithm. Calyber exposes it and models a fairer alternative."
    )

    kpi_row([
        {"label": "Trips Analyzed", "value": "54,132"},
        {"label": "Average Surge Premium", "value": "34.79%", "color": "#DC2626"},
        {"label": "Extreme Surge Trips", "value": "1,145", "color": "#DC2626"},
        {"label": "Revenue Impact of Fair Policy", "value": "-6.61%", "color": "#D97706"},
    ])

    section_header("What Calyber Does", "Three layers: prediction, decision, and comparison.")

    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.markdown("**Predict**")
        st.markdown("Forecast fares, wait times, cancellation risk, and fairness grades before you book.")
    with col2:
        st.markdown("**Decide**")
        st.markdown("Compare vehicles, routes, and what-if scenarios to make an informed choice.")
    with col3:
        st.markdown("**Compare**")
        st.markdown("See how the Calyber fair-pricing policy differs from the current system.")


# ============================================================
# PREDICT
# ============================================================
elif st.session_state.section == "Predict":
    section_header("Predict", "Six prediction tools powered by historical Mumbai data.")

    tabs = st.tabs(["Fare Forecast", "Fairness Score", "Wait Time", "Cancellation Risk", "Surge Timing", "Anomaly Detection"])

    # --- Fare Forecast ---
    with tabs[0]:
        st.markdown("### Fare Forecast")
        st.markdown("Predict your fare for the next 2 hours.")

        col1, col2 = st.columns([1, 2], gap="large")

        with col1:
            distance = st.number_input("Distance (km)", 1.0, 30.0, 7.0, 0.5, key="ff_dist")
            vehicle = st.selectbox("Vehicle type", ["Bike", "Auto", "Mini", "Sedan", "SUV", "Prime"], index=2, key="ff_veh")
            hour = st.selectbox("Current hour", list(range(24)), index=17, key="ff_hour")
            weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=3, key="ff_weather")
            predict_btn = st.button("Predict Fare", key="ff_btn", use_container_width=True)

        with col2:
            if predict_btn:
                r = predict_fare_forecast("Andheri", "BKC", distance, vehicle, hour, weather, "Monday")
                st.session_state.ff_result = r

            if "ff_result" in st.session_state:
                r = st.session_state.ff_result
                kpi_row([
                    {"label": "Fare Now", "value": "Rs " + str(r["current_fare"])},
                    {"label": "Best Fare", "value": "Rs " + str(r["best_fare"]), "color": "#059669"},
                    {"label": "Best Time", "value": r["best_time"], "color": "#059669"},
                    {"label": "Savings", "value": "Rs " + str(r["savings"])},
                ])
                st.markdown("#### Fare over next 2 hours")
                fdf = pd.DataFrame(r["forecasts"])
                line_chart(fdf, "time_label", "fare", color="#0F172A", height=340)

    # --- Fairness Score ---
    with tabs[1]:
        st.markdown("### Fairness Score")
        st.markdown("Will this ride be fair?")

        col1, col2 = st.columns([1, 2], gap="large")
        with col1:
            f_hour = st.selectbox("Hour", list(range(24)), index=18, key="fs_hour")
            f_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=4, key="fs_weather")
            f_captive = st.selectbox("Captive quartile", ["Low", "Medium", "High", "Extreme"], index=3, key="fs_captive")
            fs_btn = st.button("Calculate Fairness", key="fs_btn", use_container_width=True)

        with col2:
            if fs_btn:
                st.session_state.fs_result = predict_fairness_score(f_weather, f_hour, f_captive, "Mini")

            if "fs_result" in st.session_state:
                r = st.session_state.fs_result
                c1, c2 = st.columns([1, 1], gap="large")
                with c1:
                    fairness_badge(r["grade"], r["label"], r["color"])
                with c2:
                    metric_row([
                        {"label": "Surge", "value": str(r["surge"]) + "x"},
                        {"label": "Premium", "value": str(r["premium_pct"]) + "%", "color": r["color"]},
                    ])

    # --- Wait Time ---
    with tabs[2]:
        st.markdown("### Wait Time Forecast")
        col1, col2 = st.columns([1, 2], gap="large")
        with col1:
            w_hour = st.selectbox("Hour", list(range(24)), index=18, key="wt_hour")
            w_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=3, key="wt_weather")
            w_captive = st.selectbox("Captive quartile", ["Low", "Medium", "High", "Extreme"], index=2, key="wt_captive")
            wt_btn = st.button("Predict Wait", key="wt_btn", use_container_width=True)
        with col2:
            if wt_btn:
                st.session_state.wt_result = predict_wait_time(w_weather, w_hour, w_captive)
            if "wt_result" in st.session_state:
                r = st.session_state.wt_result
                kpi_row([
                    {"label": "Predicted Wait", "value": str(r["wait_min"]) + " min"},
                    {"label": "Range", "value": str(r["wait_range"][0]) + "-" + str(r["wait_range"][1]) + " min"},
                ])

    # --- Cancellation Risk ---
    with tabs[3]:
        st.markdown("### Cancellation Risk")
        col1, col2 = st.columns([1, 2], gap="large")
        with col1:
            c_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=4, key="cr_weather")
            c_traffic = st.selectbox("Traffic", ["Low", "Medium", "High", "Severe"], index=2, key="cr_traffic")
            c_vehicle = st.selectbox("Vehicle", ["Bike", "Auto", "Mini", "Sedan", "SUV", "Prime"], index=3, key="cr_vehicle")
            c_hour = st.selectbox("Hour", list(range(24)), index=18, key="cr_hour")
            cr_btn = st.button("Calculate Risk", key="cr_btn", use_container_width=True)
        with col2:
            if cr_btn:
                st.session_state.cr_result = predict_cancellation_risk(c_weather, c_traffic, c_vehicle, c_hour)
            if "cr_result" in st.session_state:
                r = st.session_state.cr_result
                kpi_row([
                    {"label": "Cancellation Risk", "value": str(r["risk_pct"]) + "%", "color": r["color"]},
                    {"label": "Level", "value": r["level"], "color": r["color"]},

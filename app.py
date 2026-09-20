import streamlit as st
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
    section_hero, section_divider,
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
# NAVIGATION
# ============================================================
def render_nav():
    nav_items = ["Overview", "Predict", "Decide", "Compare", "Data"]
    cols = st.columns(len(nav_items), gap="small")
    for col, item in zip(cols, nav_items):
        with col:
            is_active = st.session_state.section == item
            btn_type = "primary" if is_active else "secondary"
            if st.button(item, key="nav_" + item, use_container_width=True, type=btn_type):
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

    render_nav()
    st.markdown("---")

    hero_card(
        "THE PROBLEM",
        "Mumbai riders pay 34.79% above base fare on average. During storms, that jumps to 77.83%.",
        "Riders with no alternatives pay the most. This is not an accident. It is a pattern embedded in the pricing algorithm. Calyber exposes it and models a fairer alternative."
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
    render_nav()
    st.markdown("---")

    section_hero(
        "PREDICT",
        "See the price before you book.",
        "Six prediction tools built on 54,132 Mumbai trips. Forecast fares, check fairness, estimate wait times, and detect anomalies before you commit."
    )

    tabs = st.tabs(["Fare Forecast", "Fairness Score", "Wait Time", "Cancellation Risk", "Surge Timing", "Anomaly Detection"])

    with tabs[0]:
        st.markdown("### Fare Forecast")
        st.markdown("Predict your fare for the next 2 hours.")
        st.markdown("")

        col_form, col_result = st.columns([1, 1.4], gap="large")

        with col_form:
            distance = st.number_input("Distance (km)", 1.0, 30.0, 7.0, 0.5, key="ff_dist")
            vehicle = st.selectbox("Vehicle type", ["Bike", "Auto", "Mini", "Sedan", "SUV", "Prime"], index=2, key="ff_veh")
            hour = st.selectbox("Current hour", list(range(24)), index=17, key="ff_hour")
            weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=3, key="ff_weather")
            st.markdown("")
            if st.button("Predict Fare", key="ff_btn", use_container_width=True):
                st.session_state.ff_result = predict_fare_forecast("Andheri", "BKC", distance, vehicle, hour, weather, "Monday")

        with col_result:
            if "ff_result" in st.session_state:
                r = st.session_state.ff_result
                kpi_row([
                    {"label": "Fare Now", "value": "Rs " + str(r["current_fare"])},
                    {"label": "Best Fare", "value": "Rs " + str(r["best_fare"]), "color": "#059669"},
                ])
                kpi_row([
                    {"label": "Best Time", "value": r["best_time"], "color": "#059669"},
                    {"label": "Savings", "value": "Rs " + str(r["savings"])},
                ])
                fdf = pd.DataFrame(r["forecasts"])
                line_chart(fdf, "time_label", "fare", color="#0F172A", height=300)
            else:
                st.markdown(
                    '<div style="background:#F8FAFC; border:1px dashed #E5E7EB; '
                    'border-radius:14px; padding:80px 24px; text-align:center; '
                    'color:#94A3B8; font-size:14px;">'
                    'Results will appear here after you click Predict Fare.'
                    '</div>',
                    unsafe_allow_html=True
                )

    with tabs[1]:
        st.markdown("### Fairness Score")
        st.markdown("Will this ride be fair?")
        st.markdown("")

        col_form, col_result = st.columns([1, 1.4], gap="large")

        with col_form:
            f_hour = st.selectbox("Hour", list(range(24)), index=18, key="fs_hour")
            f_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=4, key="fs_weather")
            f_captive = st.selectbox("Captive quartile", ["Low", "Medium", "High", "Extreme"], index=3, key="fs_captive")
            st.markdown("")
            if st.button("Calculate Fairness", key="fs_btn", use_container_width=True):
                st.session_state.fs_result = predict_fairness_score(f_weather, f_hour, f_captive, "Mini")

        with col_result:
            if "fs_result" in st.session_state:
                r = st.session_state.fs_result
                c1, c2 = st.columns([1, 1], gap="medium")
                with c1:
                    fairness_badge(r["grade"], r["label"], r["color"])
                with c2:
                    metric_row([
                        {"label": "Surge", "value": str(r["surge"]) + "x"},
                        {"label": "Premium", "value": str(r["premium_pct"]) + "%", "color": r["color"]},
                    ])
            else:
                st.markdown(
                    '<div style="background:#F8FAFC; border:1px dashed #E5E7EB; '
                    'border-radius:14px; padding:80px 24px; text-align:center; '
                    'color:#94A3B8; font-size:14px;">'
                    'Fairness grade will appear here.'
                    '</div>',
                    unsafe_allow_html=True
                )

    with tabs[2]:
        st.markdown("### Wait Time Forecast")
        st.markdown("")

        col_form, col_result = st.columns([1, 1.4], gap="large")

        with col_form:
            w_hour = st.selectbox("Hour", list(range(24)), index=18, key="wt_hour")
            w_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=3, key="wt_weather")
            w_captive = st.selectbox("Captive quartile", ["Low", "Medium", "High", "Extreme"], index=2, key="wt_captive")
            st.markdown("")
            if st.button("Predict Wait", key="wt_btn", use_container_width=True):
                st.session_state.wt_result = predict_wait_time(w_weather, w_hour, w_captive)

        with col_result:
            if "wt_result" in st.session_state:
                r = st.session_state.wt_result
                kpi_row([
                    {"label": "Predicted Wait", "value": str(r["wait_min"]) + " min"},
                    {"label": "Range", "value": str(r["wait_range"][0]) + "-" + str(r["wait_range"][1]) + " min"},
                ])
            else:
                st.markdown(
                    '<div style="background:#F8FAFC; border:1px dashed #E5E7EB; '
                    'border-radius:14px; padding:80px 24px; text-align:center; '
                    'color:#94A3B8; font-size:14px;">'
                    'Wait time prediction will appear here.'
                    '</div>',
                    unsafe_allow_html=True
                )

    with tabs[3]:
        st.markdown("### Cancellation Risk")
        st.markdown("")

        col_form, col_result = st.columns([1, 1.4], gap="large")

        with col_form:
            c_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=4, key="cr_weather")
            c_traffic = st.selectbox("Traffic", ["Low", "Medium", "High", "Severe"], index=2, key="cr_traffic")
            c_vehicle = st.selectbox("Vehicle", ["Bike", "Auto", "Mini", "Sedan", "SUV", "Prime"], index=3, key="cr_vehicle")
            c_hour = st.selectbox("Hour", list(range(24)), index=18, key="cr_hour")
            st.markdown("")
            if st.button("Calculate Risk", key="cr_btn", use_container_width=True):
                st.session_state.cr_result = predict_cancellation_risk(c_weather, c_traffic, c_vehicle, c_hour)

        with col_result:
            if "cr_result" in st.session_state:
                r = st.session_state.cr_result
                kpi_row([
                    {"label": "Cancellation Risk", "value": str(r["risk_pct"]) + "%", "color": r["color"]},
                    {"label": "Level", "value": r["level"], "color": r["color"]},
                ])
            else:
                st.markdown(
                    '<div style="background:#F8FAFC; border:1px dashed #E5E7EB; '
                    'border-radius:14px; padding:80px 24px; text-align:center; '
                    'color:#94A3B8; font-size:14px;">'
                    'Cancellation risk will appear here.'
                    '</div>',
                    unsafe_allow_html=True
                )

    with tabs[4]:
        st.markdown("### Surge Timing")
        st.markdown("")

        col_form, col_result = st.columns([1, 1.4], gap="large")

        with col_form:
            s_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=3, key="st_weather")
            s_day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], key="st_day")
            st.markdown("")
            if st.button("Show Timeline", key="st_btn", use_container_width=True):
                st.session_state.st_result = predict_surge_timing(s_weather, s_day)

        with col_result:
            if "st_result" in st.session_state:
                r = st.session_state.st_result
                tdf = pd.DataFrame(r["timeline"])
                line_chart(tdf, "time_label", "surge", color="#DC2626", height=300)
                kpi_row([
                    {"label": "Peak Hour", "value": r["peak_hour"], "color": "#DC2626"},
                    {"label": "Peak Surge", "value": str(r["peak_surge"]) + "x", "color": "#DC2626"},
                ])
                kpi_row([
                    {"label": "Lowest Hour", "value": r["lowest_hour"], "color": "#059669"},
                    {"label": "Lowest Surge", "value": str(r["lowest_surge"]) + "x", "color": "#059669"},
                ])
            else:
                st.markdown(
                    '<div style="background:#F8FAFC; border:1px dashed #E5E7EB; '
                    'border-radius:14px; padding:80px 24px; text-align:center; '
                    'color:#94A3B8; font-size:14px;">'
                    'Surge timeline will appear here.'
                    '</div>',
                    unsafe_allow_html=True
                )

    with tabs[5]:
        st.markdown("### Anomaly Detection")
        st.markdown("Is your fare suspicious?")
        st.markdown("")

        col_form, col_result = st.columns([1, 1.4], gap="large")

        with col_form:
            actual_fare = st.number_input("Actual fare paid (Rs)", 10.0, 5000.0, 420.0, 10.0, key="an_fare")
            a_distance = st.number_input("Distance (km)", 1.0, 30.0, 7.0, 0.5, key="an_dist")
            a_vehicle = st.selectbox("Vehicle", ["Bike", "Auto", "Mini", "Sedan", "SUV", "Prime"], index=2, key="an_veh")
            a_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=4, key="an_weather")
            a_hour = st.selectbox("Hour", list(range(24)), index=18, key="an_hour")
            st.markdown("")
            if st.button("Check Fare", key="an_btn", use_container_width=True):
                st.session_state.an_result = detect_anomaly(actual_fare, a_distance, a_vehicle, a_weather, a_hour)

        with col_result:
            if "an_result" in st.session_state:
                r = st.session_state.an_result
                kpi_row([
                    {"label": "Status", "value": r["status"], "color": r["color"]},
                    {"label": "Deviation", "value": str(r["deviation_pct"]) + "%", "color": r["color"]},
                ])
                kpi_row([
                    {"label": "Actual Fare", "value": "Rs " + str(r["actual_fare"])},
                    {"label": "Expected Fare", "value": "Rs " + str(r["expected_fare"]), "color": "#059669"},
                ])
            else:
                st.markdown(
                    '<div style="background:#F8FAFC; border:1px dashed #E5E7EB; '
                    'border-radius:14px; padding:80px 24px; text-align:center; '
                    'color:#94A3B8; font-size:14px;">'
                    'Anomaly check will appear here.'
                    '</div>',
                    unsafe_allow_html=True
                )


# ============================================================
# DECIDE
# ============================================================
elif st.session_state.section == "Decide":
    render_nav()
    st.markdown("---")

    section_hero(
        "DECIDE",
        "Make an informed choice.",
        "Three tools to compare vehicles, routes, and what-if scenarios. Understand the trade-offs before you decide."
    )

    tabs = st.tabs(["Vehicle Recommender", "Route Comparison", "What-If Explorer"])

    with tabs[0]:
        st.markdown("### Vehicle Recommender")
        st.markdown("")

        col_form, col_result = st.columns([1, 1.4], gap="large")

        with col_form:
            v_distance = st.number_input("Distance (km)", 1.0, 30.0, 7.0, 0.5, key="vr_dist")
            v_priority = st.radio("Priority", ["cheapest", "fastest", "fairest"], horizontal=True, key="vr_priority")
            v_hour = st.selectbox("Hour", list(range(24)), index=18, key="vr_hour")
            v_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=3, key="vr_weather")
            st.markdown("")
            if st.button("Recommend", key="vr_btn", use_container_width=True):
                st.session_state.vr_result = recommend_vehicle(v_distance, v_priority, v_hour, v_weather)

        with col_result:
            if "vr_result" in st.session_state:
                r = st.session_state.vr_result
                rec = r["recommended"]
                kpi_row([
                    {"label": "Recommended", "value": rec["vehicle"], "color": "#059669"},
                    {"label": "Fare", "value": "Rs " + str(rec["fare"])},
                    {"label": "Wait", "value": str(rec["wait"]) + " min"},
                ])
                st.markdown("#### All options")
                st.dataframe(pd.DataFrame(r["all_options"]), use_container_width=True)
            else:
                st.markdown(
                    '<div style="background:#F8FAFC; border:1px dashed #E5E7EB; '
                    'border-radius:14px; padding:80px 24px; text-align:center; '
                    'color:#94A3B8; font-size:14px;">'
                    'Recommendation will appear here.'
                    '</div>',
                    unsafe_allow_html=True
                )

    with tabs[1]:
        st.markdown("### Route Comparison")
        st.markdown("")

        col_form, col_result = st.columns([1, 1.4], gap="large")

        with col_form:
            r_distance = st.number_input("Distance (km)", 1.0, 30.0, 7.2, 0.1, key="rc_dist")
            r_vehicle = st.selectbox("Vehicle", ["Bike", "Auto", "Mini", "Sedan", "SUV", "Prime"], index=2, key="rc_veh")
            r_hour = st.selectbox("Hour", list(range(24)), index=18, key="rc_hour")
            r_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=3, key="rc_weather")
            st.markdown("")
            if st.button("Compare", key="rc_btn", use_container_width=True):
                st.session_state.rc_result = compare_route(r_distance, r_vehicle, r_hour, r_weather)

        with col_result:
            if "rc_result" in st.session_state:
                r = st.session_state.rc_result
                kpi_row([
                    {"label": "Predicted Fare", "value": "Rs " + str(r["predicted_fare"])},
                    {"label": "Historical Average", "value": "Rs " + str(r["historical_avg"])},
                ])
                kpi_row([
                    {"label": "Disparity", "value": str(r["disparity_pct"]) + "%", "color": r["color"]},
                    {"label": "Status", "value": r["status"], "color": r["color"]},
                ])
            else:
                st.markdown(
                    '<div style="background:#F8FAFC; border:1px dashed #E5E7EB; '
                    'border-radius:14px; padding:80px 24px; text-align:center; '
                    'color:#94A3B8; font-size:14px;">'
                    'Route comparison will appear here.'
                    '</div>',
                    unsafe_allow_html=True
                )

    with tabs[2]:
        st.markdown("### What-If Explorer")
        st.markdown("")

        col_form, col_result = st.columns([1, 1.4], gap="large")

        with col_form:
            wi_distance = st.number_input("Distance (km)", 1.0, 30.0, 7.0, 0.5, key="wi_dist")
            wi_vehicle = st.selectbox("Vehicle", ["Bike", "Auto", "Mini", "Sedan", "SUV", "Prime"], index=2, key="wi_veh")
            wi_hour = st.selectbox("Hour", list(range(24)), index=18, key="wi_hour")
            wi_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=4, key="wi_weather")
            wi_captive = st.selectbox("Captive quartile", ["Low", "Medium", "High", "Extreme"], index=3, key="wi_captive")
            st.markdown("")
            if st.button("Explore", key="wi_btn", use_container_width=True):
                st.session_state.wi_result = what_if_analysis(wi_distance, wi_vehicle, wi_hour, wi_weather, wi_captive)

        with col_result:
            if "wi_result" in st.session_state:
                r = st.session_state.wi_result
                kpi_card("Current Fare", "Rs " + str(r["current_fare"]), color="#DC2626")
                st.markdown("#### Scenarios")
                for s in r["scenarios"]:
                    st.markdown("- **" + s["label"] + "**: Rs " + str(s["fare"]) + " (" + str(s["change"]) + ")")
            else:
                st.markdown(
                    '<div style="background:#F8FAFC; border:1px dashed #E5E7EB; '
                    'border-radius:14px; padding:80px 24px; text-align:center; '
                    'color:#94A3B8; font-size:14px;">'
                    'Scenario analysis will appear here.'
                    '</div>',
                    unsafe_allow_html=True
                )


# ============================================================
# COMPARE
# ============================================================
elif st.session_state.section == "Compare":
    render_nav()
    st.markdown("---")

    section_hero(
        "COMPARE",
        "Baseline vs Calyber.",
        "See how the fairness-aware policy differs from the current system, fare by fare, quartile by quartile, weather by weather."
    )

    tabs = st.tabs(["Policy Simulator", "Fairness Analysis"])

    with tabs[0]:
        st.markdown("### Policy Simulator")
        st.markdown("")

        col_form, col_result = st.columns([1, 1.4], gap="large")

        with col_form:
            p_distance = st.number_input("Distance (km)", 1.0, 30.0, 7.0, 0.5, key="ps_dist")
            p_vehicle = st.selectbox("Vehicle", ["Bike", "Auto", "Mini", "Sedan", "SUV", "Prime"], index=2, key="ps_veh")
            p_hour = st.selectbox("Hour", list(range(24)), index=18, key="ps_hour")
            p_weather = st.selectbox("Weather", ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"], index=4, key="ps_weather")
            p_captive = st.selectbox("Captive quartile", ["Low", "Medium", "High", "Extreme"], index=3, key="ps_captive")
            st.markdown("")
            if st.button("Compare Policies", key="ps_btn", use_container_width=True):
                st.session_state.ps_result = {
                    "baseline": _calc_scenario(p_distance, p_vehicle, p_hour, p_weather, p_captive, apply_policy=False),
                    "calyber": _calc_scenario(p_distance, p_vehicle, p_hour, p_weather, p_captive, apply_policy=True)
                }

        with col_result:
            if "ps_result" in st.session_state:
                r = st.session_state.ps_result
                comparison_card(
                    "Baseline (Current System)", "Rs " + str(r["baseline"]["fare"]),
                    "Calyber (Fair Policy)", "Rs " + str(r["calyber"]["fare"]),
                    savings=round(r["baseline"]["fare"] - r["calyber"]["fare"], 2)
                )
                st.markdown("#### Surge comparison")
                metric_row([
                    {"label": "Baseline Surge", "value": str(r["baseline"]["surge"]) + "x", "color": "#DC2626"},
                    {"label": "Calyber Surge", "value": str(r["calyber"]["surge"]) + "x", "color": "#059669"},
                ])
            else:
                st.markdown(
                    '<div style="background:#F8FAFC; border:1px dashed #E5E7EB; '
                    'border-radius:14px; padding:80px 24px; text-align:center; '
                    'color:#94A3B8; font-size:14px;">'
                    'Policy comparison will appear here.'
                    '</div>',
                    unsafe_allow_html=True
                )

    with tabs[1]:
        st.markdown("### Fairness Analysis")
        st.markdown("Where does the pricing system fail?")
        st.markdown("")

        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("#### Surge by Weather")
            bar_chart(weather_df, "Weather", "Baseline_Surge", color="#D97706", height=300)
        with col2:
            st.markdown("#### Surge by Captive Quartile")
            bar_chart(captive_df, "Captive_Quartile", "Baseline_Surge", color="#DC2626", height=300)

        st.markdown("#### Baseline vs Calyber by Captive Quartile")
        dual_bar_chart(captive_df, "Captive_Quartile", "Baseline_Surge", "Calyber_Surge", height=340)

        callout(
            "Key Finding",
            "Extreme captive riders pay 43.7% more surge than low captive riders. This is systemic.",
            color="#DC2626"
        )


# ============================================================
# DATA
# ============================================================
elif st.session_state.section == "Data":
    render_nav()
    st.markdown("---")

    section_hero(
        "DATA",
        "Explore the source.",
        "54,132 Mumbai trips. Filter by weather, captive quartile, or vehicle type. Every row is a real pricing decision."
    )

    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        weather_filter = st.selectbox("Weather", ["All"] + list(trips_df["Weather_Condition"].unique()), key="d_weather")
    with col2:
        captive_filter = st.selectbox("Captive Quartile", ["All"] + list(trips_df["captive_quartile"].unique()), key="d_captive")
    with col3:
        vehicle_filter = st.selectbox("Vehicle", ["All"] + list(trips_df["Vehicle_Type"].unique()), key="d_vehicle")

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

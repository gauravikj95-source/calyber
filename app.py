import streamlit as st
import pandas as pd
import sys
import os

# ============================================================
# PATH SETUP
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# ============================================================
# IMPORTS
# ============================================================

from predictions import (
    load_model,
    load_surge_patterns,
    predict_fare_forecast,
    predict_fairness_score,
    predict_wait_time,
    predict_cancellation_risk,
    predict_surge_timing,
    detect_anomaly,
    recommend_vehicle,
    compare_route,
    what_if_analysis,
    _calc_scenario
)

from components import (
    COLORS,
    hero_header,
    hero_card,
    section_label,
    section_header,
    section_hero,
    section_divider,
    kpi_card,
    kpi_row,
    card_label,
    result_card,
    comparison_card,
    fairness_badge,
    metric_row,
    callout,
    bar_chart,
    line_chart,
    donut_chart,
    dual_bar_chart,
    trip_context_widget
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Calyber",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# LOAD CSS
# ============================================================

def load_css():

    css_path = os.path.join(
        BASE_DIR,
        "styles.css"
    )

    if os.path.exists(css_path):

        with open(
            css_path,
            "r",
            encoding="utf-8"
        ) as f:

            st.markdown(
                "<style>" + f.read() + "</style>",
                unsafe_allow_html=True
            )


load_css()


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    return (
        pd.read_csv(
            os.path.join(
                BASE_DIR,
                "pbi_trips.csv"
            )
        ),

        pd.read_csv(
            os.path.join(
                BASE_DIR,
                "pbi_captive.csv"
            )
        ),

        pd.read_csv(
            os.path.join(
                BASE_DIR,
                "pbi_weather.csv"
            )
        ),

        pd.read_csv(
            os.path.join(
                BASE_DIR,
                "pbi_kpi.csv"
            )
        ),

        pd.read_csv(
            os.path.join(
                BASE_DIR,
                "pbi_demand.csv"
            )
        )
    )


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model_data():

    try:

        model = load_model(
            os.path.join(
                BASE_DIR,
                "demand_model.pkl"
            )
        )

        load_surge_patterns(
            os.path.join(
                BASE_DIR,
                "surge_patterns.csv"
            )
        )

        return model

    except Exception:

        return None


# ============================================================
# INITIALIZE DATA
# ============================================================

trips_df, captive_df, weather_df, kpi_df, demand_df = load_data()

model_data = load_model_data()


# ============================================================
# INITIALIZE NAVIGATION
# ============================================================

if "section" not in st.session_state:

    st.session_state.section = "Overview"


# ============================================================
# NAVIGATION
# ============================================================

def render_nav():

    nav_items = [
        "Overview",
        "Predict",
        "Decide",
        "Compare",
        "Data"
    ]

    cols = st.columns(
        len(nav_items),
        gap="small"
    )

    for col, item in zip(
        cols,
        nav_items
    ):

        with col:

            is_active = (
                st.session_state.section == item
            )

            btn_type = (
                "primary"
                if is_active
                else "secondary"
            )

            if st.button(
                item,
                key="nav_" + item,
                use_container_width=True,
                type=btn_type
            ):

                st.session_state.section = item

                st.rerun()


# ============================================================
# TAB BAR
# ============================================================

def tab_bar(
    items,
    key_prefix
):

    state_key = (
        key_prefix +
        "_selected"
    )

    if state_key not in st.session_state:

        st.session_state[state_key] = items[0]

    cols = st.columns(
        len(items),
        gap="small"
    )

    for col, item in zip(
        cols,
        items
    ):

        with col:

            is_active = (
                st.session_state[state_key]
                == item
            )

            btn_type = (
                "primary"
                if is_active
                else "secondary"
            )

            if st.button(
                item,
                key=key_prefix + "_" + item,
                use_container_width=True,
                type=btn_type
            ):

                st.session_state[state_key] = item

                st.rerun()

    return st.session_state[state_key]


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

    kpi_row(
        [
            {
                "label": "Trips Analyzed",
                "value": "54,132"
            },
            {
                "label": "Average Surge Premium",
                "value": "34.79%",
                "color": "#DC2626"
            },
            {
                "label": "Extreme Surge Trips",
                "value": "1,145",
                "color": "#DC2626"
            },
            {
                "label": "Revenue Impact of Fair Policy",
                "value": "-6.61%",
                "color": "#D97706"
            }
        ]
    )

    section_header(
        "What Calyber Does",
        "Three layers: prediction, decision, and comparison."
    )

    col1, col2, col3 = st.columns(
        3,
        gap="medium"
    )

    with col1:

        st.markdown("**Predict**")

        st.markdown(
            "Forecast fares, wait times, cancellation risk, and fairness grades before you book."
        )

    with col2:

        st.markdown("**Decide**")

        st.markdown(
            "Compare vehicles, routes, and what-if scenarios to make an informed choice."
        )

    with col3:

        st.markdown("**Compare**")

        st.markdown(
            "See how the Calyber fair-pricing policy differs from the current system."
        )


# ============================================================
# PREDICT
# SHARED TRIP CONTEXT
# ============================================================

elif st.session_state.section == "Predict":

    render_nav()

    st.markdown("---")

    section_hero(
        "PREDICT",
        "See the price before you book.",
        "Six prediction tools built on 54,132 Mumbai trips. Set your trip once, then explore every prediction."
    )

    # --------------------------------------------------------
    # SHARED TRIP CONTEXT
    # --------------------------------------------------------

    ctx = trip_context_widget(
        key_prefix="trip"
    )

    # --------------------------------------------------------
    # PREDICT TABS
    # --------------------------------------------------------

    active_tab = tab_bar(
        [
            "Fare Forecast",
            "Fairness Score",
            "Wait Time",
            "Cancellation Risk",
            "Surge Timing",
            "Anomaly Detection"
        ],
        key_prefix="predict_tabs"
    )

    st.markdown("---")


    # ========================================================
    # FARE FORECAST
    # ========================================================

    if active_tab == "Fare Forecast":

        st.markdown("### Fare Forecast")

        st.markdown(
            "Predict your fare for the next 2 hours."
        )

        r = predict_fare_forecast(
            "Andheri",
            "BKC",
            ctx["distance"],
            ctx["vehicle"],
            ctx["hour"],
            ctx["weather"],
            ctx["day"]
        )

        kpi_row(
            [
                {
                    "label": "Fare Now",
                    "value": "Rs " + str(
                        r["current_fare"]
                    )
                },
                {
                    "label": "Best Fare",
                    "value": "Rs " + str(
                        r["best_fare"]
                    ),
                    "color": "#059669"
                },
                {
                    "label": "Best Time",
                    "value": r["best_time"],
                    "color": "#059669"
                },
                {
                    "label": "Savings",
                    "value": "Rs " + str(
                        r["savings"]
                    )
                }
            ]
        )

        fdf = pd.DataFrame(
            r["forecasts"]
        )

        line_chart(
            fdf,
            "time_label",
            "fare",
            color="#0F172A",
            height=340
        )


    # ========================================================
    # FAIRNESS SCORE
    # ========================================================

    elif active_tab == "Fairness Score":

        st.markdown(
            "### Fairness Score"
        )

        st.markdown(
            "Will this ride be fair?"
        )

        r = predict_fairness_score(
            ctx["weather"],
            ctx["hour"],
            ctx["captive"],
            ctx["vehicle"]
        )

        col1, col2 = st.columns(
            [1, 1],
            gap="large"
        )

        with col1:

            fairness_badge(
                r["grade"],
                r["label"],
                r["color"]
            )

        with col2:

            metric_row(
                [
                    {
                        "label": "Surge",
                        "value": str(
                            r["surge"]
                        ) + "x"
                    },
                    {
                        "label": "Premium",
                        "value": str(
                            r["premium_pct"]
                        ) + "%",
                        "color": r["color"]
                    }
                ]
            )


    # ========================================================
    # WAIT TIME
    # ========================================================

    elif active_tab == "Wait Time":

        st.markdown(
            "### Wait Time Forecast"
        )

        r = predict_wait_time(
            ctx["weather"],
            ctx["hour"],
            ctx["captive"]
        )

        kpi_row(
            [
                {
                    "label": "Predicted Wait",
                    "value": str(
                        r["wait_min"]
                    ) + " min"
                },
                {
                    "label": "Range",
                    "value": (
                        str(r["wait_range"][0])
                        + "-"
                        + str(r["wait_range"][1])
                        + " min"
                    )
                }
            ]
        )


    # ========================================================
    # CANCELLATION RISK
    # ========================================================

    elif active_tab == "Cancellation Risk":

        st.markdown(
            "### Cancellation Risk"
        )

        r = predict_cancellation_risk(
            ctx["weather"],
            ctx["traffic"],
            ctx["vehicle"],
            ctx["hour"]
        )

        kpi_row(
            [
                {
                    "label": "Cancellation Risk",
                    "value": str(
                        r["risk_pct"]
                    ) + "%",
                    "color": r["color"]
                },
                {
                    "label": "Level",
                    "value": r["level"],
                    "color": r["color"]
                }
            ]
        )


    # ========================================================
    # SURGE TIMING
    # ========================================================

    elif active_tab == "Surge Timing":

        st.markdown(
            "### Surge Timing"
        )

        r = predict_surge_timing(
            ctx["weather"],
            ctx["day"]
        )

        tdf = pd.DataFrame(
            r["timeline"]
        )

        line_chart(
            tdf,
            "time_label",
            "surge",
            color="#DC2626",
            height=340
        )

        kpi_row(
            [
                {
                    "label": "Peak Hour",
                    "value": r["peak_hour"],
                    "color": "#DC2626"
                },
                {
                    "label": "Peak Surge",
                    "value": str(
                        r["peak_surge"]
                    ) + "x",
                    "color": "#DC2626"
                },
                {
                    "label": "Lowest Hour",
                    "value": r["lowest_hour"],
                    "color": "#059669"
                },
                {
                    "label": "Lowest Surge",
                    "value": str(
                        r["lowest_surge"]
                    ) + "x",
                    "color": "#059669"
                }
            ]
        )


    # ========================================================
    # ANOMALY DETECTION
    # ========================================================

    elif active_tab == "Anomaly Detection":

        st.markdown(
            "### Anomaly Detection"
        )

        st.markdown(
            "Enter the fare you actually paid. Everything else comes from your trip above."
        )

        actual_fare = st.number_input(
            "Actual fare paid (Rs)",
            min_value=10.0,
            max_value=5000.0,
            value=420.0,
            step=10.0,
            key="an_fare"
        )

        r = detect_anomaly(
            actual_fare,
            ctx["distance"],
            ctx["vehicle"],
            ctx["weather"],
            ctx["hour"]
        )

        kpi_row(
            [
                {
                    "label": "Status",
                    "value": r["status"],
                    "color": r["color"]
                },
                {
                    "label": "Actual Fare",
                    "value": "Rs " + str(
                        r["actual_fare"]
                    )
                },
                {
                    "label": "Expected Fare",
                    "value": "Rs " + str(
                        r["expected_fare"]
                    ),
                    "color": "#059669"
                },
                {
                    "label": "Deviation",
                    "value": str(
                        r["deviation_pct"]
                    ) + "%",
                    "color": r["color"]
                }
            ]
        )


# ============================================================
# DECIDE
# INDEPENDENT INPUTS
# ============================================================

elif st.session_state.section == "Decide":

    render_nav()

    st.markdown("---")

    section_hero(
        "DECIDE",
        "Make an informed choice.",
        "Three tools to compare vehicles, routes, and what-if scenarios. Understand the trade-offs before you decide."
    )

    active_tab = tab_bar(
        [
            "Vehicle Recommender",
            "Route Comparison",
            "What-If Explorer"
        ],
        key_prefix="decide_tabs"
    )

    st.markdown("---")


    # ========================================================
    # VEHICLE RECOMMENDER
    # ========================================================

    if active_tab == "Vehicle Recommender":

        st.markdown(
            "### Vehicle Recommender"
        )

        col_form, col_result = st.columns(
            [1, 1.4],
            gap="large"
        )

        with col_form:

            v_distance = st.number_input(
                "Distance (km)",
                min_value=1.0,
                max_value=30.0,
                value=7.0,
                step=0.5,
                key="vr_dist"
            )

            v_priority = st.radio(
                "Priority",
                [
                    "cheapest",
                    "fastest",
                    "fairest"
                ],
                horizontal=True,
                key="vr_priority"
            )

            v_hour = st.selectbox(
                "Hour",
                list(range(24)),
                index=18,
                key="vr_hour"
            )

            v_weather = st.selectbox(
                "Weather",
                [
                    "Clear",
                    "Cloudy",
                    "Foggy",
                    "Rainy",
                    "Stormy"
                ],
                index=3,
                key="vr_weather"
            )

        with col_result:

            r = recommend_vehicle(
                v_distance,
                v_priority,
                v_hour,
                v_weather
            )

            rec = r["recommended"]

            kpi_row(
                [
                    {
                        "label": "Recommended",
                        "value": rec["vehicle"],
                        "color": "#059669"
                    },
                    {
                        "label": "Fare",
                        "value": "Rs " + str(
                            rec["fare"]
                        )
                    },
                    {
                        "label": "Wait",
                        "value": str(
                            rec["wait"]
                        ) + " min"
                    }
                ]
            )

            st.markdown(
                "#### All options"
            )

            st.dataframe(
                pd.DataFrame(
                    r["all_options"]
                ),
                use_container_width=True
            )


    # ========================================================
    # ROUTE COMPARISON
    # ========================================================

    elif active_tab == "Route Comparison":

        st.markdown(
            "### Route Comparison"
        )

        col_form, col_result = st.columns(
            [1, 1.4],
            gap="large"
        )

        with col_form:

            r_distance = st.number_input(
                "Distance (km)",
                min_value=1.0,
                max_value=30.0,
                value=7.2,
                step=0.1,
                key="rc_dist"
            )

            r_vehicle = st.selectbox(
                "Vehicle",
                [
                    "Bike",
                    "Auto",
                    "Mini",
                    "Sedan",
                    "SUV",
                    "Prime"
                ],
                index=2,
                key="rc_veh"
            )

            r_hour = st.selectbox(
                "Hour",
                list(range(24)),
                index=18,
                key="rc_hour"
            )

            r_weather = st.selectbox(
                "Weather",
                [
                    "Clear",
                    "Cloudy",
                    "Foggy",
                    "Rainy",
                    "Stormy"
                ],
                index=3,
                key="rc_weather"
            )

        with col_result:

            r = compare_route(
                r_distance,
                r_vehicle,
                r_hour,
                r_weather
            )

            kpi_row(
                [
                    {
                        "label": "Predicted Fare",
                        "value": "Rs " + str(
                            r["predicted_fare"]
                        )
                    },
                    {
                        "label": "Historical Average",
                        "value": "Rs " + str(
                            r["historical_avg"]
                        )
                    },
                    {
                        "label": "Disparity",
                        "value": str(
                            r["disparity_pct"]
                        ) + "%",
                        "color": r["color"]
                    },
                    {
                        "label": "Status",
                        "value": r["status"],
                        "color": r["color"]
                    }
                ]
            )


    # ========================================================
    # WHAT-IF EXPLORER
    # ========================================================

    elif active_tab == "What-If Explorer":

        st.markdown(
            "### What-If Explorer"
        )

        col_form, col_result = st.columns(
            [1, 1.4],
            gap="large"
        )

        with col_form:

            wi_distance = st.number_input(
                "Distance (km)",
                min_value=1.0,
                max_value=30.0,
                value=7.0,
                step=0.5,
                key="wi_dist"
            )

            wi_vehicle = st.selectbox(
                "Vehicle",
                [
                    "Bike",
                    "Auto",
                    "Mini",
                    "Sedan",
                    "SUV",
                    "Prime"
                ],
                index=2,
                key="wi_veh"
            )

            wi_hour = st.selectbox(
                "Hour",
                list(range(24)),
                index=18,
                key="wi_hour"
            )

            wi_weather = st.selectbox(
                "Weather",
                [
                    "Clear",
                    "Cloudy",
                    "Foggy",
                    "Rainy",
                    "Stormy"
                ],
                index=4,
                key="wi_weather"
            )

            wi_captive = st.selectbox(
                "Captive quartile",
                [
                    "Low",
                    "Medium",
                    "High",
                    "Extreme"
                ],
                index=3,
                key="wi_captive"
            )

        with col_result:

            r = what_if_analysis(
                wi_distance,
                wi_vehicle,
                wi_hour,
                wi_weather,
                wi_captive
            )

            kpi_card(
                "Current Fare",
                "Rs " + str(
                    r["current_fare"]
                ),
                color="#DC2626"
            )

            st.markdown(
                "#### Scenarios"
            )

            for s in r["scenarios"]:

                st.markdown(
                    "- **"
                    + str(s["label"])
                    + "**: Rs "
                    + str(s["fare"])
                    + " ("
                    + str(s["change"])
                    + ")"
                )


# ============================================================
# COMPARE
# SHARED TRIP CONTEXT
# ============================================================

elif st.session_state.section == "Compare":

    render_nav()

    st.markdown("---")

    section_hero(
        "COMPARE",
        "Baseline vs Calyber.",
        "See how the fairness-aware policy differs from the current system, fare by fare."
    )

    # --------------------------------------------------------
    # IMPORTANT:
    # SAME KEY AS PREDICT
    # --------------------------------------------------------

    ctx = trip_context_widget(
        key_prefix="trip"
    )

    active_tab = tab_bar(
        [
            "Policy Simulator",
            "Fairness Analysis"
        ],
        key_prefix="compare_tabs"
    )

    st.markdown("---")


    # ========================================================
    # POLICY SIMULATOR
    # ========================================================

    if active_tab == "Policy Simulator":

        st.markdown(
            "### Policy Simulator"
        )

        baseline = _calc_scenario(
            ctx["distance"],
            ctx["vehicle"],
            ctx["hour"],
            ctx["weather"],
            ctx["captive"],
            apply_policy=False
        )

        calyber = _calc_scenario(
            ctx["distance"],
            ctx["vehicle"],
            ctx["hour"],
            ctx["weather"],
            ctx["captive"],
            apply_policy=True
        )

        comparison_card(
            "Baseline (Current System)",
            "Rs " + str(
                baseline["fare"]
            ),
            "Calyber (Fair Policy)",
            "Rs " + str(
                calyber["fare"]
            ),
            savings=round(
                baseline["fare"]
                - calyber["fare"],
                2
            )
        )

        st.markdown(
            "#### Surge comparison"
        )

        metric_row(
            [
                {
                    "label": "Baseline Surge",
                    "value": str(
                        baseline["surge"]
                    ) + "x",
                    "color": "#DC2626"
                },
                {
                    "label": "Calyber Surge",
                    "value": str(
                        calyber["surge"]
                    ) + "x",
                    "color": "#059669"
                }
            ]
        )


    # ========================================================
    # FAIRNESS ANALYSIS
    # ========================================================

    elif active_tab == "Fairness Analysis":

        st.markdown(
            "### Fairness Analysis"
        )

        st.markdown(
            "Where does the pricing system fail?"
        )

        col1, col2 = st.columns(
            2,
            gap="large"
        )

        with col1:

            st.markdown(
                "#### Surge by Weather"
            )

            bar_chart(
                weather_df,
                "Weather",
                "Baseline_Surge",
                color="#D97706",
                height=300
            )

        with col2:

            st.markdown(
                "#### Surge by Captive Quartile"
            )

            bar_chart(
                captive_df,
                "Captive_Quartile",
                "Baseline_Surge",
                color="#DC2626",
                height=300
            )

        st.markdown(
            "#### Baseline vs Calyber by Captive Quartile"
        )

        dual_bar_chart(
            captive_df,
            "Captive_Quartile",
            "Baseline_Surge",
            "Calyber_Surge",
            height=340
        )

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
        "54,132 Mumbai trips. Filter by weather, captive quartile, or vehicle type."
    )

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(
        3,
        gap="medium"
    )

    with col1:

        weather_filter = st.selectbox(
            "Weather",
            [
                "All"
            ]
            + list(
                trips_df[
                    "Weather_Condition"
                ].dropna().unique()
            ),
            key="d_weather"
        )

    with col2:

        captive_filter = st.selectbox(
            "Captive Quartile",
            [
                "All"
            ]
            + list(
                trips_df[
                    "captive_quartile"
                ].dropna().unique()
            ),
            key="d_captive"
        )

    with col3:

        vehicle_filter = st.selectbox(
            "Vehicle",
            [
                "All"
            ]
            + list(
                trips_df[
                    "Vehicle_Type"
                ].dropna().unique()
            ),
            key="d_vehicle"
        )


    # --------------------------------------------------------
    # FILTER DATA
    # --------------------------------------------------------

    filtered = trips_df.copy()

    if weather_filter != "All":

        filtered = filtered[
            filtered[
                "Weather_Condition"
            ] == weather_filter
        ]

    if captive_filter != "All":

        filtered = filtered[
            filtered[
                "captive_quartile"
            ] == captive_filter
        ]

    if vehicle_filter != "All":

        filtered = filtered[
            filtered[
                "Vehicle_Type"
            ] == vehicle_filter
        ]


    # --------------------------------------------------------
    # RESULT COUNT
    # --------------------------------------------------------

    st.markdown(
        "**Showing "
        + str(len(filtered))
        + " of "
        + str(len(trips_df))
        + " trips**"
    )


    # --------------------------------------------------------
    # DISPLAY TABLE
    # --------------------------------------------------------

    display_cols = [
        "Trip_ID",
        "Weather_Condition",
        "Vehicle_Type",
        "Distance_KM",
        "Surge_Multiplier",
        "Total_Fare",
        "captive_quartile",
        "fairness_band"
    ]

    display_cols = [
        c
        for c in display_cols
        if c in filtered.columns
    ]

    st.dataframe(
        filtered[
            display_cols
        ].head(500),
        use_container_width=True,
        height=500
    )

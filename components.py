import streamlit as st
import plotly.graph_objects as go


# ============================================================
# COLORS
# ============================================================

COLORS = {
    "navy": "#0F172A",
    "slate": "#64748B",
    "light": "#F8FAFC",
    "border": "#E5E7EB",
    "white": "#FFFFFF",

    "green": "#059669",
    "red": "#DC2626",
    "orange": "#D97706",
    "blue": "#2563EB",
    "purple": "#7C3AED",

    "text": "#0F172A",
    "muted": "#64748B",
}


# ============================================================
# HERO HEADER
# ============================================================

def hero_header(title, subtitle, description=None):
    """
    Main page hero header.
    """

    st.markdown(
        f"""
        <div style="
            padding: 10px 0 20px 0;
        ">
            <div style="
                color:#64748B;
                font-size:11px;
                font-weight:600;
                letter-spacing:0.14em;
                text-transform:uppercase;
                margin-bottom:8px;
            ">
                {title}
            </div>

            <div style="
                color:#0F172A;
                font-size:32px;
                font-weight:700;
                line-height:1.15;
                margin-bottom:10px;
            ">
                {subtitle}
            </div>

            {
                f'''
                <div style="
                    color:#64748B;
                    font-size:15px;
                    line-height:1.6;
                    max-width:850px;
                ">
                    {description}
                </div>
                '''
                if description
                else ""
            }
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HERO CARD
# ============================================================

def hero_card(label, title, description=None):
    """
    Large problem / information card.
    """

    st.markdown(
        f"""
        <div style="
            background:#F8FAFC;
            border:1px solid #E5E7EB;
            border-radius:16px;
            padding:28px;
            margin:12px 0 24px 0;
        ">
            <div style="
                color:#64748B;
                font-size:11px;
                font-weight:600;
                letter-spacing:0.12em;
                text-transform:uppercase;
                margin-bottom:10px;
            ">
                {label}
            </div>

            <div style="
                color:#0F172A;
                font-size:22px;
                font-weight:700;
                line-height:1.35;
                margin-bottom:10px;
            ">
                {title}
            </div>

            {
                f'''
                <div style="
                    color:#64748B;
                    font-size:14px;
                    line-height:1.6;
                ">
                    {description}
                </div>
                '''
                if description
                else ""
            }
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SECTION LABEL
# ============================================================

def section_label(text):
    """
    Small uppercase section label.
    """

    st.markdown(
        f"""
        <div style="
            color:#64748B;
            font-size:11px;
            font-weight:600;
            letter-spacing:0.12em;
            text-transform:uppercase;
            margin:20px 0 8px 0;
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SECTION HEADER
# ============================================================

def section_header(title, subtitle=None):
    """
    Section heading with optional subtitle.
    """

    st.markdown(
        f"""
        <div style="margin:20px 0 16px 0;">
            <div style="
                color:#0F172A;
                font-size:22px;
                font-weight:700;
                margin-bottom:6px;
            ">
                {title}
            </div>

            {
                f'''
                <div style="
                    color:#64748B;
                    font-size:14px;
                ">
                    {subtitle}
                </div>
                '''
                if subtitle
                else ""
            }
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SECTION HERO
# ============================================================

def section_hero(title, subtitle, description=None):
    """
    Hero block for Predict / Decide / Compare / Data sections.
    """

    st.markdown(
        f"""
        <div style="
            padding:8px 0 18px 0;
        ">
            <div style="
                color:#64748B;
                font-size:11px;
                font-weight:600;
                letter-spacing:0.14em;
                text-transform:uppercase;
                margin-bottom:8px;
            ">
                {title}
            </div>

            <div style="
                color:#0F172A;
                font-size:28px;
                font-weight:700;
                line-height:1.2;
                margin-bottom:8px;
            ">
                {subtitle}
            </div>

            {
                f'''
                <div style="
                    color:#64748B;
                    font-size:14px;
                    line-height:1.6;
                    max-width:850px;
                ">
                    {description}
                </div>
                '''
                if description
                else ""
            }
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SECTION DIVIDER
# ============================================================

def section_divider():
    st.markdown(
        """
        <div style="
            height:1px;
            background:#E5E7EB;
            margin:24px 0;
        "></div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CARD LABEL
# ============================================================

def card_label(text):
    st.markdown(
        f"""
        <div style="
            color:#64748B;
            font-size:11px;
            font-weight:600;
            letter-spacing:0.08em;
            text-transform:uppercase;
            margin-bottom:6px;
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# KPI CARD
# ============================================================

def kpi_card(label, value, color=None):
    """
    Single KPI card.
    """

    if color is None:
        color = "#0F172A"

    st.markdown(
        f"""
        <div style="
            background:#FFFFFF;
            border:1px solid #E5E7EB;
            border-radius:14px;
            padding:18px 20px;
            min-height:100px;
        ">
            <div style="
                color:#64748B;
                font-size:11px;
                font-weight:600;
                letter-spacing:0.08em;
                text-transform:uppercase;
                margin-bottom:8px;
            ">
                {label}
            </div>

            <div style="
                color:{color};
                font-size:25px;
                font-weight:700;
                line-height:1.2;
            ">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# KPI ROW
# ============================================================

def kpi_row(items):
    """
    Displays multiple KPI cards in one row.

    Example:
        kpi_row([
            {"label": "Fare", "value": "Rs 420"},
            {"label": "Surge", "value": "1.4x", "color": "#DC2626"}
        ])
    """

    cols = st.columns(len(items), gap="medium")

    for col, item in zip(cols, items):
        with col:
            kpi_card(
                item["label"],
                item["value"],
                item.get("color")
            )


# ============================================================
# RESULT CARD
# ============================================================

def result_card(title, value, description=None, color=None):
    """
    Result card for model outputs.
    """

    if color is None:
        color = "#0F172A"

    st.markdown(
        f"""
        <div style="
            background:#FFFFFF;
            border:1px solid #E5E7EB;
            border-radius:14px;
            padding:22px;
            margin:8px 0;
        ">
            <div style="
                color:#64748B;
                font-size:11px;
                font-weight:600;
                letter-spacing:0.08em;
                text-transform:uppercase;
                margin-bottom:8px;
            ">
                {title}
            </div>

            <div style="
                color:{color};
                font-size:30px;
                font-weight:700;
                margin-bottom:8px;
            ">
                {value}
            </div>

            {
                f'''
                <div style="
                    color:#64748B;
                    font-size:13px;
                    line-height:1.5;
                ">
                    {description}
                </div>
                '''
                if description
                else ""
            }
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# COMPARISON CARD
# ============================================================

def comparison_card(
    title1,
    value1,
    title2,
    value2,
    savings=None
):
    """
    Baseline vs Calyber comparison card.
    """

    savings_html = ""

    if savings is not None:
        savings_html = f"""
        <div style="
            margin-top:16px;
            padding-top:14px;
            border-top:1px solid #E5E7EB;
            color:#059669;
            font-size:14px;
            font-weight:600;
        ">
            Difference: Rs {savings}
        </div>
        """

    st.markdown(
        f"""
        <div style="
            background:#FFFFFF;
            border:1px solid #E5E7EB;
            border-radius:16px;
            padding:24px;
            margin:10px 0 20px 0;
        ">

            <div style="
                display:flex;
                gap:40px;
                justify-content:space-between;
            ">

                <div style="flex:1;">
                    <div style="
                        color:#64748B;
                        font-size:11px;
                        font-weight:600;
                        letter-spacing:0.08em;
                        text-transform:uppercase;
                        margin-bottom:8px;
                    ">
                        {title1}
                    </div>

                    <div style="
                        color:#DC2626;
                        font-size:30px;
                        font-weight:700;
                    ">
                        {value1}
                    </div>
                </div>

                <div style="
                    width:1px;
                    background:#E5E7EB;
                "></div>

                <div style="flex:1;">
                    <div style="
                        color:#64748B;
                        font-size:11px;
                        font-weight:600;
                        letter-spacing:0.08em;
                        text-transform:uppercase;
                        margin-bottom:8px;
                    ">
                        {title2}
                    </div>

                    <div style="
                        color:#059669;
                        font-size:30px;
                        font-weight:700;
                    ">
                        {value2}
                    </div>
                </div>

            </div>

            {savings_html}

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FAIRNESS BADGE
# ============================================================

def fairness_badge(grade, label, color):
    """
    Displays A-F fairness grade.
    """

    st.markdown(
        f"""
        <div style="
            background:#FFFFFF;
            border:1px solid #E5E7EB;
            border-radius:16px;
            padding:24px;
            text-align:center;
        ">

            <div style="
                width:90px;
                height:90px;
                border-radius:50%;
                background:{color};
                color:white;
                display:flex;
                align-items:center;
                justify-content:center;
                margin:0 auto 16px auto;
                font-size:42px;
                font-weight:700;
            ">
                {grade}
            </div>

            <div style="
                color:#0F172A;
                font-size:20px;
                font-weight:700;
                margin-bottom:6px;
            ">
                {label}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# METRIC ROW
# ============================================================

def metric_row(items):
    """
    Horizontal metric display.
    """

    cols = st.columns(len(items), gap="medium")

    for col, item in zip(cols, items):

        color = item.get("color", "#0F172A")

        with col:
            st.markdown(
                f"""
                <div style="
                    padding:14px 0;
                ">
                    <div style="
                        color:#64748B;
                        font-size:12px;
                        margin-bottom:4px;
                    ">
                        {item["label"]}
                    </div>

                    <div style="
                        color:{color};
                        font-size:24px;
                        font-weight:700;
                    ">
                        {item["value"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# CALLOUT
# ============================================================

def callout(title, text, color="#2563EB"):
    """
    Highlighted information callout.
    """

    st.markdown(
        f"""
        <div style="
            background:#F8FAFC;
            border-left:4px solid {color};
            border-radius:8px;
            padding:16px 18px;
            margin:18px 0;
        ">

            <div style="
                color:#0F172A;
                font-size:14px;
                font-weight:700;
                margin-bottom:5px;
            ">
                {title}
            </div>

            <div style="
                color:#64748B;
                font-size:13px;
                line-height:1.6;
            ">
                {text}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# BAR CHART
# ============================================================

def bar_chart(df, x, y, color="#2563EB", height=350):
    """
    Simple Plotly bar chart.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df[x],
            y=df[y],
            marker_color=color
        )
    )

    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(
            color="#0F172A"
        ),
        xaxis=dict(
            showgrid=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#E5E7EB"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# LINE CHART
# ============================================================

def line_chart(df, x, y, color="#0F172A", height=350):
    """
    Simple Plotly line chart.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df[x],
            y=df[y],
            mode="lines+markers",
            line=dict(
                color=color,
                width=3
            ),
            marker=dict(
                size=6
            )
        )
    )

    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(
            color="#0F172A"
        ),
        xaxis=dict(
            showgrid=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#E5E7EB"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# DONUT CHART
# ============================================================

def donut_chart(labels, values, height=350):
    """
    Donut chart.
    """

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.55
            )
        ]
    )

    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="white",
        showlegend=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# DUAL BAR CHART
# ============================================================

def dual_bar_chart(
    df,
    x,
    y1,
    y2,
    height=350
):
    """
    Two-series comparison bar chart.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df[x],
            y=df[y1],
            name=y1,
            marker_color="#DC2626"
        )
    )

    fig.add_trace(
        go.Bar(
            x=df[x],
            y=df[y2],
            name=y2,
            marker_color="#059669"
        )
    )

    fig.update_layout(
        barmode="group",
        height=height,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(
            color="#0F172A"
        ),
        xaxis=dict(
            showgrid=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#E5E7EB"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# SHARED TRIP CONTEXT
# ============================================================

def trip_context_widget(key_prefix="trip"):
    """
    Shared trip context widget.

    The user enters trip information once.

    Any part of the app that calls:

        trip_context_widget(key_prefix="trip")

    will use the same widget state.

    Returns:
        dict containing the current trip parameters.
    """

    # --------------------------------------------------------
    # INITIAL DEFAULT VALUES
    # --------------------------------------------------------

    if "trip_context" not in st.session_state:

        st.session_state.trip_context = {
            "distance": 7.0,
            "vehicle": "Mini",
            "hour": 18,
            "weather": "Stormy",
            "captive": "Extreme",
            "traffic": "High",
            "day": "Monday",
            "priority": "cheapest"
        }

    ctx = st.session_state.trip_context

    # --------------------------------------------------------
    # OPTIONS
    # --------------------------------------------------------

    vehicles = [
        "Bike",
        "Auto",
        "Mini",
        "Sedan",
        "SUV",
        "Prime"
    ]

    weathers = [
        "Clear",
        "Cloudy",
        "Foggy",
        "Rainy",
        "Stormy"
    ]

    captives = [
        "Low",
        "Medium",
        "High",
        "Extreme"
    ]

    traffics = [
        "Low",
        "Medium",
        "High",
        "Severe"
    ]

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    priorities = [
        "cheapest",
        "fastest",
        "fairest"
    ]

    # --------------------------------------------------------
    # HEADER CARD
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="
            background:#F8FAFC;
            border:1px solid #E5E7EB;
            border-radius:14px;
            padding:20px 24px 8px 24px;
            margin-bottom:16px;
        ">

            <div style="
                color:#64748B;
                font-size:11px;
                font-weight:600;
                letter-spacing:0.12em;
                text-transform:uppercase;
            ">
                YOUR TRIP
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # FIRST ROW
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(
        3,
        gap="medium"
    )

    # Distance + Vehicle
    with col1:

        ctx["distance"] = st.number_input(
            "Distance (km)",
            min_value=1.0,
            max_value=30.0,
            value=float(ctx["distance"]),
            step=0.5,
            key=f"{key_prefix}_distance"
        )

        ctx["vehicle"] = st.selectbox(
            "Vehicle",
            vehicles,
            index=vehicles.index(ctx["vehicle"]),
            key=f"{key_prefix}_vehicle"
        )

    # Hour + Weather
    with col2:

        ctx["hour"] = st.selectbox(
            "Hour",
            list(range(24)),
            index=int(ctx["hour"]),
            key=f"{key_prefix}_hour"
        )

        ctx["weather"] = st.selectbox(
            "Weather",
            weathers,
            index=weathers.index(ctx["weather"]),
            key=f"{key_prefix}_weather"
        )

    # Captive + Traffic
    with col3:

        ctx["captive"] = st.selectbox(
            "Captive Quartile",
            captives,
            index=captives.index(ctx["captive"]),
            key=f"{key_prefix}_captive"
        )

        ctx["traffic"] = st.selectbox(
            "Traffic",
            traffics,
            index=traffics.index(ctx["traffic"]),
            key=f"{key_prefix}_traffic"
        )

    # --------------------------------------------------------
    # SECOND ROW
    # --------------------------------------------------------

    col4, col5 = st.columns(
        2,
        gap="medium"
    )

    with col4:

        ctx["day"] = st.selectbox(
            "Day",
            days,
            index=days.index(ctx["day"]),
            key=f"{key_prefix}_day"
        )

    with col5:

        ctx["priority"] = st.selectbox(
            "Priority",
            priorities,
            index=priorities.index(ctx["priority"]),
            key=f"{key_prefix}_priority"
        )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    st.session_state.trip_context = ctx

    return ctx

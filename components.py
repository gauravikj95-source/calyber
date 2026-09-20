def trip_context_widget(key_prefix="trip"):
    """
    Shared trip context widget.
    Persists across tabs and sections using Streamlit session state.
    Returns a dict containing the current trip parameters.
    """

    # Initialize default trip context
    if "trip_context" not in st.session_state:
        st.session_state.trip_context = {
            "distance": 7.0,
            "vehicle": "Mini",
            "hour": 18,
            "weather": "Rainy",
            "captive": "Extreme",
            "traffic": "High",
            "day": "Monday",
            "priority": "cheapest"
        }

    ctx = st.session_state.trip_context

    # Options
    vehicles = ["Bike", "Auto", "Mini", "Sedan", "SUV", "Prime"]
    weathers = ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"]
    captives = ["Low", "Medium", "High", "Extreme"]
    traffics = ["Low", "Medium", "High", "Severe"]
    days = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]
    priorities = ["cheapest", "fastest", "fairest"]

    # Card
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

    # First row
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        ctx["distance"] = st.number_input(
            "Distance (km)",
            min_value=1.0,
            max_value=30.0,
            value=float(ctx["distance"]),
            step=0.5,
            key=f"{key_prefix}_dist"
        )

        ctx["vehicle"] = st.selectbox(
            "Vehicle",
            vehicles,
            index=vehicles.index(ctx["vehicle"]),
            key=f"{key_prefix}_veh"
        )

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

    with col3:
        ctx["captive"] = st.selectbox(
            "Captive quartile",
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

    # Second row
    col4, col5 = st.columns(2, gap="medium")

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

    # Save updated context
    st.session_state.trip_context = ctx

    return ctx

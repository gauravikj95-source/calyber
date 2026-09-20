def trip_context_widget(key_prefix="trip"):
    """
    Shared trip context widget. Persists across tabs and sections.
    Returns a dict with the current trip parameters.
    """
    # Initialize with defaults on first load
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

    vehicles = ["Bike", "Auto", "Mini", "Sedan", "SUV", "Prime"]
    weathers = ["Clear", "Cloudy", "Foggy", "Rainy", "Stormy"]
    captives = ["Low", "Medium", "High", "Extreme"]
    traffics = ["Low", "Medium", "High", "Severe"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    priorities = ["cheapest", "fastest", "fairest"]

    # Container styled as a card
    st.markdown(
        '<div style="background:#F8FAFC; border:1px solid #E5E7EB; '
        'border-radius:14px; padding:24px 28px; margin-bottom:24px;">'
        '<div style="color:#64748B; font-size:11px; font-weight:600; '
        'letter-spacing:0.12em; text-transform:uppercase; margin-bottom:18px;">'
        'YOUR TRIP'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        ctx["distance"] = st.number_input(
            "Distance (km)", 1.0, 30.0, ctx["distance"], 0.5,
            key=key_prefix + "_dist"
        )
        ctx["vehicle"] = st.selectbox(
            "Vehicle", vehicles, index=vehicles.index(ctx["vehicle"]),
            key=key_prefix + "_veh"
        )

    with col2:
        ctx["hour"] = st.selectbox(
            "Hour", list(range(24)), index=ctx["hour"],
            key=key_prefix + "_hour"
        )
        ctx["weather"] = st.selectbox(
            "Weather", weathers, index=weathers.index(ctx["weather"]),
            key=key_prefix + "_weather"
        )

    with col3:
        ctx["captive"] = st.selectbox(
            "Captive quartile", captives, index=captives.index(ctx["captive"]),
            key=key_prefix + "_captive"
        )
        ctx["traffic"] = st.selectbox(
            "Traffic", traffics, index=traffics.index(ctx["traffic"]),
            key=key_prefix + "_traffic"
        )

    st.markdown('</div>', unsafe_allow_html=True)

    st.session_state.trip_context = ctx
    return ctx

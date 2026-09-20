
import pandas as pd
import numpy as np
import pickle
import os

BASE_FARE_PER_KM = {
    "Bike": 9.5, "Auto": 14.0, "Mini": 17.5,
    "Sedan": 22.0, "SUV": 28.0, "Prime": 32.0
}
BASE_FARE_FLAG = {
    "Bike": 15, "Auto": 25, "Mini": 35,
    "Sedan": 45, "SUV": 60, "Prime": 80
}
DAY_MAP = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
           "Friday": 4, "Saturday": 5, "Sunday": 6}

CAPTIVE_PREMIUM = {
    "Low": 0.00, "Medium": 0.05, "High": 0.10, "Extreme": 0.15
}

# Base surge profile (for Clear weather) — this is the SURGE, not demand
BASE_SURGE_CURVE = {
    0: 1.05, 1: 1.04, 2: 1.04, 3: 1.03, 4: 1.05, 5: 1.12,
    6: 1.22, 7: 1.32, 8: 1.35, 9: 1.30, 10: 1.12, 11: 1.08,
    12: 1.08, 13: 1.09, 14: 1.10, 15: 1.14, 16: 1.20,
    17: 1.30, 18: 1.36, 19: 1.32, 20: 1.25, 21: 1.15,
    22: 1.08, 23: 1.06
}

# Weather additive premium (NOT multiplicative)
WEATHER_ADD = {
    "Clear": 0.00,
    "Cloudy": 0.00,
    "Foggy": 0.02,
    "Rainy": 0.20,
    "Stormy": 0.35
}

_surge_patterns = None


def load_surge_patterns(path="surge_patterns.csv"):
    global _surge_patterns
    if os.path.exists(path):
        _surge_patterns = pd.read_csv(path)
        return _surge_patterns
    return None


def load_model(model_path="demand_model.pkl"):
    with open(model_path, "rb") as f:
        return pickle.load(f)


def _surge_at_minute(total_minutes, weather):
    """
    Calculate surge at any minute with smooth interpolation.
    """
    total_minutes = total_minutes % (24 * 60)
    hour = total_minutes // 60
    minute = total_minutes % 60

    # Interpolate between current hour and next hour
    current_surge = BASE_SURGE_CURVE.get(hour, 1.10)
    next_surge = BASE_SURGE_CURVE.get((hour + 1) % 24, 1.10)

    # Fraction within the hour (0 to 1)
    fraction = minute / 60
    base_surge = current_surge + (next_surge - current_surge) * fraction

    # Add weather premium
    surge = base_surge + WEATHER_ADD.get(weather, 0)

    return round(min(surge, 2.5), 2)


def predict_fare_forecast(pickup_zone, drop_zone, distance_km, vehicle_type,
                          current_hour, weather, day_of_week, model_data=None,
                          current_minute=0):
    """
    Predict fares with minute-level variation.
    """
    base_fare = BASE_FARE_FLAG.get(vehicle_type, 35) + \
                BASE_FARE_PER_KM.get(vehicle_type, 17.5) * distance_km

    current_total_min = current_hour * 60 + current_minute

    forecasts = []
    for offset_min in [0, 15, 30, 45, 60, 90, 120]:
        future_total_min = current_total_min + offset_min
        future_hour = (future_total_min // 60) % 24

        surge = _surge_at_minute(future_total_min, weather)
        predicted_fare = round(base_fare * surge, 2)

        label = "Now" if offset_min == 0 else f"+{offset_min} min"
        forecasts.append({
            "offset_min": offset_min,
            "time_label": label,
            "hour": future_hour,
            "surge": surge,
            "fare": predicted_fare
        })

    best = min(forecasts, key=lambda x: x["fare"])
    current = forecasts[0]
    savings = round(current["fare"] - best["fare"], 2)

    return {
        "forecasts": forecasts,
        "current_fare": current["fare"],
        "best_fare": best["fare"],
        "best_time": best["time_label"],
        "savings": max(savings, 0),
        "base_fare": round(base_fare, 2)
    }


def predict_fairness_score(weather, hour, captive_quartile, vehicle_type):
    """Fairness grade using additive model."""
    base_surge = _surge_at_minute(hour * 60, weather)
    surge = round(base_surge + CAPTIVE_PREMIUM.get(captive_quartile, 0), 2)
    surge = min(surge, 2.5)

    if surge <= 1.2:
        grade, label, color = "A", "Fair", "#10B981"
    elif surge <= 1.4:
        grade, label, color = "B", "Good", "#3B82F6"
    elif surge <= 1.6:
        grade, label, color = "C", "Moderate", "#F59E0B"
    elif surge <= 2.0:
        grade, label, color = "D", "High", "#F97316"
    else:
        grade, label, color = "F", "Extreme", "#EF4444"

    return {
        "grade": grade,
        "label": label,
        "color": color,
        "surge": surge,
        "premium_pct": round((surge - 1.0) * 100, 1),
        "weather": weather,
        "captive": captive_quartile
    }


def predict_wait_time(weather, hour, captive_quartile):
    base_wait = 3.7
    weather_factor = {"Clear": 1.0, "Cloudy": 1.0, "Foggy": 1.1, "Rainy": 1.4, "Stormy": 1.8}
    wait = base_wait * weather_factor.get(weather, 1.0)

    if 17 <= hour <= 21:
        wait *= 1.3
    elif 5 <= hour <= 9:
        wait *= 1.25
    elif 22 <= hour or hour <= 4:
        wait *= 1.15

    captive_map = {"Low": 1.0, "Medium": 1.1, "High": 1.3, "Extreme": 1.6}
    wait *= captive_map.get(captive_quartile, 1.0)

    return {
        "wait_min": round(wait, 1),
        "wait_range": (round(wait * 0.8, 1), round(wait * 1.2, 1))
    }


def predict_cancellation_risk(weather, traffic, vehicle_type, hour):
    base_risk = 15.0
    weather_factor = {"Clear": 1.0, "Cloudy": 1.0, "Foggy": 1.05, "Rainy": 1.3, "Stormy": 1.7}
    traffic_factor = {"Low": 1.0, "Medium": 1.1, "High": 1.25, "Severe": 1.5}
    vehicle_factor = {"Bike": 0.85, "Auto": 1.0, "Mini": 1.0, "Sedan": 1.05, "SUV": 1.1, "Prime": 1.15}

    risk = base_risk * weather_factor.get(weather, 1.0)
    risk *= traffic_factor.get(traffic, 1.0)
    risk *= vehicle_factor.get(vehicle_type, 1.0)

    if 17 <= hour <= 21:
        risk *= 1.15
    elif 22 <= hour or hour <= 5:
        risk *= 1.2

    risk = min(risk, 60.0)
    if risk < 20:
        level, color = "Low", "#10B981"
    elif risk < 35:
        level, color = "Moderate", "#F59E0B"
    else:
        level, color = "High", "#EF4444"

    return {"risk_pct": round(risk, 1), "level": level, "color": color}


def predict_surge_timing(weather, day_of_week):
    timeline = []
    for h in range(24):
        surge = _surge_at_minute(h * 60, weather)
        timeline.append({
            "hour": h,
            "time_label": f"{h:02d}:00",
            "surge": surge
        })

    peak = max(timeline, key=lambda x: x["surge"])
    lowest = min(timeline, key=lambda x: x["surge"])

    return {
        "timeline": timeline,
        "peak_hour": peak["time_label"],
        "peak_surge": peak["surge"],
        "lowest_hour": lowest["time_label"],
        "lowest_surge": lowest["surge"]
    }


def detect_anomaly(actual_fare, distance_km, vehicle_type, weather, hour):
    base_fare = BASE_FARE_FLAG.get(vehicle_type, 35) + \
                BASE_FARE_PER_KM.get(vehicle_type, 17.5) * distance_km
    expected_surge = _surge_at_minute(hour * 60, weather)
    expected_fare = base_fare * expected_surge
    deviation = ((actual_fare - expected_fare) / expected_fare) * 100

    if deviation > 50:
        status, color = "SUSPICIOUS", "#EF4444"
    elif deviation > 25:
        status, color = "ELEVATED", "#F59E0B"
    else:
        status, color = "NORMAL", "#10B981"

    return {
        "actual_fare": round(actual_fare, 2),
        "expected_fare": round(expected_fare, 2),
        "deviation_pct": round(deviation, 1),
        "status": status,
        "color": color
    }


def recommend_vehicle(distance_km, priority, hour, weather):
    vehicles = ["Bike", "Auto", "Mini", "Sedan", "SUV", "Prime"]
    options = []
    surge = _surge_at_minute(hour * 60, weather)

    for v in vehicles:
        base_fare = BASE_FARE_FLAG.get(v, 35) + \
                    BASE_FARE_PER_KM.get(v, 17.5) * distance_km
        wait = predict_wait_time(weather, hour, "Medium")["wait_min"]
        fare = base_fare * surge
        fairness_premium = round((surge - 1.0) * 100, 1)

        options.append({
            "vehicle": v,
            "fare": round(fare, 2),
            "wait": round(wait, 1),
            "fairness_premium": fairness_premium
        })

    if priority == "cheapest":
        best = min(options, key=lambda x: x["fare"])
    elif priority == "fastest":
        best = min(options, key=lambda x: x["wait"])
    else:
        best = min(options, key=lambda x: x["fairness_premium"])

    return {"recommended": best, "all_options": options, "priority": priority}


def compare_route(distance_km, vehicle_type, hour, weather, historical_avg_fare=None):
    base_fare = BASE_FARE_FLAG.get(vehicle_type, 35) + \
                BASE_FARE_PER_KM.get(vehicle_type, 17.5) * distance_km
    surge = _surge_at_minute(hour * 60, weather)
    predicted_fare = base_fare * surge

    if historical_avg_fare is None:
        historical_avg_fare = base_fare * 1.25

    disparity = ((predicted_fare - historical_avg_fare) / historical_avg_fare) * 100

    if disparity > 15:
        status, color = "Overpriced", "#EF4444"
    elif disparity > -15:
        status, color = "Fair", "#10B981"
    else:
        status, color = "Underpriced", "#3B82F6"

    return {
        "predicted_fare": round(predicted_fare, 2),
        "historical_avg": round(historical_avg_fare, 2),
        "disparity_pct": round(disparity, 1),
        "status": status,
        "color": color
    }


def _calc_scenario(distance_km, vehicle_type, hour, weather, captive_quartile, apply_policy=False):
    base_fare = BASE_FARE_FLAG.get(vehicle_type, 35) + \
                BASE_FARE_PER_KM.get(vehicle_type, 17.5) * distance_km
    surge = _surge_at_minute(hour * 60, weather)
    surge += CAPTIVE_PREMIUM.get(captive_quartile, 0)

    if apply_policy:
        if captive_quartile == "Extreme":
            surge = min(surge, 1.3)
        elif captive_quartile == "High":
            surge = min(surge, 1.5)
        if weather == "Stormy":
            surge = min(surge, 1.5)
        elif weather == "Rainy":
            surge = min(surge, 1.4)

    surge = round(min(surge, 2.5), 2)
    return {"surge": surge, "fare": round(base_fare * surge, 2)}


def what_if_analysis(distance_km, vehicle_type, hour, weather, captive_quartile):
    scenarios = []
    current = _calc_scenario(distance_km, vehicle_type, hour, weather, captive_quartile)
    scenarios.append({"label": "Current trip", "fare": current["fare"], "change": 0})

    if weather != "Clear":
        alt = _calc_scenario(distance_km, vehicle_type, hour, "Clear", captive_quartile)
        scenarios.append({"label": "If weather was Clear", "fare": alt["fare"], "change": round(alt["fare"] - current["fare"], 2)})

    if not (10 <= hour <= 16):
        alt = _calc_scenario(distance_km, vehicle_type, 14, weather, captive_quartile)
        scenarios.append({"label": "If you traveled at 2 PM", "fare": alt["fare"], "change": round(alt["fare"] - current["fare"], 2)})

    if vehicle_type != "Bike":
        alt = _calc_scenario(distance_km, "Bike", hour, weather, captive_quartile)
        scenarios.append({"label": "If you booked a Bike", "fare": alt["fare"], "change": round(alt["fare"] - current["fare"], 2)})

    if captive_quartile == "Extreme":
        calyber = _calc_scenario(distance_km, vehicle_type, hour, weather, captive_quartile, apply_policy=True)
        scenarios.append({"label": "Under Calyber policy", "fare": calyber["fare"], "change": round(calyber["fare"] - current["fare"], 2)})

    return {"current_fare": current["fare"], "scenarios": scenarios}

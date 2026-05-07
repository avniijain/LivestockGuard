from __future__ import annotations

from datetime import date, timedelta

INCUBATION_PERIODS = {
    "Brucellosis": {
        "min_days": 5,
        "max_days": 60,
        "symptoms": ["Fever", "Joint pain", "Night sweats", "Fatigue", "Loss of appetite"],
    },
    "Leptospirosis": {
        "min_days": 2,
        "max_days": 30,
        "symptoms": ["High fever", "Severe headache", "Muscle aches", "Red eyes", "Jaundice"],
    },
    "Bovine_TB": {
        "min_days": 28,
        "max_days": 84,
        "symptoms": ["Persistent cough (3+ weeks)", "Night sweats", "Unexplained weight loss", "Chest pain"],
    },
    "Anthrax": {
        "min_days": 1,
        "max_days": 5,
        "symptoms": ["Black skin sore (painless)", "Swollen lymph nodes", "High fever", "Difficulty breathing"],
    },
    "Q_Fever": {
        "min_days": 14,
        "max_days": 39,
        "symptoms": ["Sudden high fever", "Severe fatigue", "Muscle pain", "Chest pain"],
    },
    "FMD": {"min_days": 2, "max_days": 6, "symptoms": ["Blisters in mouth", "Blisters on hands and feet", "Fever"]},
    "LSD": {"min_days": 4, "max_days": 14, "symptoms": ["Skin nodules", "Fever", "Swollen lymph nodes", "Nasal discharge"]},
    "Ringworm": {"min_days": 4, "max_days": 14, "symptoms": ["Circular itchy rash", "Scaly skin patch", "Hair loss in affected area"]},
}


def build_calendar(disease: str, exposure_date: date) -> dict:
    if disease not in INCUBATION_PERIODS:
        raise ValueError(f"Unsupported disease '{disease}'")

    cfg = INCUBATION_PERIODS[disease]
    min_days = int(cfg["min_days"])
    max_days = int(cfg["max_days"])
    symptoms = list(cfg["symptoms"])

    watch_start = exposure_date + timedelta(days=min_days)
    watch_end = exposure_date + timedelta(days=max_days)

    total_range = max_days - min_days
    if total_range <= 7:
        danger_start = watch_start
        danger_end = watch_end
    else:
        danger_days = max(1, int(round(total_range * 0.30)))
        danger_start = watch_start
        danger_end = watch_start + timedelta(days=danger_days)

    total_watch_days = (watch_end - watch_start).days

    return {
        "disease": disease,
        "exposure_date": exposure_date.isoformat(),
        "watch_start": watch_start.isoformat(),
        "watch_end": watch_end.isoformat(),
        "danger_window_start": danger_start.isoformat(),
        "danger_window_end": danger_end.isoformat(),
        "symptoms": symptoms,
        "total_watch_days": total_watch_days,
    }


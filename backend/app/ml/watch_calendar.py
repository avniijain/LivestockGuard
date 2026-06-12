from __future__ import annotations

from datetime import date, timedelta

_CANONICAL_KEYS = {
    "anthrax": "Anthrax",
    "bovine_tb": "Bovine_TB",
    "brucellosis": "Brucellosis",
    "fmd": "FMD",
    "leptospirosis": "Leptospirosis",
    "lsd": "LSD",
    "q_fever": "Q_Fever",
    "ringworm": "Ringworm",
    "general_illness": "General_Illness",
}


def _canonical_disease(name: str) -> str:
    key = str(name).strip().lower().replace(" ", "_")
    if key in _CANONICAL_KEYS:
        return _CANONICAL_KEYS[key]
    if key == "tb" or "tuberculosis" in key:
        return "Bovine_TB"
    if key in {"qfever", "qfev"} or key.startswith("q_fev"):
        return "Q_Fever"
    for canonical in INCUBATION_PERIODS:
        if canonical.lower() == key:
            return canonical
    return str(name).strip()


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
    "General_Illness": {
        "min_days": 1,
        "max_days": 14,
        "symptoms": [
            "Worsening fever or weakness",
            "Refusing feed or water",
            "New breathing difficulty",
            "New bleeding or discharge",
            "Sudden behaviour change",
        ],
    },
}


def build_calendar(disease: str, exposure_date: date) -> dict:
    disease_key = _canonical_disease(disease)
    if disease_key not in INCUBATION_PERIODS:
        raise ValueError(f"Unsupported disease '{disease}'")

    cfg = INCUBATION_PERIODS[disease_key]
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
        "disease": disease_key,
        "exposure_date": exposure_date.isoformat(),
        "watch_start": watch_start.isoformat(),
        "watch_end": watch_end.isoformat(),
        "danger_window_start": danger_start.isoformat(),
        "danger_window_end": danger_end.isoformat(),
        "symptoms": symptoms,
        "total_watch_days": total_watch_days,
    }


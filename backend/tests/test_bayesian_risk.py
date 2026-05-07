import time

from app.ml.bayesian_risk import compute_risk_score


def test_no_exposure_low_risk_for_lsd_and_ringworm():
    empty = {
        "direct_contact": False,
        "raw_milk_meat": False,
        "open_wounds": False,
        "children_contact": False,
        "elderly_pregnant": False,
        "unvaccinated": False,
    }
    assert compute_risk_score("LSD", empty)["score"] < 20
    assert compute_risk_score("Ringworm", empty)["score"] < 20


def test_max_exposure_critical_for_anthrax_and_brucellosis():
    full = {
        "direct_contact": True,
        "raw_milk_meat": True,
        "open_wounds": True,
        "children_contact": True,
        "elderly_pregnant": True,
        "unvaccinated": True,
    }
    assert compute_risk_score("Anthrax", full)["score"] > 80
    assert compute_risk_score("Brucellosis", full)["score"] > 80


def test_response_time_under_500ms_all_diseases():
    diseases = ["Brucellosis", "Leptospirosis", "Bovine_TB", "Anthrax", "Q_Fever", "LSD", "FMD", "Ringworm"]
    empty = {
        "direct_contact": False,
        "raw_milk_meat": False,
        "open_wounds": False,
        "children_contact": False,
        "elderly_pregnant": False,
        "unvaccinated": False,
    }
    for d in diseases:
        t0 = time.perf_counter()
        compute_risk_score(d, empty)
        dt_ms = (time.perf_counter() - t0) * 1000
        assert dt_ms < 500


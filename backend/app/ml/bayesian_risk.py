from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import product
from time import perf_counter
from typing import Any

from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from pgmpy.models import DiscreteBayesianNetwork

from app.ml.disease_priors import DISEASE_BASE_PRIORS, HOUSEHOLD_RISK_GROUPS, TRANSMISSION_ROUTES

RISK_STATES = ["Low", "Moderate", "High", "Critical"]
EXPOSURE_KEYS = [
    "direct_contact",
    "raw_milk_meat",
    "open_wounds",
    "children_contact",
    "elderly_pregnant",
    "unvaccinated",
]


def _tier(score: float) -> str:
    if score < 20:
        return "Low"
    if score <= 50:
        return "Moderate"
    if score <= 80:
        return "High"
    return "Critical"


def _action(tier: str) -> str:
    return {
        "Low": "Monitor the cow. Wash hands thoroughly after any contact.",
        "Moderate": "See a doctor within 3 days. Avoid direct contact without gloves.",
        "High": "See a doctor today and avoid further contact with the animal.",
        "Critical": "Go to a hospital immediately and call a government vet now.",
    }[tier]


def _risk_distribution_from_probability(p: float) -> list[float]:
    # Convert a scalar infection probability to a smooth 4-state distribution.
    # These cut-points are tuned to produce intuitive tiers while staying stable.
    if p <= 0:
        return [0.98, 0.02, 0.0, 0.0]

    # Soft thresholds.
    t1, t2, t3 = 0.10, 0.25, 0.45
    if p < t1:
        m = (p / t1) * 0.20
        dist = [1.0 - m, m, 0.0, 0.0]
    elif p < t2:
        x = (p - t1) / (t2 - t1)
        dist = [0.35 * (1 - x), 0.60 - 0.15 * x, 0.05 + 0.35 * x, 0.0]
    elif p < t3:
        x = (p - t2) / (t3 - t2)
        dist = [0.02 * (1 - x), 0.30 * (1 - x), 0.60 - 0.20 * x, 0.08 + 0.40 * x]
    else:
        x = min(1.0, (p - t3) / (1 - t3))
        dist = [0.0, 0.05 * (1 - x), 0.35 * (1 - x), 0.60 + 0.40 * x]

    s = sum(dist)
    if s <= 0:
        return [1.0, 0.0, 0.0, 0.0]
    return [v / s for v in dist]


def _probability_from_exposure(disease: str, exposure: dict[str, bool]) -> float:
    pri = DISEASE_BASE_PRIORS[disease]
    p = float(pri["base"])

    # Base priors represent general disease zoonotic potential, but real infection
    # risk still depends on some form of exposure. If the farmer reports *no*
    # exposure signals, dampen the baseline risk heavily.
    if not any(exposure.get(k, False) for k in EXPOSURE_KEYS):
        p *= 0.05

    # Core multipliers (per prompt).
    if exposure.get("raw_milk_meat", False):
        p *= float(pri["milk_multiplier"])
    if exposure.get("open_wounds", False):
        p *= float(pri["wound_multiplier"])
    if exposure.get("children_contact", False):
        p *= float(pri["child_multiplier"])

    # Additional evidence multipliers (kept modest, disease-agnostic).
    if exposure.get("direct_contact", False):
        p *= 1.25
    if exposure.get("elderly_pregnant", False):
        p *= 1.20
    if exposure.get("unvaccinated", False):
        p *= 1.15

    return max(0.0, min(1.0, p))


def _build_disease_network(disease: str) -> tuple[DiscreteBayesianNetwork, VariableElimination]:
    edges = [
        ("Disease", "Risk"),
        ("DirectContact", "Risk"),
        ("RawMilkMeat", "Risk"),
        ("OpenWounds", "Risk"),
        ("ChildrenContact", "Risk"),
        ("ElderlyPregnant", "Risk"),
        ("Unvaccinated", "Risk"),
    ]
    model = DiscreteBayesianNetwork(edges)

    # Disease node is fixed (single-state) because we pre-build one network per disease.
    cpd_disease = TabularCPD(variable="Disease", variable_card=1, values=[[1.0]], state_names={"Disease": [disease]})

    cpds = [cpd_disease]
    # Evidence nodes are independent Bernoulli with non-informative priors (0.5/0.5).
    for node in [
        "DirectContact",
        "RawMilkMeat",
        "OpenWounds",
        "ChildrenContact",
        "ElderlyPregnant",
        "Unvaccinated",
    ]:
        cpds.append(
            TabularCPD(
                variable=node,
                variable_card=2,
                values=[[0.5], [0.5]],
                state_names={node: [False, True]},
            )
        )

    # Risk CPD conditioned on all parents.
    parents = [
        "Disease",
        "DirectContact",
        "RawMilkMeat",
        "OpenWounds",
        "ChildrenContact",
        "ElderlyPregnant",
        "Unvaccinated",
    ]
    evidence_card = [1, 2, 2, 2, 2, 2, 2]

    values: list[list[float]] = [[] for _ in range(4)]
    state_names = {
        "Risk": RISK_STATES,
        "Disease": [disease],
        "DirectContact": [False, True],
        "RawMilkMeat": [False, True],
        "OpenWounds": [False, True],
        "ChildrenContact": [False, True],
        "ElderlyPregnant": [False, True],
        "Unvaccinated": [False, True],
    }

    for direct, milk, wounds, child, elder, unvacc in product([False, True], repeat=6):
        exp = {
            "direct_contact": direct,
            "raw_milk_meat": milk,
            "open_wounds": wounds,
            "children_contact": child,
            "elderly_pregnant": elder,
            "unvaccinated": unvacc,
        }
        p = _probability_from_exposure(disease, exp)
        dist = _risk_distribution_from_probability(p)
        for i in range(4):
            values[i].append(dist[i])

    cpd_risk = TabularCPD(
        variable="Risk",
        variable_card=4,
        values=values,
        evidence=parents,
        evidence_card=evidence_card,
        state_names=state_names,
    )
    cpds.append(cpd_risk)

    model.add_cpds(*cpds)
    model.check_model()
    infer = VariableElimination(model)
    return model, infer


# Cache all 8 models at import time.
_INFER: dict[str, VariableElimination] = {}
for _d in DISEASE_BASE_PRIORS.keys():
    _, _in = _build_disease_network(_d)
    _INFER[_d] = _in


def _score_from_posterior(posterior: dict[str, float]) -> int:
    return int(round(posterior.get("Moderate", 0.0) * 40 + posterior.get("High", 0.0) * 70 + posterior.get("Critical", 0.0) * 100))


def _infer_score(disease: str, exposure: dict[str, bool]) -> int:
    infer = _INFER[disease]
    evidence = {
        "DirectContact": exposure.get("direct_contact", False),
        "RawMilkMeat": exposure.get("raw_milk_meat", False),
        "OpenWounds": exposure.get("open_wounds", False),
        "ChildrenContact": exposure.get("children_contact", False),
        "ElderlyPregnant": exposure.get("elderly_pregnant", False),
        "Unvaccinated": exposure.get("unvaccinated", False),
    }
    q = infer.query(variables=["Risk"], evidence=evidence, show_progress=False)
    probs = {state: float(q.values[i]) for i, state in enumerate(RISK_STATES)}
    return _score_from_posterior(probs)


def compute_risk_score(disease: str, exposure: dict[str, bool]) -> dict[str, Any]:
    if disease not in _INFER:
        raise ValueError(f"Unsupported disease '{disease}'.")

    baseline = _infer_score(disease, {k: False for k in EXPOSURE_KEYS})
    final_score = _infer_score(disease, exposure)
    tier = _tier(final_score)

    contributions: dict[str, int] = {}
    for key in EXPOSURE_KEYS:
        score_k = _infer_score(disease, {k: (k == key and exposure.get(k, False)) for k in EXPOSURE_KEYS})
        delta = max(0, score_k - baseline)
        if exposure.get(key, False) and delta > 0:
            contributions[key] = int(delta)

    # Choose route from largest-driving factor.
    primary_route = TRANSMISSION_ROUTES[disease]["primary"]
    if contributions:
        top_factor = max(contributions.items(), key=lambda x: x[1])[0]
        if top_factor in ("open_wounds", "direct_contact"):
            primary_route = TRANSMISSION_ROUTES[disease]["secondary"]
        elif top_factor == "raw_milk_meat":
            primary_route = TRANSMISSION_ROUTES[disease]["primary"]

    return {
        "score": int(final_score),
        "tier": tier,
        "primary_route": primary_route,
        "per_factor_contribution": contributions,
        "at_risk_groups": HOUSEHOLD_RISK_GROUPS.get(disease, []),
        "action": _action(tier),
    }


@lru_cache(maxsize=64)
def benchmark_ms(disease: str) -> float:
    start = perf_counter()
    compute_risk_score(disease, {k: False for k in EXPOSURE_KEYS})
    return (perf_counter() - start) * 1000.0


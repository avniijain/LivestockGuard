from pydantic import BaseModel


class ExposureInput(BaseModel):
    direct_contact_without_gloves: bool
    consumed_raw_milk_or_meat: bool
    has_open_wounds: bool
    children_in_contact: bool
    elderly_or_pregnant_in_contact: bool
    vaccinated_against_relevant_disease: bool
    report_id: int | None = None


class HumanRiskOut(BaseModel):
    disease: str
    score: float
    category: str
    route_used: str
    report_id: int | None = None


class BayesianExposure(BaseModel):
    direct_contact: bool
    raw_milk_meat: bool
    open_wounds: bool
    children_contact: bool
    elderly_pregnant: bool
    unvaccinated: bool


class BayesianRiskRequest(BaseModel):
    disease: str
    exposure: BayesianExposure


class BayesianRiskOut(BaseModel):
    score: int
    tier: str
    primary_route: str
    per_factor_contribution: dict[str, int]
    at_risk_groups: list[str]
    action: str


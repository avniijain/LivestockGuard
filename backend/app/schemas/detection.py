from typing import Literal

from pydantic import BaseModel, Field


class SymptomRequest(BaseModel):
    fever: int = Field(ge=0, le=1)
    abortion: int = Field(ge=0, le=1)
    milk_drop: int = Field(ge=0, le=1)
    jaundice: int = Field(ge=0, le=1)
    coughing: int = Field(ge=0, le=1)
    weight_loss: int = Field(ge=0, le=1)
    sudden_death: int = Field(ge=0, le=1)
    nasal_discharge: int = Field(ge=0, le=1)
    swollen_lymph_nodes: int = Field(ge=0, le=1)
    limping: int = Field(ge=0, le=1)
    blisters: int = Field(ge=0, le=1)
    skin_lesions: int = Field(ge=0, le=1)
    diarrhea: int = Field(ge=0, le=1)
    eye_discharge: int = Field(ge=0, le=1)
    breathing_difficulty: int = Field(ge=0, le=1)
    lethargy: int = Field(ge=0, le=1)
    blood_from_orifices: int = Field(ge=0, le=1)
    reproductive_failure: int = Field(ge=0, le=1)

    def to_ordered_vector(self) -> list[int]:
        return [getattr(self, name) for name in self.feature_order()]

    @classmethod
    def feature_order(cls) -> list[str]:
        return [
            "fever",
            "abortion",
            "milk_drop",
            "jaundice",
            "coughing",
            "weight_loss",
            "sudden_death",
            "nasal_discharge",
            "swollen_lymph_nodes",
            "limping",
            "blisters",
            "skin_lesions",
            "diarrhea",
            "eye_discharge",
            "breathing_difficulty",
            "lethargy",
            "blood_from_orifices",
            "reproductive_failure",
        ]


class SymptomPredictionOut(BaseModel):
    disease: str
    prob: float


class SymptomDetectionResponse(BaseModel):
    status: Literal["ok", "no_symptoms", "insufficient_symptoms", "non_specific"]
    predictions: list[SymptomPredictionOut] = Field(default_factory=list)
    message: str | None = None
    recommendation: str | None = None
    symptom_scores: dict[str, float] | None = None


class FusedRequest(BaseModel):
    image_disease: str
    image_confidence: float = Field(ge=0.0, le=1.0)
    symptom_scores: dict[str, float]
    cv_weight: float = Field(default=0.6, ge=0.0, le=1.0)
    symptom_weight: float = Field(default=0.4, ge=0.0, le=1.0)


class FusedTopItem(BaseModel):
    disease: str
    score: float


class FusedResponse(BaseModel):
    final_disease: str
    final_confidence: float
    tier: Literal["confident", "moderate", "uncertain"]
    top_3: list[FusedTopItem]
    fusion_note: str


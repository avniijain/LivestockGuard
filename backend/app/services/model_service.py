from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any, Literal

import joblib
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from torchvision import models, transforms

from app.schemas.detection import SymptomRequest

CLASS_NAMES = ["fmd", "healthy", "lsd", "not_cow", "ringworm"]
CONFIDENCE_THRESHOLD = 0.6

MIN_SYMPTOMS_REQUIRED = 2

DISCRIMINATIVE_SCORES: dict[str, float] = {
    "jaundice": 1.000,
    "coughing": 1.000,
    "sudden_death": 1.000,
    "limping": 1.000,
    "blisters": 1.000,
    "skin_lesions": 1.000,
    "blood_from_orifices": 1.000,
    "diarrhea": 0.500,
    "breathing_difficulty": 0.500,
    "abortion": 0.333,
    "reproductive_failure": 0.333,
    "nasal_discharge": 0.333,
    "eye_discharge": 0.333,
    "lethargy": 0.333,
    "swollen_lymph_nodes": 0.250,
    "weight_loss": 0.250,
    "milk_drop": 0.200,
    "fever": 0.167,
}

NON_SPECIFIC_THRESHOLD = 0.25

_device: torch.device | None = None
_image_model: torch.nn.Module | None = None
_symptom_model = None
_symptom_matrix: pd.DataFrame | None = None

_transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


def _build_model(num_classes: int) -> torch.nn.Module:
    try:
        model = models.efficientnet_b0(weights=None)
    except TypeError:
        model = models.efficientnet_b0(pretrained=False)
    num_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_features, num_classes)
    return model


def load_models_once(base_path: Path) -> None:
    global _device, _image_model, _symptom_model, _symptom_matrix
    if _image_model is not None and _symptom_model is not None and _symptom_matrix is not None:
        return

    _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    image_model_path = base_path / "model_5classes.pth"
    symptom_model_path = base_path / "symptom_model.pkl"
    matrix_path = base_path / "symptom_disease_matrix.csv"

    model = _build_model(num_classes=len(CLASS_NAMES))
    model.load_state_dict(torch.load(image_model_path, map_location=_device))
    model.to(_device)
    model.eval()

    _image_model = model
    _symptom_model = joblib.load(symptom_model_path)
    _symptom_matrix = pd.read_csv(matrix_path)


def predict_image(image_bytes: bytes) -> dict[str, Any]:
    assert _image_model is not None and _device is not None
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    x = _transform(image).unsqueeze(0).to(_device)

    with torch.inference_mode():
        logits = _image_model(x)
        probs = F.softmax(logits, dim=1)
        confidence_t, predicted_t = torch.max(probs, dim=1)

    confidence = float(confidence_t.item())
    predicted_idx = int(predicted_t.item())
    predicted_class = CLASS_NAMES[predicted_idx]
    disease = "uncertain" if confidence < CONFIDENCE_THRESHOLD else predicted_class
    return {
        "disease": disease,
        "confidence": confidence,
        "predicted_class": predicted_class,
    }


def _is_non_specific(symptom_dict: dict[str, bool]) -> bool:
    active_symptoms = [key for key, value in symptom_dict.items() if value]
    if not active_symptoms:
        return True
    max_disc = max(DISCRIMINATIVE_SCORES.get(s, 0.0) for s in active_symptoms)
    return max_disc <= NON_SPECIFIC_THRESHOLD


def _norm_disease_key(s: str) -> str:
    return str(s).strip().lower().replace(" ", "_")


def fuse_predictions(
    image_disease: str,
    image_confidence: float,
    symptom_scores: dict[str, float],
    cv_weight: float = 0.6,
    symptom_weight: float = 0.4,
) -> dict[str, Any]:
    if not symptom_scores:
        raise ValueError("symptom_scores must not be empty")

    all_diseases = list(symptom_scores.keys())
    fused: dict[str, float] = {}
    img_norm = _norm_disease_key(image_disease)

    for disease in all_diseases:
        d_norm = _norm_disease_key(disease)
        img_score = image_confidence if d_norm == img_norm else 0.0
        sym_score = float(symptom_scores.get(disease, 0.0))
        fused[disease] = (cv_weight * img_score) + (symptom_weight * sym_score)

    total = sum(fused.values())
    if total > 0:
        fused = {k: v / total for k, v in fused.items()}

    top = sorted(fused.items(), key=lambda x: x[1], reverse=True)
    final_disease, final_confidence = top[0]

    if final_confidence >= 0.65:
        tier = "confident"
    elif final_confidence >= 0.40:
        tier = "moderate"
    else:
        tier = "uncertain"

    if image_confidence < 0.60:
        fusion_note = (
            f"Image scan was uncertain ({int(image_confidence * 100)}%). "
            "Symptom data was used to refine the result."
        )
    else:
        fusion_note = (
            f"Image scan ({int(image_confidence * 100)}% confident) combined with symptom data to give this result."
        )

    return {
        "final_disease": final_disease,
        "final_confidence": round(final_confidence, 3),
        "tier": tier,
        "top_3": [{"disease": d, "score": round(s, 3)} for d, s in top[:3]],
        "fusion_note": fusion_note,
    }


def predict_symptoms(payload: SymptomRequest) -> dict[str, Any]:
    assert _symptom_model is not None and _symptom_matrix is not None

    feature_order = SymptomRequest.feature_order()
    vector = payload.to_ordered_vector()
    symptom_dict: dict[str, bool] = {name: bool(vector[i]) for i, name in enumerate(feature_order)}

    active_count = int(sum(vector))
    if active_count == 0:
        return {
            "status": "no_symptoms",
            "predictions": [],
            "message": "No symptoms selected. Please select the symptoms you have observed in your animal.",
        }

    if active_count < MIN_SYMPTOMS_REQUIRED:
        return {
            "status": "insufficient_symptoms",
            "predictions": [],
            "message": "Please select at least 2 symptoms for a reliable result.",
        }

    vec_for_model = [vector]
    probabilities = _symptom_model.predict_proba(vec_for_model)[0]
    classes = list(_symptom_model.classes_)

    matrix = _symptom_matrix.copy()
    matrix["disease_key"] = matrix["Disease"].astype(str).str.lower().str.replace(" ", "_")
    selected = pd.Series(vector, index=feature_order, dtype=float)

    selected_sum = float(selected.sum())
    if selected_sum > 0:
        matrix_score_series = matrix[feature_order].mul(selected, axis=1).sum(axis=1) / selected_sum
    else:
        matrix_score_series = pd.Series(0.0, index=matrix.index)

    matrix_scores = dict(zip(matrix["disease_key"], matrix_score_series.astype(float)))
    disease_labels = {k: v for k, v in zip(matrix["disease_key"], matrix["Disease"].astype(str))}
    model_scores = {str(d).lower().replace(" ", "_"): float(p) for d, p in zip(classes, probabilities)}

    for disease in classes:
        key = str(disease).lower().replace(" ", "_")
        disease_labels.setdefault(key, str(disease))

    alpha = 0.3
    disease_keys = sorted(set(model_scores) | set(matrix_scores))
    combined_scores: dict[str, float] = {
        key: (alpha * model_scores.get(key, 0.0)) + ((1 - alpha) * matrix_scores.get(key, 0.0))
        for key in disease_keys
    }
    total = sum(combined_scores.values())
    if total > 0:
        combined_scores = {k: v / total for k, v in combined_scores.items()}

    if _is_non_specific(symptom_dict):
        return {
            "status": "non_specific",
            "predictions": [],
            "message": (
                "The symptoms you selected are common to many conditions and are not specific to any zoonotic disease. "
                "Your animal may just be unwell from a general illness."
            ),
            "recommendation": "non_zoonotic",
        }

    ranked = sorted(combined_scores.items(), key=lambda row: row[1], reverse=True)[:3]
    return {
        "status": "ok",
        "predictions": [
            {"disease": disease_labels.get(key, key), "prob": float(prob)} for key, prob in ranked
        ],
        "symptom_scores": {k: float(v) for k, v in combined_scores.items()},
    }

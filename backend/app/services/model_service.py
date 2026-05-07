from __future__ import annotations

from io import BytesIO
from pathlib import Path

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


def predict_image(image_bytes: bytes) -> dict:
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
    return {"disease": disease, "confidence": confidence}


def predict_symptoms(payload: SymptomRequest) -> dict:
    assert _symptom_model is not None and _symptom_matrix is not None

    feature_order = SymptomRequest.feature_order()
    vector = [payload.to_ordered_vector()]
    probabilities = _symptom_model.predict_proba(vector)[0]
    classes = list(_symptom_model.classes_)

    matrix = _symptom_matrix.copy()
    matrix["disease_key"] = matrix["Disease"].astype(str).str.lower().str.replace(" ", "_")
    selected = pd.Series(vector[0], index=feature_order, dtype=float)

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

    # Matrix gets higher contribution.
    alpha = 0.3
    disease_keys = sorted(set(model_scores) | set(matrix_scores))
    combined_scores = {
        key: (alpha * model_scores.get(key, 0.0)) + ((1 - alpha) * matrix_scores.get(key, 0.0))
        for key in disease_keys
    }
    total = sum(combined_scores.values())
    if total > 0:
        combined_scores = {k: v / total for k, v in combined_scores.items()}

    ranked = sorted(combined_scores.items(), key=lambda row: row[1], reverse=True)[:3]
    return {
        "predictions": [
            {"disease": disease_labels.get(key, key), "prob": float(prob)} for key, prob in ranked
        ]
    }


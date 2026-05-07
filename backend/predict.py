import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import torch.nn.functional as F

print("Script started...")

# device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# load model
model = models.efficientnet_b0(pretrained=False)
num_features = model.classifier[1].in_features

# 🔥 IMPORTANT: 5 classes
model.classifier[1] = nn.Linear(num_features, 5)

print("Loading model...")
model.load_state_dict(torch.load("model_5classes.pth", map_location=device))

model.to(device)
model.eval()

print("Model loaded successfully!")

# 🔥 SAME transform as validation (with normalization)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ⚠️ MUST match train_data.classes EXACTLY
class_names = ['fmd', 'healthy', 'lsd', 'not_cow', 'ringworm']

def predict_image(image_path):
    print("Loading image...")
    
    try:
        img = Image.open(image_path).convert("RGB")
    except Exception as e:
        print("Error loading image:", e)
        return

    print("Transforming image...")
    img = transform(img).unsqueeze(0).to(device)

    print("Running model...")
    with torch.no_grad():
        outputs = model(img)
        probs = F.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probs, 1)

    pred_class = class_names[predicted.item()]
    conf = confidence.item()

    # optional threshold handling
    if conf < 0.6:
        print("Prediction: Uncertain")
    else:
        print("Prediction:", pred_class)

    print("Confidence:", round(conf, 4))


# 🔥 USE FULL PATH
image_path = r"C:\Users\Avni Jain\livestockguard\backend\download (3).jpg"

print("Calling prediction...")
predict_image(image_path)


from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
from PIL import Image
import io
import torch
from torchvision import transforms
from knowledge_base import disease_info
import torch.nn as nn
from torchvision import models
import os

app = FastAPI()

# Create a directory for uploads if it doesn't exist
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# =========================
# LOAD MODEL FROM CHECKPOINT
# Class names and num_classes are read directly from the saved model
# so this never breaks if you retrain with different classes
# =========================
MODEL_PATH = "crop_identifier_best.pth"
IMAGE_SIZE = 224

checkpoint = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
class_names = checkpoint['class_names']
num_classes = len(class_names)

print(f"Loaded model with {num_classes} classes: {class_names}")

model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, num_classes)
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# =========================
# IMAGE TRANSFORMS
# =========================
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# =========================
# PREDICT
# =========================
def predict(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)

        if confidence.item() < 0.15:
            return "Not a valid plant image or disease not recognised", 0.0

        disease_name = class_names[predicted.item()]
        return disease_name, confidence.item()

# =========================
# GET DISEASE INFO
# =========================

# =========================
# GET DISEASE INFO (ROBUST CROSS-PLANT FALLBACK)
# =========================
def get_disease_info(disease_name):
    # 1. Try the exact match first (keeps everything working normally)
    key = disease_name.lower().replace(' ', '_')
    if key in disease_info:
        return disease_info[key]
        
    print(f"Exact match failed for '{key}'. Running cross-plant fallback...")

    # 2. If exact match fails (e.g. model guessed "rice leafs" but it's not a key),
    # extract the core symptoms to find a match from another plant.
    plant_keywords = ["maize", "rice", "tomato", "cassava", "cashew", "leaf", "leafs", "___", "__", "_"]
    
    # Clean the predicted name into clean, individual words
    pred_clean = disease_name.lower().replace('___', ' ').replace('__', ' ').replace('_', ' ')
    pred_words = [w for w in pred_clean.split() if w not in plant_keywords]
    
    # Handle the "healthy" or empty edge case
    if not pred_words or "healthy" in pred_clean:
        # If it predicted a healthy version of the wrong plant, give them maize_healthy as the baseline
        if "maize_healthy" in disease_info:
            return disease_info["maize_healthy"]
        # Fallback to any healthy key available
        for k in disease_info.keys():
            if "healthy" in k:
                return disease_info[k]

    # 3. Look through the dictionary for a matching symptom (e.g., matching "blight" or "spot")
    for key_candidate in disease_info.keys():
        key_clean = key_candidate.lower().replace('___', ' ').replace('__', ' ').replace('_', ' ')
        key_words = [w for w in key_clean.split() if w not in plant_keywords]
        
        # If the symptom words overlap, borrow the treatment info from that plant
        if any(word in key_words for word in pred_words):
            print(f"Cross-plant match found! Using info from '{key_candidate}' for prediction '{disease_name}'")
            return disease_info[key_candidate]

    # 4. Final safety net if absolutely nothing matches
    return "Disease information not found."

# =========================
# ROUTES
# =========================
@app.get("/")
def home():
    return {
        "message": "Agro AI API running",
        "model": MODEL_PATH,
        "num_classes": num_classes,
        "classes": class_names
    }

@app.get("/classes")
def get_classes():
    return {"classes": class_names, "total": num_classes}

@app.post("/predict/")
async def predict_api(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(contents)

        predicted_disease, confidence = predict(contents)
        info = get_disease_info(predicted_disease)

        return JSONResponse(content={
            "predicted_disease": predicted_disease,
            "confidence": round(confidence * 100, 2),
            "confidence_label": f"{confidence*100:.1f}%",
            "info": info
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
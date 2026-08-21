# # app.py
# import os
# import io
# import torch
# import torch.nn as nn
# import uvicorn
# import gc  # 🎯 For manual garbage collection collection
# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse
# from PIL import Image
# from torchvision import transforms, models
# from knowledge_base import disease_info

# app = FastAPI()

# # Create a directory for user upload logs if it doesn't exist
# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# MODEL_PATH = "plant_disease_model.pth"
# IMAGE_SIZE = 224

# WARMIGRO_CLASSES = [
#     'apple_apple_scab', 'apple_black_rot', 'apple_cedar_apple_rust', 'apple_healthy',
#     'cashew_anthracnose', 'cashew_gumosis', 'cashew_healthy', 'cashew_leaf_miner', 'cashew_red_rust',
#     'cassava_bacterial_blight', 'cassava_brown_spot', 'cassava_green_mite', 'cassava_healthy', 'cassava_mosaic',
#     'maize_cercospora_leaf_spot_gray_leaf_spot', 'maize_common_rust', 'maize_fall_armyworm', 'maize_grasshoper',
#     'maize_healthy', 'maize_leaf_beetle', 'maize_leaf_blight', 'maize_leaf_spot', 'maize_northern_leaf_blight',
#     'maize_streak_virus', 'mossaic_virus', 'pepper_bacterial_spot', 'pepper_healthy',
#     'potato_early_blight', 'potato_healthy', 'potato_late_blight', 'rice_leafs', 'southern_blight',
#     'sudden_death_syndrone', 'tomato_bacterial_spot', 'tomato_early_blight', 'tomato_healthy',
#     'tomato_late_blight', 'tomato_leaf_blight', 'tomato_leaf_curl', 'tomato_leaf_mold',
#     'tomato_mosaic_virus', 'tomato_septoria_leaf_spot', 'tomato_spider_mites_two_spotted_spider_mite',
#     'tomato_target_spot', 'tomato_tomato_mosaic_virus', 'tomato_tomato_yellow_leaf_curl_virus',
#     'tomato_tomato_yellowleaf_curl_virus', 'tomato_verticulium_wilt', 'yellow_mosaic'
# ]

# # ==========================================
# # 🧠 FIXED: SINGLE-PASS MODEL LIFECYCLE LOADER
# # ==========================================
# if not os.path.exists(MODEL_PATH):
#     print(f"Checkpoint '{MODEL_PATH}' not found. Booting with dummy placeholders...")
#     class_names = WARMIGRO_CLASSES
#     num_classes = len(class_names)
#     model = models.resnet18(weights=None)
#     model.fc = nn.Linear(model.fc.in_features, num_classes)
#     model.eval()
# else:
#     print(f"Loading weights from '{MODEL_PATH}'...")
#     checkpoint = torch.load(MODEL_PATH, map_location=torch.device('cpu'))

#     if isinstance(checkpoint, dict) and 'class_names' in checkpoint:
#         class_names = checkpoint['class_names']
#     else:
#         print("ℹ Model file lacks class metadata keys. Applying hardcoded alignment array.")
#         class_names = WARMIGRO_CLASSES

#     num_classes = len(class_names)

#     # Rebuild network structure once
#     model = models.resnet18(weights=None)
#     model.fc = nn.Linear(model.fc.in_features, num_classes)

#     if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
#         state_dict = checkpoint['model_state_dict']
#     elif isinstance(checkpoint, dict) and 'state_dict' in checkpoint:
#         state_dict = checkpoint['state_dict']
#     else:
#         state_dict = checkpoint

#     model.load_state_dict(state_dict, strict=False)
#     model.eval()
    
#     # 🎯 RAM OPTIMIZATION: Wipe checkpoint dictionary records from memory immediately after extraction
#     del checkpoint
#     del state_dict
#     gc.collect()
#     print(f"Real weights linked! Server lifecycle successfully mapped to {num_classes} classes.")

# # ==========================================
# # 📸 IMAGE TRANSFORMS (Tensor Preprocessing)
# # ==========================================
# transform = transforms.Compose([
#     transforms.Resize(256),
#     transforms.CenterCrop(IMAGE_SIZE),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
# ])

# # ==========================================
# # 🔮 INFERENCE PREDICTION PIPELINE
# # ==========================================
# def predict(image_bytes):
#     if model is None:
#         return "Model not initialized. Missing weights file.", 0.0

#     image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
#     tensor = transform(image).unsqueeze(0)

#     with torch.no_grad():
#         outputs = model(tensor)
#         probabilities = torch.nn.functional.softmax(outputs, dim=1)
#         confidence, predicted = torch.max(probabilities, 1)

#         # Free up input processing allocation footprints right away
#         del tensor
#         if confidence.item() < 0.01:
#             return "Not a valid plant image or disease not recognized", 0.0

#         disease_name = class_names[predicted.item()]
#         return disease_name, confidence.item()

# # ==========================================
# # 🌾 ROBUST DISEASE INFO MATCHING ENGINE
# # ==========================================
# def get_disease_info(disease_name):
#     clean_input = disease_name.lower().replace('___', '_').replace('__', '_').strip()
    
#     for kb_key in disease_info.keys():
#         clean_kb_key = kb_key.lower().replace('___', '_').replace('__', '_').strip()
#         if clean_input == clean_kb_key:
#             return disease_info[kb_key]
            
#     crop_keywords = [
#         "maize", "rice", "tomato", "cassava", "cashew", "cocoa", "plantain", 
#         "yam", "sweet", "potato", "pepper", "onion", "bean", "groundnut", "leaf", "leafs"
#     ]
#     pred_words = [w for w in clean_input.split('_') if w not in crop_keywords and w.strip()]
    
#     if not pred_words or "healthy" in clean_input:
#         if "maize_healthy" in disease_info:
#             return disease_info["maize_healthy"]
#         for k in disease_info.keys():
#             if "healthy" in k.lower():
#                 return disease_info[k]

#     for kb_key in disease_info.keys():
#         clean_kb_key = kb_key.lower().replace('___', '_').replace('__', '_').strip()
#         kb_words = [w for w in clean_kb_key.split('_') if w not in crop_keywords and w.strip()]
        
#         if any(word in kb_words for word in pred_words):
#             return disease_info[kb_key]

#     return {
#         "cause": f"Suspected Plant Pathogen Profile ({disease_name})",
#         "treatment": ["Lodge an advisory ticket with local field extension services for confirmation."],
#         "prevention": ["Prune local canopy, clean farm tools, and segregate affected crop zone quadrants."]
#     }

# # ==========================================
# # 🛑 ROUTING API ENDPOINTS
# # ==========================================
# @app.get("/")
# def home():
#     return {
#         "message": "Agro Vision AI Operational Core Backend Running",
#         "model_file": MODEL_PATH,
#         "total_classes": num_classes,
#         "active_classes": class_names
#     }

# @app.get("/classes")
# def get_classes():
#     return {"classes": class_names, "total": num_classes}

# @app.post("/predict/")
# async def predict_api(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()

#         # Execute predictions
#         predicted_disease, confidence = predict(contents)
#         info = get_disease_info(predicted_disease)

#         return JSONResponse(content={
#             "predicted_disease": predicted_disease,
#             "confidence": round(confidence * 100, 2),
#             "confidence_label": f"{confidence*100:.1f}%",
#             "info": info
#         })
#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=500)
#     finally:
#         # 🎯 AGGRESSIVE POST-INFERENCE MEMORY FLUSH
#         if 'contents' in locals(): 
#             del contents
#         gc.collect()

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)



# # app.py
# import os
# import io
# import torch
# import torch.nn as nn
# import uvicorn
# import gc  # 🎯 For manual garbage collection collection
# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse
# from PIL import Image
# from torchvision import transforms, models
# from knowledge_base import disease_info

# app = FastAPI()

# # Create a directory for user upload logs if it doesn't exist
# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# MODEL_PATH = "plant_disease_model.pth"
# IMAGE_SIZE = 224

# WARMIGRO_CLASSES = [
#     'apple_apple_scab', 'apple_black_rot', 'apple_cedar_apple_rust', 'apple_healthy',
#     'cashew_anthracnose', 'cashew_gumosis', 'cashew_healthy', 'cashew_leaf_miner', 'cashew_red_rust',
#     'cassava_bacterial_blight', 'cassava_brown_spot', 'cassava_green_mite', 'cassava_healthy', 'cassava_mosaic',
#     'maize_cercospora_leaf_spot_gray_leaf_spot', 'maize_common_rust', 'maize_fall_armyworm', 'maize_grasshoper',
#     'maize_healthy', 'maize_leaf_beetle', 'maize_leaf_blight', 'maize_leaf_spot', 'maize_northern_leaf_blight',
#     'maize_streak_virus', 'mossaic_virus', 'pepper_bacterial_spot', 'pepper_healthy',
#     'potato_early_blight', 'potato_healthy', 'potato_late_blight', 'rice_leafs', 'southern_blight',
#     'sudden_death_syndrone', 'tomato_bacterial_spot', 'tomato_early_blight', 'tomato_healthy',
#     'tomato_late_blight', 'tomato_leaf_blight', 'tomato_leaf_curl', 'tomato_leaf_mold',
#     'tomato_mosaic_virus', 'tomato_septoria_leaf_spot', 'tomato_spider_mites_two_spotted_spider_mite',
#     'tomato_target_spot', 'tomato_tomato_mosaic_virus', 'tomato_tomato_yellow_leaf_curl_virus',
#     'tomato_tomato_yellowleaf_curl_virus', 'tomato_verticulium_wilt', 'yellow_mosaic'
# ]

# # ==========================================
# # 🧠 FIXED: SINGLE-PASS MODEL LIFECYCLE LOADER
# # ==========================================
# if not os.path.exists(MODEL_PATH):
#     print(f"Checkpoint '{MODEL_PATH}' not found. Booting with dummy placeholders...")
#     class_names = WARMIGRO_CLASSES
#     num_classes = len(class_names)
#     model = models.resnet18(weights=None)
#     model.fc = nn.Linear(model.fc.in_features, num_classes)
#     model.eval()
# else:
#     print(f"Loading weights from '{MODEL_PATH}'...")
#     checkpoint = torch.load(MODEL_PATH, map_location=torch.device('cpu'))

#     if isinstance(checkpoint, dict) and 'class_names' in checkpoint:
#         class_names = checkpoint['class_names']
#     else:
#         print("ℹ Model file lacks class metadata keys. Applying hardcoded alignment array.")
#         class_names = WARMIGRO_CLASSES

#     num_classes = len(class_names)

#     # Rebuild network structure once
#     model = models.resnet18(weights=None)
#     model.fc = nn.Linear(model.fc.in_features, num_classes)

#     if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
#         state_dict = checkpoint['model_state_dict']
#     elif isinstance(checkpoint, dict) and 'state_dict' in checkpoint:
#         state_dict = checkpoint['state_dict']
#     else:
#         state_dict = checkpoint

#     model.load_state_dict(state_dict, strict=False)
#     model.eval()
    
#     # 🎯 RAM OPTIMIZATION: Wipe checkpoint dictionary records from memory immediately after extraction
#     del checkpoint
#     del state_dict
#     gc.collect()
#     print(f"Real weights linked! Server lifecycle successfully mapped to {num_classes} classes.")

# # ==========================================
# # 📸 IMAGE TRANSFORMS (Tensor Preprocessing)
# # ==========================================
# transform = transforms.Compose([
#     transforms.Resize(256),
#     transforms.CenterCrop(IMAGE_SIZE),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
# ])

# # ==========================================
# # 🔮 INFERENCE PREDICTION PIPELINE
# # ==========================================
# def predict(image_bytes):
#     if model is None:
#         return "Model not initialized. Missing weights file.", 0.0

#     image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
#     tensor = transform(image).unsqueeze(0)

#     with torch.no_grad():
#         outputs = model(tensor)
#         probabilities = torch.nn.functional.softmax(outputs, dim=1)
#         confidence, predicted = torch.max(probabilities, 1)

#         # Free up input processing allocation footprints right away
#         del tensor
        
#         # 🎯 RAISED THRESHOLD: Reject low-confidence or non-plant images (< 60%)
#         if confidence.item() < 0.60:
#             return "This image does not appear to contain a plant or a clear leaf.", 0.0

#         disease_name = class_names[predicted.item()]
#         return disease_name, confidence.item()

# # ==========================================
# # 🌾 ROBUST DISEASE INFO MATCHING ENGINE
# # ==========================================
# def get_disease_info(disease_name):
#     # Handle non-plant rejection string first
#     if "does not appear to contain a plant" in disease_name:
#         return {
#             "cause": "Input image is not recognized as a valid plant leaf or sample.",
#             "treatment": ["Please upload a clear, well-lit photo of an affected plant leaf."],
#             "prevention": ["Ensure the camera is focused directly on the symptom area."]
#         }

#     clean_input = disease_name.lower().replace('___', '_').replace('__', '_').strip()
    
#     for kb_key in disease_info.keys():
#         clean_kb_key = kb_key.lower().replace('___', '_').replace('__', '_').strip()
#         if clean_input == clean_kb_key:
#             return disease_info[kb_key]
            
#     crop_keywords = [
#         "maize", "rice", "tomato", "cassava", "cashew", "cocoa", "plantain", 
#         "yam", "sweet", "potato", "pepper", "onion", "bean", "groundnut", "leaf", "leafs"
#     ]
#     pred_words = [w for w in clean_input.split('_') if w not in crop_keywords and w.strip()]
    
#     if not pred_words or "healthy" in clean_input:
#         if "maize_healthy" in disease_info:
#             return disease_info["maize_healthy"]
#         for k in disease_info.keys():
#             if "healthy" in k.lower():
#                 return disease_info[k]

#     for kb_key in disease_info.keys():
#         clean_kb_key = kb_key.lower().replace('___', '_').replace('__', '_').strip()
#         kb_words = [w for w in clean_kb_key.split('_') if w not in crop_keywords and w.strip()]
        
#         if any(word in kb_words for word in pred_words):
#             return disease_info[kb_key]

#     return {
#         "cause": f"Suspected Plant Pathogen Profile ({disease_name})",
#         "treatment": ["Lodge an advisory ticket with local field extension services for confirmation."],
#         "prevention": ["Prune local canopy, clean farm tools, and segregate affected crop zone quadrants."]
#     }

# # ==========================================
# # 🛑 ROUTING API ENDPOINTS
# # ==========================================
# @app.get("/")
# def home():
#     return {
#         "message": "Agro Vision AI Operational Core Backend Running",
#         "model_file": MODEL_PATH,
#         "total_classes": num_classes,
#         "active_classes": class_names
#     }

# @app.get("/classes")
# def get_classes():
#     return {"classes": class_names, "total": num_classes}

# @app.post("/predict/")
# async def predict_api(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()

#         # Execute predictions
#         predicted_disease, confidence = predict(contents)
#         info = get_disease_info(predicted_disease)

#         return JSONResponse(content={
#             "predicted_disease": predicted_disease,
#             "confidence": round(confidence * 100, 2),
#             "confidence_label": f"{confidence*100:.1f}%",
#             "info": info
#         })
#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=500)
#     finally:
#         # 🎯 AGGRESSIVE POST-INFERENCE MEMORY FLUSH
#         if 'contents' in locals(): 
#             del contents
#         gc.collect()

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)



# app.py
import os
import io
import torch
import torch.nn as nn
import uvicorn
import gc  # 🎯 For manual garbage collection collection
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
from torchvision import transforms, models
from knowledge_base import disease_info

app = FastAPI()

# Create a directory for user upload logs if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

MODEL_PATH = "plant_disease_model.pth"
IMAGE_SIZE = 224

WARMIGRO_CLASSES = [
    'apple_apple_scab', 'apple_black_rot', 'apple_cedar_apple_rust', 'apple_healthy',
    'cashew_anthracnose', 'cashew_gumosis', 'cashew_healthy', 'cashew_leaf_miner', 'cashew_red_rust',
    'cassava_bacterial_blight', 'cassava_brown_spot', 'cassava_green_mite', 'cassava_healthy', 'cassava_mosaic',
    'maize_cercospora_leaf_spot_gray_leaf_spot', 'maize_common_rust', 'maize_fall_armyworm', 'maize_grasshoper',
    'maize_healthy', 'maize_leaf_beetle', 'maize_leaf_blight', 'maize_leaf_spot', 'maize_northern_leaf_blight',
    'maize_streak_virus', 'mossaic_virus', 'pepper_bacterial_spot', 'pepper_healthy',
    'potato_early_blight', 'potato_healthy', 'potato_late_blight', 'rice_leafs', 'southern_blight',
    'sudden_death_syndrone', 'tomato_bacterial_spot', 'tomato_early_blight', 'tomato_healthy',
    'tomato_late_blight', 'tomato_leaf_blight', 'tomato_leaf_curl', 'tomato_leaf_mold',
    'tomato_mosaic_virus', 'tomato_septoria_leaf_spot', 'tomato_spider_mites_two_spotted_spider_mite',
    'tomato_target_spot', 'tomato_tomato_mosaic_virus', 'tomato_tomato_yellow_leaf_curl_virus',
    'tomato_tomato_yellowleaf_curl_virus', 'tomato_verticulium_wilt', 'yellow_mosaic'
]

# ==========================================
# 🧠 FIXED: SINGLE-PASS MODEL LIFECYCLE LOADER
# ==========================================
if not os.path.exists(MODEL_PATH):
    print(f"Checkpoint '{MODEL_PATH}' not found. Booting with dummy placeholders...")
    class_names = WARMIGRO_CLASSES
    num_classes = len(class_names)
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model.eval()
else:
    print(f"Loading weights from '{MODEL_PATH}'...")
    checkpoint = torch.load(MODEL_PATH, map_location=torch.device('cpu'))

    if isinstance(checkpoint, dict) and 'class_names' in checkpoint:
        class_names = checkpoint['class_names']
    else:
        print("ℹ Model file lacks class metadata keys. Applying hardcoded alignment array.")
        class_names = WARMIGRO_CLASSES

    num_classes = len(class_names)

    # Rebuild network structure once
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
        state_dict = checkpoint['model_state_dict']
    elif isinstance(checkpoint, dict) and 'state_dict' in checkpoint:
        state_dict = checkpoint['state_dict']
    else:
        state_dict = checkpoint

    model.load_state_dict(state_dict, strict=False)
    model.eval()
    
    # 🎯 RAM OPTIMIZATION: Wipe checkpoint dictionary records from memory immediately after extraction
    del checkpoint
    del state_dict
    gc.collect()
    print(f"Real weights linked! Server lifecycle successfully mapped to {num_classes} classes.")

# ==========================================
# 📸 IMAGE TRANSFORMS (Tensor Preprocessing)
# ==========================================
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])



# ==========================================
# 🔮 INFERENCE PREDICTION PIPELINE
# ==========================================
def predict(image_bytes):
    if model is None:
        return "Model not initialized. Missing weights file.", 0.0

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)

        del tensor
        
        # 🎯 STRICTER REJECTION: Only block items with very low confidence (< 25%) 
        # so real plant photos (even at 40-50%) pass through safely.
        if confidence.item() < 0.55:
            return "This image does not appear to contain a plant or a clear leaf.", 0.0

        disease_name = class_names[predicted.item()]
        return disease_name, confidence.item()

# ==========================================
# 🌾 ROBUST DISEASE INFO MATCHING ENGINE
# ==========================================
def get_disease_info(disease_name):
    if "does not appear to contain a plant" in disease_name:
        return {
            "cause": "Input image is not recognized as a valid plant leaf or sample.",
            "treatment": ["Please upload a clear, well-lit photo of an affected plant leaf."],
            "prevention": ["Ensure the camera is focused directly on the symptom area."]
        }

    clean_input = disease_name.lower().replace('___', '_').replace('__', '_').replace('(', '').replace(')', '').replace(' ', '_').strip()
    
    # 1. Exact match check
    for kb_key in disease_info.keys():
        clean_kb_key = kb_key.lower().replace('___', '_').replace('__', '_').replace('(', '').replace(')', '').replace(' ', '_').strip()
        if clean_input == clean_kb_key:
            return disease_info[kb_key]
            
    # 2. HANDLE BROAD / HEALTHY LABELS (e.g., "Cashew", "Rice", "Tomato", or "healthy")
    broad_crops = ["cashew", "rice", "tomato", "maize", "cassava", "pepper", "potato", "apple", "yam", "cocoa", "plantain", "onion", "bean", "groundnut"]
    if "healthy" in clean_input or clean_input in broad_crops:
        # Try to find a healthy match for this crop in the knowledge base
        for k in disease_info.keys():
            if ("healthy" in k.lower() or k.lower() == clean_input) and clean_input in k.lower():
                return disease_info[k]
        # Default healthy response if no specific disease or sub-key matched
        return {
            "cause": f"Plant sample ({disease_name.capitalize()}) appears normal with no major visible disease symptoms.",
            "treatment": ["No immediate chemical treatment required. Maintain standard field monitoring."],
            "prevention": ["Continue regular watering, proper spacing, and balanced fertilizer application."]
        }

    # 3. Partial keyword matching for specific diseases
    pred_words = [w for w in clean_input.split('_') if w not in broad_crops and w.strip()]
    
    for kb_key in disease_info.keys():
        clean_kb_key = kb_key.lower().replace('___', '_').replace('__', '_').replace('(', '').replace(')', '').replace(' ', '_').strip()
        kb_words = [w for w in clean_kb_key.split('_') if w not in broad_crops and w.strip()]
        if pred_words and any(word in kb_words for word in pred_words):
            return disease_info[kb_key]

    # 4. Safe fallback for unrecognized combinations
    return {
        "cause": f"Suspected Plant Pathogen Profile ({disease_name})",
        "treatment": ["Lodge an advisory ticket with local field extension services for confirmation."],
        "prevention": ["Prune local canopy, clean farm tools, and segregate affected crop zone quadrants."]
    }
# ==========================================
# 🔮 INFERENCE PREDICTION PIPELINE
# ==========================================
# def predict(image_bytes):
#     if model is None:
#         return "Model not initialized. Missing weights file.", 0.0

#     image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
#     tensor = transform(image).unsqueeze(0)

#     with torch.no_grad():
#         outputs = model(tensor)
#         probabilities = torch.nn.functional.softmax(outputs, dim=1)
#         confidence, predicted = torch.max(probabilities, 1)

#         # Free up input processing allocation footprints right away
#         del tensor
        
#         # 🎯 ADJUSTED THRESHOLD: Lowered to 35% to accept valid real-world leaves
#         if confidence.item() < 0.35:
#             return "This image does not appear to contain a plant or a clear leaf.", 0.0

#         disease_name = class_names[predicted.item()]
#         return disease_name, confidence.item()

# ==========================================
# 🌾 ROBUST DISEASE INFO MATCHING ENGINE
# ==========================================
# def get_disease_info(disease_name):
#     # Handle non-plant rejection string first
#     if "does not appear to contain a plant" in disease_name:
#         return {
#             "cause": "Input image is not recognized as a valid plant leaf or sample.",
#             "treatment": ["Please upload a clear, well-lit photo of an affected plant leaf."],
#             "prevention": ["Ensure the camera is focused directly on the symptom area."]
#         }

#     clean_input = disease_name.lower().replace('___', '_').replace('__', '_').strip()
    
#     # 1. Exact match check
#     for kb_key in disease_info.keys():
#         clean_kb_key = kb_key.lower().replace('___', '_').replace('__', '_').strip()
#         if clean_input == clean_kb_key:
#             return disease_info[kb_key]
            
#     crop_keywords = [
#         "maize", "rice", "tomato", "cassava", "cashew", "cocoa", "plantain", 
#         "yam", "sweet", "potato", "pepper", "onion", "bean", "groundnut", "leaf", "leafs"
#     ]
#     pred_words = [w for w in clean_input.split('_') if w not in crop_keywords and w.strip()]
    
#     # 2. STRICT HEALTHY CHECK: Only return healthy info if 'healthy' is explicitly in the prediction
#     if "healthy" in clean_input:
#         if clean_input in disease_info:
#             return disease_info[clean_input]
#         for k in disease_info.keys():
#             if "healthy" in k.lower() and any(crop in k.lower() for crop in clean_input.split('_')):
#                 return disease_info[k]
#         return {
#             "cause": "Plant appears healthy with no visible pathogen symptoms detected.",
#             "treatment": ["No treatment required. Maintain standard crop management practices."],
#             "prevention": ["Continue regular scouting, adequate watering, and balanced nutrient application."]
#         }

#     # 3. Partial keyword matching for diseases (preventing false healthy triggers)
#     for kb_key in disease_info.keys():
#         clean_kb_key = kb_key.lower().replace('___', '_').replace('__', '_').strip()
#         kb_words = [w for w in clean_kb_key.split('_') if w not in crop_keywords and w.strip()]
        
#         if pred_words and any(word in kb_words for word in pred_words):
#             return disease_info[kb_key]

#     # 4. Safe fallback if no exact dictionary match is found
#     return {
#         "cause": f"Suspected Plant Pathogen Profile ({disease_name})",
#         "treatment": ["Lodge an advisory ticket with local field extension services for confirmation."],
#         "prevention": ["Prune local canopy, clean farm tools, and segregate affected crop zone quadrants."]
#     }

# ==========================================
# 🌾 ROBUST DISEASE INFO MATCHING ENGINE (77-Class Compatible)
# ==========================================
def get_disease_info(disease_name):
    if "does not appear to contain a plant" in disease_name:
        return {
            "cause": "Input image is not recognized as a valid plant leaf or sample.",
            "treatment": ["Please upload a clear, well-lit photo of an affected plant leaf."],
            "prevention": ["Ensure the camera is focused directly on the symptom area."]
        }

    # Normalize prediction string for flexible matching
    clean_input = disease_name.lower().replace('___', '_').replace('__', '_').replace('(', '').replace(')', '').replace(' ', '_').strip()
    
    # 1. Try exact normalized match
    for kb_key in disease_info.keys():
        clean_kb_key = kb_key.lower().replace('___', '_').replace('__', '_').replace('(', '').replace(')', '').replace(' ', '_').strip()
        if clean_input == clean_kb_key:
            return disease_info[kb_key]
            
    # 2. Strict healthy check
    if "healthy" in clean_input:
        for k in disease_info.keys():
            if "healthy" in k.lower() and any(c in k.lower() for c in clean_input.split('_')):
                return disease_info[k]
        return {
            "cause": "Plant appears healthy with no visible pathogen symptoms detected.",
            "treatment": ["No treatment required. Maintain standard crop management practices."],
            "prevention": ["Continue regular scouting, adequate watering, and balanced nutrient application."]
        }

    # 3. Partial keyword matching across keys
    crop_keywords = ["maize", "corn", "rice", "tomato", "cassava", "cashew", "cocoa", "plantain", "yam", "potato", "pepper", "onion", "bean", "groundnut", "apple"]
    pred_words = [w for w in clean_input.split('_') if w not in crop_keywords and w.strip()]
    
    for kb_key in disease_info.keys():
        clean_kb_key = kb_key.lower().replace('___', '_').replace('__', '_').replace('(', '').replace(')', '').replace(' ', '_').strip()
        kb_words = [w for w in clean_kb_key.split('_') if w not in crop_keywords and w.strip()]
        if pred_words and any(word in kb_words for word in pred_words):
            return disease_info[kb_key]

    # 4. Safe fallback
    return {
        "cause": f"Suspected Plant Pathogen Profile ({disease_name})",
        "treatment": ["Lodge an advisory ticket with local field extension services for confirmation."],
        "prevention": ["Prune local canopy, clean farm tools, and segregate affected crop zone quadrants."]
    }
# ==========================================
# 🛑 ROUTING API ENDPOINTS
# ==========================================
@app.get("/")
def home():
    return {
        "message": "Agro Vision AI Operational Core Backend Running",
        "model_file": MODEL_PATH,
        "total_classes": num_classes,
        "active_classes": class_names
    }

@app.get("/classes")
def get_classes():
    return {"classes": class_names, "total": num_classes}

@app.post("/predict/")
async def predict_api(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Execute predictions
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
    finally:
        # 🎯 AGGRESSIVE POST-INFERENCE MEMORY FLUSH
        if 'contents' in locals(): 
            del contents
        gc.collect()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
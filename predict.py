import torch
from torchvision import transforms
from PIL import Image
import config
from knowledge_base import disease_info
import torch.nn as nn
from torchvision import models

# Load the trained model
model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, config.NUM_CLASSES)
model.load_state_dict(torch.load(config.MODEL_SAVE_PATH))
model.eval()

# Define the same transformations used during training
transform = transforms.Compose([
    transforms.Resize((config.IMAGE_SIZE, config.IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

# Function to predict the disease
def predict(image_path):
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)  # Add batch dimension

    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
        
        # Map the predicted index to the class name
        # This depends on the dataset's class order.
        # For "beans" dataset: 0: angular_leaf_spot, 1: bean_rust, 2: healthy
        class_names = ["angular_leaf_spot", "bean_rust", "healthy"]
        disease_name = class_names[predicted.item()]
        
        return disease_name, confidence.item()

# Function to get disease information
def get_disease_info(disease_name):
    return disease_info.get(disease_name, "Disease information not found.")

if __name__ == "__main__":
    # Example usage:
    # Replace 'path/to/your/image.jpg' with the actual path to an image
    image_path = "path/to/your/image.jpg" 
    try:
        predicted_disease, confidence = predict(image_path)
        print(f"Predicted Disease: {predicted_disease.replace('_', ' ').title()}")
        print(f"Confidence: {confidence:.2f}")
        
        info = get_disease_info(predicted_disease)
        if isinstance(info, dict):
            print(f"Cause: {info['cause']}")
            print("Treatment:")
            for t in info['treatment']:
                print(f"- {t}")
            print("Prevention:")
            for p in info['prevention']:
                print(f"- {p}")
        else:
            print(info)
            
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found. Please check the path.")
    except Exception as e:
        print(f"An error occurred: {e}")

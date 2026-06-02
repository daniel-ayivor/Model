# check_dataset.py
import os
from torchvision import datasets

def check_my_setup():
    # Adjusted to check your absolute workspace path safely
    data_dir = "./plant_datasets/processed/train"
    
    print("\n==================================================")
    print("SCANNING YOUR DATASET FOLDERS")
    print("==================================================")
    
    if not os.path.exists(data_dir):
        # Fallback to look for a localized 'train' folder if 'plant_datasets/train' doesn't exist
        if os.path.exists("./train"):
            data_dir = "./train"
        else:
            print(f"Error: Could not locate your training image directory.")
            print("Checked: './plant_datasets/train' and './train'")
            print("Please check your spelling or layout structure in VS Code.")
            return
            
    print(f"Reading images from: {data_dir}\n")

    try:
        dataset = datasets.ImageFolder(data_dir)
        class_names = dataset.classes
        
        print(f"Success! PyTorch successfully detected {len(class_names)} classes.\n")
        print("Here are the exact class names your model will train on:")
        print("-" * 50)
        for i, cls in enumerate(class_names, 1):
            print(f" {i:02d}. {cls}")
        print("-" * 50)
        
    except Exception as e:
        print("Error parsing folders.")
        print(f"Details: {e}")

if __name__ == "__main__":
    check_my_setup()
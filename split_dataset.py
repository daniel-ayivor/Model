import os
import shutil
import random

# Define paths
base_dir = "./plant_datasets/processed"
train_dir = os.path.join(base_dir, "train")
val_dir = os.path.join(base_dir, "validation")

print("⚡ Starting dataset partition (80% Train / 20% Validation)...")

# Make sure validation folder exists
os.makedirs(val_dir, exist_ok=True)

# Loop through all 55 folders in train
class_count = 0
for class_name in os.listdir(train_dir):
    train_class_path = os.path.join(train_dir, class_name)
    
    if os.path.isdir(train_class_path):
        class_count += 1
        # Create the exact matching validation folder
        val_class_path = os.path.join(val_dir, class_name)
        os.makedirs(val_class_path, exist_ok=True)
        
        # Get all image files in this training folder
        images = [f for f in os.listdir(train_class_path) if os.path.isfile(os.path.join(train_class_path, f))]
        
        # Calculate 20% allocation for validation
        val_size = int(len(images) * 0.20)
        
        if val_size > 0:
            # Randomly select 20% of images to move
            val_images = random.sample(images, val_size)
            for img in val_images:
                src = os.path.join(train_class_path, img)
                dst = os.path.join(val_class_path, img)
                shutil.move(src, dst)

print(f"✅ Success! Processed {class_count} classes.")
print("Each training folder now has a perfectly matching validation partner.")
import os
import shutil

PROCESSED_DIR = "./plant_datasets/processed"
TRAIN_DIR = os.path.join(PROCESSED_DIR, "train_cleaned")
VAL_DIR = os.path.join(PROCESSED_DIR, "validation")
OLD_VAL_DIR = os.path.join(PROCESSED_DIR, "validation_old")

def fix_validation_folders():
    if not os.path.exists(TRAIN_DIR):
        print("❌ Error: Train cleaned directory not found!")
        return

    # Get the exact 44 class names from the training folder
    train_classes = sorted([d for d in os.listdir(TRAIN_DIR) if os.path.isdir(os.path.join(TRAIN_DIR, d))])
    print(f"📁 Found {len(train_classes)} valid classes in training set.")

    # If old validation exists, back it up or clear it out
    if os.path.exists(VAL_DIR):
        if os.path.exists(OLD_VAL_DIR):
            shutil.rmtree(OLD_VAL_DIR)
        print("📦 Moving old mismatched validation folder to 'validation_old'...")
        shutil.move(VAL_DIR, OLD_VAL_DIR)

    os.makedirs(VAL_DIR, exist_ok=True)

    # If we have an old validation folder, try to salvage images for the 44 classes
    salvaged_count = 0
    if os.path.exists(OLD_VAL_DIR):
        print("♻️ Salvaging validation images for matching 44 classes...")
        for cls in train_classes:
            old_cls_path = os.path.join(OLD_VAL_DIR, cls)
            new_cls_path = os.path.join(VAL_DIR, cls)
            os.makedirs(new_cls_path, exist_ok=True)
            
            if os.path.exists(old_cls_path):
                for img in os.listdir(old_cls_path):
                    src_img = os.path.join(old_cls_path, img)
                    if os.path.isfile(src_img):
                        shutil.copy(src_img, new_cls_path)
                        salvaged_count += 1
        print(f"✅ Salvaged {salvaged_count} validation images from old folder.")

    # For any class that has 0 images in the new validation folder (e.g., new classes like 'not_a_plant'), 
    # let's pull a small subset (or 20% of images) from the training folder so validation doesn't crash on empty classes!
    print("⚖️ Ensuring every validation class has at least a few samples...")
    for cls in train_classes:
        cls_val_path = os.path.join(VAL_DIR, cls)
        if not os.listdir(cls_val_path):
            print(f"   ℹ️ Populating validation split for new/empty class: {cls}")
            cls_train_path = os.path.join(TRAIN_DIR, cls)
            images = [img for img in os.listdir(cls_train_path) if os.path.isfile(os.path.join(cls_train_path, img))]
            
            # Take 20% of training images for validation (or at least a few)
            num_to_move = max(1, int(len(images) * 0.2))
            for img in images[:num_to_move]:
                shutil.copy(os.path.join(cls_train_path, img), os.path.join(cls_val_path, img))

    print("🎉 Validation folder successfully synchronized to 44 classes!")

if __name__ == "__main__":
    fix_validation_folders()
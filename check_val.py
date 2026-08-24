import os

TRAIN_DIR = "./plant_datasets/processed/train_cleaned"
VAL_DIR = "./plant_datasets/processed/validation"

def inspect_directories():
    if not os.path.exists(TRAIN_DIR) or not os.path.exists(VAL_DIR):
        print("❌ Error: Train or Validation directory path is incorrect.")
        return

    train_classes = sorted([d for d in os.listdir(TRAIN_DIR) if os.path.isdir(os.path.join(TRAIN_DIR, d))])
    val_classes = sorted([d for d in os.listdir(VAL_DIR) if os.path.isdir(os.path.join(VAL_DIR, d))])

    print(f"📁 Training Classes Count: {len(train_classes)}")
    print(f"📁 Validation Classes Count: {len(val_classes)}")

    train_set = set(train_classes)
    val_set = set(val_classes)

    only_in_train = train_set - val_set
    only_in_val = val_set - train_set

    if only_in_train:
        print(f"\n⚠️ Warning: Classes found in Train but MISSING in Validation:\n{only_in_train}")
    
    if only_in_val:
        print(f"\n⚠️ Warning: Classes found in Validation but NOT in Train (causes index out of bounds!):\n{only_in_val}")

    if not only_in_train and not only_in_val:
        print("\n✅ Perfect match! Train and Validation classes are completely identical.")

    # Check for stray files inside class folders
    print("\n🔍 Checking for non-image files or hidden files...")
    for parent_dir in [TRAIN_DIR, VAL_DIR]:
        for root, dirs, files in os.walk(parent_dir):
            for file in files:
                if not file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp')):
                    print(f"   Stray file found: {os.path.join(root, file)}")

    print("\n🏁 Inspection complete!")

if __name__ == "__main__":
    inspect_directories()
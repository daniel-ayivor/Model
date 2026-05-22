from pathlib import Path

base = Path("plant_datasets/processed")
print("=== CLASS IMAGE COUNTS ===")
for split in ["train", "validation"]:
    print(f"\n{split.upper()}:")
    split_path = base / split
    for class_dir in sorted(split_path.iterdir()):
        if class_dir.is_dir():
            imgs = list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.png"))
            print(f"  {class_dir.name:<35} {len(imgs)} images")

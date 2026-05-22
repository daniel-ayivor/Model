import shutil
from pathlib import Path

# Source: where rice images actually are
rice_source_train = Path("plant_datasets/train/rice leafs/train")
rice_source_test  = Path("plant_datasets/train/rice leafs/test")

# Destination: processed folders
rice_dest_train = Path("plant_datasets/processed/train/rice leafs")
rice_dest_val   = Path("plant_datasets/processed/validation/rice leafs")

rice_dest_train.mkdir(parents=True, exist_ok=True)
rice_dest_val.mkdir(parents=True, exist_ok=True)

def copy_images(source_root, dest_dir):
    moved = 0
    for img in source_root.rglob("*.jpg"):
        # Prefix with subfolder name to avoid name collisions
        dest = dest_dir / f"{img.parent.name}_{img.name}"
        if not dest.exists():
            shutil.copy(str(img), dest)
            moved += 1
    return moved

# Copy train rice images -> processed/train/rice leafs
t = copy_images(rice_source_train, rice_dest_train)
print(f"Copied {t} images to train/rice leafs")

# Copy test rice images -> processed/validation/rice leafs  
v = copy_images(rice_source_test, rice_dest_val)
print(f"Copied {v} images to validation/rice leafs")

# Final counts
train_total = len(list(rice_dest_train.glob("*.jpg")))
val_total   = len(list(rice_dest_val.glob("*.jpg")))
print(f"\nFinal counts:")
print(f"  train/rice leafs:      {train_total} images")
print(f"  validation/rice leafs: {val_total} images")

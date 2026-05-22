import os
from pathlib import Path

base = Path("plant_datasets")
print("=== All directories under plant_datasets ===")
for p in sorted(base.rglob("*")):
    if p.is_dir():
        img_count = len(list(p.glob("*.jpg")) + list(p.glob("*.png")) + list(p.glob("*.jpeg")))
        if img_count > 0:
            print(f"  {p}  -->  {img_count} images")

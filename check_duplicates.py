import hashlib
from pathlib import Path
from collections import defaultdict

def find_duplicates(folder_path):
    folder = Path(folder_path)
    hashes = defaultdict(list)
    
    print(f"Scanning {folder} for duplicate images...")
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    
    files = [f for f in folder.rglob("*") if f.suffix.lower() in image_extensions]
    
    for img_path in files:
        try:
            # Read file and compute MD5 hash of its bytes
            hasher = hashlib.md5()
            with open(img_path, "rb") as f:
                buf = f.read()
                hasher.update(buf)
            file_hash = hasher.hexdigest()
            hashes[file_hash].append(img_path)
        except Exception as e:
            print(f"Error reading {img_path}: {e}")
            
    # Filter out unique files, keep only duplicates
    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    
    print(f"\nScan complete. Total images checked: {len(files)}")
    print(f"Found {len(duplicates)} groups of duplicate files.")
    
    for h, paths in duplicates.items():
        print("\nDuplicate Group:")
        for p in paths:
            print(f"  - {p}")

if __name__ == "__main__":
    target_folder = r"C:\Users\Daniel Kofi Ayivor\Documents\Mine\WarmiGro\backend\Model\plant_datasets\processed\train_cleaned\not_a_plant"
    find_duplicates(target_folder)
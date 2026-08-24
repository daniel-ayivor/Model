import os
import shutil
import sys

def prune_sparse_classes(base_path, min_images=100):
    if not os.path.exists(base_path):
        print(f"Error: Path does not exist -> {base_path}")
        return

    print(f"Checking for classes with fewer than {min_images} images in: {base_path}\n")
    
    quarantine_dir = os.path.join(base_path, "_sparse_review")
    os.makedirs(quarantine_dir, exist_ok=True)

    items = os.listdir(base_path)
    for folder_name in items:
        folder_path = os.path.join(base_path, folder_name)
        
        # Skip files, system folders, or the quarantine/not_a_plant folders
        if not os.path.isdir(folder_path) or folder_name.startswith("_") or folder_name == "not_a_plant":
            continue

        # Count images in the folder
        images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        count = len(images)

        if count < min_images:
            target_path = os.path.join(quarantine_dir, folder_name)
            print(f"Quarantining sparse class '{folder_name}' ({count} images) -> moved to _sparse_review")
            if os.path.exists(target_path):
                shutil.rmtree(target_path)
            shutil.move(folder_path, target_path)

    print("\nSparse class pruning complete! Quarantined folders moved to _sparse_review.")

if __name__ == "__main__":
    target_path = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\Daniel Kofi Ayivor\Documents\Mine\WarmiGro\backend\Model\plant_datasets\processed\train"
    prune_sparse_classes(target_path)
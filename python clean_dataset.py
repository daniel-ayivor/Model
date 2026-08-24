import os
import shutil
import sys

def clean_and_restructure_dataset(base_path):
    if not os.path.exists(base_path):
        print(f"Error: Path does not exist -> {base_path}")
        return

    print(f"Starting dataset cleanup and restructuring in: {base_path}\n")

    # 1. Define Merge Rules based on your audit log
    merge_mappings = {
        'apple_apple_scab': ['Apple___Apple_scab'],
        'apple_black_rot': ['Apple___Black_rot'],
        'apple_cedar_apple_rust': ['Apple___Cedar_apple_rust'],
        'apple_healthy': ['Apple___healthy'],
        'potato_early_blight': ['Potato___Early_blight'],
        'potato_healthy': ['Potato___healthy'],
        'potato_late_blight': ['Potato___Late_blight'],
        'tomato_target_spot': ['Tomato__Target_Spot'],
        'tomato_tomato_mosaic_virus': ['Tomato__Tomato_mosaic_virus']
    }

    # Execute merges
    for canonical_name, sources in merge_mappings.items():
        canonical_dir = os.path.join(base_path, canonical_name)
        os.makedirs(canonical_dir, exist_ok=True)
        
        for src in sources:
            src_dir = os.path.join(base_path, src)
            if os.path.exists(src_dir) and src_dir != canonical_dir:
                print(f"Merging '{src}' into '{canonical_name}'...")
                for item in os.listdir(src_dir):
                    s_path = os.path.join(src_dir, item)
                    d_path = os.path.join(canonical_dir, item)
                    if os.path.isfile(s_path):
                        # Avoid name collisions
                        if not os.path.exists(d_path):
                            shutil.move(s_path, d_path)
                        else:
                            base, ext = os.path.splitext(item)
                            counter = 1
                            while os.path.exists(os.path.join(canonical_dir, f"{base}_{counter}{ext}")):
                                counter += 1
                            shutil.move(s_path, os.path.join(canonical_dir, f"{base}_{counter}{ext}"))
                # Remove empty old directory
                try:
                    os.rmdir(src_dir)
                except OSError:
                    pass

    # 2. Handle ' copy' suffix folders by merging them into their cleaned counterparts
    all_folders = os.listdir(base_path)
    for folder in all_folders:
        if " copy" in folder:
            clean_name = folder.replace(" copy", "").strip()
            src_dir = os.path.join(base_path, folder)
            target_dir = os.path.join(base_path, clean_name)
            
            if os.path.exists(src_dir) and os.path.isdir(src_dir):
                os.makedirs(target_dir, exist_ok=True)
                print(f"Merging suffix folder '{folder}' into '{clean_name}'...")
                for item in os.listdir(src_dir):
                    s_path = os.path.join(src_dir, item)
                    d_path = os.path.join(target_dir, item)
                    if os.path.isfile(s_path) and not os.path.exists(d_path):
                        shutil.move(s_path, d_path)
                shutil.rmtree(src_dir)

    # 3. Isolate Bare Crop Folders (Cashew, Maize, Tomato, etc.) 
    # Moving them to an 'unsorted_review' folder so they don't break training classes
    bare_crops = ["Cashew", "Cassava", "Maize", "Rice", "Tomato"]
    unsorted_dir = os.path.join(base_path, "_unsorted_review")
    
    for crop in bare_crops:
        crop_path = os.path.join(base_path, crop)
        if os.path.exists(crop_path) and os.path.isdir(crop_path):
            os.makedirs(unsorted_dir, exist_ok=True)
            target_crop_unsorted = os.path.join(unsorted_dir, crop)
            print(f"Isolating bare crop folder '{crop}' to '{unsorted_dir}' for manual review...")
            if os.path.exists(target_crop_unsorted):
                shutil.rmtree(target_crop_unsorted)
            shutil.move(crop_path, target_crop_unsorted)

    # 4. Create 'not_a_plant' negative class directory for anti-hallucination training
    not_a_plant_dir = os.path.join(base_path, "not_a_plant")
    os.makedirs(not_a_plant_dir, exist_ok=True)
    print(f"\n[+] Created negative class directory at: {not_a_plant_dir}")
    print("    -> Drop non-plant images (UI screenshots, architecture diagrams, random objects) here.")

    print("\nDataset cleanup and restructuring completed successfully!")

if __name__ == "__main__":
    target_path = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\Daniel Kofi Ayivor\Documents\Mine\WarmiGro\backend\Model\plant_datasets\processed\train"
    clean_and_restructure_dataset(target_path)
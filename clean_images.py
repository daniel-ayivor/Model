import os
from PIL import Image, ImageFile

# Force Pillow to be lenient with minor stream errors if possible, 
# but we still want to delete files that completely crash the loader.
ImageFile.LOAD_TRUNCATED_IMAGES = False 

def aggressive_dataset_cleaner(root_dir):
    print(f"--- Starting Aggressive Dataset Purge in: {root_dir} ---")
    purged_count = 0
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(valid_extensions):
                file_path = os.path.join(dirpath, filename)
                try:
                    with Image.open(file_path) as img:
                        # 1. Verify headers
                        img.verify()
                    
                    # 2. Re-open and force-load the actual pixel streams to catch hidden truncation
                    with Image.open(file_path) as img:
                        img.load() 
                        
                except (IOError, SyntaxError, OSError, Exception) as e:
                    print(f"❌ Removing corrupted/broken stream image: {file_path}")
                    try:
                        os.remove(file_path)
                        purged_count += 1
                    except Exception as deletion_error:
                        print(f"   Could not delete file: {deletion_error}")

    print(f"\n--- Purge complete! Safely dropped {purged_count} broken files. ---")

if __name__ == '__main__':
    aggressive_dataset_cleaner("plant_datasets/symptoms")
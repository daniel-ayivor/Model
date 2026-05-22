
import os
import shutil

def flatten_directory(base_path):
    """
    Finds directories starting with 'archive' within the base_path,
    and moves their contents up one level.
    """
    if not os.path.isdir(base_path):
        print(f"Directory not found, skipping: {base_path}")
        return

    print(f"Flattening directory: {base_path}")
    
    # Find all archive-like directories
    archive_dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d)) and d.startswith('archive')]

    if not archive_dirs:
        print("  - No 'archive' directories found to flatten.")
        return

    for archive_dir_name in archive_dirs:
        archive_dir_path = os.path.join(base_path, archive_dir_name)
        print(f"  - Processing archive directory: {archive_dir_name}")

        # Get all subdirectories (the disease folders) within the archive folder
        for item_name in os.listdir(archive_dir_path):
            source_item_path = os.path.join(archive_dir_path, item_name)
            dest_item_path = os.path.join(base_path, item_name)

            # Check if a directory with the same name already exists at the destination
            if os.path.exists(dest_item_path):
                print(f"    - WARNING: '{item_name}' already exists in '{base_path}'. Skipping move.")
                continue
            
            # Move the disease folder up one level
            try:
                print(f"    - Moving '{source_item_path}' to '{dest_item_path}'")
                shutil.move(source_item_path, dest_item_path)
            except Exception as e:
                print(f"      ERROR moving directory: {e}")
        
        # After moving all contents, remove the now-empty archive directory
        try:
            print(f"  - Removing empty archive directory: {archive_dir_path}")
            os.rmdir(archive_dir_path)
        except Exception as e:
            print(f"    - WARNING: Could not remove directory '{archive_dir_path}'. It might not be empty. {e}")


def main():
    """
    Main function to flatten the train and validation directories.
    """
    print("Starting to flatten dataset structure...")
    
    base_data_path = 'plant_datasets'
    
    flatten_directory(os.path.join(base_data_path, 'train'))
    flatten_directory(os.path.join(base_data_path, 'validation'))

    print("\nFlattening process complete.")

if __name__ == '__main__':
    main()

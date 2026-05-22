import os
import shutil
import random

def prepare_dataset(source_root='plant_datasets/train', dest_root='plant_datasets/processed', split_ratio=0.8):
    """
    Organizes a dataset from a source directory into a new destination directory
    with 'train' and 'validation' subfolders.
    """
    print("--- Starting Dataset Preparation ---")
    
    train_dir = os.path.join(dest_root, 'train')
    validation_dir = os.path.join(dest_root, 'validation')

    # Start with a clean slate
    if os.path.exists(dest_root):
        print(f"Removing existing directory: {dest_root}")
        shutil.rmtree(dest_root)

    print(f"Creating new directory structure at: {dest_root}")
    os.makedirs(train_dir)
    os.makedirs(validation_dir)

    # Find all the class directories in the source
    for class_name in os.listdir(source_root):
        class_path = os.path.join(source_root, class_name)
        if os.path.isdir(class_path):
            print(f"\nProcessing class: {class_name}")
            
            # Create corresponding class directories in train and validation sets
            train_class_dir = os.path.join(train_dir, class_name)
            validation_class_dir = os.path.join(validation_dir, class_name)
            os.makedirs(train_class_dir)
            os.makedirs(validation_class_dir)
            
            # Get all image files
            all_files = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            random.shuffle(all_files)
            
            # Split the files
            split_index = int(len(all_files) * split_ratio)
            train_files = all_files[:split_index]
            validation_files = all_files[split_index:]
            
            # Copy files to the new directories
            for file_name in train_files:
                shutil.copy(os.path.join(class_path, file_name), os.path.join(train_class_dir, file_name))
                
            for file_name in validation_files:
                shutil.copy(os.path.join(class_path, file_name), os.path.join(validation_class_dir, file_name))
                
            print(f"  -> Copied {len(train_files)} images to training set.")
            print(f"  -> Copied {len(validation_files)} images to validation set.")

    print("\n--- Dataset Preparation Finished ---")

if __name__ == '__main__':
    prepare_dataset()

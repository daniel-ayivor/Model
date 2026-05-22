import os
import shutil

def organize_dataset():
    """
    Organizes the plant disease dataset into crop-specific folders.
    """
    base_dir = "plant_datasets"
    source_dir_train = os.path.join(base_dir, "train")
    source_dir_validation = os.path.join(base_dir, "validation")
    
    dest_dir_crops = os.path.join(base_dir, "crops")

    # Mapping from disease folder to crop type
    # This is based on the folder names you provided
    disease_to_crop = {
        # Rice Diseases
        "Bacterial Leaf Blight": "Rice",
        "Brown Spot": "Rice",
        "Healthy Rice Leaf": "Rice",
        "Leaf Blast": "Rice",
        "Leaf scald": "Rice",
        "Narrow Brown Leaf Spot": "Rice",
        "Rice Hispa": "Rice",
        "Sheath Blight": "Rice",
        
        # Cashew Diseases
        "Cashew anthracnose": "Cashew",
        "Cashew gumosis": "Cashew",
        "Cashew healthy": "Cashew",
        "Cashew leaf miner": "Cashew",
        "Cashew red rust": "Cashew",

        # Cassava Diseases
        "Cassava bacterial blight": "Cassava",
        "Cassava brown spot": "Cassava",
        "Cassava green mite": "Cassava",
        "Cassava healthy": "Cassava",
        "Cassava mosaic": "Cassava",

        # Maize Diseases
        "Maize fall armyworm": "Maize",
        "Maize grasshoper": "Maize",
        "Maize healthy": "Maize",
        "Maize leaf beetle": "Maize",
        "Maize leaf blight": "Maize",
        "Maize leaf spot": "Maize",
        "Maize streak virus": "Maize",

        # Tomato Diseases
        "Tomato healthy": "Tomato",
        "Tomato leaf blight": "Tomato",
        "Tomato leaf curl": "Tomato",
        "Tomato septoria leaf spot": "Tomato",
        "Tomato verticulium wilt": "Tomato",
        "Tomato___Bacterial_spot": "Tomato",
        "Tomato___Early_blight": "Tomato",
        "Tomato___healthy": "Tomato",
        "Tomato___Late_blight": "Tomato",
        "Tomato___Leaf_Mold": "Tomato",
        "Tomato___Septoria_leaf_spot": "Tomato",
        "Tomato___Spider_mites Two-spotted_spider_mite": "Tomato",
        "Tomato___Target_Spot": "Tomato",
        "Tomato___Tomato_mosaic_virus": "Tomato",
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "Tomato",

        # General/Ambiguous - you might need to sort these manually
        "Mossaic Virus": "Tomato", # Assuming Tomato, adjust if needed
        "Southern blight": "Tomato", # Assuming Tomato, adjust if needed
        "Sudden Death Syndrone": "Tomato", # Assuming Tomato, adjust if needed
        "Yellow Mosaic": "Tomato" # Assuming Tomato, adjust if needed
    }

    for source_parent in [source_dir_train, source_dir_validation]:
        if not os.path.exists(source_parent):
            print(f"Source directory not found: {source_parent}")
            continue

        for disease_folder in os.listdir(source_parent):
            crop_type = disease_to_crop.get(disease_folder)
            
            if not crop_type:
                print(f"Warning: No crop type found for '{disease_folder}'. Skipping.")
                continue

            # Determine if we are in train or validation
            train_or_val = os.path.basename(source_parent)
            dest_folder = os.path.join(dest_dir_crops, train_or_val, crop_type)
            
            source_folder_path = os.path.join(source_parent, disease_folder)
            
            if not os.path.isdir(source_folder_path):
                continue

            print(f"Moving images from '{source_folder_path}' to '{dest_folder}'...")

            for filename in os.listdir(source_folder_path):
                source_file = os.path.join(source_folder_path, filename)
                dest_file = os.path.join(dest_folder, filename)
                
                # To avoid overwriting files with the same name from different
                # disease folders, we can add a prefix.
                if os.path.exists(dest_file):
                    new_filename = f"{disease_folder.replace(' ', '_')}_{filename}"
                    dest_file = os.path.join(dest_folder, new_filename)

                                # Use shutil.copy to be non-destructive
                shutil.copy(src_file_path, dest_file_path)
            
            # Optional: remove the now-empty disease folder
            # os.rmdir(source_folder_path)

    print("\nDataset organization complete.")
    print("Please review the 'crops' directory to ensure everything is correct.")
    print("You may need to manually sort any folders that were skipped.")

if __name__ == "__main__":
    organize_dataset()

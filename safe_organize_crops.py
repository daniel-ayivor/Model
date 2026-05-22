
import os
import shutil

# Base paths
BASE_DATA_PATH = 'plant_datasets'
CROP_DATA_PATH = os.path.join(BASE_DATA_PATH, 'crops')

# Mapping of disease subfolders to their parent crop
CROP_MAPPING = {
    # Rice Diseases
    'Bacterial Leaf Blight': 'Rice',
    'Brown Spot': 'Rice',
    'Healthy Rice Leaf': 'Rice',
    'Leaf Blast': 'Rice',
    'Leaf scald': 'Rice',
    'Narrow Brown Leaf Spot': 'Rice',
    'Rice Hispa': 'Rice',
    'Sheath Blight': 'Rice',
    # Cashew Diseases
    'Cashew anthracnose': 'Cashew',
    'Cashew gumosis': 'Cashew',
    'Cashew healthy': 'Cashew',
    'Cashew leaf miner': 'Cashew',
    'Cashew red rust': 'Cashew',
    # Cassava Diseases
    'Cassava bacterial blight': 'Cassava',
    'Cassava brown spot': 'Cassava',
    'Cassava green mite': 'Cassava',
    'Cassava healthy': 'Cassava',
    'Cassava mosaic': 'Cassava',
    # Maize Diseases
    'Maize fall armyworm': 'Maize',
    'Maize grasshoper': 'Maize',
    'Maize healthy': 'Maize',
    'Maize leaf beetle': 'Maize',
    'Maize leaf blight': 'Maize',
    'Maize leaf spot': 'Maize',
    'Maize streak virus': 'Maize',
    # Tomato Diseases
    'Mossaic Virus': 'Tomato',
    'Southern blight': 'Tomato',
    'Sudden Death Syndrone': 'Tomato',
    'Tomato healthy': 'Tomato',
    'Tomato leaf blight': 'Tomato',
    'Tomato leaf curl': 'Tomato',
    'Tomato septoria leaf spot': 'Tomato',
    'Tomato verticulium wilt': 'Tomato',
    'Tomato___Bacterial_spot': 'Tomato',
    'Tomato___Early_blight': 'Tomato',
    'Tomato___healthy': 'Tomato',
    'Tomato___Late_blight': 'Tomato',
    'Tomato___Leaf_Mold': 'Tomato',
    'Tomato___Septoria_leaf_spot': 'Tomato',
    'Tomato___Spider_mites Two-spotted_spider_mite': 'Tomato',
    'Tomato___Target_Spot': 'Tomato',
    'Tomato___Tomato_mosaic_virus': 'Tomato',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 'Tomato',
    'Yellow Mosaic': 'Tomato',
}

def organize_dataset():
    """
    Copies files from the original flat directory structure to a new
    nested structure organized by crop.
    """
    print("Starting dataset organization with safe copy...")

    # Loop over 'train' and 'validation' sets
    for set_name in ['train', 'validation']:
        source_set_path = os.path.join(BASE_DATA_PATH, set_name)
        dest_set_path = os.path.join(CROP_DATA_PATH, set_name)

        if not os.path.isdir(source_set_path):
            print(f"Source directory not found, skipping: {source_set_path}")
            continue

        print(f"Processing set: {set_name}")

        # Loop through each disease folder in the source directory
        for disease_folder in os.listdir(source_set_path):
            source_disease_path = os.path.join(source_set_path, disease_folder)

            if not os.path.isdir(source_disease_path):
                continue

            # Determine the crop type from the mapping
            crop_name = CROP_MAPPING.get(disease_folder)
            if not crop_name:
                print(f"  - WARNING: No crop mapping found for '{disease_folder}'. Skipping.")
                continue

            # Create the destination directory for the crop
            dest_crop_path = os.path.join(dest_set_path, crop_name)
            os.makedirs(dest_crop_path, exist_ok=True)

            # Copy each file from the source to the destination
            for filename in os.listdir(source_disease_path):
                source_file_path = os.path.join(source_disease_path, filename)
                dest_file_path = os.path.join(dest_crop_path, filename)

                # Check if it's a file
                if os.path.isfile(source_file_path):
                    try:
                        print(f"  - Copying '{source_file_path}' to '{dest_file_path}'")
                        shutil.copy(source_file_path, dest_file_path)
                    except Exception as e:
                        print(f"    ERROR copying file: {e}")

    print("\nDataset organization complete.")
    print("Please review the 'plant_datasets' directory.")

if __name__ == '__main__':
    organize_dataset()

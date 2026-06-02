


import os
import shutil

# COMPLETE SYMPTOM MAPPING
SYMPTOM_MAPPING = {
    # Blight Symptoms
    'Bacterial Leaf Blight': 'Blight',
    'Cassava bacterial blight': 'Blight',
    'Maize leaf blight': 'Blight',
    'Sheath Blight': 'Blight',
    'Southern blight': 'Blight',
    'Tomato leaf blight': 'Blight',
    'Tomato___Early_blight': 'Blight',
    'Tomato___Late_blight': 'Blight',

    # Spot Symptoms
    'Brown Spot': 'Leaf_Spot',
    'Cassava brown spot': 'Leaf_Spot',
    'Maize leaf spot': 'Leaf_Spot',
    'Narrow Brown Leaf Spot': 'Leaf_Spot',
    'Tomato septoria leaf spot': 'Leaf_Spot',
    'Tomato___Bacterial_spot': 'Leaf_Spot',
    'Tomato___Septoria_leaf_spot': 'Leaf_Spot',
    'Tomato___Target_Spot': 'Leaf_Spot',

    # Healthy Plants (Shared clean baseline)
    'Healthy Rice Leaf': 'Healthy',
    'Cashew healthy': 'Healthy',
    'Cassava healthy': 'Healthy',
    'Maize healthy': 'Healthy',
    'Tomato healthy': 'Healthy',
    'Tomato___healthy': 'Healthy',

    # Viruses & Mosaic Layouts
    'Cassava mosaic': 'Mosaic_Virus',
    'Maize streak virus': 'Streak_Virus',
    'Mossaic Virus': 'Mosaic_Virus',
    'Tomato leaf curl': 'Curl_Virus',
    'Tomato___Tomato_mosaic_virus': 'Mosaic_Virus',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 'Curl_Virus',
    'Yellow Mosaic': 'Mosaic_Virus',

    # Pests / Insects
    'Cashew leaf miner': 'Leaf_Miner',
    'Cashew red rust': 'Rust',
    'Cassava green mite': 'Mites',
    'Maize fall armyworm': 'Armyworm',
    'Maize grasshoper': 'Grasshopper',
    'Maize leaf beetle': 'Beetle',
    'Rice Hispa': 'Hispa_Beetle',
    'Tomato___Spider_mites Two-spotted_spider_mite': 'Mites',

    # Unique Pathogens
    'Cashew anthracnose': 'Anthracnose',
    'Cashew gumosis': 'Gumosis',
    'Leaf Blast': 'Leaf_Blast',
    'Leaf scald': 'Leaf_Scald',
    'Sudden Death Syndrone': 'Sudden_Death',
    'Tomato verticulium wilt': 'Wilt',
    'Tomato___Leaf_Mold': 'Leaf_Mold',
}

def ultimate_organizer():
    print("--- Starting the Ultimate Dataset Organizer (Fixed Path Mode) ---")
    
    # CHANGED: Point directly to 'processed' where your actual subfolders live
    base_source_path = os.path.join('plant_datasets', 'processed')
    dest_path = os.path.join('plant_datasets', 'symptoms')
    
    os.makedirs(dest_path, exist_ok=True)
    
    # Process both train and validation from the 'processed' folder
    for set_name in ['train', 'validation']:
        source_set_path = os.path.join(base_source_path, set_name)
        dest_set_path = os.path.join(dest_path, set_name)
        
        # Clear out any bad old folders in symptoms to avoid mixing plant names and symptom names
        if os.path.exists(dest_set_path):
            shutil.rmtree(dest_set_path)
        os.makedirs(dest_set_path, exist_ok=True)

        if not os.path.isdir(source_set_path):
            print(f"Source folder not found: {source_set_path}")
            continue

        print(f"\nProcessing directory: {source_set_path}")

        for dirpath, _, filenames in os.walk(source_set_path):
            parent_folder_name = os.path.basename(dirpath)
            symptom_name = SYMPTOM_MAPPING.get(parent_folder_name)
            
            if symptom_name:
                final_dest_dir = os.path.join(dest_set_path, symptom_name)
                os.makedirs(final_dest_dir, exist_ok=True)
                
                for filename in filenames:
                    source_file = os.path.join(dirpath, filename)
                    dest_file = os.path.join(final_dest_dir, filename)
                    
                    if not os.path.exists(dest_file):
                        try:
                            shutil.copy2(source_file, dest_file)
                        except Exception as e:
                            print(f"      ERROR copying file: {e}")

        # Simple verification check to make sure it organized correctly
        found_classes = os.listdir(dest_set_path) if os.path.exists(dest_set_path) else []
        print(f"Successfully organized '{set_name}'. Found {len(found_classes)} symptom categories.")

    print("\n--- Ultimate Dataset Organizer Finished ---")
    print("Your clean, matching datasets are ready in: 'plant_datasets/symptoms'")

if __name__ == '__main__':
    ultimate_organizer()
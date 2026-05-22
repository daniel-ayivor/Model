# # =========================
# # CONFIG
# # =========================
# #
# # =========================
# # DEVICE
# # =========================
# DEVICE = "cuda"

# # =========================
# # DATASET
# # =========================
# DATASET_NAME = "beans"
# CUSTOM_DATASET_PATH = "plant_datasets" # Root folder for your custom dataset

# # =========================
# # IMAGE TRANSFORMS
# # =========================
# IMAGE_SIZE = 224

# # =========================
# # DATALOADERS
# # =========================
# BATCH_SIZE = 32
# NUM_WORKERS = 0

# # =========================
# # MODEL
# # =========================
# MODEL_NAME = "resnet18"
# NUM_CLASSES = 27

# # =========================
# # TRAINING
# # =========================
# EPOCHS = 20
# LEARNING_RATE = 0.001

# # =========================
# # SAVE MODEL
# # =========================
# MODEL_SAVE_PATH = "plant_disease_model.pth"

# =========================
# CONFIG
# =========================
#
# =========================
# DEVICE
# =========================
DEVICE = "cuda"

# =========================
# DATASET
# =========================
DATASET_NAME = "beans"
# CRUCIAL UPDATE 1: Point directly to the new "symptoms" subfolder created by your organizer script
CUSTOM_DATASET_PATH = "plant_datasets/symptoms" 

# =========================
# IMAGE TRANSFORMS
# =========================
IMAGE_SIZE = 224

# =========================
# DATALOADERS
# =========================
BATCH_SIZE = 32
NUM_WORKERS = 0

# =========================
# MODEL
# =========================
MODEL_NAME = "resnet18"
# CRUCIAL UPDATE 2: Change this from 27 to 19 to match your 19 collapsed symptom classes
NUM_CLASSES = 16

# =========================
# TRAINING
# =========================
# PRO-TIP: You can drop this to 10 or 15 since 19 classes learn faster than 27+ mixed categories, 
# but keeping it at 20 is perfectly fine too!
EPOCHS = 20
LEARNING_RATE = 0.001

# =========================
# SAVE MODEL
# =========================
# CRUCIAL UPDATE 3: Rename your save file so you don't accidentally overwrite your old model weights
MODEL_SAVE_PATH = "plant_symptom_model.pth"


# train.py
import os
import shutil
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from PIL import Image, ImageFile

# 👑 CRUCIAL PILLOW CONFIGURATION
ImageFile.LOAD_TRUNCATED_IMAGES = True

# ==================================================
# 🛠️ CONFIGURATION
# ==================================================
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {DEVICE}")

TRAIN_DIR = "./plant_datasets/processed/train"
VAL_DIR = "./plant_datasets/processed/validation"

IMAGE_SIZE = 224
BATCH_SIZE = 16  
NUM_WORKERS = 0
EPOCHS = 20
LEARNING_RATE = 0.001
MODEL_SAVE_PATH = "plant_disease_model.pth"

# ==================================================
# 🧹 FILE SCRUBBING ENGINE
# ==================================================
print("🧼 Deep scrubbing datasets for hidden or corrupted files...")
VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.tiff', '.webp')

corrupt_count = 0
for target_dir in [TRAIN_DIR, VAL_DIR]:
    if not os.path.exists(target_dir):
        continue

    for root, dirs, files in os.walk(target_dir, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)

            if file.startswith('.') or file.lower() in ['desktop.ini', 'thumbs.db'] or not file.lower().endswith(VALID_EXTENSIONS):
                try:
                    os.remove(file_path)
                except Exception:
                    pass
                continue

            try:
                with Image.open(file_path) as img:
                    img.verify()  
            except Exception:
                print(f"⚠️ Removing corrupted image header: {file}")
                try:
                    os.remove(file_path)
                    corrupt_count += 1
                except Exception:
                    pass

        if root != target_dir and not os.listdir(root):
            try:
                os.rmdir(root)
            except Exception:
                pass

print(f"✅ Scrubbing complete. Eliminated {corrupt_count} corrupt image files safely.")

# ==================================================
# 📸 DATA TRANSFORMS & LOADERS
# ==================================================
train_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

val_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

print("📂 Loading datasets from processed folders...")
train_dataset = datasets.ImageFolder(root=TRAIN_DIR, transform=train_transform)
val_dataset = datasets.ImageFolder(root=VAL_DIR, transform=val_transform)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS)

num_classes = len(train_dataset.classes)
print(f"✅ Success! Detected {num_classes} matching training/validation classes.")

# ==================================================
# 🚀 MODEL & RESUME SELECTION CORE
# ==================================================
model = models.resnet18(weights=None if os.path.exists(MODEL_SAVE_PATH) else models.ResNet18_Weights.DEFAULT)
model.fc = nn.Linear(model.fc.in_features, num_classes)
model = model.to(DEVICE)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# 🔄 Dynamic State Tracking Parameters
best_acc = 0.0
start_epoch = 0

if os.path.exists(MODEL_SAVE_PATH):
    print(f"♻️ Found existing weights checkpoint at '{MODEL_SAVE_PATH}'. Restoring pipeline states...")
    try:
        checkpoint = torch.load(MODEL_SAVE_PATH, map_location=DEVICE)
        
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            start_epoch = checkpoint['epoch'] + 1  # 🌟 Advance to the next pending epoch
            best_acc = checkpoint['best_acc']
            print(f"   ✅ Successfully restored state. Resuming from Epoch {start_epoch} (Previous Best Accuracy: {best_acc:.4f})")
        else:
            model.load_state_dict(checkpoint, strict=False)
            print("   ✅ Loaded raw fallback structure weights. (Epoch indices reset to default 0).")
            
    except Exception as e:
        print(f"⚠️ State recovery failed: {e}. Starting fresh from base network configurations.")
else:
    print("🏗️ No local checkpoint discovered. Launching clean training initialization...")

# ==================================================
# 🔄 RESILIENT TRAINING & VALIDATION LOOP
# ==================================================
print("🏋️ Launching execution loop pipeline...")

for epoch in range(start_epoch, EPOCHS):
    print(f"\n--- Epoch {epoch+1}/{EPOCHS} ---")

    # --- Training Step ---
    model.train()
    running_loss, running_corrects = 0.0, 0
    train_batch_idx = 0

    train_iter = iter(train_loader)
    while True:
        try:
            inputs, labels = next(train_iter)
            train_batch_idx += 1
            if train_batch_idx % 10 == 0:
                print(f"   ⏳ Train Progress: Batch {train_batch_idx} loaded...")
        except StopIteration:
            break  
        except Exception as e:
            print(f"   ⚠️ Skipping training batch due to a broken internal data stream: {e}")
            continue

        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        _, preds = torch.max(outputs, 1)

        loss.backward()
        optimizer.step()

        running_loss += loss.item() * inputs.size(0)
        running_corrects += torch.sum(preds == labels.data)

    epoch_loss = running_loss / len(train_dataset)
    epoch_acc = running_corrects.double() / len(train_dataset)
    print(f"📈 [Epoch {epoch+1} Result] Train Loss: {epoch_loss:.4f} | Train Acc: {epoch_acc:.4f}")

    # --- Validation Step ---
    model.eval()
    val_loss, val_corrects = 0.0, 0
    val_batch_idx = 0

    val_iter = iter(val_loader)
    with torch.no_grad():
        while True:
            try:
                inputs, labels = next(val_iter)
                val_batch_idx += 1
                if val_batch_idx % 10 == 0:
                    print(f"   ⏳ Val Progress: Batch {val_batch_idx} evaluated...")
            except StopIteration:
                break  
            except Exception as e:
                print(f"   ⚠️ Skipping validation batch due to a broken internal data stream: {e}")
                continue

            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            _, preds = torch.max(outputs, 1)

            val_loss += loss.item() * inputs.size(0)
            val_corrects += torch.sum(preds == labels.data)

    val_epoch_loss = val_loss / len(val_dataset)
    val_epoch_acc = val_corrects.double() / len(val_dataset)
    print(f"📊 [Epoch {epoch+1} Result] Val Loss: {val_epoch_loss:.4f} | Val Acc: {val_epoch_acc:.4f}")

    # --- Checkpointing Block ---
    if val_epoch_acc > best_acc:
        best_acc = val_epoch_acc

        # 🌟 Save a comprehensive tracking map dictionary to allow perfect recovery
        checkpoint_data = {
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'best_acc': best_acc,
            'class_names': train_dataset.classes
        }
        torch.save(checkpoint_data, MODEL_SAVE_PATH)
        print(f"💾 Saved comprehensive state checkpoint map to {MODEL_SAVE_PATH}")

print(f"\n🎉 Pipeline Complete! Highest Valuation Accuracy Obtained: {best_acc:.4f}")
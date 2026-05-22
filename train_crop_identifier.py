# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader
# from torchvision import transforms, models, datasets
# import config
# import os
# import time

# def main():
#     print("Starting crop identifier model training...")

#     # =========================
#     # DEVICE
#     # =========================
#     device = torch.device(config.DEVICE)
#     print(f"Using device: {device}")

#     # =========================
#     # IMAGE TRANSFORMS
#     # =========================
#     data_transforms = {
#         'train': transforms.Compose([
#             transforms.RandomResizedCrop(config.IMAGE_SIZE),
#             transforms.RandomHorizontalFlip(),
#             transforms.ToTensor(),
#             transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
#         ]),
#         'validation': transforms.Compose([
#             transforms.Resize(256),
#             transforms.CenterCrop(config.IMAGE_SIZE),
#             transforms.ToTensor(),
#             transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
#         ]),
#     }

#     # =========================
#     # LOAD CROP DATASET
#     # =========================
#     CROP_DATASET_PATH = "plant_datasets/processed"
#     print(f"Loading dataset from path: {CROP_DATASET_PATH}")
#     if not os.path.exists(CROP_DATASET_PATH):
#         print(f"Error: Dataset path not found at '{CROP_DATASET_PATH}'")
#         return

#     image_datasets = {x: datasets.ImageFolder(os.path.join(CROP_DATASET_PATH, x), data_transforms[x])
#                       for x in ['train', 'validation']}
    
#     dataloaders = {x: DataLoader(image_datasets[x], batch_size=config.BATCH_SIZE, shuffle=True, num_workers=config.NUM_WORKERS)
#                    for x in ['train', 'validation']}

#     dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'validation']}
#     class_names = image_datasets['train'].classes
#     num_classes = len(class_names)

#     print(f"Found {num_classes} crop classes: {', '.join(class_names)}")

#     # =========================
#     # MODEL
#     # =========================
#     model = models.resnet18(weights="DEFAULT")
#     model.fc = nn.Linear(model.fc.in_features, num_classes)
#     model = model.to(device)

#     # =========================
#     # LOSS + OPTIMIZER
#     # =========================
#     criterion = nn.CrossEntropyLoss()
#     optimizer = optim.Adam(model.parameters(), lr=config.LEARNING_RATE)

#     # =========================
#     # TRAINING LOOP
#     # =========================
#     since = time.time()

#     for epoch in range(config.EPOCHS):
#         print(f'Epoch {epoch+1}/{config.EPOCHS}')
#         print('-' * 10)

#         for phase in ['train', 'validation']:
#             if phase == 'train':
#                 model.train()
#             else:
#                 model.eval()

#             running_loss = 0.0
#             running_corrects = 0

#             for inputs, labels in dataloaders[phase]:
#                 inputs = inputs.to(device)
#                 labels = labels.to(device)

#                 optimizer.zero_grad()

#                 with torch.set_grad_enabled(phase == 'train'):
#                     outputs = model(inputs)
#                     _, preds = torch.max(outputs, 1)
#                     loss = criterion(outputs, labels)

#                     if phase == 'train':
#                         loss.backward()
#                         optimizer.step()

#                 running_loss += loss.item() * inputs.size(0)
#                 running_corrects += torch.sum(preds == labels.data)

#             epoch_loss = running_loss / dataset_sizes[phase]
#             epoch_acc = running_corrects.double() / dataset_sizes[phase]

#             print(f'{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

#     time_elapsed = time.time() - since
#     print(f'Training complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')

#     # =========================
#     # SAVE MODEL
#     # =========================
#     CROP_MODEL_SAVE_PATH = "crop_identifier.pth"
#     model.class_names = class_names
#     torch.save(model.state_dict(), CROP_MODEL_SAVE_PATH)
#     print(f"Crop identifier model saved to {CROP_MODEL_SAVE_PATH}")


# if __name__ == "__main__":
#     main()



import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms, models, datasets
from PIL import Image
import config
import os
import time


# =========================
# SAFE IMAGE FOLDER
# Skips corrupted images instead of crashing
# =========================
class SafeImageFolder(datasets.ImageFolder):
    def __getitem__(self, index):
        while True:
            try:
                path, target = self.samples[index]
                sample = self.loader(path)
                if self.transform is not None:
                    sample = self.transform(sample)
                if self.target_transform is not None:
                    target = self.target_transform(target)
                return sample, target
            except Exception as e:
                bad_path = self.samples[index][0]
                print(f"  [WARNING] Skipping corrupted image: {bad_path} ({e})")
                index = (index + 1) % len(self.samples)


def main():
    print("Starting crop identifier model training...")

    # =========================
    # DEVICE
    # =========================
    device = torch.device(config.DEVICE)
    print(f"Using device: {device}")

    # =========================
    # IMAGE TRANSFORMS
    # =========================
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(config.IMAGE_SIZE),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'validation': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(config.IMAGE_SIZE),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    # =========================
    # LOAD DATASET
    # =========================
    CROP_DATASET_PATH = "plant_datasets/processed"
    print(f"Loading dataset from path: {CROP_DATASET_PATH}")
    if not os.path.exists(CROP_DATASET_PATH):
        print(f"Error: Dataset path not found at '{CROP_DATASET_PATH}'")
        return

    image_datasets = {
        x: SafeImageFolder(os.path.join(CROP_DATASET_PATH, x), data_transforms[x])
        for x in ['train', 'validation']
    }

    dataloaders = {
        x: DataLoader(
            image_datasets[x],
            batch_size=config.BATCH_SIZE,
            shuffle=True,
            num_workers=config.NUM_WORKERS,
            pin_memory=True if config.DEVICE == 'cuda' else False
        )
        for x in ['train', 'validation']
    }

    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'validation']}
    class_names = image_datasets['train'].classes
    num_classes = len(class_names)

    print(f"Found {num_classes} classes: {', '.join(class_names)}")
    print(f"Dataset sizes — train: {dataset_sizes['train']}, validation: {dataset_sizes['validation']}")

    # =========================
    # MODEL
    # =========================
    model = models.resnet18(weights="DEFAULT")
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model = model.to(device)

    # =========================
    # LOSS + OPTIMIZER
    # =========================
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=config.LEARNING_RATE)

    best_acc = 0.0

    # =========================
    # TRAINING LOOP
    # =========================
    since = time.time()

    for epoch in range(config.EPOCHS):
        print(f'\nEpoch {epoch+1}/{config.EPOCHS}')
        print('-' * 10)

        for phase in ['train', 'validation']:
            if phase == 'train':
                model.train()
            else:
                model.eval()

            running_loss = 0.0
            running_corrects = 0
            batch_count = 0

            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)
                batch_count += 1

                if batch_count % 20 == 0:
                    print(f"  [{phase}] batch {batch_count}, loss: {loss.item():.4f}")

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print(f'{phase} Loss: {epoch_loss:.4f}  Acc: {epoch_acc:.4f}')

            # Save best model
            if phase == 'validation' and epoch_acc > best_acc:
                best_acc = epoch_acc
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'class_names': class_names,
                    'best_acc': best_acc,
                }, "crop_identifier_best.pth")
                print(f"  ✔ New best model saved (acc: {best_acc:.4f})")

    time_elapsed = time.time() - since
    print(f'\nTraining complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')
    print(f'Best validation accuracy: {best_acc:.4f}')

    # =========================
    # SAVE FINAL MODEL
    # =========================
    CROP_MODEL_SAVE_PATH = "crop_identifier.pth"
    torch.save({
        'model_state_dict': model.state_dict(),
        'class_names': class_names,
        'num_classes': num_classes,
    }, CROP_MODEL_SAVE_PATH)
    print(f"Final model saved to {CROP_MODEL_SAVE_PATH}")


if __name__ == "__main__":
    main()
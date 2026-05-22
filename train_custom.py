import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms, models, datasets
import config
import os
import time

def main():
    print("Starting training with custom dataset...")

    # =========================
    # DEVICE
    # =========================
    device = torch.device(config.DEVICE)
    print(f"Using device: {device}")

    # =========================
    # IMAGE TRANSFORMS
    # =========================
    # Define transforms for training (with augmentation) and validation
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
    # LOAD CUSTOM DATASET
    # =========================
    print(f"Loading dataset from path: {config.CUSTOM_DATASET_PATH}")
    if not os.path.exists(config.CUSTOM_DATASET_PATH):
        print(f"Error: Dataset path not found at '{config.CUSTOM_DATASET_PATH}'")
        print("Please download and organize your datasets into 'train' and 'validation' folders within this path.")
        return

    image_datasets = {x: datasets.ImageFolder(os.path.join(config.CUSTOM_DATASET_PATH, x), data_transforms[x])
                      for x in ['train', 'validation']}
    
    dataloaders = {x: DataLoader(image_datasets[x], batch_size=config.BATCH_SIZE, shuffle=True, num_workers=config.NUM_WORKERS)
                   for x in ['train', 'validation']}

    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'validation']}
    class_names = image_datasets['train'].classes
    
    # Check if the number of classes matches the config
    if len(class_names) != config.NUM_CLASSES:
        print(f"Warning: Number of classes in dataset ({len(class_names)}) does not match config.py ({config.NUM_CLASSES}).")
        print("Please update NUM_CLASSES in config.py to match the number of folders in your train directory.")
        print("Detected classes:", class_names)
        # return

    print(f"Found {len(class_names)} classes: {', '.join(class_names)}")

    # =========================
    # MODEL
    # =========================
    model = models.resnet18(weights="DEFAULT")
    model.fc = nn.Linear(model.fc.in_features, config.NUM_CLASSES)
    model = model.to(device)

    # =========================
    # LOSS + OPTIMIZER
    # =========================
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=config.LEARNING_RATE)

    # =========================
    # TRAINING LOOP
    # =========================
    since = time.time()

    for epoch in range(config.EPOCHS):
        print(f'Epoch {epoch+1}/{config.EPOCHS}')
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'validation']:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data.
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                # forward
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print(f'{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

    time_elapsed = time.time() - since
    print(f'Training complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')

    # =========================
    # SAVE MODEL
    # =========================
    # Save the class names along with the model
    model.class_names = class_names
    torch.save(model.state_dict(), config.MODEL_SAVE_PATH)
    print(f"Model saved to {config.MODEL_SAVE_PATH}")


if __name__ == "__main__":
    main()

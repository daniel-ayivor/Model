import torch
import torch.nn as nn
import torch.optim as optim

from torch.utils.data import DataLoader
from torchvision import transforms, models
from datasets import load_dataset

import config


def main():

    # =========================
    # DEVICE
    # =========================
    device = torch.device(config.DEVICE)

    print("Using device:", device)

    # =========================
    # LOAD DATASET
    # =========================
    dataset = load_dataset(config.DATASET_NAME)

    # =========================
    # IMAGE TRANSFORMS
    # =========================
    transform = transforms.Compose([
        transforms.Resize((config.IMAGE_SIZE, config.IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(
            [0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225]
        )
    ])

    # =========================
    # TRANSFORM FUNCTION
    # =========================
    def transform_examples(example):
        images = [img.convert("RGB") for img in example["image"]]
        example["pixel_values"] = [transform(img) for img in images]
        return example

    dataset = dataset.with_transform(transform_examples)
# done
    # =========================
    # COLLATE FUNCTION
    # =========================
    def collate_fn(batch):
        images = torch.stack([x["pixel_values"] for x in batch])
        labels = torch.tensor([x["labels"] for x in batch])
        return images, labels

    # =========================
    # DATALOADERS
    # =========================
    train_loader = DataLoader(
        dataset["train"],
        batch_size=config.BATCH_SIZE,
        shuffle=True,
        collate_fn=collate_fn,
        num_workers=config.NUM_WORKERS,
        pin_memory=True
    )

    valid_loader = DataLoader(
        dataset["validation"],
        batch_size=config.BATCH_SIZE,
        shuffle=False,
        collate_fn=collate_fn,
        num_workers=config.NUM_WORKERS,
        pin_memory=True
    )

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
    for epoch in range(config.EPOCHS):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        accuracy = 100 * correct / total
        print(
            f"Epoch [{epoch+1}/{config.EPOCHS}] "
            f"Loss: {running_loss:.4f} "
            f"Accuracy: {accuracy:.2f}%"
        )

    print("Training complete!")

    # =========================
    # SAVE MODEL
    # =========================
    torch.save(model.state_dict(), config.MODEL_SAVE_PATH)
    print("Model saved!")


if __name__ == "__main__":
    main()
import torch

checkpoint = torch.load("plant_disease_model.pth", map_location="cpu")
print(len(checkpoint.get("class_names", [])))
print(checkpoint["model_state_dict"]["fc.weight"].shape)
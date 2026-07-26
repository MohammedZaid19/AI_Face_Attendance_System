import fiftyone.zoo as foz

print("Downloading Google Open Images Dataset...")

dataset = foz.load_zoo_dataset(
    "open-images-v7",
    split="validation",
    label_types=["detections"],
    classes=["Human face"],
    max_samples=500
)

print("\nDataset Downloaded Successfully!")
print("Dataset Name :", dataset.name)
print("Total Images :", len(dataset))
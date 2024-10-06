from transformers import AutoImageProcessor, AutoModelForImageClassification, AutoModelForObjectDetection
from PIL import Image
import torch
import os
# Load the image processor and model
processor = AutoImageProcessor.from_pretrained("gianlab/swin-tiny-patch4-window7-224-finetuned-crop-classification")
model = AutoModelForImageClassification.from_pretrained("gianlab/swin-tiny-patch4-window7-224-finetuned-crop-classification")
# Load model directly

# processor = AutoImageProcessor.from_pretrained("Komet/my-fruit-detection-3")
# model = AutoModelForObjectDetection.from_pretrained("Komet/my-fruit-detection-3")

def process_img(path):
    # Preprocess the image
    image = Image.open(path)
    inputs = processor(images=image, return_tensors="pt")

    # Forward pass to get predictions
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the predicted class probabilities
    logits = outputs.logits

    # Get the predicted class (index with the highest probability)
    predicted_class = torch.argmax(logits, dim=-1).item()

    # Get class labels
    class_labels = model.config.id2label  # Get the labels mapping

    # Get the predicted class label
    predicted_label = class_labels[predicted_class]
    print(f"Predicted label: {predicted_label}")

if __name__ == "__main__":

    folder_path = "test_imgs"
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        print(f"Analyzing image: {file_path}")
        process_img(file_path)
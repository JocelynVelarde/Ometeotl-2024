from transformers import AutoImageProcessor, AutoModelForObjectDetection
from PIL import Image
import torch
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import torch.nn.functional as F


# Load the image processor and model
processor = AutoImageProcessor.from_pretrained("Komet/my-fruit-detection-3")
model = AutoModelForObjectDetection.from_pretrained("Komet/my-fruit-detection-3")

# Load the image

def detect_objects(image_path):
    # Preprocess the image
    image = Image.open(image_path)

    # Preprocess the image
    inputs = processor(images=image, return_tensors="pt")

    # Forward pass to get predictions
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the predicted boxes and logits
    predicted_boxes = outputs.pred_boxes[0]  # Assuming you are dealing with a single image
    predicted_logits = outputs.logits[0]

    # Convert logits to probabilities (scores) using softmax
    predicted_scores = F.softmax(predicted_logits, dim=-1)

    # Define a confidence threshold
    confidence_threshold = 0.5

    # Get class labels (the last dimension's index corresponds to the classes)
    predicted_labels = predicted_scores.argmax(dim=-1)

    # Filter out predictions below the threshold
    boxes = []
    labels = []
    for box, score, label in zip(predicted_boxes, predicted_scores, predicted_labels):
        if score.max() >= confidence_threshold:  # Check the max score
            boxes.append(box)
            labels.append(label)

    # Visualize the results
    fig, ax = plt.subplots(1, figsize=(12, 8))
    ax.imshow(image)

    # Draw the bounding boxes
    for box, label in zip(boxes, labels):
        x1, y1, x2, y2 = box.tolist()  # Convert to list for easier handling
        width = x2 - x1
        height = y2 - y1
        rect = patches.Rectangle((x1, y1), width, height, linewidth=2, edgecolor='red', facecolor='none')
        ax.add_patch(rect)
        ax.text(x1, y1, f'{label.item()}', color='white', fontsize=12, bbox=dict(facecolor='red', alpha=0.5))

        print(f"Detected object: {label.item()}")
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    folder = "test_imgs"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        print(f"Analyzing image: {file_path}")
        detect_objects(file_path)
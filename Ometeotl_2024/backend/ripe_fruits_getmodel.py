from inference import get_model
import supervision as sv
import cv2

# define the image url to use for inference
image_file = "apple.jpeg"
image = cv2.imread(image_file)

# load a pre-trained yolov8n model
model = get_model(model_id="fruit-ripening-process/2")
results = model.infer(image)[0]

print("\n",results)
# # load the results into the supervision Detections api
detections = sv.Detections.from_inference(results)
print("\n",detections)

# # create supervision annotators
# bounding_box_annotator = sv.BoundingBoxAnnotator()
# label_annotator = sv.LabelAnnotator()

# # annotate the image with our inference results
# annotated_image = bounding_box_annotator.annotate(
#     scene=image, detections=detections)
# annotated_image = label_annotator.annotate(
#     scene=annotated_image, detections=detections)

# # display the image
# sv.plot_image(annotated_image)
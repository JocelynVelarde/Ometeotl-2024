from inference_sdk import InferenceHTTPClient
import os
from dotenv import load_dotenv
import cv2
import json

load_dotenv()

CONF_THRESHOLD = 0.5
api_k = os.getenv("ROBOFLOW_API_KEY")
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=api_k
)

img_result = cv2.imread("apple.jpeg")

# Weed detection
result = CLIENT.infer("apple.jpeg", model_id="weed-annotation/1")
weed_count = 0
for prediction in result["predictions"]:
    if (prediction.get("confidence") > CONF_THRESHOLD):
        weed_count += 1
        #draw bbox
        x1 = prediction["x"]
        y1 = prediction["y"]
        x2 = prediction["x"] + prediction["width"]
        y2 = prediction["y"] + prediction["height"]
        x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
        cv2.rectangle(img_result, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Illness -> need to translate
illnesses = {"unlabeled" : "Uncertain", "przelana": "Overwatered", "sucha": "Dry", "variegata": "Variegated", "zdrowa": "Healthy"}
illness_result = []
result = CLIENT.infer("apple.jpeg", model_id="plant-illnesses/1")
for prediction in result["predictions"]:
    if (prediction.get("confidence") < CONF_THRESHOLD):
        continue
    cl = prediction.get("class")
    illness_result.append(illnesses[cl])
    print(illnesses[cl])


# healthy leaf/unhealthy leaf
healty_leaf_count = 0
unhealthy_leaf_count = 0
result = CLIENT.infer("apple.jpeg", model_id="plant-disease-detection-qrtk3/1")
for prediction in result["predictions"]:
    if (prediction.get("confidence") < CONF_THRESHOLD):
        continue
    if prediction.get("class") == "healthy":
        healty_leaf_count += 1
    else:
        unhealthy_leaf_count += 1
    # print(prediction.get("class"))

# Ripe fruits
result = CLIENT.infer("apple.jpeg", model_id="fruit-ripening-process/2")
ripe_results = []
for prediction in result["predictions"]:
    if (prediction.get("confidence") > CONF_THRESHOLD):
        ripe_results.append(prediction.get("class"))
        #draw bbox
        x1 = prediction["x"]
        y1 = prediction["y"]
        x2 = prediction["x"] + prediction["width"]
        y2 = prediction["y"] + prediction["height"]
        x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
        cv2.rectangle(img_result, (x1, y1), (x2, y2), (0, 255, 0), 2)
# print(ripe_results)

# Pests, fungo, potassio
result = CLIENT.infer("apple.jpeg", model_id="agrovision-hv9yk/1")
pest_translate = { "Ferrugem": "Rust", "Fungo": "Fungus", "Potassio": "Potassium", "Praga": "Pest", "Queimada": "Burning" }
pest_results = []
for prediction in result["predictions"]:
    if prediction.get("class") == "Potassio":
            continue
    if (prediction.get("confidence") > CONF_THRESHOLD):
        pest_results.append(pest_translate[prediction.get("class")])
        
        #draw bbox
        x1 = prediction["x"]
        y1 = prediction["y"]
        x2 = prediction["x"] + prediction["width"]
        y2 = prediction["y"] + prediction["height"]
        x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
        cv2.rectangle(img_result, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Health 
result = CLIENT.infer("apple.jpeg", model_id="sf-m70df/1")
for prediction in result["predictions"]:
    if (prediction.get("confidence") > CONF_THRESHOLD):
        if prediction.get("class") == "healthy_plant":
            healty_leaf_count += 1
        else:
            unhealthy_leaf_count += 1
        #draw bbox
        x1 = prediction["x"]
        y1 = prediction["y"]
        x2 = prediction["x"] + prediction["width"]
        y2 = prediction["y"] + prediction["height"]
        x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
        cv2.rectangle(img_result, (x1, y1), (x2, y2), (0, 255, 0), 2)


json_data = {
    "weed_count": weed_count,
    "illnesses": illness_result,
    "healthy_count": healty_leaf_count,
    "unhealthy_count": unhealthy_leaf_count,
    "ripe_fruits": ripe_results,
    "pests": pest_results
}

print("\n")
json_string = json.dumps(json_data, indent=4)
print(json_string)
cv2.imwrite("apple_ripe.jpeg", img_result)
from inference_sdk import InferenceHTTPClient
import os
from dotenv import load_dotenv
import json
import streamlit as st
from algorithms.gpt_analysis import *
import cv2
from datetime import datetime

colors = [
    (0, 128, 255),  # Light Blue
    (0, 64, 128),   # Dark Blue
    (0, 220, 50),    # Green
    (0, 128, 0),    # Dark Green
    (192, 192, 192), # Silver
    (128, 128, 128), # Gray
    (169, 169, 169), # Dark Gray
    (70, 130, 180),  # Steel Blue
    (64, 224, 208),  # Turquoise
    (102, 205, 170), # Medium Aquamarine
]

class CropAnalyzer:
    CONF_THRESHOLD = 0.5
    # load_dotenv()
    # key = os.getenv("ROBOFLOW_API_KEY")
    key = st.secrets["Roboflow"]["ROBOFLOW_API_KEY"]

    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key=key
    )

    @classmethod
    def drawBbox(cls, image, x1, y1, x2, y2, label, color):
        text_color = (255, 255, 255)  # White color for text
        cv2.rectangle(image, (x1, y1 + 10), (x2, y2), color, 2)
        font, font_scale, thickness = cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2
        text_size = cv2.getTextSize(label, font, font_scale, thickness)[0]
        cv2.rectangle(image, (x1, y1 - text_size[1] + 5), (x2, y1 + 10), color, -1)
        cv2.putText(image, label, (x1, y1 + 10), font, font_scale, text_color, thickness)
        return image
    
    @classmethod
    def interpret_data(cls, results):
        prompt = results
        system_message = "You will receive a json object with results of an image analysis that contains information about the healthy or unhealthy plants detected, illnessess, among other attributes. This image was taken by a farmer. Help the farmer by interpreting the results, summarizing them (very briefly), providing an explanation about the results and give any recommendations if necessary."
        return get_gpt_prompt_response(prompt, system_message)
    
    @classmethod 
    def analyze_image(cls, image, cx, cy):

        result_image = image
        i = 0

        # Weed detection
        result = cls.CLIENT.infer(image, model_id="weed-annotation/1")
        weed_count = 0
        for prediction in result["predictions"]:
            if (prediction.get("confidence") > cls.CONF_THRESHOLD):
                weed_count += 1

        # Illness -> need to translate
        illnesses = {"unlabeled" : "Uncertain", "przelana": "Overwatered", "sucha": "Dry", "variegata": "Variegated", "zdrowa": "Healthy"}
        illness_result = {"Uncertain": 0, "Overwatered": 0, "Dry": 0, "Variegated": 0, "Healthy": 0}
        result = cls.CLIENT.infer(image, model_id="plant-illnesses/1")
        for prediction in result["predictions"]:
            if (prediction.get("confidence") < cls.CONF_THRESHOLD):
                continue
            cl = prediction.get("class")
            illness_result[illnesses[cl]] += 1

            x, y, width, height = map(int, (prediction["x"], prediction["y"], prediction["width"], prediction["height"]))
            x1, y1, x2, y2 = x - width // 2, y - height // 2, x + width // 2, y + height // 2

            label = prediction["class"]
            bbox_color = colors[i]
            result_image = cls.drawBbox(result_image, x1, y1, x2, y2, label, bbox_color)
        i+=1

        # healthy leaf/unhealthy leaf
        healty_leaf_count = 0
        unhealthy_leaf_count = 0
        result = cls.CLIENT.infer(image, model_id="plant-disease-detection-qrtk3/1")
        for prediction in result["predictions"]:
            if (prediction.get("confidence") < cls.CONF_THRESHOLD):
                continue
            if prediction.get("class") == "healthy-leaf":
                healty_leaf_count += 1
            else:
                unhealthy_leaf_count += 1
            
            x, y, width, height = map(int, (prediction["x"], prediction["y"], prediction["width"], prediction["height"]))
            x1, y1, x2, y2 = x - width // 2, y - height // 2, x + width // 2, y + height // 2
            label = prediction["class"]
            bbox_color = colors[i]
            result_image = cls.drawBbox(result_image, x1, y1, x2, y2, label, bbox_color)
        i+=1
            

        # Ripe fruits
        result = cls.CLIENT.infer(image, model_id="fruit-ripening-process/2")
        #freshripe freshunripe overripe ripe rotten unripe
        ripe_results = {"freshripe": 0, "freshunripe": 0, "overripe": 0, "ripe": 0, "rotten": 0, "unripe": 0}
        for prediction in result["predictions"]:
            if (prediction.get("confidence") > cls.CONF_THRESHOLD):
                ripe_results[prediction.get("class")] += 1

                x, y, width, height = map(int, (prediction["x"], prediction["y"], prediction["width"], prediction["height"]))
                x1, y1, x2, y2 = x - width // 2, y - height // 2, x + width // 2, y + height // 2
                label = prediction["class"]
                bbox_color = colors[i]
                result_image = cls.drawBbox(result_image, x1, y1, x2, y2, label, bbox_color)
        i+=1

        # Pests, fungo, potassio
        result = cls.CLIENT.infer(image, model_id="agrovision-hv9yk/1")
        pest_translate = { "Ferrugem": "Rust", "Fungo": "Fungus", "Potassio": "Potassium", "Praga": "Pest", "Queimada": "Burning" }
        pest_results = {"Rust": 0, "Fungus": 0, "Pest": 0, "Burning": 0}
        for prediction in result["predictions"]:
            if prediction.get("class") == "Potassio":
                    continue
            if (prediction.get("confidence") > cls.CONF_THRESHOLD):
                pest_results[pest_translate[prediction.get("class")]] += 1

                x, y, width, height = map(int, (prediction["x"], prediction["y"], prediction["width"], prediction["height"]))
                x1, y1, x2, y2 = x - width // 2, y - height // 2, x + width // 2, y + height // 2
                label = pest_translate[prediction["class"]]
                bbox_color = colors[i]
                result_image = cls.drawBbox(result_image, x1, y1, x2, y2, label, bbox_color)
        i+=1

        # Leaf types
        leaf_types = []
        result = cls.CLIENT.infer(image, model_id="plant-model-fjlgk/5")
        for prediction in result["predictions"]:
            if (prediction.get("confidence") > cls.CONF_THRESHOLD):
                leaf_types.append(prediction.get("class"))
                
                x, y, width, height = map(int, (prediction["x"], prediction["y"], prediction["width"], prediction["height"]))
                x1, y1, x2, y2 = x - width // 2, y - height // 2, x + width // 2, y + height // 2
                label = prediction["class"]
                bbox_color = colors[i]
                result_image = cls.drawBbox(result_image, x1, y1, x2, y2, label, bbox_color)
        i+=1

        # Health 
        result = cls.CLIENT.infer(image, model_id="sf-m70df/1")
        for prediction in result["predictions"]:
            if (prediction.get("confidence") > cls.CONF_THRESHOLD):
                if prediction.get("class") == "healthy_plant":
                    healty_leaf_count += 1
                else:
                    unhealthy_leaf_count += 1

                x, y, width, height = map(int, (prediction["x"], prediction["y"], prediction["width"], prediction["height"]))
                x1, y1, x2, y2 = x - width // 2, y - height // 2, x + width // 2, y + height // 2
                label = prediction["class"]
                bbox_color = colors[i]
                result_image = cls.drawBbox(result_image, x1, y1, x2, y2, label, bbox_color)
        i+=1

        json_data = {
            "results": {
                "coordinate": (cx, cy),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "plot_data": ripe_results,
                "weed_count": weed_count,
                "healthy_plants": healty_leaf_count,
                "unhealthy_plants": unhealthy_leaf_count,
                "illnesses": illness_result,
                "pests": pest_results,
                "leaf_types": {
                    "leaf_type_count": len(leaf_types),
                    "leaf_types": leaf_types
                }
            }
        }


        json_string = json.dumps(json_data, indent=4)
        print(json_string)
        print("\n")
        cv2.imwrite("result.jpg", result_image)
        return result_image, json_string

if __name__ == "__main__":

    folder_path = "test_imgs"
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        print(f"Analyzing image: {file_path}")
        CropAnalyzer.analyze_image(file_path, 1, 2)
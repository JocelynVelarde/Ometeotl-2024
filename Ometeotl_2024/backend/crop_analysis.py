from inference_sdk import InferenceHTTPClient
import os
from dotenv import load_dotenv
import cv2
import json

class CropAnalysis:
    CONF_THRESHOLD = 0.5
    load_dotenv()
    key = os.getenv("ROBOFLOW_API_KEY")

    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key=key
    )
    
    @classmethod 
    def analyze_image(cls, path, cx, cy):
        # Weed detection
        result = cls.CLIENT.infer(path, model_id="weed-annotation/1")
        weed_count = 0
        for prediction in result["predictions"]:
            if (prediction.get("confidence") > cls.CONF_THRESHOLD):
                weed_count += 1

        # Illness -> need to translate
        illnesses = {"unlabeled" : "Uncertain", "przelana": "Overwatered", "sucha": "Dry", "variegata": "Variegated", "zdrowa": "Healthy"}
        illness_result = {"Uncertain": 0, "Overwatered": 0, "Dry": 0, "Variegated": 0, "Healthy": 0}
        result = cls.CLIENT.infer(path, model_id="plant-illnesses/1")
        for prediction in result["predictions"]:
            if (prediction.get("confidence") < cls.CONF_THRESHOLD):
                continue
            cl = prediction.get("class")
            illness_result[illnesses[cl]] += 1
            print(illnesses[cl])


        # healthy leaf/unhealthy leaf
        healty_leaf_count = 0
        unhealthy_leaf_count = 0
        result = cls.CLIENT.infer(path, model_id="plant-disease-detection-qrtk3/1")
        for prediction in result["predictions"]:
            if (prediction.get("confidence") < cls.CONF_THRESHOLD):
                continue
            if prediction.get("class") == "healthy":
                healty_leaf_count += 1
            else:
                unhealthy_leaf_count += 1

        # Ripe fruits
        result = cls.CLIENT.infer(path, model_id="fruit-ripening-process/2")
        #freshripe freshunripe overripe ripe rotten unripe
        ripe_results = {"freshripe": 0, "freshunripe": 0, "overripe": 0, "ripe": 0, "rotten": 0, "unripe": 0}
        for prediction in result["predictions"]:
            if (prediction.get("confidence") > cls.CONF_THRESHOLD):
                ripe_results[prediction.get("class")] += 1

        # Pests, fungo, potassio
        result = cls.CLIENT.infer(path, model_id="agrovision-hv9yk/1")
        pest_translate = { "Ferrugem": "Rust", "Fungo": "Fungus", "Potassio": "Potassium", "Praga": "Pest", "Queimada": "Burning" }
        pest_results = {"Rust": 0, "Fungus": 0, "Pest": 0, "Burning": 0}
        for prediction in result["predictions"]:
            if prediction.get("class") == "Potassio":
                    continue
            if (prediction.get("confidence") > cls.CONF_THRESHOLD):
                pest_results[pest_translate[prediction.get("class")]] += 1

        # Leaf types
        leaf_types = []
        result = cls.CLIENT.infer(path, model_id="plant-model-fjlgk/5")
        for prediction in result["predictions"]:
            if (prediction.get("confidence") > cls.CONF_THRESHOLD):
                leaf_types.append(prediction.get("class"))

        # Health 
        result = cls.CLIENT.infer(path, model_id="sf-m70df/1")
        for prediction in result["predictions"]:
            if (prediction.get("confidence") > cls.CONF_THRESHOLD):
                if prediction.get("class") == "healthy_plant":
                    healty_leaf_count += 1
                else:
                    unhealthy_leaf_count += 1

        json_data = {
            "results": {
                "coordinate": (cx, cy),
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

if __name__ == "__main__":

    folder_path = "test_imgs"
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        print(f"Analyzing image: {file_path}")
        CropAnalysis.analyze_image(file_path, 1, 2)

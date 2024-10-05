from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="yKWYXTJEc9q44FfyfHHz"
)

result = CLIENT.infer("apple.jpeg", model_id="fruit-ripening-process/2")

# Draw results on image
for prediction in result["predictions"]:
    print(prediction)
    
print(result)
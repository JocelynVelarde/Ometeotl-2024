import streamlit as st
from PIL import Image
import base64
import requests
from io import BytesIO


def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")  # Saving the image to a byte stream
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def get_image_analysis(images, prompt):

    # Ensure `images` is a list, even if it's a single image
    if not isinstance(images, list):
        images = [images]
    
    # Encode each image
    encoded_images = [
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{encode_image(image)}"
            }
        } for image in images
    ]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.secrets['open_ai_key']}"
    }

    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are an AI assistant for a farmer. You can help the farmer with their queries. They can provide images of their crops and ask questions about them. You can analyze the images and provide ttechnical information about the crops. Finally, you should answer with technical terminology and provide detailed information."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt  
                }
            ] + encoded_images
        }
    ]

    # Prepare the payload
    payload = {
        "model": "gpt-4o-mini",
        "messages": messages,
        "max_tokens": 350
    }

    # Make the API request
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()

    output_message = response_data['choices'][0]['message']['content']

    return output_message  

def get_gpt_prompt_response(prompt, system_message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.secrets['open_ai_key']}"
    }

    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": system_message
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt  
                }
            ]
        }
    ]

    # Prepare the payload
    payload = {
        "model": "gpt-4o-mini",
        "messages": messages,
        "max_tokens": 350
    }

    # Make the API request
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()


    output_message = response_data['choices'][0]['message']['content']

    return output_message
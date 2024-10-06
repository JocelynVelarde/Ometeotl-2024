import requests
import json

# Replace these variables with your own values
api_url = "https:///v1/messages"  # Update with your API URL
access_token = "EAAUvhit0i70BOZBQT7I2vf9YWnXJxS9ZA4vsTZAyZAM2auCXnOcZAdLn5FQ9hZCs1xUlwnr68cpMJCVqgbuOlFPWu2EaqWrJk0o80DpSJPcTVtf4qMvkXQymxECze3dI5GoWhdhmTFZBZA7kAQzJn4I2ipAxjcQh6nS0ULlIt1Vnid1lMmsfUaKN8e9iweg4DLR5Rd2WPvGZCyzEVGFE4QPoTgQKgjkYZD"  # Your access token
to_phone_number = "<RECIPIENT_PHONE_NUMBER>"  # Recipient's phone number with country code
message = "Hello from Python using WhatsApp Business API!"

# Prepare the message payload
payload = {
    "messaging_product": "whatsapp",
    "to": to_phone_number,
    "type": "text",
    "text": {
        "body": message
    }
}

# Set headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Send the request
response = requests.post(api_url, headers=headers, data=json.dumps(payload))

# Check response
if response.status_code == 200:
    print("Message sent successfully!")
else:
    print("Failed to send message:", response.json())

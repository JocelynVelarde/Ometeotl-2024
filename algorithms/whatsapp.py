from twilio.rest import Client
import os
from dotenv import load_dotenv

class WhatsappSender:
    load_dotenv()

    ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

    @classmethod
    def send_message(cls, to_phone_number, message):
        message = cls.CLIENT.messages.create(
            from_='whatsapp:+14155238886',
            body=message,
            to=f'whatsapp:{to_phone_number}'
        )

        return message.sid
    
if __name__ == "__main__":
    WhatsappSender.send_message("+5218111751674", "This is a custom test")
    print("Message sent successfully!")

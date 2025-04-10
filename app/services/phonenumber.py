import random
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()


ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER") 

def send_verification_code(to_phone_number, code):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    
    message = client.messages.create(
        body=f"Your One Time Password (OTP) is: {code}",
        from_=TWILIO_PHONE_NUMBER,
        to=to_phone_number
    )
    
    print(f"Message sent with SID: {message.sid}")

def generate_otp():
    return random.randint(1000, 9999)


def send_otp(phone_number):
    code = generate_otp()
    send_verification_code(phone_number, code)
    return code


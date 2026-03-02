from fastapi import FastAPI
import os
import resend
from twilio.rest import Client

app = FastAPI()

# Resend setup
resend.api_key = os.getenv("RESEND_API_KEY")

# Twilio setup
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_client = Client(account_sid, auth_token)

@app.post("/register")
def register_user(name: str, email: str):

    try:
        # 1️⃣ Send Email
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": os.getenv("EMAIL_USER"),
            "subject": "New User Registration",
            "html": f"<p>Name: {name}</p><p>Email: {email}</p>"
        })

        # 2️⃣ Send WhatsApp
        twilio_client.messages.create(
            body=f"New User Registered\nName: {name}\nEmail: {email}",
            from_=os.getenv("TWILIO_WHATSAPP_FROM"),
            to=os.getenv("MY_PHONE_NUMBER")
        )

        return {"message": "Email & WhatsApp sent successfully"}

    except Exception as e:
        return {"error": str(e)}


        
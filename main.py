from fastapi import FastAPI
import os
import resend

app = FastAPI()

resend.api_key = os.getenv("RESEND_API_KEY")

@app.post("/register")
def register_user(name: str, email: str):

    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": os.getenv("EMAIL_USER"),
            "subject": "New User Registration",
            "html": f"<p>Name: {name}</p><p>Email: {email}</p>"
        })

        return {"message": "Email sent successfully"}

    except Exception as e:
        return {"error": str(e)}
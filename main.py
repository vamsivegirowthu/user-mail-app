from fastapi import FastAPI
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()


@app.post("/register")
def register_user(name: str, email: str):

    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    # Debug prints (remove later in production)
    print("Sender:", sender)
    print("Password:", password)

    # If env variables missing
    if not sender or not password:
        return {"error": "Email credentials not found in .env file"}

    # Create email message
    msg = MIMEText(f"New user registered:\nName: {name}\nEmail: {email}")
    msg["Subject"] = "New User Registration"
    msg["From"] = sender
    msg["To"] = sender

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)

        return {"message": "User registered & email sent"}

    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}
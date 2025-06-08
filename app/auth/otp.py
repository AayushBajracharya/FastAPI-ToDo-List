import os
import random
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

'''This module provides functionality for generating, storing, and verifying One-Time Passwords (OTPs) for password reset operations.
It includes functions to generate a 6-digit OTP, store it with an expiration time, verify the OTP against stored values, and send the OTP via email.'''

otp_storage = {}

def generate_otp() -> str:
    """Generate a 6-digit OTP."""
    return str(random.randint(100000, 999999))

def store_otp(email: str, otp: str, expiry_minutes: int = 10):
    """Store OTP with expiration time for the given email."""
    expiry = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    otp_storage[email] = (otp, expiry)

def verify_otp(email: str, otp: str) -> bool:
    """Verify if the OTP is valid and not expired for the given email."""
    if email not in otp_storage:
        return False
    stored_otp, expiry = otp_storage[email]
    if datetime.utcnow() > expiry:
        del otp_storage[email]
        return False
    if stored_otp != otp:
        return False
    del otp_storage[email] # Remove OTP after verification
    return True

def send_otp_email(email: str, otp: str):
    """Send OTP to the given email address."""
    msg = MIMEText(f"Your password reset OTP is: {otp}\nIt is valid for 10 minutes.")
    msg["Subject"] = "Password Reset OTP"
    msg["From"] = SMTP_USER
    msg["To"] = email

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, email, msg.as_string())
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")
    
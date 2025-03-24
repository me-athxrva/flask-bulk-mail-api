import os
import smtplib
import base64
import requests
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from api.extensions import mongo
from celery_worker import celery

TOKEN_URL = "https://oauth2.googleapis.com/token"

def refresh_access_token(refresh_token, user_email):
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }

    response = requests.post(TOKEN_URL, data=data)
    new_token = response.json()

    if "access_token" in new_token:
        new_access_token = new_token["access_token"]
        expires_in = new_token.get("expires_in", 3600)
        issued_at = int(time.time())

        mongo.db.users.update_one(
            {"email": user_email},
            {"$set": {
                "oauth_token.access_token": new_access_token,
                "oauth_token.expires_in": expires_in,
                "oauth_token.issued_at": issued_at
            }}
        )
        print("[DEBUG] Access token refreshed successfully!")
        return new_access_token
    else:
        print("[ERROR] Failed to refresh token:", new_token)
        return None

@celery.task
def send_bulk_mail(user_email, recipients, subject, body):
    try:
        user_data = mongo.db.users.find_one({"email": user_email})
        if not user_data:
            return {"error": "User not found, please login again."}

        access_token = user_data['oauth_token'].get('access_token')
        refresh_token = user_data['oauth_token'].get('refresh_token')
        issued_at = user_data['oauth_token'].get('issued_at', 0)
        expires_in = user_data['oauth_token'].get('expires_in', 3600)

        if not access_token or not refresh_token:
            return {"error": "Invalid or missing OAuth tokens. Please reauthenticate."}
        
        current_time = int(time.time())
        if current_time - issued_at >= expires_in:
            access_token = refresh_access_token(refresh_token, user_email)
            if not access_token:
                return {"error": "Failed to refresh access token. Please login again."}

        # access token encoding
        auth_string = f"user={user_email}\x01auth=Bearer {access_token}\x01\x01"
        auth_bytes = base64.b64encode(auth_string.encode("ascii")).decode("ascii")

        # Gmail SMTP Connection
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.set_debuglevel(1)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()

        # XOAUTH2 authentication
        code, response = smtp_server.docmd("AUTH", f"XOAUTH2 {auth_bytes}")
        if code != 235:
            smtp_server.quit()
            return {"error": f"SMTP Authentication failed: {response.decode()}"}

        # Send emails
        for recipient in recipients:
            msg = MIMEMultipart()
            msg["From"] = user_email
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "html"))
            smtp_server.sendmail(user_email, recipient, msg.as_string())

        smtp_server.quit()
        return {"status": "Emails sent successfully"}

    except smtplib.SMTPAuthenticationError as e:
        return {"error": f"SMTP Authentication failed: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

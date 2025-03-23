from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # mongo uri
    MONGO_URI = os.getenv("MONGO_URI")

    # OAuth
    SECRET_KEY = os.getenv('APP_SECRET_KEY')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_AUTH_REDIRECT_URI = os.getenv("GOOGLE_AUTH_REDIRECT_URI", "http://localhost:5000/auth/callback")
    GOOGLE_SCOPE = "https://mail.google.com/ https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid"

    # Celery and Redis
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_URL')

    # jwt 
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
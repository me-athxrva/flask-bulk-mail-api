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
    GOOGLE_AUTH_REDIRECT_URI = os.getenv("GOOGLE_AUTH_REDIRECT_URI")
    GOOGLE_SCOPE = "https://mail.google.com/ https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid"

    # Celery and Redis
    broker_url = os.getenv('broker_url')
    result_backend = os.getenv('result_backend')

    # jwt 
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
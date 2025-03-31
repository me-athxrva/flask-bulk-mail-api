from pymongo import MongoClient
import redis
from celery import Celery
import os

def check_mongo():
    try:
        client = MongoClient(os.getenv("MONGO_URI"), serverSelectionTimeoutMS=2000)
        client.admin.command("ping")
        print("MongoDB Connected")
        return True
    except Exception as e:
        print("MongoDB Error:", e)
        return False

def check_celery():
    try:
        celery_app = Celery(broker=os.getenv('CELERY_BROKER_URL'))
        inspect = celery_app.control.inspect()
        workers = inspect.ping()
        if workers:
            print("Celery Workers Found:", workers)
            return True
        else:
            print("No Celery Workers Found")
    except Exception as e:
        print("Celery Error:", e)
    return False

# Check all services
all_connected = check_mongo() and check_celery()
print("\nFinal Status:", all_connected)

def checkServerStatus():
    all_connected = check_mongo() and check_celery()
    if all_connected == True:
        return True
    return False
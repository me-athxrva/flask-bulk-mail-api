from flask import request
from flask_restful import Resource
from api.create_app import limiter
from datetime import datetime
from flask_jwt_extended import get_jwt_identity, jwt_required

class BulkMailSender(Resource):
    decorators = [limiter.limit("10 per minute")]
    @jwt_required()
    def post(self):
        from api.tasks import send_bulk_mail
        
        user = get_jwt_identity()

        data = request.get_json()
        user_email = user
        recipient_list = data.get("recipients", [])
        subject = data.get("subject", "No Subject")
        message = data.get("body", "No Message")

        if not recipient_list:
            return {"error": "Email list is empty"}, 400

        task = send_bulk_mail.delay(user_email, recipient_list, subject, message)
        return {"task_id": task.id, "message": "Bulk email sending started"}, 200


def convert_datetime(obj):
    if isinstance(obj, dict):
        return {k: convert_datetime(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetime(v) for v in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    return obj


class TaskHistory(Resource):
    @jwt_required()
    def get(self):
        from api.extensions import mongo
        user_email = get_jwt_identity()  

        logs = list(mongo.db.task_logs.find({"user_email": user_email}, {"_id": 0}))

        if not logs:
            return {"message": "No task logs found for this user"}, 404

        return convert_datetime(logs), 200  

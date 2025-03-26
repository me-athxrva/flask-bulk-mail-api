from flask import request
from flask_restful import Resource
from api.create_app import limiter
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

class TaskStatus(Resource):
    # decorators = [limiter.limit("2 per minute")]
    def get(self, task_id):
        from api.extensions import mongo
        log = mongo.db.task_logs.find_one({"task_id": task_id}, {"_id": 0})

        if not log:
            return {"error": "Task not found"}, 404
        
        # covert datetime format to string
        if "created_at" in log:
            log["created_at"] = log["created_at"].isoformat()
        if "updated_at" in log:
            log["updated_at"] = log["updated_at"].isoformat()
        
        return log, 200

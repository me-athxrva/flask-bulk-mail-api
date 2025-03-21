from flask import request
from flask_restful import Resource
from api.create_app import limiter

class BulkMailSender(Resource):
    decorators = [limiter.limit("1 per minute")]
    def post(self):
        from api.tasks import send_bulk_mail 
        
        data = request.get_json()
        email_list = data.get("emails", [])
        subject = data.get("subject", "No Subject")
        message = data.get("message", "No Message")

        if not email_list:
            return {"error": "Email list is empty"}, 400

        task = send_bulk_mail.delay(email_list, subject, message)
        return {"task_id": task.id, "message": "Bulk email sending started"}, 202

class TaskStatus(Resource):
    def get(self, task_id):
        from celery_worker import celery  
        task = celery.AsyncResult(task_id)
        return {"task_id": task_id, "status": task.state, "result": task.result}

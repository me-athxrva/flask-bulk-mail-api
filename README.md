# Email Sending Application

This api is a simple utility that allows you to send emails to multiple recipients using a json request. It uses the GMail API to send emails and the Flask framework to handle the resful api. It used celery and redis for task queue management for handling the server load efficiently. Supports HTML mails.

## Requirements

-   Python 3
-   Flask
-   Redis
-   Celery
-   AuthLib (OAuth2)

## Usage

1.  Clone the repository and navigate to the project directory.
2.  Install the required packages by running `pip install -r requirements.txt`.
3.  Add `.env` file in the project root and add your GMail Username and App Password. (.env format is given below.)
4.  Run the application by executing `python -m api.app`.
5.  Run the celery worker by executing `celery -A celery_worker.celery worker --loglevel=info --pool=solo`.
6.  Send an GET request on api end point `http://localhost:5000/auth/login` to login first.
7.  In your postman, go to `http://localhost:5000/sendMail` to access the api endpoint.
8.  Click on the "Send" button to send the task to celery worker.
9.  Response with a task id will be generated on successful task initalisation.

## .env format

```python
# OAuth credentials
APP_SECRET_KEY = 'Your-Secret-Key'
GOOGLE_CLIENT_ID = 'Your-OAuth-Client-Id'
GOOGLE_CLIENT_SECRET = 'Your-OAuth-Client-Secret'
GOOGLE_AUTH_REDIRECT_URI = 'http://localhost:5000/auth/callback'
GOOGLE_SCOPE = "https://mail.google.com/ https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid"


# Celery worker backend credentials
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
REDIS_SERVER_URL = 'redis://localhost:6379/0'

# mongo uri
MONGO_URI = 'mongodb://localhost:27017/Your-MongoDB-URI'
```

## API json format

```json
{
    "user_email": "yourmail@gmail.com",
    "recipients": ["recipient@example.com", "recipient@example.com"],
    "subject": "API Test Mail",
    "body": "<h1>this is h1 txt</h1><h2>this is h2 txt</h2>"
}
```

## Email format

The email format should be "Designation<emailid@{}>"

## Built With

-   [Flask](https://flask.palletsprojects.com/en/2.1.x/) - The api framework used
-   [Redis](https://redis.io/docs/latest/) - Message broker for celery
-   [Celery](https://docs.celeryq.dev/en/stable/) - Distributed task queue


## Project Website

You can find the project website at [NULL](coming soon)


## Authors

-   [Atharva](https://github.com/me-athxrva)

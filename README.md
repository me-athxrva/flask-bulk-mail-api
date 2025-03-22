# Email Sending Application

This api is a simple utility that allows you to send emails to multiple recipients using a json request. It uses the GMail API to send emails and the Flask framework to handle the resful api. It used celery and redis for task queue management for handling the server load efficiently.

## Requirements

-   Python 3
-   Flask
-   Redis
-   Celery

## Usage

1.  Clone the repository and navigate to the project directory.
2.  Install the required packages by running `pip install -r requirements.txt`.
3.  Edit the `.env` file in the project root and add your GMail Username and App Password.
4.  Run the application by executing `python -m api.app`.
5.  Run the celery worker by executing `celery -A celery_worker.celery worker --loglevel=info --pool=solo`.
6.  In your postman, go to `http://localhost:5000/sendMail` to access the api endpoint.
7.  Click on the "Send" button to send the task to celery worker.
8. Response with a task id will be generated on successful task initalisation.

## API json format

{
    "emails": ["yourmail1@example.com", "yourmail2@example.com"],
    "subject": "API Test Mail",
    "message": "This is an test mail using flask bulk mailing api."
}

## Email format

The email format should be "Designation<emailid@{}>"

## Built With

-   [Flask](https://flask.palletsprojects.com/en/2.1.x/) - The api framework used
-   [Redis](https://flask.palletsprojects.com/en/2.1.x/) - Message broker for celery
-   [Celery](https://flask.palletsprojects.com/en/2.1.x/) - Distributed task queue


## Project Website

You can find the project website at [NULL](coming soon)


## Authors

-   [Atharva](https://github.com/me-athxrva)

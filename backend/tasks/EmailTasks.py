import celery
from flask_mail import Message

from app import app, mail


@app.task
def send_async_email(email_data):
    msg = Message(email_data['subject'],
                  sender='egarcia@pospan.com',
                  recipients=[email_data['to']])

    msg.body = email_data['body']

    with app.app_context():
        mail.send(msg)

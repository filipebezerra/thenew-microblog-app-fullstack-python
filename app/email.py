from threading import Thread
from flask_mail import Message
from app import mail, app


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(sender, recipients, subject, text_body, html_body):
    msg = Message(sender=sender, recipients=recipients,
                  subject=subject, body=text_body,  html=html_body)
    Thread(target=send_async_email, args=(app, msg)).start()

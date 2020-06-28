from flask_mail import Message
from flask import render_template
from app import mail, app
from app.time import to_human_readable_time


def send_email(sender, recipients, subject, text_body, html_body):
    msg = Message(sender=sender, recipients=recipients,
                  subject=subject, body=text_body,  html=html_body)
    mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    expires_time = to_human_readable_time(
        int(app.config['PASSWORD_RESET_EXPIRES_AT']))
    send_email(
        sender=app.config['ADMINS'][0],
        recipients=[user.email],
        subject='[Microblog] Password Reset Request',
        text_body=render_template('email/reset_password.txt',
                                  user=user, token=token,
                                  expires_time=expires_time),
        html_body=render_template('email/reset_password.html',
                                  user=user, token=token,
                                  expires_time=expires_time))


def send_password_reset_confirmation_email(user):
    send_email(sender=app.config['ADMINS'][0],
               recipients=[user.email],
               subject='[Microblog] Password Reset Confirmation',
               text_body=render_template('email/password_reset_confirmation.txt',
                                         user=user),
               html_body=render_template('email/password_reset_confirmation.html',
                                         user=user))

from flask import current_app
from flask_mail import email_dispatched
from flask_login import user_logged_in, user_logged_out
from app.logger import log_user_operation, log_email_operation


def _after_sending_email_hook(message, app):
    log_email_operation(message, 'sent')


email_dispatched.connect(_after_sending_email_hook)


# @user_logged_in.connect_via(current_app)
def _after_user_logged_in_hook(sender, user, **extra):
    log_user_operation(user, 'logged in')


user_logged_in.connect(_after_user_logged_in_hook)


# @user_logged_out.connect_via(current_app)
def _after_user_logged_out_hook(sender, user, **extra):
    log_user_operation(user, 'logged out')


user_logged_out.connect(_after_user_logged_out_hook)

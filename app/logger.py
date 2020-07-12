from flask import current_app
from app.date import fromtimestamp, now


def log_user_operation(user, operation):
    date_formatted = now().strftime(current_app.config['DATE_TIME_FORMAT'])
    current_app.logger.info(
        f'User {user.username} {operation} at {date_formatted}')


def log_email_operation(message, operation):
    formatted_date = fromtimestamp(message.date).strftime(
        current_app.config['DATE_TIME_FORMAT'])
    subject = message.subject
    current_app.logger.info(
        f'Email {subject} {operation} at {formatted_date}')

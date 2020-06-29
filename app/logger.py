from app import app
from app.date import fromtimestamp, now

_DATE_TIME_FORMAT = app.config['DATE_TIME_FORMAT']


def log_user_operation(user, operation):
    date_formatted = now().strftime(_DATE_TIME_FORMAT)
    app.logger.info(f'User {user.username} {operation} at {date_formatted}')


def log_email_operation(message, operation):
    formatted_date = fromtimestamp(message.date).strftime(_DATE_TIME_FORMAT)
    subject = message.subject
    app.logger.info(f'Email {subject} {operation} at {formatted_date}')

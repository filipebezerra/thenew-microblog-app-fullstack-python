from flask_mail import email_dispatched
from datetime import datetime, timezone
from app import app


def log_sending_email(message, app):
    date = datetime.fromtimestamp(message.date, tz=timezone.utc)
    app.logger.info(f'Email {message.subject} '
                    f'sent at {date.strftime("%Y-%m-%dT%H:%M:%S,%f")}')


email_dispatched.connect(log_sending_email)

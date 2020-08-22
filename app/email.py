from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(sender, recipients, subject, text_body, html_body,
               attachments=None, sync=False):
    if not current_app.config['MAIL_SERVER']:
        current_app.logger.info('Application not sending emails. '
                                'Reason: Mail server isn\'t configured.')
        return

    msg = Message(sender=sender, recipients=recipients,
                    subject=subject, body=text_body, html=html_body)
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email,
                args=(current_app._get_current_object(), msg)).start()

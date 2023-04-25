import logging
import os

from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail, Message


load_dotenv()


logger = logging.getLogger(__name__)


MAIL_ADDRESS = os.getenv("MAIL_ADDRESS", default="from@example.com")


def send_to_email(app: Flask, subject: str, recipients: list[str], body: str):
    mail = Mail(app)
    msg = Message(subject=subject, sender=MAIL_ADDRESS, recipients=recipients)
    msg.body = body
    logger.info("Message: %s" % body)

    try:
        mail.send(msg)
    except Exception as exc:
        logger.error(exc)

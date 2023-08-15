import os
import logging
import smtplib

from django.core.mail import send_mail

logging.basicConfig(filename='books/logs/Pictures.log', level=logging.WARNING,
                    format="%(asctime)s - %(levelname)s - %(pathname)s: %(lineno)d - %(message)s - %(url)s")


def send_email(text, contact_email):
    try:
        send_mail(
            'Обратная связь',
            f'{text}',
            contact_email,
            [os.getenv('EMAIL')],
            fail_silently=False,
        )
    except smtplib.SMTPException as e:
        logging.warning(e)

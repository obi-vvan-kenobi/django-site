import os
import logging
import smtplib

from django.core.mail import send_mail
# import sys
# sys.path.append("..")

logging.basicConfig(filename='../books/logs/Pictures.log', level=logging.WARNING,
                    format="%(asctime)s - %(levelname)s - %(pathname)s: %(lineno)d - %(message)s - %(url)s")


def send_email(text):
    try:
        send_mail(
            'Обратная связь',
            f'{text}',
            'v.gornix@yandex.ru',
            [os.getenv('EMAIL')],
            fail_silently=False,
        )
    except smtplib.SMTPException as e:
        logging.warning(e)

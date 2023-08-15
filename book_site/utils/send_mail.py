import os

from django.core.mail import send_mail
# import sys
# sys.path.append("..")


def send_email(text):
    send_mail(
        'Обратная связь',
        f'{text}',
        'v.gornix@yandex.ru',
        [os.getenv('EMAIL')],
        fail_silently=False,
    )

FROM python:3.9.5
ENV PYTHONUNBUFFERED 1

RUN bash -c 'mkdir -p /web_django/media/ && mkdir -p /web_django/books/logs'
WORKDIR /web_django

COPY  . /web_django/
RUN pip install --upgrade pip && pip install -r requirements.txt

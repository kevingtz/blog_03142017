FROM python:3.6-alpine

RUN \
  echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
  && echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories;

ENV FLASK_APP manage.py
ENV FLASK_CONFIG docker

WORKDIR /my_blog

RUN apk update \
  && apk upgrade --update-cache --available \
  && apk upgrade apk-tools \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

COPY app app
#COPY migrations migrations
#COPY manage.py config.py boot.sh ./
COPY manage.py config.py ./

# runtime configuration
EXPOSE 5000

ENTRYPOINT venv/bin/python manage.py runserver
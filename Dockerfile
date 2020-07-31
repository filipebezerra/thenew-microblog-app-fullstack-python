FROM python:3.7.6-alpine

RUN adduser -D microblog

WORKDIR /home/microblog

COPY requirements requirements
RUN apk update && apk upgrade
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev
RUN python -m venv venv
RUN venv/bin/pip install -U pip
RUN venv/bin/pip install -r requirements/docker.txt

COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP=microblog.py

RUN chown -R microblog:microblog ./
USER microblog

EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]

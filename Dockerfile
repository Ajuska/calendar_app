FROM python:3.6-alpine

RUN adduser -D calendar_app

WORKDIR /home/calendar_app

COPY requirements.txt requirements.txt
RUN python -m venv __venv__
RUN __venv__/bin/pip install -r requirements.txt
RUN __venv__/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY calendar_app.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP calendar_app.py

RUN chown -R calendar_app:calendar_app ./
USER calendar_app

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

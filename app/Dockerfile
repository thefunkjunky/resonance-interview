# syntax=docker/dockerfile:1
FROM python:3.9-slim-buster

# Needed by the Flask module
ENV FLASK_APP=ping.py

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ping.py ping.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

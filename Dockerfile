# Dockerfile to make a Docker image and container with the
# TeamReel DS API (in application.py) and related packages.

FROM python:3.7-slim

COPY . /video-journal-for-teams-ds
WORKDIR /video-journal-for-teams-ds

RUN apt-get update && apt-get install libsndfile1 -y && pip install pipenv && pipenv install --deploy --system

EXPOSE 5000

CMD gunicorn --timeout 300 application:application

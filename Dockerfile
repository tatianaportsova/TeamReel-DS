# Dockerfile to make a Docker image and container with the
# TeamReel DS API (in main.py) and related packages.

FROM python:3.7-slim

COPY . /video-journal-for-teams-ds
WORKDIR /video-journal-for-teams-ds

RUN apt-get update && apt-get install -y libsndfile1
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]

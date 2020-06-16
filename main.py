"""
Main function for DS TeamReel.
"""

# Import modules/libraries we will use:

# Import external/third-party libraries we will use:
from dotenv import load_dotenv
import json
import os
import psycopg2

# Import internal functions we need for TeamReel data infra, video and DB:
from data_infra.data_pipelines import get_next_video
from data_infra.postgresql_db_functions import get_feedback_for_user
from data_infra.postgresql_db_functions import get_feedback_for_video, get_video_info

from audio_analysis.audio_functions import get_audio_from_video
# from audio_analysis.audio_functions import analyse_audio, remove_files

# Import functions we need from facial_analysis package

# Import functions we need from audio_analysis.background_noise module


# ----------------------------------------------------------------------------
# SETUP:

# Get access info from .env file:
load_dotenv()

# PostgreSQL DB info:
PG_DB_HOST = os.getenv("PG_DB_HOST")
PG_DB_PORT = os.getenv("PG_DB_PORT")
PG_DB_NAME = os.getenv("PG_DB_NAME")
PG_DB_USER = os.getenv("PG_DB_USER")
PG_DB_PW = os.getenv("PG_DB_PW")
PG_DB_URI = os.getenv("PG_DB_URI")

# Open a connection to our PostgreSQL DB:
pg_conn = psycopg2.connect(
    host = PG_DB_HOST,
    port = PG_DB_PORT,
    database = PG_DB_NAME,
    user = PG_DB_USER,
    password = PG_DB_PW
)

# Instantiate a cursor using this connection:
pg_cursor = pg_conn.cursor()

# ----------------------------------------------------------------------------
# GET BASE MATERIALS: VIDEO, AUDIO, TRANSCRIPT:

# Get next video in line for analysis (recently uploaded by a user):
# (1) video_analysis dict = info about that video from our DB (video_id, etc.)
# (2) download .MP4 video file to project directory
video_analysis = get_next_video()
print(video_analysis)

try:
    video_s3_key = video_analysis['video']['s3_key']
    video_filename = video_analysis['video']['s3_filename']
except KeyError:
    "KeyError: There is no information about this video in our database."

# Get audio from the video file:
get_audio_from_video(video_file=video_filename)
audio_filename = 'audio.wav'

# ----------------------------------------------------------------------------
# SENTIMENT: AUDIO:

# Directory paths
dirname = r"audio_chunks/"
path = r"text_chunks/"

# analyse_audio() function is the one function that does both: audio-sentiment analysis,
# and gets number of words per minute

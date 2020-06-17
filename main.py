"""
[To update this... Main function for DS TeamReel.]
"""

# Import modules/libraries we will use:

# Import external/third-party libraries we will use:
from dotenv import load_dotenv
import json
import numpy as np
import pandas as pd
import os
import psycopg2

# Import internal functions we need for TeamReel data infra, video and DB:
from data_infra.data_pipelines import get_next_video
from data_infra.postgresql_db_functions import get_feedback_for_user
from data_infra.postgresql_db_functions import get_feedback_for_video, get_video_info

from audio_analysis.audio_functions import get_audio_from_video, get_transcript_from_audio
from audio_analysis.audio_functions import get_audio_sentiment_analysis, get_speed_of_speech
from audio_analysis.audio_functions import get_text_sentiment, remove_files

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
# (1) video_info dict = info about that video from our DB (video_id, etc.)
# (2) download .MP4 video file to project directory
video_info = get_next_video()

try:
    video_filename = video_info['video']['s3_filename']
    video_id = video_info['video']['video_id']
    video_s3_key = video_info['video']['s3_key']
except KeyError:
    "KeyError: There is no information about this video in our database."

# Get audio from the video file:
audio_filename = get_audio_from_video(video_filename=video_filename,
                                      save_audio_as='audio.wav')

# Get transcript for the audio (which is from the video):
transcript_filename = get_transcript_from_audio(audio_filename=audio_filename,
                                                save_transcript_as='audio_transcript.txt')
transcript_string = open(transcript_filename).read().replace("\n", " ")


# ----------------------------------------------------------------------------
# SENTIMENT ANALYSIS:

# VISUAL SENTIMENT:

# [?? To add: Facial centering: Call Chris Huskey's master function and get results ??]
# visual_sentiment_results = [?? To add ??]

# Values for our DB videos_feedback table:
sentiment_visual = np.random.uniform(0, 5)  # [?? To do: REMOVE this ??]
sentiment_visual_details_fake = {
    "emotions": {
        "sad": 0.4816375482887931,
        "calm": 0.8443668165181737,
        "fear": 0.9012952623858596,
        "angry": 0.031246441854258622,
        "happy": 0.45286566659565175,
        "confused": 0.163269892703233,
        "disgusted": 0.9995419575080721,
        "surprised": 0.7591465415994776
    }
}
sentiment_visual_details = json.dumps(sentiment_visual_details_fake)

# AUDIO AND TEXT SENTIMENT:

audio_sentiment = get_audio_sentiment_analysis(audio_filename=audio_filename)
text_sentiment = get_text_sentiment(file=transcript_filename)

# Values for our DB videos_feedback table:
sentiment_audio = np.random.uniform(0, 5)  # [?? To do: REMOVE this ??]
sentiment_audio_details = json.dumps(audio_sentiment)


# ----------------------------------------------------------------------------
# SPEAKING SPEED:

speaking_speed = get_speed_of_speech(transcript_filename=transcript_filename,
                                      audio_filename=audio_filename)

# Values for our DB videos_feedback table:
speaking_speed = np.random.uniform(0, 5)  # [?? To do: REMOVE this ??]


# ----------------------------------------------------------------------------
# BACKGROUND NOISE:

# [To add:] Background noise: Call Chris Howell's master function and get results
# background_noise_score = [?? To add ??]

# Values for our DB videos_feedback table:
background_noise = np.random.uniform(0, 5)  # [?? To do: REMOVE this ??]


# ----------------------------------------------------------------------------
# APPEARANCE: FACIAL CENTERING:

# [To add:] Facial alignment and centering: Call Chris Huskey's master function
# and get results
# appearance_facial_centering = [?? To add ??]

# Values for our DB videos_feedback table:
appearance_facial_centering = np.random.uniform(0, 5)  # [?? To do: REMOVE this ??]


# ----------------------------------------------------------------------------
# HUMAN FEEDBACK:

# Get all human feedback on this video from our DB:
human_feedback_for_video = get_feedback_for_video(video_id=video_id)

# If there is no human feedback for this video yet, set all human feedback items to 0 in our DB
# (in our DB, 0 indicates no value yet):
if human_feedback_for_video.shape[0] < 1:
    human_overall_performance = 0
    human_delivery_and_presentation = 0
    human_response_quality = 0
    human_audio_quality = 0
    human_visual_environment = 0

# If there is human feedback for this user, get the average ratings:
else:
    human_overall_performance = human_feedback_for_video['overall_performance'].mean()
    human_delivery_and_presentation = human_feedback_for_video['delivery_and_presentation'].mean()
    human_response_quality = human_feedback_for_video['response_quality'].mean()
    human_audio_quality = human_feedback_for_video['audio_quality'].mean()
    human_visual_environment = human_feedback_for_video['visual_environment'].mean()


# ----------------------------------------------------------------------------
# ADD VIDEO ANALYSIS RESULTS TO OUR TEAMREEL DB:

# Set values, with zeros representing "not set yet" in our TeamReel DB:
# (i.e., "not set yet" items are what future Labs cohorts may want to implement)
video_id = video_id
overall_performance = np.random.uniform(0, 5)  # [?? To do: REMOVE this ??]
delivery_and_presentation = 0
response_quality = human_response_quality
audio_quality = 0
visual_environment = 0
attitude = 0
sentiment_visual = sentiment_visual
sentiment_visual_details = sentiment_visual_details
sentiment_audio = sentiment_audio
sentiment_audio_details = sentiment_audio_details
speaking_confidence = 0
speaking_volume = 0
speaking_vocabulary = 0
speaking_speed = speaking_speed
speaking_filler_words = 0
background_visual_environment = 0
background_noise = background_noise
appearance_facial_centering = appearance_facial_centering
appearance_posture = 0
appearance_gesticulation = 0
human_overall_performance = human_overall_performance
human_delivery_and_presentation = human_delivery_and_presentation
human_response_quality = human_response_quality
human_audio_quality = human_audio_quality
human_visual_environment = human_visual_environment

# For our SQL queries below: Dictionary of values to insert into SQL queries:
values_to_insert = {
    'video_id': video_id,
    'overall_performance': overall_performance,
    'delivery_and_presentation': delivery_and_presentation,
    'response_quality': response_quality,
    'audio_quality': audio_quality,
    'visual_environment': visual_environment,
    'attitude': attitude,
    'sentiment_visual': sentiment_visual,
    'sentiment_visual_details': sentiment_visual_details,
    'sentiment_audio': sentiment_audio,
    'sentiment_audio_details': sentiment_audio_details,
    'speaking_confidence': speaking_confidence,
    'speaking_volume': speaking_volume,
    'speaking_vocabulary': speaking_vocabulary,
    'speaking_speed': speaking_speed,
    'speaking_filler_words': speaking_filler_words,
    'background_visual_environment': background_visual_environment,
    'background_noise': background_noise,
    'appearance_facial_centering': appearance_facial_centering,
    'appearance_posture': appearance_posture,
    'appearance_gesticulation': appearance_gesticulation,
    'human_overall_performance': human_overall_performance,
    'human_delivery_and_presentation': human_delivery_and_presentation,
    'human_response_quality': human_response_quality,
    'human_audio_quality': human_audio_quality,
    'human_visual_environment': human_visual_environment
}

# Add the analysis for this video to the videos_feedback table in our DB:

# Check if record for this video exists in the videos_feedback table yet,
# and UPDATE or CREATE the record accordingly:
query = f"SELECT EXISTS (SELECT * FROM videos_feedback WHERE video_id = {video_id})"
pg_cursor.execute(query)
exists_in_vf_table = pg_cursor.fetchall()[0][0]

if exists_in_vf_table:
    print('yes, update it in videos_feedback table')  # [?? To do: REMOVE this ??]
    # Update record in videos_feedback table:
    pg_cursor.execute(
        """
        UPDATE videos_feedback
        SET
            overall_performance = %(overall_performance)s,
            delivery_and_presentation = %(delivery_and_presentation)s,
            response_quality = %(response_quality)s,
            audio_quality = %(audio_quality)s,
            visual_environment = %(visual_environment)s,
            attitude = %(attitude)s,
            sentiment_visual = %(sentiment_visual)s,
            sentiment_visual_details = %(sentiment_visual_details)s,
            sentiment_audio = %(sentiment_audio)s,
            sentiment_audio_details = %(sentiment_audio_details)s,
            speaking_confidence = %(speaking_confidence)s,
            speaking_volume = %(speaking_volume)s,
            speaking_vocabulary = %(speaking_vocabulary)s,
            speaking_speed = %(speaking_speed)s,
            speaking_filler_words = %(speaking_filler_words)s,
            background_visual_environment = %(background_visual_environment)s,
            background_noise = %(background_noise)s,
            appearance_facial_centering = %(appearance_facial_centering)s,
            appearance_posture = %(appearance_posture)s,
            appearance_gesticulation = %(appearance_gesticulation)s,
            human_overall_performance = %(human_overall_performance)s,
            human_delivery_and_presentation = %(human_delivery_and_presentation)s,
            human_response_quality = %(human_response_quality)s,
            human_audio_quality = %(human_audio_quality)s,
            human_visual_environment = %(human_visual_environment)s
        WHERE video_id = %(video_id)s
        """,
        values_to_insert
    )
else:
    print('no, insert into videos_feedback table')  # [?? To do: REMOVE this ??]
    # Create record in videos_feedback table:
    pg_cursor.execute(
        """
        INSERT INTO videos_feedback(??)
        VALUES (%(overall_performance)s,
                %(delivery_and_presentation)s,
                %(response_quality)s,
                %(audio_quality)s,
                %(visual_environment)s,
                %(attitude)s,
                %(sentiment_visual)s,
                %(sentiment_visual_details)s,
                %(sentiment_audio)s,
                %(sentiment_audio_details)s,
                %(speaking_confidence)s,
                %(speaking_volume)s,
                %(speaking_vocabulary)s,
                %(speaking_speed)s,
                %(speaking_filler_words)s,
                %(background_visual_environment)s,
                %(background_noise)s,
                %(appearance_facial_centering)s,
                %(appearance_posture)s,
                %(appearance_gesticulation)s,
                %(human_overall_performance)s,
                %(human_delivery_and_presentation)s,
                %(human_response_quality)s,
                %(human_audio_quality)s,
                %(human_visual_environment)s
                )
        WHERE video_id = %(video_id)s
        """,
    values_to_insert
    )

pg_conn.commit()


# [?? To do: REMOVE this ??]
print(f"video_info is: \n{video_info}")  # [?? To do: REMOVE this ??]
print(f"audio_filename is: {audio_filename}")  # [?? To do: REMOVE this ??]
print(f"transcript_filename is: {transcript_filename}")  # [?? To do: REMOVE this ??]
print(f"audio_sentiment is: {audio_sentiment}")  # [?? To do: REMOVE this ??]
print(f"text_sentiment is: {text_sentiment}")  # [?? To do: REMOVE this ??]
print(f"speaking_speed is: {speaking_speed}\n")  # [?? To do: REMOVE this ??]
print(f"other values in dict are: \n{values_to_insert}")


# ----------------------------------------------------------------------------
# REMOVE FILES:

remove_files(specified_files_list=[transcript_filename, audio_filename])

# ----------------------------------------------------------------------------

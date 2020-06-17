#!python
# Author: Chris Huskey

"""
Module of functions for working with our TeamReel PostgreSQL DB.
"""

# Import libraries we will use:
from dotenv import load_dotenv
import os
import pandas as pd
import psycopg2


# -------------------------------------------------------------------------
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


# -------------------------------------------------------------------------
def get_feedback_for_user(user_id:int):
    """
    Using the user's user_id in our database (= 'owner_id' in the 'feedback' table),
    looks up and returns all feedback on all of that user's videos.
    """

    # Check to make sure input param video_id is the right type:
    if type(user_id) is not int:
        raise ValueError('Invalid user_id')

    # Get all feedback for the given video from our PostgreSQL DB:
    pg_cursor.execute(f"SELECT fb.id, fb.post, fb.video_id, fb.created_at, fb.updated_at, fb.overall_performance, fb.delivery_and_presentation, fb.response_quality, fb.audio_quality, fb.visual_environment FROM feedback as fb, videos as vds WHERE (fb.video_id = vds.id AND vds.owner_id={user_id});")
    column_names = [column_name[0] for column_name in pg_cursor.description]

    feedback_dataframe = pd.DataFrame(data=pg_cursor.fetchall(), columns=column_names)

    return feedback_dataframe


# -------------------------------------------------------------------------
def get_feedback_for_video(video_id:int):
    """
    Using the video's video_id in our database, looks up and
    returns all feedback on that video.
    """

    # Check to make sure input param video_id is the right type:
    if type(video_id) is not int:
        raise ValueError('Invalid video_id')

    # Get all feedback for the given video from our PostgreSQL DB:
    pg_cursor.execute(f"SELECT * FROM feedback WHERE video_id={video_id};")
    column_names = [column_name[0] for column_name in pg_cursor.description]

    feedback_dataframe = pd.DataFrame(data=pg_cursor.fetchall(), columns=column_names)

    return feedback_dataframe


# -------------------------------------------------------------------------
def get_video_info(video_s3_key:str):
    """
    Using the video's S3 key, looks up info for that video, user and prompt
    in our PostgreSQL database, and returns all info in a dictionary with
    the following top-level keys:
    {
        'video': {
            info for the video itself
        },
        'prompt': {
            info for the prompt the video was responding to
        },
        'user': {
            includes info for the user who posted the video
        }
    }
    """

    # Return error if the input video_s3_key param is not a string:
    if type(video_s3_key) is not str:
        raise ValueError('Invalid video_s3_key')

    video_info = {'video': {},
                  'prompt': {},
                  'user': {}}

    # Lookup info for this video and user in our DB:

    # From DB table: 'videos'
    lookup_table_videos = lookup_in_videos_table(video_s3_key)
    if lookup_table_videos != "No data for this key in this table.":
        # Video info: Add video info to the video_info dict we will return:
        video_info['video']['video_id'] = lookup_table_videos['id']
        video_info['video']['title'] = lookup_table_videos['title']
        s3_key = lookup_table_videos['video_url']
        video_info['video']['s3_key'] = s3_key
        video_info['video']['s3_filename'] = s3_key.split('/')[-1]
        video_info['video']['created_at'] = lookup_table_videos['created_at']
        video_info['video']['updated_at'] = lookup_table_videos['updated_at']

        video_info['user']['user_id'] = lookup_table_videos['owner_id']
        video_info['prompt']['prompt_id'] = lookup_table_videos['prompt_id']

        # From DB table: 'users'
        lookup_table_users = lookup_in_users_table(video_info['user']['user_id'])
        if lookup_table_users != "No data for this key in this table.":
            # User info: Add user info to the video_info dict we will return:
            first_name = lookup_table_users['first_name'].capitalize()
            last_name = lookup_table_users['last_name'].capitalize()
            video_info['user']['first_name'] = first_name
            video_info['user']['last_name'] = last_name
            video_info['user']['name'] = first_name + " " + last_name
            video_info['user']['username'] = lookup_table_users['username']

        # From DB table: 'prompts'
        lookup_table_prompts = lookup_in_prompts_table(video_info['prompt']['prompt_id'])
        if lookup_table_prompts != "No data for this key in this table.":
            # Prompt info: Add prompt/question info to the the video_info dict:
            video_info['prompt']['question'] = lookup_table_prompts['question']

    return video_info


# -------------------------------------------------------------------------
def lookup_in_videos_table(video_s3_key):
    """
    Using an S3 key for a video (e.g., from a message in our SQS queue),
    get the info for this video from our DB table 'videos' and return it as a dict.
    """

    pg_cursor.execute(f"SELECT * FROM videos WHERE video_url='{video_s3_key}';")
    results = pg_cursor.fetchall()

    # Check to make sure results are not empty (i.e., no data in this table):
    if results == []:
        return "No data for this key in this table."

    # If there is data for this user_id in this table, return it:
    values = results[0]
    column_names = [column_name[0] for column_name in pg_cursor.description]
    results = dict(zip(column_names, values))

    return results


# -------------------------------------------------------------------------
def lookup_in_users_table(user_id):
    """
    Using a user_id in our TeamReel production DB (= owner_id in the 'users' table),
    get the info for this user from our DB table 'users' and return it as a dict.
    """

    pg_cursor.execute(f"SELECT * FROM users WHERE id={user_id};")
    results = pg_cursor.fetchall()

    # Check to make sure results are not empty (i.e., no data in this table):
    if results == []:
        return "No data for this key in this table."

    # If there is data for this user_id in this table, return it:
    values = results[0]
    column_names = [column_name[0] for column_name in pg_cursor.description]
    results = dict(zip(column_names, values))

    return results


# -------------------------------------------------------------------------
def lookup_in_prompts_table(prompt_id):
    """
    Using a user_id in our TeamReel production DB (= owner_id in the 'users' table),
    get the info for this user from our DB table 'users' and return it as a dict.
    """

    pg_cursor.execute(f"SELECT * FROM prompts WHERE id={prompt_id};")
    results = pg_cursor.fetchall()

    # Check to make sure results are not empty (i.e., no data in this table):
    if results == []:
        return "No data for this key in this table."

    # If there is data for this user_id in this table, return it:
    values = results[0]
    column_names = [column_name[0] for column_name in pg_cursor.description]
    results = dict(zip(column_names, values))

    return results

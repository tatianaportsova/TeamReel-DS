#!python
# Author: Chris Huskey

"""
Data pipeline for working with our AWS services and PostgreSQL DB
to process videos uploaded by TeamReel users.
"""

# Import external modules, packages, libraries we will use:
from dotenv import load_dotenv
import json
import os

# Import internal modules, packages, libraries for this project:
from .aws_sqs_functions import sqs_queue_get_next_item
from .aws_sqs_functions import sqs_delete_message_from_queue
from .aws_s3_functions import s3_download_file
from .postgresql_db_functions import get_video_info


# -------------------------------------------------------------------------
# SETUP:

# Get access info from .env file:
load_dotenv()

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


# -------------------------------------------------------------------------
def get_next_video():
    """
    Checks for newly uploaded videos (by our users) --> then downloads the
    raw video file of the next-in-line video to the project directory, and
    returns a dictionary with info about that video, prompt and user pulled
    from our DB.

    (1) Checks our TeamReel AWS SQS queue for new messages from newly
    uploaded videos (our S3 bucket sends a notification for each new video);
    (2) downloads the raw video file from S3 to your project directory;
    (3) gets info about that video, prompt, and user from our PostgreSQL DB;
    (4) deletes the message from our queue after processing; and
    (5) returns a Python dictionary of the video info pulled from the DB.

    Returns
    -------
    - If queue has >=1 messages in it: A dictionary with all relevant info
    about that video, prompt, and user from our DB.
    - If queue is empty: String: "No messages in queue."
    """

    # Get next message from SQS queue
    # (messages are auto-added by our S3 bucket each time a new video is uploaded to our S3 bucket):
    message = sqs_queue_get_next_item()

    # Check to see if queue is empty:
    if message == "No messages in queue.":
        return "No messages in queue."

    # If queue has messages (is not empty):
    else:

        # Message info, for deleting it after processing below:
        receipt_handle = message['ReceiptHandle']
        message_id_sqs = message['MessageId']

        # Get video's S3 key and filename from the SQS message:
        video_s3_key = json.loads(message['Body'])['Records'][0]['s3']['object']['key']
        video_s3_filename = video_s3_key.split('/')[-1]

        # -----------------------------------------------------------------------

        # Downloads the raw video file from the S3 bucket to your project directory:
        s3_download_file(bucket=S3_BUCKET_NAME,
                         filename=video_s3_filename,
                         key=video_s3_key)

        video_info = get_video_info(video_s3_key)

        # Delete the message now that we have received and processed it:
        sqs_delete_message_from_queue(receipt_handle=receipt_handle)

        return video_info

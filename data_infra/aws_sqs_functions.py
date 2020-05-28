#!python
# Author: Chris Huskey

"""
Module of functions for working with our AWS SQS Queue for Videos.
"""

# Import libraries we will use:
import boto3  # boto3 is AWS's Python SDK, by AWS
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os


# -------------------------------------------------------------------------
# SETUP:

# Get access info from .env file:
load_dotenv()

AWS_ACCESS_KEY_ID =os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

SQS_QUEUE_NAME = os.getenv("SQS_QUEUE_NAME")

# Create an SQS Service Resource:
sqs = boto3.resource('sqs',
                     aws_access_key_id=AWS_ACCESS_KEY_ID,
                     aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                    )

# Create a client object for SQS, using the access keys in our .env file:
sqs_client = boto3.client('sqs',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                         )

# Get our queue from SQS:
queue = sqs.get_queue_by_name(QueueName=SQS_QUEUE_NAME)


# -------------------------------------------------------------------------
def sqs_queue_get_next_item():
    """
    Gets the next message from our AWS SQS (Simple Queue Service) queue, and returns it.
    """

    # Get next message from SQS queue
    # (messages are auto-added by our S3 bucket each time a new video is uploaded to our S3 bucket):
    message = sqs_client.receive_message(QueueUrl=queue.url,
                                         MaxNumberOfMessages=1,
                                         MessageAttributeNames=['All']
                                        )

    # Check to see if queue is empty:
    if message == []:
        return "No messages in queue."
    elif (type(message) is dict) and ('Messages' not in message.keys()):
        return "No messages in queue."

    # If queue has messages (is not empty):
    else:
        message = message['Messages'][0]
        return message


# -------------------------------------------------------------------------
def sqs_delete_message_from_queue(receipt_handle:str):
    """
    Deletes a just-received message from the queue. (Note: Valid only within
    30 seconds of receiving the message, because that is our SQS queue's
    visibility timeout. So it is ideal to delete the message in the same run
    or same code cell during which you received the message).
    """
    
    # Delete message received from SQS queue:
    sqs_client.delete_message(
        QueueUrl=queue.url,
        ReceiptHandle=receipt_handle
    )

    return True

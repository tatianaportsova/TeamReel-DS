#!python
# Author: Chris Huskey

"""
Module of functions for working with our AWS S3 buckets for video storage.
"""

# Import libraries we will use:
import boto3  # boto3 is AWS's Python SDK, by AWS
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import json
import logging
import os


# -------------------------------------------------------------------------
# SETUP:

# Get access info from .env file:
load_dotenv()

AWS_ACCESS_KEY_ID =os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Create an S3 Service Resource:
s3 = boto3.resource('s3',
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                   )

# Make an S3 client with boto3:
s3_client = boto3.client('s3')  # Automatically loads AWS keys from .env file


# -------------------------------------------------------------------------
# Function that uploads the specified file to the specified S3 bucket:
def s3_download_file(bucket, filename, key=None):
    """
    Download the specified file from the specified S3 bucket.

    Parameters:
    bucket: Name of the bucket to get the file from
    filename: File to download
    key: S3 key of the file to download

    Returns: True if file was downloaded, else False.
    """

    # If S3 key and/or object_name were not specified, fill in based on filename:
    if key is None:
        key = 'videos/' + filename

    # Upload the file to the specified S3 bucket:
    try:
        response = s3_client.download_file(Bucket=bucket,
                                           Filename=filename,
                                           Key=key)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# -------------------------------------------------------------------------
# Function that uploads the specified file to the specified S3 bucket:
def s3_upload_file(bucket, filename, key=None):
    """
    Upload a file to an S3 bucket.

    Parameters:
    bucket: Name of the bucket to upload to
    filename: File to upload
    key: S3 key to upload the file as (e.g., 'videos/<file-name>')

    Returns: True if file was uploaded, else False.
    """

    # If S3 key and/or object_name were not specified, fill in based on filename:
    if key is None:
        key = 'videos/' + filename

    # Upload the file to the specified S3 bucket:
    try:
        response = s3_client.upload_file(Bucket=bucket,
                                         Filename=filename,
                                         Key=key)
    except ClientError as e:
        logging.error(e)
        return False
    return True

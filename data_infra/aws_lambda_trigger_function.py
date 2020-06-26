#!python
# Author: Chris Huskey

"""
TeamReel DS AWS Lambda Trigger Function: When a TeamReel user uploads a new
video to TeamReel -> video goes to S3 bucket -> S3 posts notification message
to SQS queue -> SQS queue launches this AWS Lambda function -> this Lambda
function calls our TeamReel DS API to trigger our main application.py
function to analyze that video (and add/update the TeamReel DB with the analysis).
"""

# Import modules/libraries we will use:

# Import external/third-party libraries we will use:
import json
from dotenv import load_dotenv
import os
import requests

# Get access info from .env file:
load_dotenv()


# -------------------------------------------------------------------------
# SETUP:

# TeamReel DS API Endpoints:
api_url = os.getenv("TEAMREEL_DS_API_URL")
endpoint_home = ""
endpoint_analyze_new_video = "analyze_new_video"
endpoint_get_user_performance = "get_user_performance"
endpoint_get_prompt_top_responses = "get_prompt_top_responses"
endpoint_get_video_analysis = "get_video_analysis"


# -------------------------------------------------------------------------
# FUNCTION:

# def lambda_handler(event, context):
#     # TODO implement
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Hello from Lambda!')
#     }

def ds_api_analyze_new_video(event, context):
    """
    Make a GET request to our TeamReel DS API's /analyze_new_video endpoint,
    to trigger our main DS analyze_new_video function and analyze the
    newly-posted video (from our queue).
    """

    # Request to /analyze_new_video endpoint:
    response = requests.get(url = api_url + endpoint_analyze_new_video)

    # Response:
    print(f"Response OK?: {response.ok}, with status code {response.status_code}")
    print(f"From URL: {response.url}")

    if response.text == 'No new videos uploaded since last check.':
        return response.text
    else:
        return response.json()

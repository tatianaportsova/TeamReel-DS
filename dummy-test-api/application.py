"""
Dummy Test API for Team Reel user and video analysis: Takes in and returns
dummy (fake data) for the following test endpoints:
- "/user_performance": Takes in a user_id, and returns a JSON with an analysis
of that user's interview performance to date.
- "/prompt_top_responses": Takes in a JSON with a prompt_id, and returns a
JSON with the top 3 video responses to that prompt.
- "/video_analyze": Takes in a user_id, prompt_id, video_id, video_s3_key and
video_s3_filename (of the raw video file), analyzes that video file, and adds
the resulting analysis to that user's info in our database. Returns only the
string "True" if received.
"""


from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template
import os


# Global variables/constants:
# None

# Get secret keys from .env file:
load_dotenv()

# Dummy API placeholder data:
import dummy_data

DUMMY_INPUT_USER_PERFORMANCE = dummy_data.DUMMY_INPUT_USER_PERFORMANCE
DUMMY_INPUT_PROMPT_TOP = dummy_data.DUMMY_INPUT_PROMPT_TOP
DUMMY_INPUT_VIDEO_ANALYZE = dummy_data.DUMMY_INPUT_VIDEO_ANALYZE

DUMMY_OUTPUT_USER_PERFORMANCE = dummy_data.DUMMY_OUTPUT_USER_PERFORMANCE
DUMMY_OUTPUT_PROMPT_TOP = dummy_data.DUMMY_OUTPUT_PROMPT_TOP
DUMMY_OUTPUT_VIDEO_ANALYZE = dummy_data.DUMMY_OUTPUT_VIDEO_ANALYZE


# Initialize our flask app (API):
application = Flask(__name__)

# Load our model:
# None

# Base route just so AWS doesn't show status as problematic:
@application.route('/')
def root():
    title = """Welcome to the Team Reel Interview Analysis API (Dummy Test
    Version)!"""
    api_welcome_string = "Endpoints:\n"
    endpoint_1="""/user_performance: Takes in a JSON with a user_id, and returns
    a JSON with analysis of that user's interview performance to date."""
    endpoint_2="""/prompt_top_responses: Takes in a JSON with a prompt_id, and
    returns a JSON with that prompt's top 3 video responses."""
    endpoint_3="""/video_analyze: Takes in a JSON with the user_id, prompt_id,
    video_id, video_s3_key and video_s3_filename (of the raw video file),
    analyzes that video file, and adds the resulting analysis to that user's
    info in our database. Returns string "True" if received."""

    return render_template("home.html",
                           title=title,
                           text=api_welcome_string,
                           endpoint_1=endpoint_1,
                           endpoint_2=endpoint_2,
                           endpoint_3=endpoint_3
                           )

# "/user_performance" API endpoint: Takes in a user_id, and returns a JSON with
# an analysis of that user's interview performance to date.
@application.route('/user_performance', methods=['POST'])
def user_performance():
    """
    "/user_performance" API endpoint: Takes in a user_id, and returns a
    JSON with an analysis of that user's interview performance to date.
    """
    # Check to make sure we received a valid JSON with the request:
    if not request.json:
        return jsonify({"error": "no request received"})

    # Get user ID from incoming API request JSON:
    input_user_id = request.get_json(force=True)['user_id']

    # Model analysis goes here:
    # None (dummy model)

    # Return JSON with analysis of user's interview performance:
    return jsonify(DUMMY_OUTPUT_USER_PERFORMANCE)

# "/prompt_top_responses" API endpoint: Takes in a JSON with a prompt_id, and
# returns a JSON with that prompt's top 3 video responses.
@application.route('/prompt_top_responses', methods=['POST'])
def prompt_top_responses():
    """
    "/prompt_top_responses" API endpoint: Takes in a JSON with a prompt_id, and
    returns a JSON with that prompt's top 3 video responses.
    """
    # Check to make sure we received a valid JSON with the request:
    if not request.json:
        return jsonify({"error": "no request received"})

    # Get incoming request with the image data:
    input_prompt_id = request.get_json(force=True)['prompt_id']

    # Model analysis goes here:
    # None (dummy model)

    # Return JSON with analysis of user's interview performance:
    return jsonify(DUMMY_OUTPUT_PROMPT_TOP)

# "/video_analyze" API endpoint: Takes in a JSON with the user_id, prompt_id,
# video_id, video_s3_key and video_s3_filename (of the raw video file),
# analyzes that video file, and adds the resulting analysis to that user's
# info in our database. Returns string "True" if received.
@application.route('/video_analyze', methods=['POST'])
def video_analyze():
    """
    "/video_analyze" API endpoint: Takes in a JSON with the user_id, prompt_id,
    video_id, video_s3_key and video_s3_filename (of the raw video file),
    analyzes that video file, and adds the resulting analysis to that user's
    info in our database. Returns string "True" if received.
    """
    # Check to make sure we received a valid JSON with the request:
    if not request.json:
        return jsonify({"error": "no request received"})

    # Get incoming request with the image data:
    input_video_s3_key = request.get_json(force=True)['video_s3_key']

    # Model analysis goes here:
    # None (dummy model)

    # Return JSON with analysis of user's interview performance:
    return DUMMY_OUTPUT_VIDEO_ANALYZE

# -------------------------------------------------------------------
# While debugging:
if __name__ == "__main__":
    application.run(debug=False, port=8080)

"""
TeamReel audio_analysis Python package: modules and functions for
working with audio from TeamReel users' video responses, including
to get audio from a video file (get_audio_from_video), get a
speech-to-text transcription of the audio (get_transcript_from_audio),
and for audio sentiment analysis.
"""

from .audio_functions import get_audio_from_video, get_transcript_from_audio
from .audio_functions import get_audio_sentiment_analysis


__all__ = ["get_audio_from_video",
           "get_transcript_from_audio",
           "get_audio_sentiment_analysis"]

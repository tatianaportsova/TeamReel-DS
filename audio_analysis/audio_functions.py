#!python
# Author: Tatiana Portsova

"""
Module of functions for audio processing and ML audio analysis for
TeamReel videos.
"""

# Import external modules, packages, libraries we will use:
import contextlib
from gensim.utils import simple_preprocess
import json
import keras
from keras.models import Model, model_from_json
import librosa
import moviepy.editor
import numpy as np
import os
import pandas as pd
import pickle
from pydub import AudioSegment
from pydub.utils import make_chunks
import re
import speech_recognition as sr
import shutil
from textblob import TextBlob
import tensorflow as tf
import wave

# Import internal modules, packages, libraries for this project:
from data_infra.data_pipelines import get_next_video


# LOAD MODELS:

# Get relative file path for models:
cwd = os.getcwd().split('/')[-1]

if cwd == 'video-journal-for-teams-ds':
    MODELS_PATH = './models/'
elif cwd == 'audio_analysis':
    MODELS_PATH = '../models/'

# loading json and model architecture
json_file = open(MODELS_PATH + 'audio_analysis_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# load weights into new model
loaded_model.load_weights(MODELS_PATH + 'audio_analysis_weights.h5')

# compile loaded model
opt = keras.optimizers.rmsprop(lr=0.00001, decay=1e-6)
loaded_model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

# load class labels
infile = open(MODELS_PATH + 'audio_analysis_labels','rb')
lb = pickle.load(infile)
infile.close()



# FUNCTIONS FOR SENTIMENT ANALYSIS:

def get_audio_from_video(video_filename:str, save_audio_as:str):
    """
    Gets an audio file from user's video
    """
    video = moviepy.editor.VideoFileClip(video_filename)
    audio = video.audio
    audio.write_audiofile(save_audio_as)
    audio_filename = save_audio_as

    return audio_filename

def get_audio_sentiment_analysis(audio_filename:str):
    """
    A function to get sentiment/emotion analysis from the audio
    """
    audio = AudioSegment.from_file(audio_filename, "wav")
    chunk_length_ms = 4000
    chunks = make_chunks(audio, chunk_length_ms)

    #Export all of the individual chunks as wav files
    path = "audio_sentiment/"
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    for i, chunk in enumerate(chunks):
        chunk_name = f"{path}chunk{i}.wav"
        chunk.export(chunk_name, format="wav")

    lists_of_files = os.listdir(path)
    test_predictions = pd.DataFrame(columns=['predictions'])

    for filename in lists_of_files:
        try:
            data, sample_rate = librosa.load(f"{path}{filename}",
                                             res_type='kaiser_fast',
                                             sr=44100)
            #print(filename)
            sample_rate = np.array(sample_rate)
            mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate, n_mfcc=13),axis=0)
            newdf = pd.DataFrame(data=mfccs).T

            # Apply predictions
            newdf= np.expand_dims(newdf, axis=2)
            newpred = loaded_model.predict(newdf,batch_size=16,verbose=1)

            # Get the final predicted label
            final = newpred.argmax(axis=1)
            final = final.astype(int).flatten()
            final = (lb.inverse_transform((final)))
            #print(final)
            test_predictions.loc[filename] = final
        except:
            pass

    labels = test_predictions.predictions.value_counts(normalize=True).keys().tolist()

    values= []
    predictions = {}
    for i in test_predictions.predictions.value_counts(normalize=True).tolist():
        values.append(round(i,2))
    for key in labels:
        for value in values:
            predictions[key] = value
            values.remove(value)
            break

    return predictions



# FUNCTIONS FOR SPEECH RECOGNITION AND AUDIO TRANSCRIPTION:

def break_audio_file(audio_filename:str):
    """
    Breaks an audio file into smaller chunks
    """
    myaudio = AudioSegment.from_file(audio_filename, "wav")
    chunk_length_ms = 20000 # pydub calculates in millisec
    chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of 20 sec

    #Export all of the individual chunks as wav files
    path = "audio_chunks/"
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    for i, chunk in enumerate(chunks):
        chunk_name = "audio_chunks/chunk{0}.wav".format(i)
        chunk.export(chunk_name, format="wav")
    return path

def get_file_paths(folder_path:str):
    """
    Gets file paths for files in the provided folder from the directory.
    """
    # Standardize inputs: Add '/' to end of folder name string if not present:
    if folder_path[-1] != '/':
        folder_path = folder_path + '/'

    # Get file paths for files in the specified folder:
    file_paths = []
    for root, directories, files in os.walk(folder_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

def speech_to_text(file):
    """
    Applies SpeechRecognition to the audio files
    """
    recognizer = sr.Recognizer()
    a = ''
    with sr.AudioFile(file) as source:
        #recognizer.adjust_for_ambient_noise(source)  # adjust for noisy audio
        audio = recognizer.record(source)
        try:
            a =  recognizer.recognize_google(audio)   # recognize_google_cloud for GC API
        except sr.UnknownValueError:
            a = "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            a = "Could not request results from Google Speech Recognition service; {0}".format(e)
    return a

def get_text_chunks(audio_chunks_path:str):
    # Create a new directory to store the chunks of txt
    text_chunks_path = 'text_chunks/'
    try:
        os.mkdir(text_chunks_path)
    except OSError:
        print ("Creation of the directory %s failed" % text_chunks_path)
    else:
        print ("Successfully created the directory %s " % text_chunks_path)

    audio_chunks_files = get_file_paths(folder_path=audio_chunks_path)
    for file in audio_chunks_files:
        (filepath, ext) = os.path.splitext(file)
        file_name = os.path.splitext(os.path.basename(file))[0]
        # only process audio if the file is a '.wav' audio file:
        if ext == '.wav':
            transcription_text = speech_to_text(file)
            with open(f"{text_chunks_path}{file_name}.txt", "w") as f:
                f.write(transcription_text+". ")
    return text_chunks_path

def get_transcript_from_audio(audio_filename:str, save_transcript_as:str):
    """
    A function to get a text transcript from an audio file.
    """
    transcript_filename = save_transcript_as
    audio_chunks_path = break_audio_file(audio_filename=audio_filename)
    text_chunks_path = get_text_chunks(audio_chunks_path=audio_chunks_path)
    files = get_file_paths(folder_path='text_chunks')
    files.sort(key=lambda x: int(re.sub('\D', '', x)))
    #sorted(files, key=lambda x: int(re.sub('\D', '', x)))

    # Combine text segments into one .txt file transcript for the audio file:
    with open(transcript_filename, 'w+') as f:
        for file in files:
            with open(file) as infile:
                f.write(infile.read()+'\n')
    return transcript_filename

# Tokenize data
def tokenize(text):
    return [token for token in simple_preprocess(text)]   # (if token not in STOPWORDS)

def get_tokens(transcript_filename:str):
    with open(transcript_filename) as file:
      text = file.read().strip('\n')
      tokens = tokenize(str(text))
    return tokens


# FUNCTIONS FOR SPEED OF SPEECH:

def get_audio_duration(filename:str='audio.wav'):
    with contextlib.closing(wave.open(filename,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = (frames / float(rate)) / 60
        return duration

def get_speed_of_speech(transcript_filename:str, audio_filename:str):
    tokens = get_tokens(transcript_filename=transcript_filename)
    speed_of_speech = len(tokens) / get_audio_duration(filename=audio_filename)
    return speed_of_speech


# FUNCTIONS FOR TEXT SENTIMENT ANALYSIS (ON TEXT TRANSCRIPT FROM AUDIO):

def get_text_sentiment(file = 'audio_transcript.txt'):
    with open(file, 'r') as f:
        text = f.read()
        sentiment = TextBlob(text).sentiment.polarity
        return sentiment


# Function that removes directories and files after we are done with them:

def remove_files(specified_files_list=[], specified_folders_list=[]):
    """
    Removes files and directories after they're no longer needed.
    """
    files_to_remove = {'audio_transcript.txt', 'audio.wav'}
    folders_to_remove = {'audio_chunks', 'text_chunks', 'audio_sentiment'}

    # Add any specified files/folders (input params):
    for file in specified_files_list:
        files_to_remove.add(file)
    for folders in specified_folders_list:
        folders_to_remove.add(folder)

    # Add name of video file to remove:
    for file in os.listdir('.'):
        ext = os.path.splitext(file)[-1]
        if file.startswith('ALPACAVID', 0) and (ext == '.mp4' or ext == '.webm'):
            files_to_remove.add(file)

    # Delete the files and folders:
    for file in files_to_remove:
        if file in os.listdir('.'):
            try:
                os.remove(file)
            except OSError as e:
                print("Error: %s : %s" % (file, e.strerror))

    for folder in folders_to_remove:
        if folder[-1] == '/':
            folder = folder[:-1]
        # Remove the folder and all files in it:
        if folder in os.listdir('.'):
            if folder[-1] != '/':
                folder = folder + '/'
            try:
                shutil.rmtree(folder)
            except OSError as e:
                print("Error: %s : %s" % (file, e.strerror))


# Main function to analyse the audio:

def analyse_audio(audio_filename:str):
    # Transcript:
    transcript_filename = get_transcript_from_audio(audio_filename=audio_filename,
                                                    save_transcript_as='audio_transcript.txt')
    # Analysis:
    audio_sentiment = get_audio_sentiment_analysis(audio_filename=audio_filename)
    speed_of_speech = get_speed_of_speech(transcript_filename=transcript_filename,
                                          audio_filename=audio_filename)
    text_sentiment = get_text_sentiment(file=transcript_filename)

    return audio_sentiment, text_sentiment, speed_of_speech
    # returns tuple
    # e.g. ({'positive': 0.41, 'neutral': 0.31, 'negative': 0.27},
    #        0.20464141414141415, 130.51674964953835)

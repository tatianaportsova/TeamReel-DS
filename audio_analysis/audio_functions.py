# Import external modules, packages, libraries we will use:
from textblob import TextBlob
from gensim.utils import simple_preprocess
import shutil
import re 
import speech_recognition as sr
import os
import moviepy.editor
from pydub import AudioSegment
from pydub.utils import make_chunks
import numpy as np
import pandas as pd
import pickle
import json
import keras
import wave
import contextlib
from keras.models import Model, model_from_json
import tensorflow as tf
import librosa

# Import internal modules, packages, libraries for this project:
from data_infra.data_pipelines import get_next_video

"""
Load models
"""
# loading json and model architecture 
json_file = open('Pickled_files/MLModel.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# load weights into new model
loaded_model.load_weights("Pickled_files/Augmented_Model.h5")
 
# compile loaded model
opt = keras.optimizers.rmsprop(lr=0.00001, decay=1e-6)
loaded_model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

# load lables
infile = open('Pickled_files/labels','rb')
lb = pickle.load(infile)
infile.close()



'''  Functions for Sentiment Analysis  '''


def get_audio_from_video(video_file):
    """
    Gets an audio file from user's video
    """
    video = moviepy.editor.VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile('audio.wav')
    
def get_sentiment_analysis():
    """
    A function to get sentiment/emotion analysis from the audio
    """
    get_audio_from_video()
    audio = AudioSegment.from_file("audio.wav", "wav")
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
        chunk_name = "audio_sentiment/chunk{0}.wav".format(i)
        chunk.export(chunk_name, format="wav")
    
    lists_of_files = os.listdir(path)
    test_predictions = pd.DataFrame(columns=['predictions'])
    
    for filename in lists_of_files:
        try:
            data, sample_rate = librosa.load("audio_sentiment/{}".format(filename),
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



'''   Functions for Speed of Speech   '''


def break_audio_file(file_name = 'audio.wav'):
    """
    Breaks an audio file into smaller chunks
    """
    myaudio = AudioSegment.from_file(file_name, "wav") 
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

dirname = "audio_chunks/"
def get_file_paths(dirname):
    """
    Gets file paths from the directory
    """
    file_paths = []  
    for root, directories, files in os.walk(dirname):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  
    return file_paths 

def process_file(file):
    """
    Applies SpeechRecognition to the audio files
    """
    r = sr.Recognizer()
    a = ''
    with sr.AudioFile(file) as source:
        #r.adjust_for_ambient_noise(source)  # adjust for noisy audio
        audio = r.record(source)    
        try:
            a =  r.recognize_google(audio)   # recognize_google_cloud for GC API
        except sr.UnknownValueError:
            a = "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            a = "Could not request results from Google Speech Recognition service; {0}".format(e)  
    return a

def get_text():
    # Create a new directory to store the chunks of txt
    path = 'text_chunks/'
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
    
    files = get_file_paths(dirname)                             
    for file in files:                                           
        (filepath, ext) = os.path.splitext(file)                  
        file_name = os.path.splitext(os.path.basename(file))[0]
        # only interested if extension is '.wav'
        if ext == '.wav':                                         
            a = process_file(file)
            with open("text_chunks/{}.txt".format(file_name), "w") as f:
                f.write(a+". ")  

path = r"text_chunks/"
def get_transcripts_from_audio(audio_file='audio.wav'):
    """
    A function to get a transcripts from the audio (stores text into separate chunks of text)
    """
    break_audio_file()
    get_text()
    files = get_file_paths(path)
    files.sort(key=lambda x: int(re.sub('\D', '', x)))
    #sorted(files, key=lambda x: int(re.sub('\D', '', x)))
    with open('outputfile.txt', 'w+') as f: 
        for file in files:
            with open(file) as infile:
                f.write(infile.read()+'\n')

# Tokenize data
def tokenize(text):
    return [token for token in simple_preprocess(text)]   # (if token not in STOPWORDS)

def gather_data(path_to_data): 
    data = []
    for f in os.listdir(path):
        if os.path.isdir(f) == False:
            if f[-3:] == 'txt':
                with open(os.path.join(path,f)) as t:
                    text = t.read().strip('\n')
                    data.append(tokenize(str(text)))       
    return data

def get_audio_duration(file_name = 'audio.wav'):
    with contextlib.closing(wave.open(file_name,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = (frames / float(rate)) / 60
        return duration
    
def get_speed_of_speech():
    tokens = gather_data('outputfile.txt')
    count = 0
    for i in tokens:
        count += len(i)    
    speed_of_speech = count / get_audio_duration(file_name = 'audio.wav')
    return speed_of_speech


'''  Function for Text (from Audio) Sentiment Analysis  '''

def get_text_sentiment(file = 'outputfile.txt'):
    with open(file, 'r') as f:
        text = f.read()
        sentiment = TextBlob(text).sentiment.polarity
        return sentiment


'''  A function that removes directories and files after we are done with them  ''' 

def remove_files():
    """
    Removes files and directories after they're no longer needed
    """
    paths = ['audio_chunks/', 'audio_sentiment/', 'text_chunks/']
    os.remove('outputfile.txt')
    
    for i in paths:
        try:
            shutil.rmtree(i)
        except OSError as e:
            print("Error: %s : %s" % (i, e.strerror))


'''  The main function to analyse the audio  '''

def analyse_audio():
    path = r"text_chunks/"
    audio_sentiment = get_sentiment_analysis()
    get_transcripts_from_audio(audio_file='audio.wav')
    speed_of_speech = get_speed_of_speech()
    text_sentiment = get_text_sentiment()
    return audio_sentiment, text_sentiment, speed_of_speech
    # returns tuple
    # e.g. ({'positive': 0.41, 'neutral': 0.31, 'negative': 0.27},
    #        0.20464141414141415, 130.51674964953835)


###  A POSSIBLE ALTERNATIVE TO SPEECH RECOGNITON GOOGLE API  ###

So far, for this project we used Google Chrome Web Speech API but it has certain limitations.

As an alternative, we experimented with DeepSpeech 0.7.4. The result we got from a short lecture clip you can see in the outputTest.txt file. It's far from perfect and it isn't suitable for production, but it can be improved.
If DeepSpeech is something you want to give a better try, then some of the possible ways this could be taken further are:
   ~ training a DeepSpeech model for 44100hz data;
   ~ teaching it new words.

Here are the steps to use a Pre-trained model locally:
 1. mkdir DeepSpeech
 2. cd DeepSpeech
 3. python3 -m venv ./some/pyenv/dir/path/DeepSpeech
 4. source ./some/pyenv/dir/path/DeepSpeech/bin/activate
 5. pip3 install deepspeech==0.7.4
 6. curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.7.4/deepspeech-0.7.4-models.pbmm
 7. curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.7.4/deepspeech-0.7.4-models.scorer
 8. ###place an audio file you want to transcribe into the DeepSpeech folder
 9. ###copy DeepSpeech_functions.py into the DeepSpeech folder
 10. ###specify the audio file path in DeepSpeech_functions.py
 11. python DeepSpeech_functions.py
 

Reference links: https://deepspeech.readthedocs.io/en/v0.7.4/
                 https://github.com/mozilla/DeepSpeech/blob/master/native_client/python/client.py

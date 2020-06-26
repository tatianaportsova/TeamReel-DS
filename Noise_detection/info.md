This noise reduction module is currently meant to be deployed seperately and called as an API. 

However, with a few modifications it could be deployed on the main Heroku instance.

To do so, the code splitting the audio from the video and cutting it into clips should be removed
and the function can call the smae clips that the audio sentiment function uses.

# TeamReel
## TeamReel is the platform for teams to practice and get feedback for their on-screen talking skills asynchronously. 
### The web app built on a Postgres database and a Node Express backend. The front-end is built on React & Redux. Websockets will be used for bi-directional real time updates.  Front End is deployed on amplify.   Backend is deployed on AWS.
## https://teamreel.org/

The task for the DS team was to collect and analyze feedback — both human feedback and automated ML feedback — on user-submitted video responses, and use it to:
- provide interviewee users with suggestions on improving their presentation skills;
- provide TLs with a way to efficiently see students' performance.

We provided an API that returns the following to Web/front-end:
- **Interview performance scores:** Calculates and provides an "overall performance score" for each user, based on their interview performance (most recent 3 video responses), using both the human feedback items + ML feedback items.
- **User performance visualization/dashboard:** Provides each user with clear visualizations of their interview performance, working with Web and iOS to display these in the front-end.


***Breakdown of the "overall perforance score":***

- **Speaking Speed:**
The speaking speed scores are created by transcribing the video and dividing by the length of the video.  The raw statistic is turned into a score based on researched (linked here) showing that a typical average speaking speed is around 150 words per minute.  
 ● 5 for speech with  between 135 and 165 words per minute
 ● 4 for speech with between 120 and 135 or 165 and 180 words per minute
 ● 3 for speech with between 100 and 135 or 180 and 195 words per minute
 ● 2 for speech with between   85 and 100 or 195 and 210 words per minute
 ● 1 for all other speaking speeds


- **Sentiment:**
This score is produced by using a neural network to detect sentiment in the video using facial features. The neural network rates each frame of a  video as positive, negative, or neutral.   The total amount of time with negative sentiment is then divided by the length of the video to determine the percentage of negative sentiment.
 ● 5 for videos with negative sentiment detected for less than 20% of the video
 ● 4 for videos with negative sentiment detected for 20-40% of the video
 ● 3 for videos with negative sentiment detected for 40-60%  of the video
 ● 2 for videos with negative sentiment detected for c%  of the video
 ● 1 for videos with negative sentiment detected for more than 80% of the video


- **Facial Centering:**
This score is produced by measuring if a speaker’s face is in the central region of the video, and whether the user’s face is upright (vertical).  For each frame of video, we use neural network facial recognition technology to find the speaker’s face position and note where the face is located, and then the user’s nose is used to determine if the user’s head is upright.
 ● 5 for videos with the user’s face centered for more than 90% of the video
 ● 4 for videos with the user’s face centered for 80 - 90% of the video
 ● 3 for videos with the user’s face centered for 70 - 80%  of the video
 ● 2 for videos with the user’s face centered for 60-70%  of the video
 ● 1 for videos with the user’s face centered for less than 60% of the video


- **Background Noise:**
This score is produced by using a neural network to detect background noise in the audio. The total amount of time with background noise is then divided by the length of the video to determine the percentage of noisy video
 ● 5 for videos with the background noise detected for less than 10% of the video
 ● 4 for videos with the background noise detected for 10-20% of the video
 ● 3 for videos with the background noise detected for 20-30%  of the video
 ● 2 for videos with the background noise detected for 30-40%  of the video
 ● 1 for videos with the background noise detected for more than 40% of the video


- **Human Feedback**
All scores from other users’ feedback for a video are averaged and the average is displayed.  The following are the user feedback categories:
 ● Content
 ● Presentation
 ● Audio Quality
 ● Video Quality

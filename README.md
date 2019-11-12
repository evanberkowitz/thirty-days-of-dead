# thirty-days-of-dead
Let there be songs to fill the air!


[30 Days of Dead][thirty] is a tradition the Grateful Dead does every November, where each day is a contest with a different snippet of a live recording.  If you can identify the recording (meaning, where and when it was recorded) you might win a prize.

Once the day is over, the recording is made available in full for download.  This script helps you download these full-length recordings.

If you `pip3 install mp3_tagger` you should be able to run `get.py`.  By editing the `DAYS` variable you can download any span of days you desire.

This script may not work in future years, but presumably all that would need changing is the `url` and `parse` functions, in the event that [dead.net][dead] changed their URL scheme or HTML formatting that allowed me to pull the info out of the page.





[thirty]:   https://www.dead.net/30daysofdead
[dead]:     https://www.dead.net

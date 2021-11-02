# thirty-days-of-dead
Let there be songs to fill the air!


[30 Days of Dead][thirty] is a tradition the Grateful Dead does every November, where each day is a contest with a different snippet of a live recording.  If you can identify the recording (meaning, where and when it was recorded) you might win a prize.

Once the day is over, the recording is made available in full for download.  This script helps you download these full-length recordings.  You can get every recording up to but excluding today.

If you `pip3 install mp3_tagger` you should be able to run `get.py`.

```
usage: get.py [-h] [--year YEAR] [--day DAY] [--artist ARTIST] [--album ALBUM]
              [--format FORMAT] [--overwrite] [--verbose]

optional arguments:
  -h, --help       show this help message and exit
  --year YEAR      The current year by default.
  --day DAY        1:(the current day in November) by default.
                   During November, the default latest day is the current day;
                   during other months the default is 1:31. You can specify
                   a single number '--day 7', a list of comma-separated numbers, 
                   '--day 1,3,5', or a python-style range '--day 1:10:2'.
                   You can use open-ended ranges like '10:' or ':10' to get
                   everything starting on or up to but not including day 10,
                   respectively.
  --artist ARTIST  'Grateful Dead' by default. Depending on your music library's
                   organization you might want to change the artist. One example
                   would be 'The Grateful Dead' (with 'The')
  --album ALBUM    '30 Days of Dead 2021' by default.
  --format FORMAT  A format string for the song name. 
                   Defaults to '{TITLE} - {DATE} - {LOCATION}'.
                   Other possible fields are DAY, ALBUM, and ARTIST
  --overwrite      If a song file already exists, redownload it nevertheless and
                   overwrite the old one.
  --verbose        Print a lot more information, used for debugging.
```

# Album Art
You've got to do it yourself; I'd wait until the end of the month.

# Caveat Emptor

This script may not work in future years, but presumably all that would need changing is the `url` and `parse` functions, in the event that [dead.net][dead] changed their URL scheme or HTML formatting that allowed me to pull the info out of the page.



[thirty]:   https://www.dead.net/30daysofdead
[dead]:     https://www.dead.net

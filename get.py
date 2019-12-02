#!/usr/bin/env python3

# GPLv3, Evan Berkowitz, 2019
# https://github.com/evanberkowitz/thirty-days-of-dead

import requests
import re
from pathlib import Path
import datetime
from mp3_tagger import MP3File, VERSION_BOTH


ALBUM="30 Days of Dead 2019"
ARTIST="Grateful Dead"
# 30 days hath ... November.  Also, it is THIRTY Days of Dead!
DAYS=range(1,31)    # ...but of course range goes to the end-1.

def url(november):
    # This is the URL that you get if you look at "PAST DATES"
    # on https://www.dead.net/30daysofdead
    return f"https://www.dead.net/30daysofdead/nov-{november:02d}-2019"

def parse(content):
    # With the page content in hand we need to extract the relevant information.

    # Most importantly, where does the mp3 live?
    mp3 = re.findall(rb'http[s]?://rhino.*\.mp3', content)
    mp3 = mp3[0].decode("utf-8")

    # What is the song's title?
    title = re.findall(rb'field-song-title"><.*>.*</div></div><div class="views-field', content)[0].decode("utf-8")
    title = title.split(">")[2].split("<")[0]

    # At what venue was the performance?
    location = re.findall(rb'"views-field views-field-field-show-answer"><div class="field-content">.*</div></div><div class="views-field views-field-field-show-answer-date"', content)[0].decode("utf-8")
    location = location.split(">")[2].split("<")[0]

    # ... and when?
    date = re.findall(rb'datetime">.*</time', content)[0].decode("utf-8")
    date = date.split(">")[1].split("<")[0]
    date = datetime.datetime.strptime(date, '%B %d, %Y').strftime('%Y-%m-%d')

    return mp3, title, location, date

for DAY in DAYS:
    URL  = url(DAY)
    page = requests.get(URL)
    content = page.content

    try:
        remote, title, location, date = parse(content)
    except:
        continue

    SONG=f"{title} - {date} - {location}"
    print(f"Day {DAY:02}: {SONG}")

    # Download the remote file.
    file = Path(remote).name        # Figure out where to store it.
    download = requests.get(remote) # Get it from afar.
    song = open(file, 'wb')         # Prepare to write it in binary,
    song.write(download.content)    # dump it to disk,
    song.close()                    # and save.

    # Unfortunately, the ID3 tag is essentially empty.
    # So, use an ID3 library to add some of the data we parsed.

    mp3=MP3File(file)
    mp3.set_version(VERSION_BOTH)
    mp3.artist=ARTIST
    mp3.album=ALBUM
    mp3.song=SONG
    mp3.year=date.split("-")[0]     # the year of recording, not THIS year!
    mp3.track=str(DAY)              # which day of THIS NOVEMBER was the song available?
    mp3.url=URL
    mp3.save()

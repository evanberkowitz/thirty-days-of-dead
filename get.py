#!/usr/bin/env python3

# GPLv3, Evan Berkowitz, 2019
# https://github.com/evanberkowitz/thirty-days-of-dead

import requests
import re
from pathlib import Path
import datetime
from mp3_tagger import MP3File, VERSION_BOTH

import argparse
parser = argparse.ArgumentParser()

today=datetime.date.today()
CURRENT_YEAR=today.strftime("%Y")
CURRENT_MONTH=today.strftime("%m")
CURRENT_DAY=today.strftime("%d")

if CURRENT_MONTH == '11':
    default_day=CURRENT_DAY
else:
    default_day='31'

parser.add_argument('--year', type=str, default=CURRENT_YEAR, help=f"{CURRENT_YEAR} by default.")
# 30 days hath  ... November.  Also, it is THIRTY Days of Dead!
#               ...but of course range goes to the end-1.
parser.add_argument('--day', type=str, default=f"1:{default_day}", help=f"1:{default_day} by default.  During November, the default latest day is the current day; during other months the default is 1:31.  You can specify a single number '--day 7', a list of comma-separated numbers, '--day 1,3,5', or a python-style range '--day 1:10:2'.  You can use open-ended ranges like '10:' or ':10' to get everything starting on or up to but not including day 10, respectively.")
parser.add_argument('--artist', type=str, default="Grateful Dead", help="'Grateful Dead' by default.  Depending on your music library's organization you might want to change the artist.  One example would be 'The Grateful Dead' (with 'The')")
parser.add_argument('--album', type=str, default=f"30 Days of Dead {CURRENT_YEAR}", help=f"'30 Days of Dead {CURRENT_YEAR}' by default.")
parser.add_argument('--format', type=str, default="{TITLE} - {DATE} - {LOCATION}", help="A format string for the song name.  Defaults to '{TITLE} - {DATE} - {LOCATION}'.  Other possible fields are DAY, ALBUM, and ARTIST")
parser.add_argument('--overwrite', action='store_true', help="If a song file already exists, redownload it nevertheless and overwrite the old one.")
parser.add_argument('--verbose', action='store_true', help="Print a lot more information, used for debugging.")

args = parser.parse_args()

# vprint prints normally if --verbose is passed, otherwise it's no-op.
if args.verbose:
    vprint=print
else:
    vprint = lambda *a, **k: None

vprint(args)

YEAR=args.year
ALBUM=args.album
ARTIST=args.artist
FORMAT=args.format
OVERWRITE=args.overwrite

if ":" in args.day:
    control = args.day.split(":")
    if   len(control) == 2:
        if control[0] == '':
            DAYS=range(1,int(control[1]))
        elif control[-1] == '':
            DAYS=range(int(control[0]), 31)
        else:
            DAYS=range(int(control[0]), int(control[1]))
    elif len(control) == 3:
        DAYS=range(int(control[0]), int(control[1]), int(control[2]))
    else:
        exit()
elif ',' in args.day:
    DAYS = [int(d) for d in args.day.split(",")]
else:
    DAYS = [int(args.day)]

vprint(f"{YEAR=}")
vprint(f"{DAYS=}")

vprint(f"{ALBUM=}")
vprint(f"{ARTIST=}")
vprint(f"{FORMAT=}")
vprint(f"{OVERWRITE=}")

def url(november):
    # This is the URL that you get if you look at "PAST DATES"
    # on https://www.dead.net/30daysofdead
    return f"https://www.dead.net/30daysofdead/nov-{november:02d}-{YEAR}"

def parse(content):
    # With the page content in hand we need to extract the relevant information.

    # Most importantly, where does the mp3 live?
    mp3 = re.findall(rb'http[s]?://d2cstorage-a.akamaihd.net/.*\.mp3', content)
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
    vprint(f"Day {DAY:02} URL: {URL}")
    page = requests.get(URL)
    content = page.content

    try:
        remote, title, location, date = parse(content)
    except:
        print(f"Day {DAY:02} failed to parse.")
        continue

    SONG=FORMAT.format(**{
        'DAY': DAY, 
        'ALBUM': ALBUM, 
        'ARTIST': ARTIST,
        'TITLE': title,
        'DATE': date,
        'LOCATION': location
        })
    print(f"Day {DAY:02}: {SONG}")

    file = Path(Path(remote).name)# Figure out where to store it.

    if file.is_file() and (not OVERWRITE):
        print(f"Day {DAY:02}: file {file.name} already exists.  Pass --overwrite to re-download and overwrite.")
        continue
    else:
        print(f"Day {DAY:02}: file {file.name}")

    try:
        # Download the remote file.
        download = requests.get(remote) # Get it from afar.
        song = open(file.name, 'wb')         # Prepare to write it in binary,
        song.write(download.content)    # dump it to disk,
        song.close()                    # and save.
    except:
        print(f"Day {DAY:02} failed to download.")

    try:
        # Unfortunately, the ID3 tag is essentially empty.
        # So, use an ID3 library to add some of the data we parsed.

        mp3=MP3File(file.name)
        mp3.set_version(VERSION_BOTH)
        mp3.artist=ARTIST
        mp3.album=ALBUM
        mp3.song=SONG
        mp3.year=date.split("-")[0]     # the year of recording, not THIS year!
        mp3.track=str(DAY)              # which day of THIS NOVEMBER was the song available?
        mp3.url=URL
        mp3.save()
    except:
        print(f"Day {DAY:02} failed to tag, but file {file.name} exists.")

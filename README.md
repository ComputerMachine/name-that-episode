# Name that episode
Star trek trivia web server. Guess the name of an episode by listening to a short audio clip. Server powered by Pyramid, and made possible by data collected from Chakoteya.net and Trekcore.com.

To generate your own audio clips, you will need to have episodes downloaded onto your machine. This package has 3 sample files per episode included for The Next Generation only.

## Installing pyramid webserver
* Setup a [virtualenv](https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/install.html)
* Install project: `env/bin/pip install -e ".[testing]"`

## Setup PostgreSQL
Update `sql.cfg`, run `db_setup.py`

## How to generate episode samples
You'll need to have an entire series downloaded and your files will have to follow naming constraints.

To work without editing, all files must be named as such:

`Star.Trek.TNG.S02E02 - Where Silence Has Lease.mkv`

Season and episode numbers must be 2 digits. If this doesn't work for you then edit line 44 in `generate_clips.py`.

## Generating 10 second audio clips
Update `config.ini` with your own paths, run `get_episode_clips.py` 

## Downloading episode descriptions
Episode descriptions were not included in the transcripts downloaded from chakoteya.net, so they are scraped from trekcore. Memory Alpha also has an API which may be a more elegant solution to be incorporated in a future update.

Run `get_episode_descriptions.py`

## Generating thumbnails for your samples
Run `get_episode_thumbnails.py`

If the thumbnails folder doesn't exist inside the scripts directory, simply copy, paste and rename the sample folder and delete all .ogg files in those directories.

Once thumbnails are generated for your specific samples, drop them into the static folder so they can be accessed by Pyramid.
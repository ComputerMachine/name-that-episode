

## How to use
Make your way into the webserver folder,
* Setup your [virtualenv](https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/install.html)
* Install the project in editable mode with its testing requirements

`env/bin/pip install -e ".[testing]"`

## How to generate clips
You'll need to have an entire series downloaded and your files will have to follow naming constraints.

To work without editing, all files must be named as such:

`Star.Trek.TNG.S02E02 - Where Silence Has Lease.mkv`

Season and episode numbers must be 2 digits. If this doesn't work for you then edit line 44 in `generate_clips.py`.


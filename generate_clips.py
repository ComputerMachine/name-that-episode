import os
import subprocess
import datetime
import random
import json

import sr

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

global leopard_

def get_episode_data(series):
    """Return season number, episode number, title and the path to all the episodes in a specified series."""
    if series == "tng":
        series_path = "/media/tazg/Storage/movies/star trek/tng"
    elif series == "ds9":
        series_path = "/media/tazg/Storage/movies/star trek/ds9"
    elif series == "voy":
        series_path = "/media/tazg/Storage/movies/star trek/voy"
    elif series == "tos":
        series_path = "/media/tazg/Storage/movies/star trek/tos"
    elif series == "ent":
        series_path = "/media/tazg/Storage/movies/star trek/ent"

    episode_paths = []

    for subdir, dirs, files in os.walk(series_path):
        for file in files:
            episode_paths.append(os.path.join(subdir, file))

    for episode_path in episode_paths:
        if episode_path.endswith(".mkv"):
            episode, name_ = episode_path.split("Star.Trek.TNG.")[1].split(" - ")
            name = name_.split(".mkv")[0]
            try:
                season, episode = episode.split("E")
                season = season.split("S")[1] # Remove letters from all season variables
            except ValueError:
                # Too many values to unpack, it's a 2 part episode 
                # (Star.Trek.TNG.S01E01E02 - Encounter at Farpoint.mkv) instead of:
                # (Star.Trek.TNG.S02E02 - Where Silence Has Lease.mkv)
                data = episode.split("E") # ex: ['S01', '01', '02']
                season = data[0].split("S")[1]
                episode = "{}&{}".format(*data[1:])

            yield dict(
                season=season,
                episode=episode,
                name=name,
                path=episode_path
            )

def create_sample(episode):
    """"""
    dirpath = os.getcwd() + "/samples/s{season}/{n}".format(
        season=episode.get("season"),
        n=episode.get("episode")
    )

    try:
        os.makedirs(dirpath) # make the dir if it doesnt exist already
    except FileExistsError:
        pass

    # create 3 different clips for each episode

    for x in range(1, 4):
        sample_path = "{episode_folder_path}/{x}.ogg".format(episode_folder_path=dirpath, x=x)

        if os.path.exists(sample_path):
            print (bcolors.WARNING + "Sample file already exists... Delete it manually if you want to create a new sample." + bcolors.ENDC)
            continue

        sample_not_guessable = True

        while sample_not_guessable:
            start_time = datetime.timedelta(
                minutes=random.randrange(6,37),
                seconds=random.randrange(0,60)
            )
            end_time = start_time + datetime.timedelta(seconds=10)
            print ("Start: {} | Stop: {}".format(start_time, end_time))

            ffmpeg_process = subprocess.Popen([
                "ffmpeg",
                "-hide_banner",
                "-loglevel", "error",
                "-n",                   
                "-i", episode.get("path"), # input file path
                "-ss", str(start_time), # start cut time
                "-to", str(end_time), # end cut time
                "-c:a", "libvorbis", # encoding
                "-b:a", "96k", # sample bitrate
                "-vn", # extract audio only
                sample_path
            ])

            ffmpeg_process.wait()

            # Check if the sample obtained is guessable
            transcript, words = sr.leopard.process_file(sample_path)
            if is_guessable(transcript):
                print (bcolors.OKGREEN + "Successfully created sample {} for Season {} Episode {} - {}".format(
                    x,
                    episode.get("season"),
                    episode.get("episode"),
                    episode.get("name")
                    ) + bcolors.ENDC
                )
                sample_not_guessable = False
            else:
                os.remove(sample_path)

    answer = {
        "Season": episode.get("season"),
        "Episode": episode.get("episode"),
        "Name": episode.get("name"),
        "Samples": [
            "{}\\1.ogg".format(dirpath),
            "{}\\2.ogg".format(dirpath),
            "{}\\3.ogg".format(dirpath),
        ]
    }

    return answer

def is_guessable(text):
    """Return a boolean whether the text provides at the very least some information to make it guessable."""
    data = sr.pos_tag(sr.word_tokenize(text))
    # jj - adjectives, nn - nouns
    adjectives = 0
    nouns = 0

    for word in data:
        if word[1] == "JJ":
            adjectives += 1
        elif word[1] == "NN":
            nouns += 1

    # Arbitrarly declare that the presence of 5 adjectives and nouns combined is a good enough sample to be guessed without going ham into speech processing
    if adjectives + nouns >= 5:
        #print ("Provided sample has potential for being guessed... Continuing...")
        return True
    else:
        #print ("Provided sample is unlikely to be guessed.")
        return False

if __name__ == "__main__":
    data = get_episode_data("tng")
    episodes = [e for e in data]
    answers = []

    #leopard = create(access_key="nk9fLX10chKKm7GoLD5LXM9C/R+Wluajw4p7mgmSA3gCEL11u6DVVA==")

    for episode in episodes:
        print ("---------------------------------------------------------------")
        print ("Now working on episode: ", episode.get("name"))
        data = create_sample(episode)
        answers.append(data)

    with open("answers.json", "w") as f:
        json.dump(answers, f)

    print ("ALL DONE")
import os
import subprocess
import datetime
import random


def get_episodes():
    tng_path = "G:\movies\star_trek_tng"
    episodes = []
    for subdir, dirs, files in os.walk(tng_path):
        for file in files:
            episodes.append(os.path.join(subdir, file))
    for ep in episodes:
        if ep.endswith(".mkv"):
            e, n = ep.split("Star.Trek.TNG.")[1].split(" - ")
            season = None
            try:
                s, episode = e.split("E")
            except ValueError:
                # too many values to unpack, it's a 2 part episode
                s = e.split("E")
                season = s[0].split("S")[1]
                episode = "{}&{}".format(*s[1:])

            name = n.split(".mkv")[0]
            if not season:
                season = s.split("S")[1]
            path = ep
            yield dict(
                season=season, 
                episode=episode, 
                name=name, 
                path=path
            )
            #print ("Season: {}, Episode: {}, Name: {}".format(season, episode, name))

def create_sample(episode):
    dirpath = os.getcwd() + "\samples\season_{season}\episode_{episode}".format(
        season=episode.get("season"),
        episode=episode.get("episode")
    )

    try:
        os.makedirs(dirpath) # make the dir if it doesnt exist already
    except FileExistsError:
        pass

    print ("---------------------------------------------------------------")

    # create 3 different clips for each episode
    for x in range(1, 4):
        print ("Creating sample {} for Season {} Episode {} - {}".format(
            x,
            episode.get("season"),
            episode.get("episode"),
            episode.get("name")
            )
        )

        start_time = datetime.timedelta(
            minutes=random.randrange(6,37),
            seconds=random.randrange(0,60)
        )
        end_time = start_time + datetime.timedelta(seconds=10)

        print ("Start: {} | Stop: {}".format(start_time, end_time))

        subprocess.Popen([
            "ffmpeg.exe",
            "-n",                   
            "-i", episode.get("path"),                                # input file path
            "-ss", str(start_time),                                   # start cut time
            "-to", str(end_time),                                     # end cut time
            "-c:a", "libvorbis",                                      # encoding
            "-b:a", "96k",                                            # sample bitrate
            "-vn",                                                    # extract audio only
            "{episode_path}\\{x}.ogg".format(
                episode_path=dirpath,
                x=x
            )
        ])

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

    #answer = {
    #    "Season_{}".format(episode.get("season")): {
    #    "Episode_{}".format(episode.get("episode")): {
    #        "Name": episode.get("name"),
    #        "Samples": [
    #            "{}\\1.ogg".format(dirpath),
    #            "{}\\2.ogg".format(dirpath),
    #            "{}\\3.ogg".format(dirpath),
    #        ]
    #    }
    #    }
    #}

    return answer

if __name__ == "__main__":
    episodes = get_episodes()
    eps = []
    for e in episodes:
        eps.append(e)

    answers = []

    for episode in eps:
        data = create_sample(episode)
        answers.append(data)

    import json

    with open("answers.json", "w") as f:
        json.dump(answers, f)

    """
    for season in eps:
        for episode in season:
            print ("-------------------------- ", episode)
            print ("CREATING SAMPLE FOR SEASON {} EPISODE {}".format(
                episode.get("season"),
                episode.get("episode")
            ))
            data = create_sample(episode)
            answers.append(data)

            print (answers)
            break

    # Create answer key


"""
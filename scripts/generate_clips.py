import os
import subprocess
import datetime
import random
import json
import sr
import configparser


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

config = configparser.ConfigParser()
config.read("config.ini")

def get_episode_data(series):
    """Return season number, episode number, title and the path to all the episodes in a specified series."""
    if series == "tng":
        series_path = config["PATHS"]["tng"]
    elif series == "ds9":
        series_path = config["PATHS"]["ds9"]
    elif series == "voy":
        series_path = config["PATHS"]["voy"]
    elif series == "tos":
        series_path = config["PATHS"]["tos"]
    elif series == "ent":
        series_path = config["PATHS"]["ent"]

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
    tmp_name = random.randrange(1000000,100000000000)
    sample = {}
    dir_path = "{path}/samples/s{season}/{n}".format(
        path=os.getcwd(),
        season=episode.get("season"),
        n=episode.get("episode")
    )
    try:
        os.makedirs(dir_path)
    except FileExistsError:
        # Episode directory already exists
        pass

    tmp_path = os.getcwd() + "/samples/tmp/"
    sample_path = os.getcwd() + "/samples/tmp/{name}.ogg".format(name=tmp_name)
    try:
        os.makedirs(tmp_path)
    except FileExistsError:
        # Episode directory already exists
        pass

    sample_not_guessable = True

    while sample_not_guessable:
        start_time = datetime.timedelta(
            minutes=random.randrange(0,42),
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
        if sr.is_guessable(transcript):
            print (bcolors.OKGREEN + "Successfully created sample for Season {} Episode {} - {}".format(
                episode.get("season"),
                episode.get("episode"),
                episode.get("name")
                ) + bcolors.ENDC
            )
            sample_not_guessable = False
            sample_fn = "{}.ogg".format(tmp_name)
            #sample_file_name = "s{}/{}/{name}.ogg".format(episode.get("season"), episode.get("episode"), name=tmp_name)
            sample[sample_fn] = [transcript, start_time]
        else:
            os.remove(sample_path)

    # only returns an answer dict if all samples have been created
    return {
        "Season": episode.get("season"),
        "Episode": episode.get("episode"),
        "Name": episode.get("name"),
        "Samples": sample
    }
    


def create_sample_trio(episode):
    """Create an audio sample, save it and return the answer."""
    dirpath = os.getcwd() + "/samples/s{season}/{n}".format(
        season=episode.get("season"),
        n=episode.get("episode")
    )

    try:
        os.makedirs(dirpath) # make the dir if it doesnt exist already
    except FileExistsError:
        pass

    # create 3 different clips for each episode

    samples = {}

    for x in range(1, 4):
        sample_path = "{episode_folder_path}/{x}.ogg".format(episode_folder_path=dirpath, x=x)

        if os.path.exists(sample_path):
            print (bcolors.WARNING + "Sample file {} already exists... Delete it manually if you want to create a new sample.".format(x) + bcolors.ENDC)
            if x == 3:
                break
            else:
                continue

        sample_not_guessable = True

        while sample_not_guessable:
            start_time = datetime.timedelta(
                minutes=random.randrange(0,42),
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
            if sr.is_guessable(transcript):
                print (bcolors.OKGREEN + "Successfully created sample {} for Season {} Episode {} - {}".format(
                    x,
                    episode.get("season"),
                    episode.get("episode"),
                    episode.get("name")
                    ) + bcolors.ENDC
                )
                sample_not_guessable = False
                sample_file_name = "s{}/{}/{}.ogg".format(episode.get("season"), episode.get("episode"), x)
                samples[sample_file_name] = dict(
                    transcript=transcript,
                    start=start_time
                )
                update_answer_file([{
                    "Season": episode.get("season"),
                    "Episode": episode.get("episode"),
                    "Name": episode.get("name"),
                    "Samples": samples
                }])
            else:
                os.remove(sample_path)

    # only returns an answer dict if all samples have been created
    return {
        "Season": episode.get("season"),
        "Episode": episode.get("episode"),
        "Name": episode.get("name"),
        "Samples": samples
    }

def update_answer_file(new_data):
    """Take a list of dicts of new episode data and update the answer file."""
    try:
        with open("answers.json", "r") as f:
            old_data = json.load(f)
    except FileNotFoundError:
        with open("answers.json", "w") as f:
            json.dump(new_data, f, default=str)
            return True
            
    updated_data = old_data + new_data

    # Update answers
    for index, a1 in enumerate(old_data):
        for a2 in new_data:
            if a1["Name"] == a2["Name"]:
                print ("Updating {}... ".format(a1["Name"]))
                for sample in a2["Samples"]:
                    if a1["Samples"].get(sample) == a2["Samples"].get(sample):
                        continue
                    else:
                        updated_data[index]["Samples"].update(a2["Samples"])

    with open("answers.json", "w") as f:
        json.dump(updated_data, f, default=str) #serialize timedelta into a str

    return True

def update_sample_answer(new_answers):
    with open("answers.json", "r") as f:
        data = json.load(f)
    for a, i in enumerate(data):
        if new_answers['Name'] == a['Name']:
            data[i] = new_answers # update old answers with the new ones
    with open("answers.json", "w") as f:
        json.dump(data, f)
    return True


def update_answers_path(new_path):
    """Updates the path to the samples folder."""
    with open("answers.json", "r") as f:
        data = json.load(f)
    for i, episode in enumerate(data):
        paths = []
        for x in range(3):
            season_folders = data[i]["Samples"][x].split("/samples/")[1]
            paths.append(new_path + season_folders)
        data[i]["Samples"] = paths
    with open("answers.json", "w") as f:
        json.dump(data, f)
    print (data)


if __name__ == "__main__":
    data = get_episode_data("tng")
    episodes = [e for e in data]
    answers_exist = os.path.exists("{}/answers.json".format(os.getcwd()))
    answers = []

    try:
        for episode in episodes:
            print ("Now working on episode: ", episode.get("name"))
            sample_answers = create_sample_trio(episode)
            if sample_answers.get("Samples") == {}:
                continue
            answers.append(sample_answers)
    except KeyboardInterrupt:
        print ("INTERRUPTED!")

    """if answers_exist:
        try:
            update_answer_file(answers)
        except json.decoder.JSONDecodeError:
            print ("Invalid JSON or empty answers file perhaps?")
            try_again = True
            while try_again:
                s = input("> try again? (y/n)")
                if s == "y":
                    try:
                        update_answer_file(answers)
                    except:
                        pass
                else:
                    try_again = False
        except FileNotFoundError:
            with open("answers.json", "w") as f:
                json.dump(answers, f)
    else:
        with open("answers.json", "w") as f:
            json.dump(answers, f, default=str)
    """
    print ("ALL DONE")
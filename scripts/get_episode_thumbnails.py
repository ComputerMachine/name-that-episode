import cv2
import os
import configparser
import psycopg2
import math

from get_episode_clips import get_episode_data


def get_episode_paths():
    config = configparser.ConfigParser()
    config.read("config.ini")

    series_path = config["PATHS"]["sample_folder_path_linux"]
    subdirs = []

    for subdir, dirs, files in os.walk(series_path):
        try:
            season, episode = subdir.split("/s0")[1].split("/")
            subdirs.append(dict(
                season=season,
                episode=episode,
                path=subdir
            ))
        except (IndexError, ValueError):
            # it's just the season directory
            continue

    #assert len(subdirs) == 175, "We didn't get all the episodes!"
    return subdirs

def get_sample_thumbnail(episode, sample):
    cap = cv2.VideoCapture(episode.get("path"))
    fps = cap.get(cv2.CAP_PROP_FPS)
    start_frame = fps*int(float(samples[sample]["start_time"]))
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    success, image = cap.read()

    thumbnail_path = "thumbnails/" + sample.split(".ogg")[0] + ".jpg"
    print (thumbnail_path)
    #save_to = "/".join(("s" + episode.get("season"), episode.get("episode")))

    if success:
        cv2.imwrite(thumbnail_path, image)
        return True

    return False

if __name__ == "__main__":
    config = configparser.RawConfigParser()
    config.read("../sql.cfg")
    con = psycopg2.connect(
        database=config.get("auth", "name"), 
        user=config.get("auth", "user"), 
        password=config.get("auth", "pass"), 
        port=config.get("auth", "port")
    )

    episodes = [e for e in get_episode_data("tng")]
    cursor = con.cursor()
    count = 0

    for episode in episodes:
        cursor.execute(
            "SELECT samples FROM nte_episode WHERE season = %s AND episode = %s", (
                episode.get("season"),
                episode.get("episode")
            )
        )
        samples = cursor.fetchone()[0]

        for sample in samples:
            start = int(float(samples[sample]["start_time"])) # convert str float value into float then int
            vpath = episode.get("path") # path to the original video file

            print ("Start: {}\n Path: {}\n Sample: {}".format(start, vpath, samples[sample]))
            success = get_sample_thumbnail(episode, sample)
            print (success)

    print ("All done.")
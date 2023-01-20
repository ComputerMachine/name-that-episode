import json
import os
import configparser


config = configparser.ConfigParser()
config.read("config.ini")

def test_sample_answers():
    samples_path = os.getcwd() + "/samples/"
    samples = [f for _, _2, f in os.walk(os.getcwd() + "/samples/")]
    samples_created = sum(len(f) for f in samples)

    with open("answers.json", "r") as f:
        data = json.load(f)

    answers_created = 0

    for i, episode in enumerate(data):
        for sample in episode.get("Samples"):
            answers_created += 1

    print ("{} Samples created, {} answers created".format(samples_created, answers_created))

    assert samples_created == answers_created, "The number of samples don't match the number of answers we have"


if __name__ == "__main__":
    test_sample_answers()
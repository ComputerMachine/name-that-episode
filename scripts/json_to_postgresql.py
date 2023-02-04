import psycopg2
import json


def convert_json_to_postgresql(data):
    con = psycopg2.connect(
        database="nte_db",
        user="nte_user",
        password="she sells sea shells on the sea shore"
    )

    cursor = con.cursor()

    for episode in data:
        sample = json.dumps(episode["samples"])
        print ("{}: S{} E{}".format(
            episode["title"],
            episode["season"],
            episode["episode"]
        ))
        cursor.execute("INSERT INTO nte_episode (title, season, episode, samples) VALUES (%s, %s, %s, %s)", (
            episode["title"],
            episode["season"],
            episode["episode"],
            sample
        ))

    con.commit()
    return True

if __name__ == "__main__":
    with open("episode_data.json", "r") as f:
        data = json.load(f)

    convert_json_to_postgresql(data)
    
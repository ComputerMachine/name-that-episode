import redis
import json


r = redis.Redis(password="kXD66BK1IJ75aSqVmfZkGyO6QXRf/v5maJ/awDo863CylPVtYrbzsy8HgeY4iNpADvJU0f3raP1l4xjf", decode_responses=True)

def get_redis_episode_data(sample_folder):
    samples = {}
    for i in range(1, 4): # there's 3 sample files for every episode
        sample_fn = "{}/{}.ogg".format(sample_folder, i) # ex: s06/05/1.ogg
        sample_info = r.hgetall(sample_fn)
        samples[sample_fn] = dict(
            transcript=sample_info["transcript"],
            start_time=sample_info["start_time"]
        )
    return dict(
        title=sample_info["name"],
        season=sample_info["season"],
        episode=sample_info["episode"],
        samples=samples
    )

def export_redis_db_to_json():
    counter = 0
    data = []
    samples_completed = []
    for sample_fn in r.keys("*"):
        season, episode, sample_n = sample_fn.split("/")
        sample_folder_path = "/".join([season, episode])
        if sample_folder_path in samples_completed:
            continue
        data.append(get_redis_episode_data(sample_folder_path))
        samples_completed.append(sample_folder_path)
        counter += 1

    assert counter == 175, "some samples were missed!"

    with open("redis_data.json", "w") as f:
        json.dump(data, f)
    
    return True


if __name__ == "__main__":
    pass
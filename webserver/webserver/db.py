import redis


def redis_db():
    r_ = redis.Redis(
        password="kXD66BK1IJ75aSqVmfZkGyO6QXRf/v5maJ/awDo863CylPVtYrbzsy8HgeY4iNpADvJU0f3raP1l4xjf",
        decode_responses=True
    )
    return r_
from pyramid.config import Configurator
from webserver.db import redis_db
import json
import psycopg2


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    #episode_keys = [b for b in redis_db().keys("*")]
    #episode_data = []

    #for k in episode_keys:
    #    v = redis_db().hgetall(k)
    #    episode_data.append({k:v})

    #settings["episode_data"] = json.dumps(episode_data)
    con = psycopg2.connect(
        database="nte_db",
        user="nte_user",
        password="she sells sea shells on the sea shore"
    )

    cursor = con.cursor()
    cursor.execute("SELECT * FROM nte_episode")
    data = cursor.fetchall()
    episodes = []

    for episode in data:
        episodes.append(dict(
            id=episode[0], 
            title=episode[1], 
            season=episode[2], 
            episode=episode[3], 
            samples=episode[4]
        ))

    settings["episode_data"] = json.dumps(episodes)

    with Configurator(settings=settings) as config:
        config.include('pyramid_mako')
        config.include('.routes')
        config.scan()

    return config.make_wsgi_app()
from pyramid.config import Configurator
from webserver.db import redis_db
import json


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    episode_keys = [b for b in redis_db().keys("*")]
    episode_data = []

    for k in episode_keys:
        v = redis_db().hgetall(k)
        episode_data.append({k:v})

    settings["episode_data"] = json.dumps(episode_data)

    with Configurator(settings=settings) as config:
        config.include('pyramid_mako')
        config.include('.routes')
        config.scan()

    return config.make_wsgi_app()
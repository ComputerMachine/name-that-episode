from pyramid.config import Configurator
from webserver.db import redis_db
import json


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    #episode_keys = [b for b in redis_db().keys("*")]
    episode_keys = ["s01/01&02/1.ogg", "s01/01&02/2.ogg", "s01/01&02/3.ogg"]
    episode_data = [
        {"s01/01&02/1.ogg": {
            "name": "encounter at farpoint", 
            "season": "ye", 
            "episode": "yus"}},
        {"s01/01&02/2.ogg": {"name": "encounter at farpoint", "season": "ye", "episode": "yus"}},
        {"s01/01&02/3.ogg": {"name": "encounter at farpoint", "season": "ye", "episode": "yus"}}
    ]

    #for k in episode_keys:
    #    v = redis_db().hgetall(k)
    #    episode_data.append({k:v})

    settings["episode_data"] = json.dumps(episode_data)

    with Configurator(settings=settings) as config:
        config.include('pyramid_mako')
        config.include('.routes')
        config.scan()

    return config.make_wsgi_app()
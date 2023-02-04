import json
import psycopg2
import configparser

from pyramid.config import Configurator
from webserver.db import redis_db


def episode_info(episode):
    keys = (
        "id", 
        "flagged", 
        "flagged_reason", 
        "title", 
        "prod_code", 
        "star_date", 
        "air_date", 
        "description", 
        "season", 
        "episode", 
        "samples"
    )
    keys_values = zip(keys, episode)
    return dict(keys_values)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = configparser.RawConfigParser()
    config.read("../sql.cfg")
    con = psycopg2.connect(
        database=config.get("auth", "name"), user=config.get("auth", "user"), 
        password=config.get("auth", "pass"), port=config.get("auth", "port")
    )

    cursor = con.cursor()
    cursor.execute("SELECT * FROM nte_episode")
    data = cursor.fetchall()
    episodes = list(map(episode_info, data))
    settings["episode_data"] = json.dumps(episodes, default=str)

    with Configurator(settings=settings) as config:
        config.include('pyramid_mako')
        config.include('.routes')
        config.scan()

    return config.make_wsgi_app()
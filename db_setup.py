import psycopg2
import configparser
import json

from scripts.redis_to_json import insert_json_into_postgresql


def write_sql_config(dbname, dbuser, dbpass, dbport):
    """Write the database configuration to file sql.conf."""
    config = configparser.RawConfigParser()
    config.add_section("auth")
    config.set("auth", "name", dbname)
    config.set("auth", "user", dbuser)
    config.set("auth", "pass", dbpass)
    config.set("auth", "port", dbport)
    with open("sql.cfg", "w") as configfile:
        config.write(configfile)

def database_setup():
    """Setup the database."""
    tables = [
        "CREATE TABLE IF NOT EXISTS nte_episode ( id SERIAL NOT NULL PRIMARY KEY, flagged BOOLEAN DEFAULT false, flagged_reason VARCHAR(1024), title VARCHAR(256), production_code VARCHAR(16), star_date VARCHAR(32), air_date DATE, description VARCHAR(10240), season VARCHAR(16), episode VARCHAR(16), samples JSON NOT NULL )"]
    config = configparser.RawConfigParser()
    config.read("sql.cfg")
    try:
        con = psycopg2.connect(
            database=config.get("auth", "name"), 
            user=config.get("auth", "user"), 
            password=config.get("auth", "pass"), 
            port=config.get("auth", "port")
        )
    except Exception as e:
        raise Exception(e)
        
    for t in tables:
        cursor = con.cursor()
        cursor.execute(t)
    
    con.commit()
    return True

if __name__ == "__main__":
    database_setup()

    with open("episode_data.json", "r") as f:
        data = json.load(f)
    
    insert_json_into_postgresql(data)
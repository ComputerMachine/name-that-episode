import urllib.request
import os
import json
import psycopg2
import configparser

from bs4 import BeautifulSoup, SoupStrainer


def get_tng_episode_hrefs():
    """Return a list of dicts containing information about each episode."""
    url = "https://tng.trekcore.com/episodes/index.html"
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as req_data:
        data = req_data.read()

    soup = BeautifulSoup(data, "html.parser")
    episode_tables = soup.body.table.find_all(class_="sortable")

    for etable in episode_tables:
        ids = etable.find_all(class_='col1')
        hrefs = etable.find_all("a")
        titles = etable.find_all(class_='col2')
        prod_codes = etable.find_all(class_='col3')
        air_dates = etable.find_all(class_='col4')
        star_dates = etable.find_all(class_='col5')

        for y, tag in enumerate(ids):
            id = ids[y].text # season x episode, 4x20
            episode_url = hrefs[y]["href"]
            episode = dict(
                id=id,
                season="0"+id.split("x")[0],
                episode=id.split("x")[1],
                href=episode_url,
                title=" ".join(titles[y].text.split()),
                prod_code=prod_codes[y].text,
                air_date=air_dates[y].text,
                star_date=star_dates[y].text,
                summary=get_summary(episode_url)
            )
            yield episode

def get_summary(episode_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }
    req = urllib.request.Request(episode_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as req_data:
            data = req_data.read()
    except urllib.error.HTTPError:
        print ("No dice... ", episode_url)
        return None
    soup = BeautifulSoup(data, "html.parser")
    summary = " ".join(soup.table.find(id="table3").text.split())
    return summary

def get_synopsis_url(episode_url):
    """Find the URL that contains the synopsis and return it."""
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }
    req = urllib.request.Request(episode_url, headers=headers)
    with urllib.request.urlopen(req) as req_data:
        data = req_data.read()
    soup = BeautifulSoup(data, "html.parser")
    synopsis_url = soup.body.find(id="table4").find("a", text="SYNOPSIS")["href"]
    if synopsis_url[0:4] != "http":
        synopsis_url = episode_url.split("index.html")[0] + synopsis_url
    return synopsis_url

def get_synopsis(synopsis_url):
    """Find and return the synopsis from the synopsis url."""
    if synopsis_url is None:
        return False
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }
    req = urllib.request.Request(synopsis_url, headers=headers)
    with urllib.request.urlopen(req) as req_data:
        data = req_data.read()
    soup = BeautifulSoup(data, "html.parser")
    # encounter at farpoint workss with this
    #syn_block = soup.find("b", text="OFFICIAL SYNOPSIS").parent.parent
    #syn_block.b.decompose() # remove some unwanted tags
    #syn_block.span.decompose() # remove some unwanted tags

    # this works with all other transcripts
    syn_block = soup.find("b", text="OFFICIAL SYNOPSIS").parent.parent.next_sibling

    # split the synopsis block at double new lines, then remove single new lines and extra spaces with split
    synopsis = [" ".join(p.split()) for p in syn_block.text.split("\n\n") if p != ""]
    return synopsis

def insert_summary_into_postgresql():
    """Read episode descriptions from JSON file and insert them into the PostgreSQL database."""
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

    config = configparser.RawConfigParser()
    config.read("../sql.cfg")
    con = psycopg2.connect(
        database=config.get("auth", "name"), 
        user=config.get("auth", "user"), 
        password=config.get("auth", "pass"), 
        port=config.get("auth", "port")
    )

    with open("episode_descriptions.json", "r") as f:
        data = json.load(f)

    cursor = con.cursor()
    cursor.execute("SELECT * FROM nte_episode")
    psql_episodes = map(episode_info, cursor.fetchall())

    for psql_episode in psql_episodes:
        for trekcore_episode in data:
            if trekcore_episode.get("season") == psql_episode.get("season") and trekcore_episode.get("episode") == psql_episode.get("episode"):
                cursor.execute(
                    "UPDATE nte_episode SET production_code = %s, star_date = %s, air_date = %s, description = %s WHERE season = %s AND episode = %s", (
                        trekcore_episode.get("prod_code"),
                        trekcore_episode.get("star_date"),
                        trekcore_episode.get("air_date"),
                        trekcore_episode.get("summary"),
                        psql_episode.get("season"),
                        psql_episode.get("episode")
                    ))
                print ("{} description added successfully...".format(trekcore_episode.get("title")))
    con.commit()
    return True


if __name__ == "__main__":
    insert_summary_into_postgresql()
    #episodes_urls = get_tng_episode_hrefs() # get links to all episode pages
    #for episode_url in episodes_urls:
    #    syn_url = get_synopsis_url(episode_url.get("href"))

    #download_episodes("tng")
    #download_episodes("ds9")
    #download_episodes("voy")
    #download_episodes("ent")
    #download_episodes("tos") # TAS links are posted on TOS episodes page
    print ("All done.")
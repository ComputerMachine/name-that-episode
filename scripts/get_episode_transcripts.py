import urllib.request
import os
import json

from bs4 import BeautifulSoup, SoupStrainer

def get_all_episodes(series):
    if series == "tng":
        url = "http://www.chakoteya.net/NextGen/episodes.htm"
    elif series == "ds9":
        url = "http://www.chakoteya.net/DS9/episodes.htm"
    elif series == "voy":
        url = "http://www.chakoteya.net/Voyager/episode_listing.htm"
    elif series == "tos":
        url = "http://www.chakoteya.net/StarTrek/episodes.htm"
    elif series == "ent":
        url = "http://www.chakoteya.net/Enterprise/episodes.htm"

    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")

    seasons = []
    season_headers = soup.find_all("h2")

    # enterprise series: there's an unrelated table just after the first h2 element, so skip the first result
    if series == "ent":
        season_tables = [h2.find_next("table") for h2 in season_headers[1:]]
    else:
        season_tables = [h2.find_next("table") for h2 in season_headers]

    for x, table in enumerate(season_tables, 1):
        episode_counter = 1
        episodes = []

        # skip the first row, that's just a legend
        for row in table.find_all("tr")[1:]:
            col = row.find_all("td")
            
            result = dict(
                season=x,
                episode=episode_counter,
                href=col[0].find("a").get("href"),
                name=col[0].text.strip().replace("\r", " ").replace("\n", ""),
                production=col[1].text.strip().replace("\r", " ").replace("\n", ""),
                date=col[2].text.strip().replace("\r", " ").replace("\n", "")
            )

            # this transcript file accounts for 2 episodes
            if "&" in result.get("production") or "+" in result.get("production"):
                episode_counter += 1 # skip an episode in the counter
            
            episodes.append(result)
            episode_counter += 1
        
        seasons.append(episodes)

    return seasons

def download_episodes(series):
    transcript_folder = os.getcwd() + "/transcripts"

    if series == "tng":
        url = "http://www.chakoteya.net/NextGen/"
        series_folder = "/tng/"
    elif series == "ds9":
        url = "http://www.chakoteya.net/DS9/"
        series_folder = "/ds9/"
    elif series == "voy":
        url = "http://www.chakoteya.net/Voyager/"
        series_folder = "/voy/"
    elif series == "tos":
        url = "http://www.chakoteya.net/StarTrek/"
        series_folder = "/tos/"
    elif series == "ent":
        url = "http://www.chakoteya.net/Enterprise/"
        series_folder = "/ent/"

    #s#easons = get_all_episodes(series)

    if not os.path.exists(transcript_folder + series_folder):
        os.makedirs(transcript_folder + series_folder)
        print ("Creating {} directory...".format(series))
    
    for season in seasons:
        for episode in season:
            transcript_filename = episode.get("href")
            if "TAS" in transcript_filename:
                series_folder = "/tas/"
                series = "tas"
                if not os.path.exists(transcript_folder + series_folder):
                    print ("Creating {} directory...".format(series))
                    os.makedirs(transcript_folder + series_folder)

            if "#" in transcript_filename:
                print ("Anchor in URL detected, skipping since we've already downloaded the appropiate transcript.")
                continue

            if os.path.exists(transcript_folder + series_folder + transcript_filename):
                print ("Transcript file already exists for {}: {} ... Skipping".format(series_folder, transcript_filename))
                continue

            print ("Downloading {} transcript from {}".format(series, url + transcript_filename))

            new_file_path = transcript_folder + series_folder + transcript_filename

            response = urllib.request.urlopen(url + transcript_filename)
            html = response.read()
            soup = BeautifulSoup(html, "html.parser")

            # insert some information here that isn't available directly in the transcript
            tags = [
                soup.new_tag("span", id="season", value=episode.get("season")),
                soup.new_tag("span", id="episode", value=episode.get("episode")),
                soup.new_tag("span", id="name", value=episode.get("name")),
                soup.new_tag("span", id="airdate", value=episode.get("date")),
                soup.new_tag("span", id="production", value=episode.get("production"))
            ]

            for tag in tags:
                soup.html.append(tag)

            with open(new_file_path, "w", encoding="utf-8") as f:
                f.write(str(soup))
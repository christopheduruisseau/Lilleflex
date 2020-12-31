import requests
import json

# from django.utils import six
import os, time
from django.conf import settings
from datetime import datetime

# if six.PY2:
# from urllib import quote
# else:
from urllib.parse import quote


def get_new_token():
    apikey = "7188264b"
    # username = 'gupta.chetan1997'
    # userkey = '217AEB727734271F'
    # payload = json.dumps({'apikey':apikey,'username':username,'userkey':userkey})
    # url = 'https://api.thetvdb.com/login'
    # headers={"Content-Type":"application/json","Accept": "application/json", "User-agent": "Mozilla/5.0"}
    # r = requests.post(url, data=payload, headers=headers)
    return apikey


def get_token():
    try:
        new_token = get_new_token()
    except:
        print("API MUST BE DOWN")
        return None
    return new_token


def search_series_list(series_name):
    token = get_token()
    # headers={"Content-Type":"application/json","Accept": "application/json",'Authorization' : 'Bearer '+token, "User-agent": "Mozilla/5.0"}
    url = "https://omdbapi.com/?i=tt00654661&apikey=" + token
    try:
        show_info = {}
        r = requests.get(url)
        json_r = json.loads(r.text)
        show_info["Title"] = "tt00654661"
        show_info["seriesName"] = json_r["Title"]
        show_info["banner"] = json_r["Poster"]
        show_info["status"] = json_r["Response"]
        show_info["firstAired"] = json_r["Released"]
        # json_r = requests.get(url, headers=headers).json()
        # return json_r['data'][:5]
        return show_info
    except:
        return None


def get_series_with_id(imdbID):
    token = get_token()
    # headers={"Content-Type":"application/json","Accept": "application/json",'Authorization' : 'Bearer '+token, "User-agent": "Mozilla/5.0"}
    url = "https://omdbapi.com/?i='" + imdbID + "&apikey=" + token
    try:
        # json_r = requests.get(url, headers=headers).json()
        # json_r = requests.get(url).json()
        # json_r = json_r['data']
        r = requests.get(url)
        json_r = json.loads(r.text)
        show_info = {}
        show_info["tvdbID"] = "tt00654661"
        show_info["seriesName"] = json_r["Title"]
        show_info["banner"] = json_r["Poster"]
        show_info["status"] = json_r["Response"]
        show_info["firstAired"] = json_r["Released"]
        show_info["overview"] = json_r["Plot"]
        show_info["imdbID"] = json_r["imdbID"]
        show_info["genre"] = json_r["Genre"]
        show_info["siteRating"] = json_r["Ratings"][0]["Value"]
        show_info["network"] = json_r["Rated"]
        return show_info
    except:
        return None


def get_season_episode_list(tvdbID, number):
    token = get_token()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer " + token,
        "User-agent": "Mozilla/5.0",
    }
    url = (
        "https://api.thetvdb.com/series/"
        + str(tvdbID)
        + "/episodes/query?airedSeason="
        + str(number)
    )
    try:
        json_r = requests.get(url, headers=headers).json()
        season_data = []
        json_r = json_r["data"]
        for episode in json_r:
            episode_data = {}
            episode_data["number"] = episode["airedEpisodeNumber"]
            episode_data["episodeName"] = episode["episodeName"]
            episode_data["firstAired"] = episode["firstAired"]
            episode_data["tvdbID"] = episode["id"]
            episode_data["overview"] = episode["overview"]
            season_data.append(episode_data)
        return season_data
    except:
        return None


def get_all_episodes(tvdbID, start_season):
    show = {}
    for i in range(start_season, 100):
        season_data = get_season_episode_list(tvdbID, i)
        if season_data:
            show["Season" + str(i)] = season_data
        else:
            break
    return show


def download_image(url, slug):
    r = requests.get(url)
    slug = slug + ".jpg"
    imageFile = open(os.path.join("media_cdn", os.path.basename(slug)), "wb")
    for chunk in r.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()
    return os.path.join("media", os.path.basename(slug))

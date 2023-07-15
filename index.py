"""Module principal """

from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS
from jikanpy import Jikan

app = Flask(__name__)
CORS(app)
jikan = Jikan()

client = MongoClient("mongodb://localhost:27017")
db = client["seriesSensei"]
collection = db["series"]


@app.route("/series/getall", methods=["GET"])
def get_all_series():
    """Function return all series"""
    series = collection.find()
    response = {}
    for series_object in series:
        for serie in series_object.keys():
            if serie != "_id":
                response[serie] = {
                    "sinopsis": series_object[serie].get("sinopsis", ""),
                    "genres": series_object[serie].get("genres", ""),
                    "url": series_object[serie].get("url", ""),
                }
    return response


@app.route("/series/extra-info", methods=["POST"])
def set_extra_info():
    """Function for set extra data"""
    print(get_anime_list())
    # search_result = jikan.search("anime", "berserk")

    for serie in get_anime_list():
        if serie != "_id":
            search_result = jikan.search("anime", serie)
            print(search_result["data"][0]["images"]["jpg"]["image_url"])
            url = search_result["data"][0]["images"]["jpg"]["image_url"]
            collection.update_one(
                {
                    f"{serie}": {"$exists": True},
                },
                {"$set": {f"{serie}.url": url}},
            )
    return {}


def get_anime_list():
    """Function return anime list in mongodb"""
    series = collection.find()
    for series_object in series:
        list_of_animes = series_object.keys()
        return list_of_animes

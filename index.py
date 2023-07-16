"""Module principal """

from flask import Flask, request
from pymongo import MongoClient
from flask_cors import CORS
from jikanpy import Jikan
import time

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
        print(series_object)
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
    series = collection.find()
    mongo_series = {}

    for series_object in series:
        mongo_series = series_object

    for serie in mongo_series.keys():
        if serie != "_id":
            if "url" in mongo_series[serie]:
                continue
            print(f"search -> {serie}")
            time.sleep(max(1 / 60, 1 / 3))  # Sleep for the max of 1/60 and 1/3 seconds

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


@app.route("/series/get-chatgpt-data", methods=["GET"])
def get_chatgpt_data():
    """Function for get data from chatgpt"""
    anime = request.args.get("anime", default=None)
    print(anime)
    return "ok"

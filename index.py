"""Module principal """

from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
                    "sinopsis": series_object[serie]["sinopsis"],
                    "genres": series_object[serie]["genres"],
                }
    return response

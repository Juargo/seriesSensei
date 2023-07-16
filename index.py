"""Module principal """

import time
import json
import openai

from flask import Flask, request, jsonify
from pymongo import MongoClient, errors
from flask_cors import CORS
from jikanpy import Jikan
import config


app = Flask(__name__)
CORS(app)
jikan = Jikan()
openai.api_key = config.API_KEY


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
    if not anime:
        return jsonify({"error": "Parámetro 'anime' no proporcionado"}), 400

    response = {}
    anime = request.args.get("anime", default=None)

    prompt = f"""
    Eres un experto crítico de anime. Conociendo el "Análisis de la historia y los personajes" y una "sinopsis" del anime de {anime}.

    Ten en cuenta la siguiente lista de generos de anime que te muestro entre triple comilla.
    \"\"\"
    {config.GENRES}
    \"\"\"

    usando los resultados que obtuviste de "Análisis de la historia y los personajes" y una "sinopsis"  Proporciona una descomposición de los géneros (lista de generos) del anime  {anime} y asigna porcentajes para cada género en función de su relevancia.
    Debes presentar todos los generos de la "lista de generos".

    Como respuesta debes entregar un JSON que cumpla con el siguiente formato que te muestro dentro de los triple comilla:

    \"\"\"
    {config.FORMAT}
    \"\"\"
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
    )

    print(response.choices[0].message["content"])
    print(response.usage)

    response_content = response.choices[0].message["content"]
    response_json = json.loads(response_content)  # Convierte la cadena a un objeto JSON

    series = collection.find()
    mongo_series = {}

    for series_object in series:
        mongo_series = series_object

    for serie in mongo_series.keys():
        if serie != anime:
            continue
        print(f"search -> {serie}")
        try:
            collection.update_one(
                {
                    f"{anime}": {"$exists": True},
                },
                {"$set": {f"{anime}.genres": response_json}},
            )
        except errors.PyMongoError as mongo_exception:
            return (
                jsonify(
                    {"error": f"Error al actualizar MongoDB: {str(mongo_exception)}"}
                ),
                500,
            )
    return jsonify({"message": "Actualización exitosa"}), 200

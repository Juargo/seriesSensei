"""Module principal """

from flask import Flask

app = Flask(__name__)


@app.route("/series/getall", methods=["GET"])
def get_all_series():
    """Function return all series"""
    return {
        "07-Ghost": {
            "sinopsis": (
                "Un joven llamado Teito es el único superviviente de su país,"
                " el cual fue destruido por el Imperio de Barsburg."
                " Ahora, Teito se encuentra en la academia militar de Barsburg,"
                " donde entabla amistad con otros estudiantes y"
                " descubre que tiene poderes sobrenaturales."
                " Así comienza su búsqueda de venganza contra el Imperio y"
                " su lucha por descubrir su verdadero destino."
            ),
            "genres": {
                "Action": "50%",
                "Adventure": "80%",
                "Drama": "90%",
                "Mystery": "60%",
                "Supernatural": "100%",
                "Fantasy": "100%",
                "Romance": "40%",
                "Slice of life": "20%",
                "Ecchi": "0%",
                "Erotica": "0%",
                "Hentai": "0%",
                "Sci-Fi": "0%",
            },
        },
        "Berserk": {
            "sinopsis": (
                "La historia se centra en Guts, un guerrero solitario cuya"
                " única misión en la vida es matar demonios llamados Apóstoles,"
                " los cuales son seres inhumanos que se alimentan de humanos."
                " Guts es un poderoso espadachín conocido como el Espadachín Negro,"
                " y su espada maldita le otorga una fuerza formidable."
                " A lo largo de la historia, Guts se enfrenta a múltiples enemigos y"
                " se ve envuelto en una lucha épica por la supervivencia y la redención."
            ),
            "genres": {
                "Action": "100%",
                "Adventure": "90%",
                "Horror": "80%",
                "Drama": "100%",
                "Supernatural": "70%",
                "Fantasy": "100%",
                "Romance": "10%",
                "Suspense": "60%",
                "Gourmet": "0%",
                "Slice of life": "10%",
                "Ecchi": "0%",
                "Erotica": "0%",
                "Hentai": "0%",
                "Sci-Fi": "0%",
            },
        },
    }

import random
from models import Posts


def obtener_posts_populares():
    # Devuelve 3 random posts populares para el main.
    indexes = range(7)
    random.shuffle(indexes)
    posts_populares = []
    for i in range(3):
        pp = Posts.objects.filter(es_respuesta=False, eliminado=False).order_by(
            '-votos_positivos')[indexes.pop()]
        posts_populares.append(pp)

    return posts_populares

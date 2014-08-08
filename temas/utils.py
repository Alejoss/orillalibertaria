import random
from models import Posts


def obtener_posts_populares():
    # Devuelve 3 random posts populares para el main.
    pp_obj = Posts.objects.filter(es_respuesta=False, eliminado=False).order_by('-votos_positivos')[:7]
    posts_populares = random.sample(pp_obj, 3)
    return posts_populares

import random
from models import Posts
from videos.models import Videos


def obtener_posts_populares(numero):
    # Devuelve x random posts populares.
    query_cantidad = numero+2
    pp_obj = Posts.objects.filter(es_respuesta=False, eliminado=False).order_by('-votos_positivos')[:query_cantidad]
    posts_populares = random.sample(pp_obj, numero)
    return posts_populares


def obtener_videos_populares(numero):
	# Devuelve x random videos populares.
	query_cantidad = numero+2
	vp_obj = Videos.objects.filter(eliminado=False, es_youtube=True).order_by('-favoritos_recibidos')[:query_cantidad]
	videos_populares = random.sample(vp_obj, numero)
	return videos_populares

import random
from models import Posts
from videos.models import Videos


# Main, Login
def obtener_posts_populares(numero):
    # Devuelve x random posts populares, sacados de una lista de len numero(arg)+numero extra
    numero_extra = 2
    query_cantidad = numero+numero_extra
    pp_obj = Posts.objects.filter(es_respuesta=False, eliminado=False).order_by('-votos_positivos')[:query_cantidad]
    posts_populares = random.sample(pp_obj, numero)
    return posts_populares


# Main
def obtener_videos_populares(numero):
	# Devuelve x random videos populares
	query_cantidad = numero*2
	vp_obj = Videos.objects.filter(eliminado=False, es_youtube=True).order_by('-favoritos_recibidos')[:query_cantidad]
	videos_populares = random.sample(vp_obj, numero)
	return videos_populares

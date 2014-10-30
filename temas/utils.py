import random
from models import Posts
from videos.models import Videos


# Main, Login
def obtener_posts_recientes(numero):
    # Devuelve x random posts populares, sacados de una lista de len numero(arg)+numero extra
    numero_extra = 2
    query_cantidad = numero+numero_extra
    pr_obj = Posts.objects.filter(es_respuesta=False, eliminado=False).order_by('-id')[:query_cantidad]
    posts_recientes = random.sample(pr_obj, numero)
    return posts_recientes


# Main
def obtener_videos_populares(numero):
	# Devuelve x random videos populares
	query_cantidad = numero*2
	vr_obj = Videos.objects.filter(eliminado=False, es_youtube=True).order_by('-id')[:query_cantidad]
	videos_recientes = random.sample(vr_obj, numero)
	return videos_recientes

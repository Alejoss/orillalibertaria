import random
import pytz

from datetime import datetime

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


# Sumar Post, Voteup
def popularidad_actividad_tema(tema, cambio_popularidad):
    cinco_posts = Posts.objects.filter(
                tema=tema, eliminado=False).order_by('-fecha')[:5]

    cinco_videos = Videos.objects.filter(tema=tema, eliminado=False).order_by('-fecha')[:5]
    n_actividad = 0
    hoy = (datetime.today()).replace(tzinfo=pytz.UTC)

    for post in cinco_posts:
        timedelta = hoy-post.fecha
        if timedelta.days > 30 and timedelta.days < 60:
            n_actividad += 1
        elif timedelta.days > 20:
            n_actividad += 3
        elif timedelta.days > 10:
            n_actividad += 5
        elif timedelta.days > 5:
            n_actividad += 7
        elif timedelta.days > 3:
            n_actividad += 9
        elif timedelta.days > 1:
            n_actividad += 11
        elif timedelta.days == 0:
            n_actividad += 13

    for video in cinco_videos:
        timedelta = hoy-video.fecha
        if timedelta.days > 30 and timedelta.days < 60:
            n_actividad += 1
        elif timedelta.days > 20:
            n_actividad += 3
        elif timedelta.days > 10:
            n_actividad += 5
        elif timedelta.days > 5:
            n_actividad += 7
        elif timedelta.days > 3:
            n_actividad += 9
        elif timedelta.days > 1:
            n_actividad += 11
        elif timedelta.days == 0:
            n_actividad += 13

    tema.nivel_actividad = n_actividad
    if cambio_popularidad == "positivo":
        tema.nivel_popularidad += 1
        print tema.nivel_popularidad
    elif cambio_popularidad == "negativo":
        tema.nivel_popularidad -= 1
    tema.save()

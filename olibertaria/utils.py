# -*- coding: utf-8 -*-

from temas.models import Votos, Posts
from notificaciones.models import Notificacion
from videos.models import Videos
from citas.models import Cita
from imagenes.models import Imagen


def obtener_num_notificaciones(perfil):
    num_notificaciones = Notificacion.objects.filter(target=perfil, leida=False).count()
    return num_notificaciones


def obtener_string_fav_voteup(numero):
    # Recibe un numero, devuelve un string que se utilizara en la notificacion.
    string = "diez"
    if numero > 90:
        string = "cien"
    elif numero > 990:
        string = "mil"
    return string


def obtener_args_notificacion(notificacion):
    tipo_objeto = notificacion.tipo_objeto
    tipo_notificacion = notificacion.tipo_notificacion
    string_votos = None

    if tipo_objeto == "post":
        objeto = Posts.objects.get(id=notificacion.objeto_id)
        if tipo_notificacion == "num":
            string_votos = obtener_string_fav_voteup(objeto.votos_total)

    elif tipo_objeto == "video":
        objeto = Videos.objects.get(id=notificacion.objeto_id)
        if tipo_notificacion == "num":
            string_votos = obtener_string_fav_voteup(objeto.favoritos_recibidos)

    elif tipo_objeto == "cita":
        objeto = Cita.objects.get(id=notificacion.objeto_id)
        if tipo_notificacion == "num":
            string_votos = obtener_string_fav_voteup(objeto.favoritos_recibidos)

    elif tipo_objeto == "imagen":
        objeto = Imagen.objects.get(id=notificacion.objeto_id)
        if tipo_notificacion == "num":
            string_votos = obtener_string_fav_voteup(objeto.favoritos_recibidos)

    notificacion_list = [notificacion, objeto]  # [notificacion, objeto, extras...]
    if string_votos is not None:
        notificacion_list.append(string_votos)
    return notificacion_list


def obtener_notificaciones(perfil):
    # Recibe un Perfil object
    notificaciones = Notificacion.objects.filter(target=perfil).order_by('-id')[:5]
    lista_de_notificaciones = []
    for notificacion in notificaciones:
        notificacion_args = obtener_args_notificacion(notificacion)
        lista_de_notificaciones.append(notificacion_args)

    return lista_de_notificaciones


def obtener_imagenes_display(numero):
    # Recibe un numero.
    # Devuelve una lista con el mismo numero de imagenes, si hay disponibles.
    numero_de_imagenes = 1
    imagenes_disponibles = Imagen.objects.filter(eliminada=False).count()
    if imagenes_disponibles < numero:
        numero_de_imagenes = imagenes_disponibles
    else:
        numero_de_imagenes = numero

    imagenes_populares = Imagen.objects.filter(eliminada=False).order_by(
        '-favoritos_recibidos')[:numero_de_imagenes]
    lista_urls = []
    for i in imagenes_populares:
        lista_urls.append(i.url)
    return lista_urls


def obtener_voted_status(post, perfil):
    # Recibe un post object y un perfil object.
    # Devuelve el voted_status (no-vote, voted-up etc.)
    voted_status = "no-vote"
    if post.creador == perfil:
        voted_status = "propio_post"
    else:
        if Votos.objects.filter(post_votado=post, usuario_votante=perfil).exists():
            voto = Votos.objects.get(post_votado=post, usuario_votante=perfil)
            if voto.tipo == 1:
                voted_status = "voted-up"
            elif voto.tipo == -1:
                voted_status = "voted-down"
            else:
                voted_status = "no-vote"

    return voted_status


def obtener_imagen_tema(tema):
    # Devuelve la imagen correspondiente al tema, si no, devuelve un default.
    imagen = "http://csunlibertarian.files.wordpress.com/2012/02/porcupine.gif"
    if len(tema.imagen) > 10:
        imagen = tema.imagen
    return imagen

# -*- coding: utf-8 -*-
import os
import re
import pytz
import random
from datetime import datetime

from django.core.exceptions import ImproperlyConfigured

from perfiles.models import Perfiles
from temas.models import Votos, Posts, Respuestas
from notificaciones.models import Notificacion
from videos.models import Videos
from citas.models import Cita
from imagenes.models import Imagen


def obtener_avatar_large(perfil):
    avatar_large = None
    if perfil.imagen_perfil is not None:
        if "facebook" in perfil.imagen_perfil:
            avatar_large = "%s?type=large" % (perfil.imagen_perfil)
        elif "twimg" in perfil.imagen_perfil:
            avatar_large = (perfil.imagen_perfil).replace("_normal", "")
        elif "google" in perfil.imagen_perfil:
            avatar_large = (perfil.imagen_perfil).replace("sz=50", "sz=400")
    else:
        avatar_large = "no tiene avatar larga, remplazar con default"

    return avatar_large


def obtener_respuestas_post(post):
    #obtiene un post object y devuelve dos respuestas para la vista previa.
    respuestas_obj = Respuestas.objects.filter(post_padre=post,
                                               post_padre__eliminado=False).order_by('-id')[:2]
    respuestas = []
    for r in respuestas_obj:
        if len(r.post_padre.texto) > 1:
            respuestas.append(r.post_respuesta)

    return respuestas


def obtener_env_secret_key():
    try:
        return os.environ["OL_SECRET_KEY"]
    except KeyError:
        error_msg = "Falta la OL_SECRET_KEY virtualenv"
        raise ImproperlyConfigured(error_msg)


def obtener_avatar(strategy, details, response, user, *args, **kwargs):
    #pipeline para python social auth. Obtiene la URL del avatar y la guarda.
    url = None
    print strategy.backend.name
    if strategy.backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
    elif strategy.backend.name == "twitter":
        if response['profile_image_url'] != '':
            url = response['profile_image_url']
    elif strategy.backend.name == "google-oauth2":
        if response['image'].get('url') is not None:
            url = response['image'].get('url')

    perfil_usuario, creado = Perfiles.objects.get_or_create(usuario=user)

    perfil_usuario.imagen_perfil = url
    perfil_usuario.save()

    return kwargs


def crear_perfil(strategy, details, response, user, *args, **kwargs):
    #pipeline para python social auth. Crea la tabla de Perfil del usuario.
    if Perfiles.objects.filter(usuario=user).exists():
        pass
    else:
        nuevo_perfil = Perfiles(usuario=user)
        nuevo_perfil.save()
    return kwargs


def crear_nickname(strategy, details, response, user, *args, **kwargs):
    #pipeline que crea un default nickname para cada usuario.
    perfil_usuario, creado = Perfiles.objects.get_or_create(usuario=user)
    if perfil_usuario.nickname is None:
        rand_num = random.randint(99)
        nickname = "%s_nick_%s" % (user.username, rand_num)
        perfil_usuario.nickname = nickname
        perfil_usuario.save()
    return kwargs


def tiempo_desde(hora_object):
    unaware = datetime.today()
    ahora = unaware.replace(tzinfo=pytz.UTC)
    dif_segundos = (ahora-hora_object).total_seconds()
    dif_minutos = dif_segundos/60
    mensaje = ""
    dif_dias = (ahora-hora_object).days
    diasdelasemana = {0: "Lunes", 1: "Martes", 2: "Miercoles", 3: "Jueves",
                      4: "Viernes", 5: "Sabado", 6: "Domingo"}
    meses = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
             7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
    if dif_dias > 1:  # braket para mas de un dia
        if dif_dias < 6:
            x = hora_object.weekday()
            dia_nombre = diasdelasemana[x]
            mensaje = "el %s" % (dia_nombre)
        elif dif_dias < 300:
            mes = meses[hora_object.month]
            mensaje = "el %s de %s" % (hora_object.day, mes)
        else:
            ano = hora_object.year
            mes = meses[hora_object.month]
            mensaje = "%s del %s" % (mes, ano)
    else:
        if dif_minutos < 60:  # braket para menos de una hora
            if dif_minutos < 30:
                if dif_minutos < 15:
                    if dif_minutos < 5:
                        mensaje = "hace unos minutos"
                    elif dif_minutos < 8 and dif_minutos > 5:
                        mensaje = "hace cinco minutos"
                    else:
                        mensaje = "hace diez minutos"
                else:
                    if dif_minutos < 19:
                        mensaje = "hace quince minutos"
                    else:
                        mensaje = "hace veinte minutos"
            else:
                if dif_minutos < 40:
                    mensaje = "hace media hora"
                else:
                    mensaje = "hace cuarenta minutos"
        else:  # braket para mas de una hora
            if dif_minutos < 180:
                if dif_minutos < 120:
                    mensaje = "hace una hora"
                else:
                    mensaje = "hace dos horas"
            else:
                if dif_minutos < 480:
                    if dif_minutos < 240:
                        mensaje = "hace tres horas"
                    elif dif_minutos < 300:
                        mensaje = "hace cuatro horas"
                    elif dif_minutos < 360:
                        mensaje = "hace cinco horas"
                    else:
                        mensaje = "hace unas horas"
                else:
                    if dif_dias == 0:
                        mensaje = "hace varias horas"
                    else:
                        mensaje = "Ayer"
    return mensaje


def bersuit_vergarabat():
    dia = datetime.today().weekday()
    if dia > 5:
        numero1 = "cinco"
        numero2 = "tres"
        respuesta = "ocho"  # opciones: 5 y 8
    elif dia < 5 and dia > 2:
        numero1 = "dos"
        numero2 = "tres"
        respuesta = "cinco"
    else:
        numero1 = "seis"
        numero2 = "dos"
        respuesta = "ocho"

    return [numero1, numero2, respuesta]


def procesar_espacios(texto):
    texto_final = re.sub('(?:\r\n|\r|\n)', '<br />', texto)
    return texto_final


def obtener_cita(cita):
    #Recibe una cita, devuelve una lista con:
    #[Cita, tiene_fuente(boolean), fuente]
    fuente = cita.fuente
    tiene_fuente = False
    if fuente is not None and len(fuente) > 0:
        tiene_fuente = True
    texto_procesado = procesar_espacios(cita.texto)
    return [cita, tiene_fuente, cita.fuente, texto_procesado]


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

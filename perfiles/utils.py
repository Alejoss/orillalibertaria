# -*- coding: utf-8 -*-

from imagenes.models import Ifavoritas
from citas.models import Cfavoritas
from videos.models import VFavoritos
from temas.models import Votos


    # Perfiles, editar perfil descripcion
def obtener_links_perfil(perfil):
    # Recibe un Perfil object
    # Devuleve una lista con los links.
    def evaluar_link(link, lista):
        # Se asegura que los links sean mas largos que 4 caracteres
        if link is not None:
            lista.append(link)

    link1 = perfil.link1
    link2 = perfil.link2
    link3 = perfil.link3
    link4 = perfil.link4
    link5 = perfil.link5
    links = []

    evaluar_link(link1, links)
    evaluar_link(link2, links)
    evaluar_link(link3, links)
    evaluar_link(link4, links)
    evaluar_link(link5, links)
    return links


def obtener_num_favoritos(perfil):
    # Recibe un perfil devuelve una lista con el numero de favoritos en este orden:
    # Imágenes, Frases, Videos, Posts
    num_imagenes_fav = Ifavoritas.objects.filter(
        perfil=perfil, eliminado=False).count()
    num_frases_fav = Cfavoritas.objects.filter(
        perfil=perfil).count()
    num_videos_fav = VFavoritos.objects.filter(
        perfil=perfil, eliminado=False).count()
    num_posts_fav = Votos.objects.filter(tipo=1,
        usuario_votante=perfil, post_votado__es_respuesta=False,
        post_votado__eliminado=False).count()

    return [num_imagenes_fav, num_frases_fav, num_videos_fav, num_posts_fav]

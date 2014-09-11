# -*- coding: utf-8 -*-
# VIEWS IMAGENES

from math import sqrt

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from endless_pagination.decorators import page_template
from models import Imagen, Ifavoritas, Idenunciadas
from forms import FormNuevaImagen
from perfiles.models import Perfiles
from notificaciones.models import Notificacion
from olibertaria.utils import bersuit_vergarabat


@page_template('index_page_imagenes.html')
def index(request, queryset, template='imagenes/galeria.html', extra_context=None):
    if request.user.is_authenticated():
        #si esta login.
        perfil_usuario = Perfiles.objects.get(usuario=request.user)
        imagenes_favoritas_obj = Ifavoritas.objects.filter(
            perfil=perfil_usuario, eliminado=False)
        imagenes_favoritas_ids = []  # contiene las ids de las imagenes fav del usuario.
        for i in imagenes_favoritas_obj:
            imagenes_favoritas_ids.append(int(i.imagen.id))

    # Filtra el Queryset y asigna la clase active para el boton del filtro.
    populares = ""
    recientes = ""
    q = ""
    if queryset == "populares":
        q = "-favoritos_recibidos"
        populares = "active"
    else:
        q = "-id"
        recientes = "active"

    imagenes = []
    imagenes_obj = Imagen.objects.filter(eliminada=False).order_by(q)
    for imagen in imagenes_obj:
        es_favorita = "no_es_favorita"
        if request.user.is_authenticated():
        #si esta login marca las favoritas del usuario.
            if imagen.id in imagenes_favoritas_ids:
                es_favorita = "es_favorita"
        imagenes.append([imagen, es_favorita])

    context = {'imagenes': imagenes, 'populares':
               populares, 'recientes': recientes}

    if extra_context is not None:  # endless pagination
        context.update(extra_context)
    return render(request, template, context)


def imagen(request, imagen_id):
    template = 'imagenes/imagen.html'
    imagen = Imagen.objects.get(id=imagen_id)

    if request.user.is_authenticated():
        #si esta login
        perfil_usuario = Perfiles.objects.get(usuario=request.user)
        # Saber si la imagen es fav del usuario visitante
        imagenes_favoritas_obj = Ifavoritas.objects.filter(
            perfil=perfil_usuario, eliminado=False)
        imagenes_favoritas = []
        for i in imagenes_favoritas_obj:
            imagenes_favoritas.append(i.imagen)
        es_favorita = "no_es_favorita"
        if imagen in imagenes_favoritas:
            es_favorita = "es_favorita"
    else:
        es_favorita = "no_es_favorita"

    context = {'imagen': imagen, 'es_favorita': es_favorita}
    return render(request, template, context)


@login_required
def nueva(request):
    template = 'imagenes/nueva.html'
    if request.method == "POST":
        form = FormNuevaImagen(request.POST)
        if form.is_valid():
            favorita = form.cleaned_data['favorita']
            url = form.cleaned_data['url']
            perfil_usuario = Perfiles.objects.get(usuario=request.user)
            nueva_imagen = Imagen(url=url, perfil=perfil_usuario)
            nueva_imagen.save()
            if favorita:
                # marco como favorita la imagen que subio.
                nueva_imagen.favoritos_recibidos += 1
                Ifavorita_obj = Ifavoritas(
                    imagen=nueva_imagen, perfil=perfil_usuario)
                Ifavorita_obj.save()
                nueva_imagen.save()

            return HttpResponseRedirect(reverse('imagenes:index', args=[u'recientes']))
        else:
            form_nueva_imagen = FormNuevaImagen()
            lista_bersuit = bersuit_vergarabat()  # honeypot
            context = {'form_nueva_imagen': form_nueva_imagen, 'lista_bersuit': lista_bersuit}
            return render(request, template, context)
    else:
        lista_bersuit = bersuit_vergarabat()
        form_nueva_imagen = FormNuevaImagen()
        context = {'form_nueva_imagen': form_nueva_imagen, 'lista_bersuit': lista_bersuit}
        return render(request, template, context)


@login_required
def marcar_favorito(request):
    if request.is_ajax():
        imagen_id = request.GET.get('imagen_id', '')
        imagen = get_object_or_404(Imagen, pk=imagen_id)
        perfil_usuario = Perfiles.objects.get(usuario=request.user)
        # revisa si ya marco como favorito a esa imagen
        fue_eliminado = False
        registro_existe = Ifavoritas.objects.filter(
            imagen=imagen, perfil=perfil_usuario).exists()
        if registro_existe:
            registro_favorito = Ifavoritas.objects.get(
                imagen=imagen, perfil=perfil_usuario)
            fue_eliminado = registro_favorito.eliminado
            if fue_eliminado:
                # el usuario había desmarcado esa imagen como favorita
                imagen.favoritos_recibidos += 1
                registro_favorito.eliminado = False
                imagen.save()
                registro_favorito.save()
                return HttpResponse("favorito marcado")
            else:
                # significa que le esta eliminando de sus favoritos
                imagen.favoritos_recibidos -= 1
                registro_favorito.eliminado = True
                # Asegurarse de que no van a haber 2 portadas.
                registro_favorito.portada = False
                imagen.save()
                registro_favorito.save()
                return HttpResponse("favorito eliminado")
        else:
            imagen.favoritos_recibidos += 1
            registro_favorito = Ifavoritas(
                imagen=imagen, perfil=perfil_usuario)
            registro_favorito.save()
            imagen.save()

        #Notificaciones de imagen
            if perfil_usuario != imagen.perfil:
                # para que no le lleguen notificaciones al usuario de sus propias acciones
                notificacion_imagen_fav = Notificacion(actor=perfil_usuario, target=imagen.perfil,
                                                       objeto_id=imagen.id, tipo_objeto="imagen",
                                                       tipo_notificacion="fav_voteup")
                notificacion_imagen_fav.save()

            if imagen.favoritos_recibidos == 100 or imagen.favoritos_recibidos == 1000:
                notificacion_imagen_num = Notificacion(target=imagen.perfil,
                                                       objeto_id=imagen.id, tipo_objeto="imagen",
                                                       tipo_notificacion="num")
                notificacion_imagen_num.save()

        return HttpResponse("favorito marcado")


@login_required
def marcar_portada_ajax(request):
    if request.is_ajax():
        imagen_id = request.GET.get('imagen_id', '')
        imagen = get_object_or_404(Imagen, id=imagen_id)
        perfil_usuario = Perfiles.objects.get(usuario=request.user)
        ya_tiene_portada = Ifavoritas.objects.filter(
            perfil=perfil_usuario, eliminado=False, portada=True).exists()
        if ya_tiene_portada:
            portada_anterior = Ifavoritas.objects.filter(
                perfil=perfil_usuario, portada=True)
            for p in portada_anterior:
                #  desmarca la portada anterior
                p.portada = False
                p.save()
            nueva_portada = Ifavoritas.objects.get(
                imagen=imagen, perfil=perfil_usuario, eliminado=False)
            nueva_portada.portada = True
            nueva_portada.save()
        else:
            registro_portada = Ifavoritas.objects.get(
                imagen=imagen, perfil=perfil_usuario, eliminado=False)
            registro_portada.portada = True
            registro_portada.save()
    return HttpResponse('nueva portada marcada')


def favoritas(request, username):
    template = 'imagenes/favoritas.html'
    user_object = get_object_or_404(User, username=username)
    perfil_usuario = Perfiles.objects.get(usuario=user_object)
    propio_usuario = False
    Ifavoritas_objects = Ifavoritas.objects.filter(perfil=perfil_usuario, eliminado=False).order_by('-fecha')
    imagenes_favoritas = []

    if request.user.is_authenticated():
        if request.user == user_object:
            propio_usuario = True  # usuario viendo sus imágenes favoritas
        if propio_usuario:
            for i in Ifavoritas_objects:
                if i.portada is True:
                    imagenes_favoritas.append([i.imagen, True])  # imagen de portada
                else:
                    imagenes_favoritas.append([i.imagen, False])
        else:
            perfil_usuario_visitante = Perfiles.objects.get(usuario=request.user)
            favoritas_usuario_visitante_obj = Ifavoritas.objects.filter(
                perfil=perfil_usuario_visitante, eliminado=False)
            favoritas_usuario_visitante = []
            for x in favoritas_usuario_visitante_obj:
                favoritas_usuario_visitante.append(x.imagen)
            for i in Ifavoritas_objects:
                # suma la clase a las favoritas del usuario visitante
                if i.imagen in favoritas_usuario_visitante:
                    imagenes_favoritas.append([i.imagen, "es_favorita"])
                else:
                    imagenes_favoritas.append([i.imagen, "no_es_favorita"])
    else:
        for i in Ifavoritas_objects:
            imagenes_favoritas.append([i.imagen, "no_es_favorita"])

    context = {
        'imagenes_favoritas': imagenes_favoritas, 'perfil_usuario': perfil_usuario,
        'propio_usuario': propio_usuario, 'username': username}
    return render(request, template, context)


@login_required
def denunciar(request):
    if request.is_ajax():
        reputacion_necesaria = 10
        imagen_id = request.GET.get('imagen_id')
        imagen = get_object_or_404(Imagen, pk=imagen_id)
        perfil_usuario = Perfiles.objects.get(usuario=request.user)
        ya_denuncio = False
        ya_denuncio = Idenunciadas.objects.filter(
            imagen=imagen, perfil=perfil_usuario).exists()
        if ya_denuncio:
            return HttpResponse('imagen ya denunciada')
        else:
            if perfil_usuario.votos_recibidos > reputacion_necesaria:
                # crea un idenunciada object si el usuario tiene la reputación
                idenunciada_object = Idenunciadas(
                    imagen=imagen, perfil=perfil_usuario)
                imagen.denunciada += 1
                idenunciada_object.save()
                if imagen.denunciada > 3:
                    imagen.eliminada = True

                    #Notificacion imagen eliminada al que subio la imagen
                    notificacion_denuncia = Notificacion(target=imagen.perfil,
                                                         objeto_id=imagen.id, tipo_objeto="imagen",
                                                         tipo_notificacion="denuncia")
                    notificacion_denuncia.save()

                imagen.save()
        return HttpResponse('imagen denunciada')


@login_required
def colaborar_organizar(request):
    template = 'imagenes/imagenes_coorg.html'
    perfil_usuario = Perfiles.objects.get(usuario=request.user)
    progress_bar = 100
    imagenes_denunciadas = []
    hay_imagenes_denunciadas = Imagen.objects.filter(
        eliminada=True, removidatotalmente=False).exists()
    if hay_imagenes_denunciadas:
        imagenes_denunciadas_obj = Imagen.objects.filter(
            eliminada=True, removidatotalmente=False)

        # diferentes tonos para la cantidad de denuncias recibidas
        success_uno = "#dff0d8"
        success_dos = "#d0e9c6"
        danger_uno = "#f2dede"
        danger_dos = "#ebcccc"
        default = "#ebebeb"

        # iconos & color de imagenes denunciadas. font awesome icons
        for i in imagenes_denunciadas_obj:
            estado = []
            color = ""
            if i.denunciada < 4:
                color = success_uno
                if i.denunciada == 3:
                    estado = ["check-circle"]
                else:
                    color = success_dos
                    estado = ["check-circle", "check-circle"]
            elif i.denunciada > 4:
                color = danger_uno
                if i.denunciada == 5:
                    estado = ["times-circle"]
                else:
                    color = danger_dos
                    estado = ["times-circle", "times-circle"]
            else:
                color = default

            # accion usuario. Revisa si el usuario ya a marcado con visto o con x
            # cambia el icono a -circle con respecto a la accion que haya hecho
            accion_usr = ["", ""]
            if Idenunciadas.objects.filter(imagen=i, perfil=perfil_usuario).exists():
                idenunciada_obj = Idenunciadas.objects.get(
                    imagen=i, perfil=perfil_usuario)
                if idenunciada_obj.eliminado is False:
                    accion_usr = ["", "-circle"]
                else:
                    accion_usr = ["-circle", ""]

            imagenes_denunciadas.append([i, color, estado, accion_usr])

        # progress bar. 100% = ya no quedan imágenes denunciadas.
        num_imagenes_eliminadas = imagenes_denunciadas_obj.count()
        max_y = num_imagenes_eliminadas * 3
        y = 0
        for x in imagenes_denunciadas_obj:
            z = 4 - x.denunciada
            y += sqrt(z * z)
        porcentaje_avanzado = float(y) / float(max_y)
        progress_bar = str(porcentaje_avanzado * 100)

    context = {
        'imagenes_denunciadas': imagenes_denunciadas, 'progress_bar': progress_bar,
        'hay_imagenes_denunciadas': hay_imagenes_denunciadas}
    return render(request, template, context)


@login_required
def marcar_visto(request, imagen_id):
    imagen = get_object_or_404(Imagen, id=imagen_id)
    perfil_usuario = Perfiles.objects.get(usuario=request.user)
    if Idenunciadas.objects.filter(imagen=imagen, perfil=perfil_usuario).exists():
        # Usuario ya marco esta imagen
        idenunciada_obj = Idenunciadas.objects.get(
            imagen=imagen, perfil=perfil_usuario)
        if idenunciada_obj.eliminado is False:
            # Usuario habia marcado con X y ahora marca con visto. (x2)
            imagen.denunciada -= 2
            idenunciada_obj.eliminado = True
            idenunciada_obj.save()
        elif idenunciada_obj.eliminado is True:
            # Usuario ya marco con visto. No pasa nada.
            pass
    else:
        imagen.denunciada -= 1  # visto reduce numero de denuncias por uno.
        idenunciada_obj = Idenunciadas(
            imagen=imagen, perfil=perfil_usuario, eliminado=True)
        idenunciada_obj.save()

    if imagen.denunciada <= 1:
        # retira la imaginadas de la pagina de eliminadas
        imagen.eliminada = False
    imagen.save()

    return redirect('imagenes:colaborar_organizar')


@login_required
def marcar_x(request, imagen_id):
    imagen = Imagen.objects.get(id=imagen_id)
    perfil_usuario = Perfiles.objects.get(usuario=request.user)
    if Idenunciadas.objects.filter(imagen=imagen, perfil=perfil_usuario).exists():
        idenunciada_obj = Idenunciadas.objects.get(
            imagen=imagen, perfil=perfil_usuario)
        if idenunciada_obj.eliminado is False:
            pass
        elif idenunciada_obj.eliminado is True:
            imagen.denunciada += 2
            idenunciada_obj.eliminado = False
            idenunciada_obj.save()
    else:
        imagen.denunciada += 1
        idenunciada_obj = Idenunciadas(imagen=imagen, perfil=perfil_usuario)
        idenunciada_obj.save()

    if imagen.denunciada >= 7:
        # remueve la imagen totalmente
        imagen.removidatotalmente = True
    imagen.save()

    return redirect('imagenes:colaborar_organizar')

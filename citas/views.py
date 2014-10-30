# -*- coding: utf-8 -*-
# VIEWS CITAS

from math import sqrt
from datetime import datetime
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from endless_pagination.decorators import page_template
from olibertaria.utils import obtener_imagenes_display, obtener_cita, bersuit_vergarabat, tiempo_desde
from models import Cita, Cfavoritas, Ceditadas, Cdenunciadas
from perfiles.models import Perfiles
from forms import FormNuevaCita, FormEditarCita
from notificaciones.models import Notificacion
from perfiles.utils import obtener_num_favoritos


@page_template('index_page_citas.html')  # endless pagination
def index(request, queryset, template='citas/index.html', extra_context=None):
    if request.user.is_authenticated():
        #si user esta login, obtener citas favoritas del usuario:
        perfil_usuario = Perfiles.objects.get(usuario=request.user)
        cfavoritas_objects = Cfavoritas.objects.filter(eliminado=False, perfil=perfil_usuario)
        citas_favoritas = []
        for x in cfavoritas_objects:
            citas_favoritas.append(x.cita)
    else:
        #no login
        citas_favoritas = []

    #queryset y clase "active" para button de filtro
    autor = ""
    recientes = ""
    populares = ""
    q = ""
    if queryset == "autor":
        q = "autor"
        autor = "active"
    elif queryset == "populares":
        q = "-favoritos_recibidos"
        populares = "active"
    else:
        q = "-fecha"
        recientes = "active"

    #citas obj.
    citas = []
    citas_obj = Cita.objects.filter(eliminada=False).order_by(q)

    for c in citas_obj:
        cita = obtener_cita(c)
        if request.user.is_authenticated():
            # sumar clase a las citas favoritas del usuario
            if c in citas_favoritas:
                citas.append([cita, "dorado"])
            else:
                citas.append([cita, ""])
        else:
            citas.append([cita, ""])

    #imagenes slider
    imagenes_display = obtener_imagenes_display(7)

    context = {
        'citas': citas, 'imagenes_display': imagenes_display, 'autor': autor,
        'recientes': recientes, 'populares': populares}

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


def cita(request, cita_id):
    template = 'citas/cita.html'
    cita = Cita.objects.get(id=cita_id)

    # verificar si es favorita
    if request.user.is_authenticated():
        perfil_usuario = Perfiles.objects.get(usuario=request.user)
        cfavoritas_objects = Cfavoritas.objects.filter(
            eliminado=False, perfil=perfil_usuario)
        citas_favoritas = []
        for x in cfavoritas_objects:
            citas_favoritas.append(x.cita)

        if cita in citas_favoritas:
            es_favorita = "dorado"
        else:
            es_favorita = ""
    else:
        es_favorita = ""

    cita = obtener_cita(cita)

    #imagenes slider
    imagenes_display = obtener_imagenes_display(7)

    context = {'cita': cita, 'es_favorita': es_favorita, 'imagenes_display': imagenes_display}
    return render(request, template, context)


@login_required
def nueva(request):
    #suma una frase
    template = 'citas/nueva.html'
    if request.method == "POST":
        #obtener perfil y crear nueva cita
        form = FormNuevaCita(request.POST)
        if form.is_valid():
            nueva_cita = form.save(commit=False)
            perfil_usuario = Perfiles.objects.get(usuario=request.user)
            nueva_cita.creador = perfil_usuario
            nueva_cita.save()
            return HttpResponseRedirect(reverse('citas:index', kwargs={'queryset': (u'recientes')}))
        else:
            pass

    # obtener lista de autores para ayudar al usuario. (sidebar+autocomplete)
    lista_de_autores = []
    lista_de_autores_obj = Cita.objects.filter(
        eliminada=False).values('autor').order_by('autor')
    for x in lista_de_autores_obj:
        if x['autor'] not in lista_de_autores:
            lista_de_autores.append(x['autor'])
    lista_de_autores_json = json.dumps(lista_de_autores)

    form = FormNuevaCita()

    #honeypot antispan
    lista_bersuit = bersuit_vergarabat()

    context = {'FormNuevaCita': FormNuevaCita, 'lista_bersuit': lista_bersuit,
               'lista_de_autores': lista_de_autores, 'lista_de_autores_json': lista_de_autores_json}
    return render(request, template, context)


@login_required
def marcar_favorito(request):
    # AJAX marca una cita como favorita
    if request.is_ajax():
        cita_id = request.GET.get('frase_id', '')
        cita = get_object_or_404(Cita, pk=cita_id)
        perfil_usuario = Perfiles.objects.get(usuario=request.user)
        # revisa si ya marco como favorita a esa cita
        fue_eliminada = False
        registro_existe = Cfavoritas.objects.filter(
            cita=cita, perfil=perfil_usuario).exists()

        if registro_existe:
            registro_favorito = Cfavoritas.objects.get(
                cita=cita, perfil=perfil_usuario)
            fue_eliminada = registro_favorito.eliminado
            # marca la cita como favorita
            if fue_eliminada is True:
                cita.favoritos_recibidos += 1
                registro_favorito.eliminado = False
                registro_favorito.fecha = datetime.today()
                cita.save()
                registro_favorito.save()
                return HttpResponse('nueva frase favorita')
            # desmarca la cita como favorita
            else:
                cita.favoritos_recibidos -= 1
                registro_favorito.eliminado = True
                cita.save()
                registro_favorito.save()
                return HttpResponse('frase favorita removida')
        else:
            # suma la cita como nueva favorita
            cita.favoritos_recibidos += 1
            registro_favorito = Cfavoritas(cita=cita, perfil=perfil_usuario)
            registro_favorito.save()
            cita.save()

            #Notificaciones de cita
            if perfil_usuario != cita.creador:
                notificacion_cita_fav = Notificacion(actor=perfil_usuario, target=cita.creador,
                                                     objeto_id=cita.id, tipo_objeto="cita",
                                                     tipo_notificacion="fav_voteup")
                notificacion_cita_fav.save()

            if cita.favoritos_recibidos == 100 or cita.favoritos_recibidos == 1000:
                notificacion_cita_num = Notificacion(target=cita.creador,
                                                     objeto_id=cita.id, tipo_objeto="cita",
                                                     tipo_notificacion="num")
                notificacion_cita_num.save()

            return HttpResponse('nueva frase favorita')
    else:
        return HttpResponse("ajax error fav cita")


def favoritas(request, username):
    # muestra las citas favoritas de un usuario
    template = 'citas/favoritas.html'
    user_object = User.objects.get(username=username)

    perfil_usuario = Perfiles.objects.get(usuario=user_object)  # perfil usuario visitado
    num_favoritos = obtener_num_favoritos(perfil_usuario)
    Cfavoritas_objects = Cfavoritas.objects.filter(perfil=perfil_usuario, eliminado=False).order_by('-fecha')
    propio_usuario = False
    citas_favoritas = []

    if request.user.is_authenticated():
        if user_object == request.user:
            propio_usuario = True  # usuario revisando sus propias favoritas
        if propio_usuario:
            for c in Cfavoritas_objects:
                citas_favoritas.append([c.cita, "dorado", c.fecha])
        else:
            # obiene las citas favoritas del usuario visitante y suma la clase "dorado".
            perfil_usuario_visitante = Perfiles.objects.get(usuario=request.user)
            cfavoritas_usuario_visitante = Cfavoritas.objects.filter(
                perfil=perfil_usuario_visitante, eliminado=False)
            citas_favoritas_visitante = []
            for x in cfavoritas_usuario_visitante:
                citas_favoritas_visitante.append(x.cita)
            for c in Cfavoritas_objects:
                if c.cita in citas_favoritas_visitante:
                    citas_favoritas.append([c.cita, "dorado", c.fecha])
                else:
                    citas_favoritas.append([c.cita, "", c.fecha])
    else:
        for c in Cfavoritas_objects:
            citas_favoritas.append([c.cita, "", c.fecha])

    context = {
        'citas_favoritas': citas_favoritas,
        'perfil_usuario': perfil_usuario, 'propio_usuario': propio_usuario,
        'num_favoritos': num_favoritos}

    return render(request, template, context)


@login_required
def colaborar_organizar(request):
    # Pagina que obtiene las citas eliminadas y las despliega.

    template = 'citas/citas_coorg.html'
    citas_eliminadas = Cita.objects.filter(
        eliminada=True, removidatotalmente=False).order_by('-id')
    perfil_usuario = Perfiles.objects.get(usuario=request.user)

    # para llenar la tabla de citas eliminadas.
    tabla_citas = []
    for cita in citas_eliminadas:
        frase = [cita.texto, cita.autor, cita.fuente, cita.id]
        correcciones = []
        # ediciones realizadas a las citas eliminadas.
        if Ceditadas.objects.filter(cita=cita).exists():
            correcciones_objects = Ceditadas.objects.filter(cita=cita)
            for c in correcciones_objects:
                fecha = tiempo_desde(c.fecha)
                razon = c.razon
                perfil = c.perfil.nickname
                correccion = [fecha, razon, perfil]
                correcciones.append(correccion)
        #borde_color & iconos
        borde_color = []
        estado = []
        if cita.denunciada < 4:
            borde_color = ["green", "double"]
            if cita.denunciada == 3:
                estado.append(["check-circle"])
            else:
                borde_color = ["green", "solid"]
                estado.append(["check-circle", "check-circle"])
        elif cita.denunciada > 4:
            borde_color = ["red", "double"]
            if cita.denunciada == 5:
                estado.append(["times-circle"])
            else:
                borde_color = ["red", "solid"]
                estado.append(["times-circle", "times-circle"])
        else:
            borde_color = ["#ebebeb", "double"]
            estado.append(["flag"])

        # accion del usuario.
        accion_usr = ["", ""]
        if Cdenunciadas.objects.filter(cita=cita, perfil=perfil_usuario).exists():
            cdenunciada_obj = Cdenunciadas.objects.get(
                cita=cita, perfil=perfil_usuario)
            if cdenunciada_obj.eliminado is False:
                accion_usr = ["", "-circle"]
            else:
                accion_usr = ["-circle", ""]
        tabla_citas.append([frase, correcciones, estado, borde_color, accion_usr])

    # variables y calculo del progress bar
    if citas_eliminadas.count() > 0:
        num_citas_eliminadas = citas_eliminadas.count()
        max_y = num_citas_eliminadas * 3
        y = 0
        for x in citas_eliminadas:
            z = 4 - x.denunciada
            y += sqrt(z * z)
        porcentaje_avanzado = float(y) / float(max_y)
        progress_bar = str(porcentaje_avanzado * 100)
    else:
        progress_bar = 100

    context = {'tabla_citas': tabla_citas, 'progress_bar': progress_bar}
    return render(request, template, context)


@login_required
def denunciar_cita(request):
    reputacion_necesaria = 10
    if request.is_ajax:
        cita_id = request.GET.get('frase_id', '')
        cita_denunciada = get_object_or_404(Cita, id=cita_id)
        perfil_usuario = Perfiles.objects.get(usuario=request.user)
        ya_denuncio = False
        ya_denuncio = Cdenunciadas.objects.filter(
            cita=cita_denunciada, perfil=perfil_usuario).exists()
        if ya_denuncio:
            return HttpResponse("cita ya denunciada")
        else:
            # marcar la cita como denunciada si el usuario tiene la reputacion necesaria
            if perfil_usuario.votos_recibidos > reputacion_necesaria:
                cdenunciada_obj = Cdenunciadas(
                    cita=cita_denunciada, perfil=perfil_usuario)
                cita_denunciada.denunciada += 1
                if cita_denunciada.denunciada > 3:
                    # Notificacion imagen eliminada para quien subio la imagen.
                    notificacion_denuncia = Notificacion(target=cita_denunciada.perfil,
                                                         objeto_id=cita_denunciada.id, tipo_objeto="cita",
                                                         tipo_notificacion="denuncia")
                    notificacion_denuncia.save()

                    cita_denunciada.eliminada = True
                cita_denunciada.save()
                cdenunciada_obj.save()
        return HttpResponse("cita denunciada")


@login_required
def marcar_visto(request, cita_id):
    # obtiene la cita eliminada y reduce el numero de "denuncias" por con 1.
    # si la cita tiene <= 1 numero de denuncias, regresa al Banco de Frases
    cita = get_object_or_404(Cita, id=cita_id)
    perfil_usuario = Perfiles.objects.get(usuario=request.user)

    if Cdenunciadas.objects.filter(cita=cita, perfil=perfil_usuario).exists():
        cdenunciada_obj = Cdenunciadas.objects.get(
            cita=cita, perfil=perfil_usuario)
        if cdenunciada_obj.eliminado is False:  # Si el mismo usuario había denunciado esa cita antes.
            cita.denunciada -= 2  # remueve la denuncia y ademas marca el visto (x2)
            cdenunciada_obj.eliminado = True  # el cdenunciada_obj es marcado como eliminado
            cdenunciada_obj.save()
        elif cdenunciada_obj.eliminado is True:
            pass  # esta marcando con visto a una que ya marco con visto.
    else:
        cita.denunciada -= 1
        cdenunciada_obj = Cdenunciadas(
            cita=cita, perfil=perfil_usuario, eliminado=True)
        cdenunciada_obj.save()

    if cita.denunciada <= 1:
        cita.eliminada = False
    cita.save()

    return redirect('citas:colaborar_organizar')


@login_required
def marcar_x(request, cita_id):
    # obtiene la cita eliminada y aumenta el numero de "denuncias" por con 1.
    # si la cita tiene <= 7 numero de denuncias, es removida totalmente
    cita = Cita.objects.get(id=cita_id)
    perfil_usuario = Perfiles.objects.get(usuario=request.user)
    if Cdenunciadas.objects.filter(cita=cita, perfil=perfil_usuario).exists():
        cdenunciada_obj = Cdenunciadas.objects.get(
            cita=cita, perfil=perfil_usuario)
        if cdenunciada_obj.eliminado is False:
            pass
        elif cdenunciada_obj.eliminado is True:
            cita.denunciada += 2
            cdenunciada_obj.eliminado = False
            cdenunciada_obj.save()
    else:
        cita.denunciada += 1
        cdenunciada_obj = Cdenunciadas(cita=cita, perfil=perfil_usuario)
        cdenunciada_obj.save()

    if cita.denunciada >= 7:
        cita.removidatotalmente = True
    cita.save()

    return redirect('citas:colaborar_organizar')


@login_required
def coorg_editar(request, cita_id):
    template = 'citas/editar_cita.html'
    cita = get_object_or_404(Cita, id=cita_id)
    perfil_usuario = Perfiles.objects.get(usuario=request.user)
    if request.method == 'POST':
        form = FormEditarCita(request.POST)
        if form.is_valid():
            texto = form.cleaned_data['texto']
            autor = form.cleaned_data['autor']
            fuente = form.cleaned_data['fuente']
            razon = form.cleaned_data['razon']
            if texto != cita.texto:
                cita.texto = texto
            if autor != cita.autor:
                cita.autor = autor
            if fuente != cita.fuente:
                cita.fuente = fuente
            cita.save()
            ceditadas_obj = Ceditadas(
                cita=cita, perfil=perfil_usuario, razon=razon)  # campo que guarda datos sobre la edición.
            ceditadas_obj.save()
            return redirect('citas:colaborar_organizar')

    form_editar_cita = FormEditarCita(initial={'texto': cita.texto,
                                               'autor': cita.autor,
                                               'fuente': cita.fuente})

    # lista de autores para ayudar al usuario (autocomplete - sidebar)
    lista_de_autores = []
    lista_de_autores_obj = Cita.objects.filter(eliminada=False).values('autor').order_by('autor')
    for x in lista_de_autores_obj:
        if x['autor'] not in lista_de_autores:
            lista_de_autores.append(x['autor'])

    lista_de_autores_json = json.dumps(lista_de_autores)

    # honeypot
    lista_bersuit = bersuit_vergarabat()

    context = {'form_editar_cita': form_editar_cita, 'cita_id': cita_id,
               'lista_de_autores': lista_de_autores, 'lista_bersuit': lista_bersuit,
               'lista_de_autores_json': lista_de_autores_json}

    return render(request, template, context)

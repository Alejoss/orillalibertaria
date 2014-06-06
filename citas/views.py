# -*- coding: utf-8 -*-
from math import sqrt
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from endless_pagination.decorators import page_template
from olibertaria.utils import obtener_imagenes_display, obtener_cita
from models import Cita, Cfavoritas, Ceditadas, Cdenunciadas
from perfiles.models import Perfiles
from forms import FormNuevaCita, FormEditarCita
from imagenes.models import Imagen
from notificaciones.models import Notificacion


# Create your views here.
@page_template('index_page_citas.html')
def index(request, queryset, template='citas/index.html', extra_context=None):
    if request.user.is_authenticated():
        #si user esta login:
        perfil_usuario = Perfiles.objects.get(usuario=request.user)
        cfavoritas_objects = Cfavoritas.objects.filter(eliminado=False, perfil=perfil_usuario)
        citas_favoritas = []
        for x in cfavoritas_objects:
            citas_favoritas.append(x.cita)
    else:
        #no login
        citas_favoritas = []

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

    citas = []
    citas_obj = Cita.objects.filter(eliminada=False).order_by(q)

    for c in citas_obj:
        cita = obtener_cita(c)
        if request.user.is_authenticated():
            if c in citas_favoritas:
                citas.append([cita, "dorado"])
            else:
                citas.append([cita, ""])
        else:
            citas.append([cita, ""])

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

    if request.user.is_authenticated():
        #si usuario login
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

    imagenes_display = obtener_imagenes_display(7)

    context = {'cita': cita, 'es_favorita': es_favorita, 'imagenes_display': imagenes_display}
    return render(request, template, context)


def nueva(request):
    template = 'citas/nueva.html'
    if request.method == "POST":
        form = FormNuevaCita(request.POST)
        if form.is_valid():
            nueva_cita = form.save(commit=False)
            perfil_usuario = Perfiles.objects.get(usuario=request.user)
            nueva_cita.creador = perfil_usuario
            nueva_cita.save()
            return HttpResponseRedirect(reverse('citas:index', kwargs={'queryset': (u'recientes')}))
        else:
            pass  # !!! enviar errores

    lista_de_autores = []
    lista_de_autores_obj = Cita.objects.filter(
        eliminada=False).values('autor').order_by('autor')
    for x in lista_de_autores_obj:
        if x['autor'] not in lista_de_autores:
            lista_de_autores.append(x['autor'])

    form = FormNuevaCita()
    context = {'FormNuevaCita': FormNuevaCita,
               'lista_de_autores': lista_de_autores}
    return render(request, template, context)


def marcar_favorito(request):
    if request.is_ajax():
        cita_id = request.GET.get('frase_id', '')
        cita = Cita.objects.get(pk=cita_id)
        perfil_usuario = Perfiles.objects.get(usuario=request.user)
        # revisa si ya marco como favorito a esa cita
        fue_eliminado = False
        registro_existe = Cfavoritas.objects.filter(
            cita=cita, perfil=perfil_usuario).exists()
        if registro_existe:
            registro_favorito = Cfavoritas.objects.get(
                cita=cita, perfil=perfil_usuario)
            fue_eliminado = registro_favorito.eliminado
            if fue_eliminado is True:
                cita.favoritos_recibidos += 1
                registro_favorito.eliminado = False
                registro_favorito.fecha = datetime.today()
                cita.save()
                registro_favorito.save()
                return HttpResponse('nueva frase favorita')
            else:
                cita.favoritos_recibidos -= 1
                registro_favorito.eliminado = True
                cita.save()
                registro_favorito.save()
                return HttpResponse('frase favorita removida')
        else:
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
        return HttpResponse("error_fav_cita")  # !!!raise 404


def favoritas(request, username):
    template = 'citas/favoritas.html'
    user_object = User.objects.get(username=username)

    perfil_usuario = Perfiles.objects.get(usuario=user_object)
    Cfavoritas_objects = Cfavoritas.objects.filter(perfil=perfil_usuario, eliminado=False).order_by('-fecha')
    propio_usuario = False
    citas_favoritas = []
    
    if request.user.is_authenticated():
        if user_object == request.user:
            propio_usuario = True
        if propio_usuario:
            for c in Cfavoritas_objects:
                citas_favoritas.append([c.cita, "dorado", c.fecha])
        else:
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
        citas_favoritas.append([c.cita, "", c.fecha])

    imagenes_display = Imagen.objects.all().order_by(
        '-favoritos_recibidos')[:5]

    context = {
        'citas_favoritas': citas_favoritas, 'imagenes_display': imagenes_display,
        'user_object': user_object, 'propio_usuario': propio_usuario}

    return render(request, template, context)


def colaborar_organizar(request):
    template = 'citas/citas_coorg.html'
    citas_eliminadas = Cita.objects.filter(
        eliminada=True, removidatotalmente=False)
    perfil_usuario = Perfiles.objects.get(usuario=request.user)
    success_uno = "#dff0d8"
    success_dos = "#d0e9c6"
    danger_uno = "#f2dede"
    danger_dos = "#ebcccc"
    default = "#ebebeb"

    # para llenar la tabla de citas eliminadas.
    tabla_citas = []
    for cita in citas_eliminadas:
        frase = [cita.texto, cita.autor, cita.fuente, cita.id]
        correcciones = []
        # ediciones
        if Ceditadas.objects.filter(cita=cita).exists():
            correcciones_objects = Ceditadas.objects.filter(cita=cita)
            for c in correcciones_objects:
                fecha = c.fecha
                razon = c.razon
                perfil = c.perfil.usuario.username
                correccion = [fecha, razon, perfil]
                correcciones.append(correccion)
        #color & iconos
        color = ""
        estado = []
        if cita.denunciada < 4:
            color = success_uno
            if cita.denunciada == 3:
                estado.append(["check-circle"])
            else:
                color = success_dos
                estado.append(["check-circle", "check-circle"])
        elif cita.denunciada > 4:
            color = danger_uno
            if cita.denunciada == 5:
                estado.append(["times-circle"])
            else:
                color = danger_dos
                estado.append(["times-circle", "times-circle"])
        else:
            color = default
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
        print color
        tabla_citas.append([frase, correcciones, estado, color, accion_usr])

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


def denunciar_cita(request):
    if request.is_ajax:
        cita_id = request.GET.get('frase_id', '')
        cita_denunciada = Cita.objects.get(id=cita_id)
        perfil_usuario = Perfiles.objects.get(usuario=request.user)
        ya_denuncio = False
        ya_denuncio = Cdenunciadas.objects.filter(
            cita=cita_denunciada, perfil=perfil_usuario).exists()
        if ya_denuncio:
            return HttpResponse("cita ya denunciada")
        else:
            if perfil_usuario.votos_recibidos > 10:
                cdenunciada_obj = Cdenunciadas(
                    cita=cita_denunciada, perfil=perfil_usuario)
                cita_denunciada.denunciada += 1
                if cita_denunciada.denunciada > 3:
                    #Notificacion imagen denunciada
                    notificacion_denuncia = Notificacion(target=cita_denunciada.perfil,
                                                         objeto_id=cita_denunciada.id, tipo_objeto="cita",
                                                         tipo_notificacion="denuncia")
                    notificacion_denuncia.save()

                    cita_denunciada.eliminada = True
                cita_denunciada.save()
                cdenunciada_obj.save()
        return HttpResponse("cita denunciada")


def marcar_visto(request, cita_id):
    cita = Cita.objects.get(id=cita_id)
    print cita.denunciada
    perfil_usuario = Perfiles.objects.get(usuario=request.user)
    if Cdenunciadas.objects.filter(cita=cita, perfil=perfil_usuario).exists():
        cdenunciada_obj = Cdenunciadas.objects.get(
            cita=cita, perfil=perfil_usuario)
        if cdenunciada_obj.eliminado is False:
            cita.denunciada -= 2
            cdenunciada_obj.eliminado = True
            cdenunciada_obj.save()
        elif cdenunciada_obj.eliminado is True:
            pass
    else:
        cita.denunciada -= 1
        cdenunciada_obj = Cdenunciadas(
            cita=cita, perfil=perfil_usuario, eliminado=True)
        cdenunciada_obj.save()

    if cita.denunciada <= 1:
        cita.eliminada = False
    cita.save()

    return redirect('citas:colaborar_organizar')


def marcar_x(request, cita_id):
    cita = Cita.objects.get(id=cita_id)
    print cita.denunciada
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


def coorg_editar(request, cita_id):
    template = 'citas/editar_cita.html'
    cita = Cita.objects.get(id=cita_id)
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
                cita=cita, perfil=perfil_usuario, razon=razon)
            ceditadas_obj.save()
            return redirect('citas:colaborar_organizar')
        else:
            form_editar_cita = FormEditarCita(initial={'texto': cita.texto,
                                                       'autor': cita.autor, 'fuente': cita.fuente})
            #!!! enviar errores

    else:
        form_editar_cita = FormEditarCita(initial={'texto': cita.texto,
                                                   'autor': cita.autor, 'fuente': cita.fuente})

    context = {'form_editar_cita': form_editar_cita, 'cita_id': cita_id}
    return render(request, template, context)

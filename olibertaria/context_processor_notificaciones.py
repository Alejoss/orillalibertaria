from utils import obtener_notificaciones, obtener_num_notificaciones
from temas.models import Perfiles


def procesar_notificaciones(request):
    context = {}
    if request.user.is_authenticated():
        perfil_usuario = Perfiles.objects.get(usuario=request.user)
        notificaciones = obtener_notificaciones(perfil_usuario)
        num_notificaciones = obtener_num_notificaciones(perfil_usuario)
        context = {'notificaciones': notificaciones,
                   'num_notificaciones': num_notificaciones}

        return context

    else:
        return context

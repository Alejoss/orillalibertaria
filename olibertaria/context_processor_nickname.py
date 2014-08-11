from temas.models import Perfiles


def procesar_nickname(request):
	perfil = Perfiles.objects.get(usuario=request.user)
	nickname = perfil.nickname
	context = {'nickname': nickname}

	return context

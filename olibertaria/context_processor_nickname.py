from temas.models import Perfiles


def procesar_nickname(request):
	context = {}
	if request.user.is_authenticated():
		perfil = Perfiles.objects.get(usuario=request.user)
		nickname = perfil.nickname
		context['nickname'] = nickname

	return context

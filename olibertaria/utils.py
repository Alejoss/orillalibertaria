from imagenes.models import Imagen
from temas.models import Votos

def obtener_imagenes_display(numero):
	#Recibe un numero.
	#Devuelve una lista con el mismo numero de imagenes, si hay disponibles.
	numero_de_imagenes = 1
	imagenes_disponibles = Imagen.objects.filter(eliminada=False).count()
	if imagenes_disponibles < numero:
		numero_de_imagenes = imagenes_disponibles
	else:
		numero_de_imagenes = numero

	imagenes_populares = Imagen.objects.filter(eliminada=False).order_by('-favoritos_recibidos')[:numero_de_imagenes]
	lista_urls = []
	for i in imagenes_populares:
		lista_urls.append(i.url)
	return lista_urls

def obtener_voted_status(post, perfil):
	#Recibe un post object y un perfil object. 
	#Devuelve el voted_status (no-vote, voted-up etc.)
	voted_status = "no-vote"
	if post.creador == perfil:
		voted_status = "propio_post"
	else:
		if Votos.objects.filter(post_votado = post, usuario_votante = perfil).exists():
			voto = Votos.objects.get(post_votado=post, usuario_votante=perfil)
			if voto.tipo == 1:
				voted_status = "voted-up"
			elif voto.tipo == -1:
				voted_status = "voted-down"
			else:
				voted_status = "no-vote"

	return voted_status

def obtener_imagen_tema(tema):
	#Devuelve la imagen correspondiente al tema, si no, devuelve un default.
	imagen = "http://csunlibertarian.files.wordpress.com/2012/02/porcupine.gif"
	if len(tema.imagen) > 10:
		imagen = tema.imagen
	return imagen




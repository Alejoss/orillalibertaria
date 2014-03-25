import random
from models import Posts, Temas

def obtener_posts_populares():
	indexes = range(7)
	random.shuffle(indexes)
	posts_populares = []
	for i in range(3):
		pp = Posts.objects.filter(es_respuesta=False, eliminado=False).order_by('-votos_positivos')[indexes.pop()]
		posts_populares.append(pp)

	return posts_populares

def obtener_imagen(id):
		tema = Temas.objects.get(id=id)
		imagen = ""
		if tema.imagen == None:
			imagen = "http://csunlibertarian.files.wordpress.com/2012/02/porcupine.gif"
		else:
			imagen = tema.imagen
		return imagen
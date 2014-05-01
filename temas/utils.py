import random
from models import Posts, Temas, Votos

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

def obtener_voted_status(post, user):
		#recibe un post object y un user object. Generalmente ser request.user.
		if post.creador.usuario == user:
			voted_status = "propio_post"
		else:
			if Votos.objects.filter(post_votado=post, usuario_votante=user).exists():
				voto = Votos.objects.get(post_votado=post, usuario_votante=user)
				if voto.tipo == 1:
					voted_status = "voted-up"
				elif voto.tipo == -1:
					voted_status = "voted-down"
				else:
					voted_status = "no-vote"
			else:
				voted_status = "no-vote"
		return voted_status
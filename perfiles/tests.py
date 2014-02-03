from django.test import TestCase


class PerfilesViewsTestCase(TestCase):
	def test_registrar(self):
		#prueba si registrar da status code 200, 
		#si user_creation_form esta en el context pasado por el Response object
		#si email esta en el user_creation_form
		resp = self.client.get('/perfiles/registrar/')
		self.assertEqual(resp.status_code, 200)
		self.assertTrue('user_creation_form' in resp.context)
		self.assertTrue('email' in resp.context['user_creation_form'].fields)

	def test_post_registrar(self):
		#prueba si el form de registro maneja bien los datos.
		#!!! deberia crear un fixture de la dtabase y revisar si se creo correctamente el usuario.
		client_post = self.client.post('/perfiles/registrar/', 
			{'usuario': 'doctor', 'email': 'doctor@gmail.com', 'password1': 'doctor99',
			'password2': 'doctor99' })
		self.assertEqual(client_post.status_code, 200)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from biblioteca_app.models import Libro, Prestamo,Usuario


class BibliotecaApiTestCase(APITestCase):

    def create_normal_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='normal_user', password='password', tipo_usuario='normal')
        token = Token.objects.create(user=user)
        return user, token

    def create_admin_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='admin_user', password='password', tipo_usuario='admin')
        token = Token.objects.create(user=user)
        return user, token

    def setUp(self):
        Libro.objects.create(titulo='Libro 1', autor='Autor 1', genero='Genero 1', year_publication='2022-01-01')
        Libro.objects.create(titulo='Libro 2', autor='Autor 2', genero='Genero 2', year_publication='2022-02-01')
        Libro.objects.create(titulo='Libro 3', autor='Autor 3', genero='Genero 3', year_publication='2022-03-01')        

        self.normal_user, self.normal_token = self.create_normal_user()
        self.admin_user, self.admin_token = self.create_admin_user()    

    def test_list_libros(self):
        url = reverse('libros_todos')
        response = self.client.get(url,format= 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_detalle_libro(self):
        libro = Libro.objects.first()
        url = reverse('libro_detalle', kwargs={'pk': 8})
        response = self.client.get(url,format= 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_crear_libro(self):
        url = reverse('libro_crear_actualizar')
        data = {
                'titulo': 'caperusita roja',
                'autor': 'el senor',
                'genero': 'cuento',
                'year_publication': '2024-02-09'
                }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)    
    
        
    def test_crear_prestamo(self):
        url = reverse('crear_prestamo')
        data = {                
                'libro': 5
                }

        libro = Libro.objects.first()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.normal_token.key}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_prestamo_usuario(self):
        Prestamo.objects.create(libro_id= 14,usuario_id=9,fecha_prestamo= '2022-01-01',estado= 'activo')
        url = reverse('prestamo_activo',kwargs={'pk': 9})
        response = self.client.get(url, format= 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)         
    
    
    
    




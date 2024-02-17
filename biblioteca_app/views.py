from django.shortcuts import render
from django.http import QueryDict,Http404,HttpResponseBadRequest
from django.db.models import Q
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from .models import Libro, Usuario, Prestamo
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.authentication import TokenAuthentication
from .serializers import (
    UsuarioSerializer,
    UsuarioCrearSerializer,
    CompactLibroSerializer,
    FullLibroSerializer,
    LibroCreateSerializer,
    PrestamoCreationSerializer,
    PrestamoSerializer)
# Create your views here.

class CrearUsuario(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UsuarioCrearSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        serialized_user = UsuarioSerializer(user)
        headers = self.get_success_headers(serializer.data)
        return Response(serialized_user.data, status=status.HTTP_201_CREATED,headers=headers)


class ObtainAuthToken(generics.GenericAPIView):
    queryset = Usuario.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UsuarioSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username,password)
        user = authenticate(username= username, password= password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
class UsuarioIsAdmin(permissions.BasePermission):    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo_usuario == 'admin'
    
class UsuarioIsNormal(permissions.BasePermission):    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo_usuario == 'normal'

class LibrosTodos(generics.ListAPIView):
    queryset = Libro.objects.all()
    serializer_class = CompactLibroSerializer

class LibrosDisponibles(generics.ListAPIView):
    queryset = Libro.objects.filter(Q(prestamo__isnull=True) | Q(prestamo__estado='devuelto'))
    serializer_class = CompactLibroSerializer

class LibroDetalle(generics.RetrieveAPIView):    
    queryset = Libro.objects.all()
    serializer_class = FullLibroSerializer
    def get_object(self):
        pk = self.kwargs.get('pk')    
        try:
            libro = Libro.objects.get(pk=pk)
            return libro 
        except Libro.DoesNotExist:
            raise NotFound("Libro no encontrado.")
            #content = {'error': 'Libro no encontrado.'}
            #return Response(content, status=status.HTTP_404_NOT_FOUND) 
        
class CrearActualizarLibro(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroCreateSerializer
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated,UsuarioIsAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,headers=headers)
    
    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            instance = self.get_object()
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            #raise ValidationError("ID necesario para update.")
            content = {'error': 'ID necesario para update.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

class PrestamoActivo(generics.ListAPIView):
    queryset = Prestamo.objects.filter(estado='activo')
    serializer_class = PrestamoSerializer

    def get_queryset(self):
        usuario_pk = self.kwargs.get('pk')
        #print(usuario_pk)
        
        prestamos = self.queryset.filter(usuario_id=usuario_pk)
        #print(repr(prestamos))
        print('Existe:',prestamos.exists())
        if prestamos.exists():
            print(prestamos.exists())
            return prestamos
        else:
            raise NotFound("Sin prestamos activos.")
            #content = {'error': 'Libro no encontrado.'}
            #return Response(content, status=status.HTTP_404_NOT_FOUND)
        
class RealizarPrestamo(generics.CreateAPIView)   :
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoCreationSerializer
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, UsuarioIsNormal]


    def create(self, request, *args, **kwargs):
        user_id = ''
        libro_id = self.request.data.get('libro')
        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            token_parts = authorization_header.split()
            if len(token_parts) == 2 and token_parts[0].lower() == 'bearer':
                token = token_parts[1]
                access_token = AccessToken(token)
                user_id = access_token.payload.get('user_id')
            elif len(token_parts) == 2 and token_parts[0].lower() == 'token':
                user = request.user
                user_id = user.id
        mutable_data = request.data.copy()
        mutable_data['usuario'] = user_id
        libro = Libro.objects.filter(pk=libro_id).first()   
        if not libro:
            print('error libro')
            content = {'error': 'Libro no existe'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            libroEstado = Prestamo.objects.filter(libro=libro).latest('fecha_prestamo')
            print(libroEstado.estado)
            if libroEstado.estado == 'activo':
                print('error libro activo')
                content = {'error': 'Libro en préstamo'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            pass

        serializer = self.get_serializer(data = mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,headers=headers)   
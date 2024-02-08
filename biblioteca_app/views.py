from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from .models import Libro, Usuario, Prestamo
from .serializers import LibroSerializer, UsuarioSerializer, PrestamoSerializer
# Create your views here.

class LibroDetalle(generics.ListAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
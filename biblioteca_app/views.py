from django.shortcuts import render
from django.http import Http404
from django.db.models import Q
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from .models import Libro, Usuario, Prestamo
from .serializers import (
    CompactLibroSerializer,
    FullLibroSerializer,
    UsuarioSerializer,
    PrestamoSerializer)
# Create your views here.

class LibrosCompacto(generics.ListAPIView):
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
            raise Http404("Libro no encontrado.")

        
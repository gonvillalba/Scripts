from django.shortcuts import render
from django.http import Http404
from django.db.models import Q
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from .models import Libro, Usuario, Prestamo
from .serializers import (
    CompactLibroSerializer,
    FullLibroSerializer,
    LibroCreateSerializer,
    PrestamoCreationSerializer,
    PrestamoSerializer)
# Create your views here.

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
            raise Http404("Libro no encontrado.")
        
class CrearActualizarLibro(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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
            raise ValueError("ID necesario para update.")

class PrestamoActivo(generics.ListAPIView):
    queryset = Prestamo.objects.filter(estado='activo')
    serializer_class = PrestamoSerializer

    def get_queryset(self):
        usuario_pk = self.kwargs.get('pk')
        print(usuario_pk)
        try:
            prestamos = self.queryset.filter(usuario_id=usuario_pk)
            print(repr(prestamos))
            return prestamos
        except Prestamo.DoesNotExist:
            raise Http404("Libro no encontrado.")
        
class RealizarPrestamo(generics.CreateAPIView)   :
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoCreationSerializer

    def perform_create(self, serializer):
        usuario_id = self.request.data.get('usuario')
        libro_id = self.request.data.get('libro')
        usuario = Usuario.objects.filter(pk=usuario_id).first()
        libro = Libro.objects.filter(pk=libro_id).first()

        if not usuario:
            raise ValueError("Usuario ID invalido.")
        if not libro:
            raise ValueError("Libro ID invalido.")

        serializer.save()


        
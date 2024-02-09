from django.urls import path
from .views import (
    LibrosCompacto,
    LibroDetalle)

urlpatterns = [
     path('libros/disponibles/',LibrosCompacto.as_view(), name='libros_disponibles'),
     path('libros/<int:pk>/',LibroDetalle.as_view(), name='libro_detalle'),
]
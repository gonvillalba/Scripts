from django.urls import path
from .views import LibroDetalle

urlpatterns = [
     path('libros/todos/',LibroDetalle.as_view(), name='libros_todo'),
]
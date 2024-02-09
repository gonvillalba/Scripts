from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    ObtainAuthToken,
    LibrosTodos,
    LibrosDisponibles,
    LibroDetalle,
    CrearActualizarLibro,
    PrestamoActivo,
    RealizarPrestamo)

urlpatterns = [
    path('api/tokenBasico/', ObtainAuthToken.as_view(), name='obtain_auth_token'),
    path('api/tokenJWT/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/tokenJWT/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('libros/todos/',LibrosTodos.as_view(), name='libros_todos'),
    path('libros/disponibles/',LibrosDisponibles.as_view(), name='libros_disponibles'),
    path('libros/<int:pk>/',LibroDetalle.as_view(), name='libro_detalle'),
    path('libros/crear/',CrearActualizarLibro.as_view(), name='libro_crear_actualizar'),
    path('libros/crear/<int:pk>',CrearActualizarLibro.as_view(), name='libro_crear_actualizar'),
    path('prestamo/usuario/<int:pk>',PrestamoActivo.as_view(), name='prestamo_activo'),
    path('prestamo/crear/', RealizarPrestamo.as_view(), name= 'crear_prestamo')
]

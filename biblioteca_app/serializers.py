from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Libro, Usuario, Prestamo

#User = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create_user(self, validated_data):        
        user = Usuario.objects.create_user(**validated_data)
        user.save()
        return user
    
class CompactLibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id','titulo', 'autor', 'genero']

class LibroCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'

class FullLibroSerializer(serializers.ModelSerializer):
    estado = serializers.SerializerMethodField()

    class Meta:
        model = Libro
        fields = ['id','titulo', 'autor', 'genero','year_publication','estado']

    def get_estado(self,obj):
        prestamo_existe = Prestamo.objects.filter(libro_id=obj.id).exists()
        if prestamo_existe:
            prestamo = Prestamo.objects.filter(libro_id=obj.id).latest('fecha_prestamo')
            return prestamo.estado
        else:
            return 'devuelto'


class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = '__all__'

class PrestamoCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = ['usuario', 'libro', 'fecha_prestamo', 'fecha_devolucion', 'estado']
        read_only_fields = ['id','fecha_prestamo','fecha_devolucion', 'estado']
    
    def create(self, validated_data):
        # Set fecha_prestamo to today's date and estado to 'activo' automatically
        validated_data['fecha_prestamo'] = timezone.now().date()
        validated_data['estado'] = 'activo'
        return Prestamo.objects.create(**validated_data)


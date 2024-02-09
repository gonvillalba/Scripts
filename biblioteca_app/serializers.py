from rest_framework import serializers
from .models import Libro, Usuario, Prestamo

class UsuarioSerializer(serializers.ModelSerializer):
    pasword = serializers.CharField(write_only=True)

    def Create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user

    class Meta:
        model = Usuario
        fields = ('username','email','tipo_usuario','password')

class CompactLibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id','titulo', 'autor', 'genero']

class PrestamoEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = ['estado']

class FullLibroSerializer(serializers.ModelSerializer):
    estado = serializers.SerializerMethodField()

    class Meta:
        model = Libro
        fields = ['id','titulo', 'autor', 'genero','estado','estado']

    def get_estado(self,obj):
        prestamo_existe = Prestamo.objects.filter(libro_id=obj.id).exists()
        print(prestamo_existe)        
        if prestamo_existe:
            prestamo = Prestamo.objects.filter(libro_id=obj.id).latest('fecha_prestamo')
            print(prestamo.estado) 
            return prestamo.estado
        else:
            return 'devuelto'


class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = '__all__'


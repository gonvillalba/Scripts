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

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'

class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = '__all__'
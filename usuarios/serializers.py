from rest_framework import serializers
from .models import *

class AccesoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccesoUsuario
        fields = ('__all__')

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('__all__')

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = ('__all__')
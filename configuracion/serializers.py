from rest_framework import serializers
from .models import *

class TipoIdentificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoIdentificacion
        fields = ('__all__')

class AsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignatura
        fields = ('__all__')

class GradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grado
        fields = ('__all__')

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = ('__all__')

class DepartamentoSerializeer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ('__all__')

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ('__all__')
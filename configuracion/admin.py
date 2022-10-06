from django.contrib import admin
from .models import *

# Register your models here.
class TipoIdentificacionAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'sigla', 'descripcion', 'activo', 'fecha_creacion')
    list_filter = ('descripcion',)


admin.site.register(TipoIdentificacion, TipoIdentificacionAdmin)
admin.site.register(Asignatura)
admin.site.register(Grado)
admin.site.register(Grupo)
admin.site.register(Departamento)
admin.site.register(Municipio)
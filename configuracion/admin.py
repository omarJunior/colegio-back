from django.contrib import admin
from .models import *

# Register your models here.
class TipoIdentificacionAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'sigla', 'descripcion', 'activo', 'fecha_creacion')
    list_filter = ('descripcion',)

class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre_asignatura', 'activo', 'fecha_creacion',)
    list_filter = ('nombre_asignatura',)

class GradoAdmin(admin.ModelAdmin):
    list_display = ('grado', 'activo', 'fecha_creacion')
    list_filter = ('grado',)

class GrupoAdmin(admin.ModelAdmin):
    list_display = ('get_grado', 'codigo', 'nombre_grupo', 'activo', 'fecha_creacion',)
    list_filter = ('nombre_grupo',)

    def get_grado(self, request):
        if request.fk_grado:
            return f"N° Grado: {request.fk_grado.grado}"
        return ""
    get_grado.short_description = "Grado"

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('')
    list_filter = ('')

class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('',)
    list_filter = ('',)


admin.site.register(TipoIdentificacion, TipoIdentificacionAdmin)
admin.site.register(Asignatura, AsignaturaAdmin)
admin.site.register(Grado, GradoAdmin)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Departamento)
admin.site.register(Municipio)
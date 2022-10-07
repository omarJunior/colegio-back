#https://django-grappelli.readthedocs.io/en/3.0.3/customization.html#grappellisortablehiddenmixin
from django.contrib import admin
from .models import *

# Register your models here.
class TipoIdentificacionAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'sigla', 'descripcion', 'activo', 'fecha_creacion')
    list_filter = ('descripcion',)

class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre_asignatura', 'activo', 'fecha_creacion',)
    list_filter = ('nombre_asignatura',)

class GrupoInline(admin.StackedInline):
    model = Grupo
    extra = 0

class GradoAdmin(admin.ModelAdmin):
    inlines = (GrupoInline, )
    list_display = ('grado', 'activo', 'fecha_creacion')
    list_filter = ('grado',)

class GrupoAdmin(admin.ModelAdmin):
    list_display = ('get_grado', 'codigo', 'nombre_grupo', 'activo', 'fecha_creacion',)
    list_filter = ('nombre_grupo',)
    search_fields = ('codigo', 'nombre_grupo',)

    def get_grado(self, request):
        if request.fk_grado:
            return f"N° Grado: {request.fk_grado.grado}"
        return ""
    get_grado.short_description = "Grado"

class MunicipioInline(admin.StackedInline):
    model = Municipio
    extra = 0

class DepartamentoAdmin(admin.ModelAdmin):
    inlines = (MunicipioInline,)
    list_display = ('codigo', 'nombre_departamento', 'activo', 'fecha_creacion')
    list_filter = ('nombre_departamento',)

class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('get_departamento', 'nombre_municipio', 'activo', 'fecha_creacion')
    list_filter = ('nombre_municipio',)

    def get_departamento(self, request):
        if request.fk_departamento:
            return f"{request.fk_departamento.nombre_departamento}"
        return ""

    get_departamento.short_description = "Departamento"


admin.site.register(TipoIdentificacion, TipoIdentificacionAdmin)
admin.site.register(Asignatura, AsignaturaAdmin)
admin.site.register(Grado, GradoAdmin)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Municipio, MunicipioAdmin)
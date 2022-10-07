from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


# Register your models here.
class UsuarioIline(admin.StackedInline):
    model = Usuario
    extra = 0

class AdminUser(BaseUserAdmin):
    inlines = (UsuarioIline,)

    def save_model(self, request, obj, form, change):
        obj.save()
        if not change:
            #si no existe
            grupo = Group.objects.get(id = 1) #rol Estudiantes
            obj.groups.add(grupo)
            obj.save()
            obj_usuario = Usuario()
            obj_usuario.fk_user = obj
            obj_usuario.save()
            obj.save()

class AccesoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'estado', 'fecha_creacion',)
    list_filter = ('fk_user',)

    def get_user(self, request):
        if request.fk_user:
            return str(self.fk_user.get_full_name())
        return ""
    get_user.short_description = "Nombre Completo"


class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('fk_user', 'fk_asignatura', 'get_calificacion', 'activo', 'fecha_creacion',)
    list_filter = ('fk_user', 'fk_asignatura',)

    def get_user(self, request):
        if request.fk_user:
            return str(request.fk_user.get_full_name())
        return ""
    
    def get_asignatura(self, request):
        if request.fk_asignatura:
            return str(request.fk_asignatura.nombre_asignatura)
        return ""

    def get_calificacion(self, request):
        if request.calificacion:
            calificacion = float(request.calificacion)
            sticker = ""
            if calificacion == 0:
                sticker = "😰"
            elif calificacion >= 1 and calificacion < 3:
                sticker = "😪"
            elif calificacion >= 3 and calificacion < 4:
                sticker = "🤗"
            elif calificacion >= 4 and calificacion < 5:
                sticker = "😎"
            elif calificacion == 5:
                sticker = "🙀✨"
            return "{} {}".format(request.calificacion, sticker)
        return ""
    
    get_user.short_description = "Nombre Completo"
    get_asignatura.short_description = "Asignatura"
    get_calificacion.short_description = "Calificación"   

admin.site.unregister(User)
admin.site.register(User, AdminUser)
admin.site.register(AccesoUsuario, AccesoUsuarioAdmin)
admin.site.register(Calificacion, CalificacionAdmin)
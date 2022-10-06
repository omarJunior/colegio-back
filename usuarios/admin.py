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

admin.site.unregister(User)
admin.site.register(User, AdminUser)
admin.site.register(AccesoUsuario)
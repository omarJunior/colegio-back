from django.db import models
from django.contrib.auth.models import User
from configuracion.models import (
    Asignatura,
    Grupo,
)

# Create your models here.
class Usuario(models.Model):
    fk_user = models.OneToOneField(User, verbose_name = "Usuario", null=True, blank=True, on_delete=models.CASCADE, related_name="user_usuario", unique=True)


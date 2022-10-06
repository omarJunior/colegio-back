from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from configuracion.models import (
    TipoIdentificacion,
    Asignatura,
    Grupo,
    Departamento,
    Municipio,
)

# Create your models here.
class AccesoUsuario(models.Model):
    fk_user = models.ForeignKey(User, verbose_name="Usuario de acceso", null=True, blank=True, on_delete=models.SET_NULL, related_name="user_acceso")
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(verbose_name="Fecha de actualización", auto_now=True)

    class Meta:
        verbose_name="Acceso Usuario"
        verbose_name_plural = "Acceso de Usuarios"

    def __str__(self):
        return str(self.fk_user)



class Usuario(models.Model):
    fk_user = models.OneToOneField(User, verbose_name = "Usuario", null=True, blank=True, on_delete=models.SET_NULL, related_name="user_usuario", unique=True)
    fk_asignatura = models.ManyToManyField(Asignatura, verbose_name="Asignatura")
    fk_grupo = models.ForeignKey(Grupo, verbose_name="Grupo", null=True, blank=True, on_delete=models.SET_NULL, related_name="grupo_usuario")
    fk_departamento = models.ForeignKey(Departamento, verbose_name="Departamento", on_delete=models.SET_NULL, blank=True, null=True)
    fk_municipio = models.ForeignKey(Municipio, verbose_name="Municipio", on_delete=models.SET_NULL, blank=True, null=True)
    fk_tipoIdentificacion = models.ForeignKey(TipoIdentificacion, verbose_name="Tipo identificacion", null=True, blank=True, on_delete=models.SET_NULL, related_name="tipoidentificacion_usuario")
    numero_identificacion = models.CharField(verbose_name="Numero de identificación", max_length=100, null=True, blank=True)
    choice_genero = (
       ('masculino', "Masculino"),
       ('femenino', "Femenino"),
       ('otro', "Otro"),
    )
    genero = models.CharField(verbose_name="Genero", max_length= 50, choices = choice_genero, null=True, blank=True)
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento", null=True, blank=True)
    direccion = models.CharField(verbose_name="Direccion", max_length = 100, null=True, blank=True)
    telefono = models.CharField(verbose_name="Telefono", max_length = 100, null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(verbose_name="Fecha de actualización", auto_now=True)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return str(self.fk_user)


class Calificacion(models.Model):
    fk_user = models.ForeignKey(User, verbose_name="Usuario de acceso", null=True, blank=True, on_delete=models.SET_NULL, related_name="user_calificacion")
    fk_asignatura = models.ForeignKey(Asignatura, verbose_name="Asignatura", null=True, blank=True, on_delete=models.SET_NULL, related_name="asignatura_calificacion")
    calificacion = models.CharField(verbose_name = "Calificación del usuario", max_length=100, null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(verbose_name="Fecha de actualización", auto_now=True)

    class Meta:
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"

    def __str__(self):
        return str(self.fk_user) + ":" + str(self.fk_asignatura)

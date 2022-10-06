from email.policy import default
from enum import unique
from tabnanny import verbose
from django.db import models

# Create your models here.
class TipoIdentificacion(models.Model):
    codigo = models.CharField(verbose_name="Codigo de identificacion", max_lenght = 100, unique=True)
    sigla = models.CharField(verbose_name="Sigla del tipo identificacion", max_lenght = 10)
    descripcion = models.CharField(verbose_name="Tipo identificacion", max_lenght = 255, unique=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(verbose_name="Fecha de actualización", auto_now=True)

    class Meta:
        verbose_name = "Tipo identificación"
        verbose_name_plural = "Tipos de identificaciónes"

    def __str__(self):
        return str(self.descripcion)


class Asignatura(models.Model):
    codigo = models.CharField(verbose_name="Codigo asignatura", max_lenght = 100, unique=True)
    nombre_asignatura = models.CharField(verbose_name="Asignatura", max_lenght = 255, null = True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(verbose_name="Fecha de actualización", auto_now=True)

    class Meta:
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"

    def __str__(self):
        return str(self.nombre_asignatura)


class Grado(models.Model):
    grado = models.IntegerField(verbose_name="Grado")
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(verbose_name="Fecha de actualización", auto_now=True)

    class Meta:
        verbose_name = "Grado"
        verbose_name_plural = "Grados"
    
    def __str__(self):
        return str(self.grado)


class Grupo(models.Model):
    fk_grado = models.ForeignKey(Grado, verbose_name="Grado", null=True, blank=True, on_delete=models.CASCADE, related_name="grado_grupo")
    codigo = models.CharField(verbose_name="Codigo del grupo", max_lenght = 150, unique=True)
    nombre_grupo = models.CharField(verbose_name="Nombre del grupo", max_length = 255, null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(verbose_name="Fecha de actualización", auto_now=True)

    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"

    def __str__(self):
        return str(self.nombre_grupo)


class Departamento(models.Model):
    codigo = models.CharField(verbose_name="Código del departamento", max_length=50)
    descripcion = models.CharField(verbose_name="Descripción", max_length=255)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return str(self.descripcion)


class Municipio(models.Model):
    fk_departamento = models.ForeignKey(Departamento, verbose_name="Departamento", on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255, verbose_name="Descripción")
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.descripcion)

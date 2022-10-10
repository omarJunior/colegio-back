from rest_framework.routers import DefaultRouter

from .viewsets import *

router = DefaultRouter()
router.register(r'tipo_identificacion', TipoIdentificacionViewSet, basename="tipo_identificacion")
router.register(r'asignatura', AsignaturaViewSet, basename="asignatura")
router.register(r'grado', GradoViewSet, basename="grado")
router.register(r'grupo', GrupoViewSet, basename="grupo")
router.register(r'departamento', DepartamentoViewSet, basename="departamento")
router.register(r'municipio', MunicipioViewSet, basename="municipio")

urlpatterns = router.urls
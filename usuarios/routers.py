from rest_framework.routers import DefaultRouter
from .viewsets import *

router = DefaultRouter()
router.register(r'acceso_usuario', AccesoUsuarioViewSet, basename="acceso_usuario")
router.register(r'usuario', UsuarioViewSet, basename="usuario")
router.register(r'calificacion', CalificacionViewSet, basename="calificacion")

urlpatterns = router.urls
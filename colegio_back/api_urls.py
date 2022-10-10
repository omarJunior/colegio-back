from django.urls import path, include
from usuarios.viewsets import (
    LoginUser,
    RegistroUser,
)

urlpatterns = [
    path('app_config/', include('configuracion.routers')),
    path('app_usuario/', include('usuarios.routers')),
    path('auth/login/', LoginUser.as_view(), name="login_user"),
    path('auth/register/', RegistroUser.as_view(), name="register"),
]
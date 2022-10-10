from django.urls import path, include

urlpatterns = [
    path('app_config/', include('configuracion.routers')),
    path('app_usuario/', include('usuarios.routers')),
]
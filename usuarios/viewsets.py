from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import viewsets, pagination, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import *
from .models import *

class PaginationClass(pagination.PageNumberPagination):
    page_size = 10
    max_page_size = 1000000

class AccesoUsuarioViewSet(viewsets.ModelViewSet):
    queryset = AccesoUsuario.objects.all()
    serializer_class = AccesoUsuarioSerializer
    pagination_class = PaginationClass

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    pagination_class = PaginationClass

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    pagination_class = PaginationClass


class LoginUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        obj_user = authenticate(
            username = username,
            password = password,
            request = request
        )
        if obj_user is not None:
            if obj_user.is_active:
                refresh = RefreshToken.for_user(obj_user)
                obj_persona = Usuario.objects.filter(fk_user = obj_user).first()
                userDict = {
                    'pk': obj_user.pk,
                    'pk_persona': obj_persona.pk if obj_persona else "",
                    'usuario': obj_user.username,
                    'nombre_completo': obj_user.get_full_name(),
                    "roles": [rol.name for rol in obj_user.groups.all()],
                    "refresh": str(refresh),
                    "access_token": str(refresh.access_token),
                }
                return Response(userDict, status=status.HTTP_200_OK)
                
            return Response({'error': 'El usuario se encuentra inactivo'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Usuario o contraseñas incorrectas'}, status=status.HTTP_400_BAD_REQUEST)

class RegistroUser(APIView):
    pass
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
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
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username is None or password is None:
            return Response({'error': 'El username o contraseñas son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

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
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        nombres = request.data.get('nombres', None)
        apellidos = request.data.get('apellidos', None)
        email = request.data.get('email', None)
        password = request.data.get('contrasena', None)
        password2 = request.data.get('contrasena2', None)
        pk_rol = request.data.get('pk_rol', None)
        arr_pksAsignaturas = request.data.get('pk_asignaturas', None)
        pk_grupo = request.data.get('pk_grupo', None)
        pk_departamento = request.data.get('pk_departamento', None)
        pk_municipio = request.data.get('pk_municipio', None)
        pk_tipoIdentificacion = request.data.get('pk_tipoIdentificacion', None)
        numero_identificacion = request.data.get('numero_identificacion', None)
        genero = request.data.get('genero', None)
        fecha_nacimiento = request.data.get('fecha_nacimiento', None)
        direccion = request.data.get('direccion')
        telefono = request.data.get('telefono')

        if nombres is None or apellidos is None:
            return Response({'error': 'Nombres o apellidos requeridos'}, status=status.HTTP_400_BAD_REQUEST)
        if email is None or password is None:
            return Response({'error':'Email o contraseñas requeridas'}, status=status.HTTP_400_BAD_REQUEST)
        if password != password2:
            return Response({'error':'Asegurate de que las contraseñas coincidan'}, status=status.HTTP_400_BAD_REQUEST)

        q_user = User.objects.filter(Q(email = email)| Q(username = email))
        if q_user.count() > 0:
            return Response({'error': 'Ya existe un usuario con ese username o email: {}'.format(email)}, status=status.HTTP_400_BAD_REQUEST)

        obj_user = User()
        obj_user.username = email
        obj_user.email = email
        obj_user.password = make_password(password2)
        obj_user.first_name = nombres
        obj_user.last_name = apellidos
        obj_user.save() 
        obj_user.groups.add(Group.objects.get(id = pk_rol))

        obj_persona = Usuario()
        obj_persona.fk_user = obj_user
        obj_persona.save()
        if arr_pksAsignaturas is not None:
            for asig_pk in arr_pksAsignaturas:
                obj_persona.fk_asignatura.add(Asignatura.objects.get(id = asig_pk))
        if pk_grupo is not None:
            obj_persona.fk_grupo = Grupo.objects.get(id = pk_grupo)
        if pk_departamento is not None:
            obj_persona.fk_departamento = Departamento.objects.get(id = pk_departamento)
        if pk_municipio is not None:
            obj_persona.fk_municipio = Municipio.objects.get(id = pk_municipio)
        if pk_tipoIdentificacion is not None:
            obj_persona.fk_tipoIdentificacion = TipoIdentificacion.objects.get(id = pk_tipoIdentificacion)
        if numero_identificacion is not None:
            obj_persona.numero_identificacion = numero_identificacion
        if genero is not None:
            obj_persona.genero = genero
        if fecha_nacimiento is not None:
            obj_persona.fecha_nacimiento = fecha_nacimiento
        if direccion is not None:
            obj_persona.direccion = direccion
        if telefono is not None:
            obj_persona.telefono = telefono
        obj_persona.save()

        return Response({'msj': 'Registro completado exitosamente'}, status=status.HTTP_201_CREATED)
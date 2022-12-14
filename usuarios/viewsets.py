import base64
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from django.contrib.auth.hashers import check_password, make_password
from django.core.files.base import ContentFile
from django.db.models import Q
from rest_framework import viewsets, pagination, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
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
    serializer_class = UsuarioSerializer
    pagination_class = PaginationClass

    def get_queryset(self):
        qs = Usuario.objects.all()
        return qs
    
    #datos del usuario
    @action(detail=False, methods=['get'], url_path="get_user", url_name="get-user")
    def get_user(self, request):
        if request.user.is_authenticated:
            q_persona = Usuario.objects.filter(fk_user = request.user)
            if q_persona.count() > 0:
                value_persona = Usuario.objects.filter(fk_user = request.user).values('fk_grupo__nombre_grupo', 'fk_departamento__nombre_departamento', 'fk_municipio__nombre_municipio', 'fk_tipoIdentificacion__descripcion', 'numero_identificacion', 'genero', 'fecha_nacimiento', 'direccion', 'telefono',)
                for value in value_persona:
                    try:
                        grupo = value.get('fk_grupo__nombre_grupo')
                    except:
                        grupo = ""

                    try:
                        departamento = value.get('fk_departamento__nombre_departamento')
                    except:
                        departamento = ""

                    try:
                        municipio = value.get('fk_municipio__nombre_municipio')
                    except:
                        municipio = ""

                    try:
                        tipo_identificacion = value.get('fk_tipoIdentificacion__descripcion')
                    except:
                        tipo_identificacion = ""

                    try:
                        numero_identificacion = value.get('numero_identificacion')
                    except:
                        numero_identificacion = ""

                    try:
                        genero = value.get('genero')
                    except:
                        genero = ""

                    try:
                        fecha_nacimiento = value.get('fecha_nacimiento')
                    except:
                        fecha_nacimiento = ""

                    try:
                        direccion = value.get('direccion')
                    except:
                        direccion = ""
                    
                    try:
                        telefono = value.get('telefono')
                    except:
                        telefono = ""

                userData = {
                    "nombre_completo": request.user.get_full_name(),
                    "username": request.user.username,
                    "email": request.user.email,
                    "asignatura": [asig.nombre_asignatura for asig in q_persona[0].fk_asignatura.all()],
                    "grupo ": grupo,
                    "departamento": departamento ,
                    "municipio": municipio,
                    "tipo_identificacion": tipo_identificacion,
                    "numero_identificacion": numero_identificacion,
                    "genero": genero,
                    "fecha_nacimiento": fecha_nacimiento,
                    "direccion": direccion,
                    "telefono": telefono,
                }
                return Response(userData, status=status.HTTP_200_OK)

            return Response({'error': 'Ha ocurrido un error'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'El usuario debe estar autenticado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path="update_user", url_name="update-user")
    def update_user(self, request):
        try:
            foto_perfil = request.data['foto_perfil']
        except:
            foto_perfil = None

        try:
            username = request.data['username']
        except:
            username = None

        try:
            first_name = request.data['first_name']
        except:
            first_name = None

        try:
            last_name = request.data['last_name']
        except:
            last_name = None

        try:
            telefono = request.data['telefono']
        except:
            telefono = None

        try:    
            direccion = request.data['direccion']
        except:
            direccion = None

        obj_user = User.objects.filter(id = request.user.id).first()
        if obj_user is not None:
            obj_usuario = Usuario.objects.filter(fk_user = obj_user).first()
            if obj_usuario is not None:
                if username is not None:
                    q_user = User.objects.filter(username = username)
                    if q_user.count() > 0:
                        user = q_user.first()
                        if user.id == obj_user.id:
                            obj_user.username = username
                        else:
                            return Response({'error': 'El username ya existe en la base de datos'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        obj_user.username = username

                if first_name is not None:
                    obj_user.first_name = first_name
                if last_name is not None:
                    obj_user.last_name = last_name
                obj_user.save()

                if foto_perfil is not None:
                    try:
                        format, imgstr = foto_perfil.split(';base64,') 
                        ext = format.split('/')[-1] 
                        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext) # You can save this
                        obj_usuario.f_fotoPerfil = data
                    except:
                        pass

                if telefono is not None:
                    obj_usuario.telefono = telefono

                if direccion is not None:
                    obj_usuario.direccion = direccion
                obj_usuario.save()

                return Response({'msj': 'Datos actualizados correctamente'}, status=status.HTTP_200_OK)
            
            return Response({'error': 'Ha ocurrido un error'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'El usuario no existe'}, status=status.HTTP_400_BAD_REQUEST)
    
    #registrar grupo y asignaturas
    @action(detail=False, methods=['post'], url_path="register_group", url_name="register-group")
    def register_group(self, request):
        asignaturas_pk = request.data['asignaturas_pk']
        grupo_pk = request.data['grupo_pk']

        arreglo_ids = []
        hasAsignatura = True
        for x in asignaturas_pk:
            CONT_ASIGN = Asignatura.objects.filter(id = x).count()
            if CONT_ASIGN == 0:
                arreglo_ids.append(str(x))
                hasAsignatura = False

        if not hasAsignatura:
            c_asignaturas = ','.join(arreglo_ids)
            return Response({'error':f'Las siguientes asignaturas con el id no existen: {c_asignaturas}.'}, status=status.HTTP_400_BAD_REQUEST)
        q_asignatura = Asignatura.objects.filter(pk__in = asignaturas_pk)
        if q_asignatura.count() != len(asignaturas_pk):
            return Response({'error': 'Una de las asignaturas escogidas no existen'}, status=status.HTTP_400_BAD_REQUEST)

        obj_grupo = Grupo.objects.filter(id = grupo_pk).first()
        if obj_grupo is None:
            return Response({'error': f'No existe un grupo con el id: {grupo_pk}'}, status=status.HTTP_400_BAD_REQUEST)

        obj_usuario = Usuario.objects.filter(fk_user = request.user, fk_grupo__isnull=False).first()

        if obj_usuario is not None:
            if obj_usuario.fk_grupo.pk == obj_grupo.pk: 
                for asign in asignaturas_pk:
                    try:
                        obj_usuario.fk_asignatura.add(Asignatura.objects.get(pk = asign))
                    except:
                        pass
            else:
                return Response({'error': f'El usuario: {obj_usuario.fk_user.get_full_name()} ya se encuentra asignado en el grupo: {obj_usuario.fk_grupo.nombre_grupo.upper()}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            obj_usuario = Usuario.objects.filter(fk_user = request.user).first()
            obj_usuario.fk_grupo = obj_grupo
            obj_usuario.save()
            for asig in asignaturas_pk:
                try:
                    obj_usuario.fk_asignatura.add(Asignatura.objects.get(pk = asig))
                except:
                    pass
        return Response({'msj': 'Datos registrados correctamente'}, status=status.HTTP_201_CREATED)


    #registrar calificacion
    @action(detail=False, methods=['post'], url_path="add_calification", url_name="add-calification")
    def add_calification(self, request):
        pk_profesor = request.data['pk_profesor']
        calificacion = request.data['calificacion']

        obj_persona = Usuario.objects.filter(fk_user__pk = pk_profesor).first()
        if obj_persona is None:
            return Response({'error': 'No existe una persona con el id: {}'.format(obj_persona.pk)}, status=status.HTTP_400_BAD_REQUEST)

        q_calificacion = CalificacionPersona.objects.filter(fk_user = request.user, fk_docente = obj_persona.fk_user)
        if q_calificacion.count() > 0:
            return Response({'error': f'{request.user.get_full_name()} ya ha calificado al docente {obj_persona.fk_user.get_full_name()}'}, status=status.HTTP_400_BAD_REQUEST)
    
        contador = 1
        if obj_persona.calificacion:
            obj_persona.calificacion = (int(obj_persona.calificacion) + int(calificacion))  / (obj_persona.conteo + contador)
            obj_persona.conteo += contador
        else:
            obj_persona.calificacion = calificacion 
            obj_persona.conteo = contador

        obj_persona.save()

        obj_calificacion = CalificacionPersona()
        obj_calificacion.fk_user = request.user
        obj_calificacion.fk_docente = obj_persona.fk_user
        obj_calificacion.calificacion = calificacion
        obj_calificacion.save()
        return Response({'msj': 'Calificaci??n con exito'}, status=status.HTTP_201_CREATED)


class CalificacionViewSet(viewsets.ModelViewSet):
    serializer_class = CalificacionSerializer
    pagination_class = PaginationClass

    def get_queryset(self):
        qs = Calificacion.objects.all().order_by('calificacion')

        pk_usuario = self.request.query_params.get('pk_usuario')
        pk_asignatura = self.request.query_params.get('pk_asignatura')
        calificacion = self.request.query_params.get('calificacion')

        if pk_usuario is not None:
            qs = qs.filter(fk_user__pk = pk_usuario)

        if pk_asignatura is not None:
            qs = qs.filter(fk_asignatura__pk = pk_asignatura)

        if calificacion is not None:
            qs = qs.filter(calificacion = calificacion)

        return qs 


class CalificacionPersonaViewSet(viewsets.ModelViewSet):
    queryset = CalificacionPersona.objects.all()
    serializer_class = CalificacionPersonaSerializer
    pagination_class = PaginationClass    


class LoginUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username is None or password is None:
            return Response({'error': 'El username o contrase??as son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

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

                AccesoUsuario.objects.create(fk_user = obj_user)

                return Response(userDict, status=status.HTTP_200_OK)
                
            return Response({'error': 'El usuario se encuentra inactivo'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Usuario o contrase??as incorrectas'}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({'error':'Email o contrase??as requeridas'}, status=status.HTTP_400_BAD_REQUEST)
        if password != password2:
            return Response({'error':'Asegurate de que las contrase??as coincidan'}, status=status.HTTP_400_BAD_REQUEST)

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
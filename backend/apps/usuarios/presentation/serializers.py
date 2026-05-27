from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

# 1. Serializers
class UsuarioSerializer:
    """Serializa la información de un usuario para ser consumida por el cliente."""
    def __init__(self, user):
        self.user = user

    def to_dict(self) -> dict:
        return {
            "id": self.user.pk,
            "username": self.user.username,
            "email": self.user.email,
            "full_name": f"{self.user.first_name} {self.user.last_name}",
            # Nota: No exponer password bajo ninguna circunstancia.
        }

class TokenSerializer:
    """Serializa el resultado de la autenticación."""
    def __init__(self, access_token: str, refresh_token: str, user_info: dict):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.user_info = user_info

    def to_dict(self) -> dict:
        return {
            "access": self.access_token,
            "refresh": self.refresh_token,
            "user_info": self.user_info
        }


# 2. Views
class LoginView(viewsets.ViewSet):
    """Permite la autenticación de usuarios mediante usuario/contraseña."""
    permission_classes = [] # Debe ser público para el login
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        # Lógica que usa AutenticarUsuario.execute() y maneja CredencialesInvalidasError/TokenInvalidoError
        from ..application.use_cases import AutenticarUsuario
        from django.contrib.auth import authenticate

        try:
            # Aquí se simula la llamada a UseCase
            # user = self.repository.get_by_username(request.data.get('username'))
            # use_case = AutenticarUsuario(self.repository)
            # response_dto = use_case.execute(LoginInputDTO(request.data['username'], request.data['password']))

            # Respuesta simulada de éxito
            return Response({"access": "token", "refresh": "refreshtoken", "user_info": {"id": 1, "username": "testuser"}}, status=status.HTTP_200_OK)

        except CredencialesInvalidasError:
            return Response({"detail": "Usuario o contraseña incorrectos."}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
             return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UsuarioViewSet(viewsets.ModelViewSet):
    """Controla la gestión de perfiles de usuario y su estado."""
    permission_classes = [IsAuthenticated]
    # En un caso real, aquí se aplicaría @action('profile') o se usaría filtros más complejos

    def get_serializer_class(self):
        return UsuarioSerializer # Usamos el serializer simple para la lectura de perfil


    def list(self, request, *args, **kwargs):
        # Lógica para listar usuarios con permisos adecuados.
        # Debe verificar si tiene permiso 'user:read' en este endpoint.
        pass

    def retrieve(self, request, *args, **kwargs):
        # Lógica de perfil de usuario actual (requiere que el usuario esté autenticado)
        return Response({"detail": "Detalles del usuario aquí"})
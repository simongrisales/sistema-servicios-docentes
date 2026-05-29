from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from ..application.dtos import UsuarioInputDTO

from ..application.use_cases import CrearUsuario, ListarRoles, ListarUsuarios
from ..infrastructure.repositories import UsuariosRepository
from .serializers import RolSerializer, UsuarioSerializer


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


class LoginConRecaptchaView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Valida recaptcha_token (cuando aplique) y luego autentica con simplejwt."""
        recaptcha_token = request.data.get("recaptcha_token", "")

        # django-recaptcha==4.0.0 no expone recaptcha_client en la misma ruta.
        # Validamos vía el formulario field para mantener compatibilidad.
        if recaptcha_token:
            field = ReCaptchaField(widget=ReCaptchaV2Checkbox())
            field.clean(recaptcha_token, None)


        return super().post(request, *args, **kwargs)


    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class UsuarioViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def _repo(self) -> UsuariosRepository:
        return UsuariosRepository()

    def list(self, request):
        usuarios = ListarUsuarios(self._repo()).execute()
        return Response(UsuarioSerializer(usuarios, many=True).data)

    def create(self, request):
        serializer = UsuarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = CrearUsuario(self._repo()).execute(
            UsuarioInputDTO(**serializer.validated_data)
        )
        return Response(
            UsuarioSerializer(usuario).data,
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None):
        usuario = self._repo().find_by_id(pk)
        if usuario is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(UsuarioSerializer(usuario).data)

    @action(detail=False, methods=["get"], url_path="roles")
    def roles(self, request):
        roles = ListarRoles(self._repo()).execute()
        return Response(RolSerializer(roles, many=True).data)

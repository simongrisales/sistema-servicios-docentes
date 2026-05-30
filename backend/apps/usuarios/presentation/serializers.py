from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Usuario"))
    password = serializers.CharField(write_only=True, label=_("Contrasena"))
    recaptcha_token = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
        label=_("Token reCAPTCHA"),
    )


class UsuarioSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(label=_("Usuario"))
    email = serializers.EmailField(label=_("Correo electronico"))
    password = serializers.CharField(
        write_only=True,
        required=False,
        label=_("Contrasena"),
    )
    role_code = serializers.CharField(
        required=False,
        allow_blank=True,
        label=_("Codigo de rol"),
    )
    role_name = serializers.CharField(read_only=True, label=_("Nombre del rol"))
    departamento = serializers.CharField(
        required=False,
        allow_blank=True,
        label=_("Departamento"),
    )
    cargo = serializers.CharField(
        required=False,
        allow_blank=True,
        label=_("Cargo"),
    )


class RolSerializer(serializers.Serializer):
    role_id = serializers.IntegerField(label=_("ID del rol"))
    code = serializers.CharField(label=_("Codigo"))
    name = serializers.CharField(label=_("Nombre"))
    description = serializers.CharField(label=_("Descripcion"))


class RolInputSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50, label=_("Codigo"))
    name = serializers.CharField(max_length=100, label=_("Nombre"))
    description = serializers.CharField(
        allow_blank=True,
        required=False,
        label=_("Descripcion"),
    )


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField(label=_("Token de acceso"))
    refresh = serializers.CharField(label=_("Token de renovacion"))

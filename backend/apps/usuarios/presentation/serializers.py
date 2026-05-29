from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    recaptcha_token = serializers.CharField(
        required=False, allow_blank=True, write_only=True
    )


class UsuarioSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=False)
    role_code = serializers.CharField(required=False, allow_blank=True)
    role_name = serializers.CharField(read_only=True)
    departamento = serializers.CharField(required=False, allow_blank=True)
    cargo = serializers.CharField(required=False, allow_blank=True)


class RolSerializer(serializers.Serializer):
    role_id = serializers.IntegerField()
    code = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

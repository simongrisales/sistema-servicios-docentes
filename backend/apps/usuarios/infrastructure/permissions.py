from rest_framework.permissions import BasePermission


class RolPermissionBase(BasePermission):
    required_roles: tuple[str, ...] = ()

    def has_permission(self, request, view) -> bool:
        user = getattr(request, "user", None)
        if user is None or not user.is_authenticated:
            return False

        if user.is_superuser or user.is_staff:
            return True

        role_code = getattr(user, "role_code", "") or getattr(
            getattr(user, "role", None),
            "code",
            "",
        )
        return role_code in self.required_roles


class EsAdministrador(RolPermissionBase):
    required_roles = ("administrador",)


class EsLiderDOC(RolPermissionBase):
    required_roles = ("lider_doc", "lider_sd")


class EsAuxiliarDOC(RolPermissionBase):
    required_roles = ("auxiliar_doc", "auxiliar_sd")


class EsFacultad(RolPermissionBase):
    required_roles = ("facultad",)


class EsAdmisiones(RolPermissionBase):
    required_roles = ("admisiones",)


class EsAdministradorOLiderDOC(RolPermissionBase):
    required_roles = ("administrador", "lider_doc", "lider_sd")

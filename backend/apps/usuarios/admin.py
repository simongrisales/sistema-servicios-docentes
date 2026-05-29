from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .infrastructure.models import PermissionModel, RoleModel, UsuarioModel


@admin.register(UsuarioModel)
class UsuarioModelAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Información Académica/Rol", {"fields": ("role", "departamento", "cargo")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Información Académica/Rol", {"fields": ("role", "departamento", "cargo")}),
    )
    list_display = ("username", "email", "role", "departamento", "is_staff")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "departamento")


@admin.register(RoleModel)
class RoleModelAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "description")
    search_fields = ("name", "code")


@admin.register(PermissionModel)
class PermissionModelAdmin(admin.ModelAdmin):
    list_display = ("resource", "action", "description")
    search_fields = ("resource", "action")

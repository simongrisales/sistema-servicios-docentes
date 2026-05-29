"""Admin de la app parametros."""

from django.contrib import admin

from .infrastructure.models import CatalogoParametroModel


@admin.register(CatalogoParametroModel)
class CatalogoParametroAdmin(admin.ModelAdmin):
    list_display = ("clave", "grupo", "activo", "actualizado_en")
    list_filter = ("grupo", "activo")
    search_fields = ("clave", "descripcion")
    ordering = ("grupo", "clave")
    readonly_fields = ("creado_en", "actualizado_en")

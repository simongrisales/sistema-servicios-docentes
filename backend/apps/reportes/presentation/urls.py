# backend/apps/reportes/presentation/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReporteViewSet

router = DefaultRouter()

# Ruta principal para listar y solicitar reportes (POST)
router.register(r'reportes', ReporteViewSet, basename='reporte')

urlpatterns = [
    path('', include(router.urls)), # /api/reportes/
]
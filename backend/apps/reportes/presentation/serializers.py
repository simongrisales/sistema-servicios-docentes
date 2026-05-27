# backend/apps/reportes/presentation/serializers.py
from rest_framework import serializers
from backend.apps.reportes.domain.entities import ReporteTipo, Reporte
from backend.apps.reportes.infrastructure.models import ReporteModel, ReporteTipoModel

class ReporteTipoSerializer(serializers.ModelSerializer):
    """Serializador para la configuración de tipos de reporte."""
    class Meta:
        model = ReporteTipoModel
        fields = ['codigo', 'nombre_completo', 'descripcion']

class ReporteSerializer(serializers.ModelSerializer):
    """Serializador para exponer el estado y detalles de un reporte solicitado."""
    # Campos principales del modelo base
    reporte_id = serializers.IntegerField()
    titulo = serializers.CharField()
    fecha_solicitud = serializers.DateTimeField()
    periodo_inicio = serializers.DateField()
    periodo_fin = serializers.DateField()
    estado = serializers.CharField(read_only=True)

    # Campo calculado o agregado desde la capa de dominio
    contenido_estructurado = serializers.JSONField(required=False, allow_null=True)

    class Meta:
        model = ReporteModel
        fields = [
            'reporte_id',
            'titulo',
            'fecha_solicitud',
            'periodo_inicio',
            'periodo_fin',
            'estado',
            'contenido_estructurado'
        ]

    # Overriding read/write logic si es necesario, pero para exposición de estado es suficiente.
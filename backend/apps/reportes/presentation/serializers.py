from rest_framework import serializers


class ReporteSolicitudSerializer(serializers.Serializer):
    reporte_tipo_codigo = serializers.CharField()
    periodo_inicio = serializers.DateField()
    periodo_fin = serializers.DateField()


class ReporteSerializer(serializers.Serializer):
    reporte_id = serializers.IntegerField()
    titulo = serializers.CharField()
    estado = serializers.CharField()
    contenido_estructurado = serializers.JSONField(required=False, allow_null=True)


class ReporteTipoSerializer(serializers.Serializer):
    codigo = serializers.CharField()
    nombre_completo = serializers.CharField()
    descripcion = serializers.CharField()

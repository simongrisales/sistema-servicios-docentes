from rest_framework import serializers
from ..domain.entities import Aula, Grupo # Importaciones de Entidades para serialización

# --- Serializers de Aulas y Recursos Físicos ---

class AulaSerializer(serializers.ModelSerializer):
    """Serializador para exponer el estado completo de un aula."""
    class Meta:
        model = 'apps.academico.infrastructure.models.AulaModel' # Referencia al modelo ORM
        fields = ['id', 'nombre', 'capacidad', 'tipo', 'disponible', 'restricciones']

class AulaOutputSerializer(serializers.Serializer):
    """Serializador para los resultados de búsqueda (ej: disponibles)."""
    aula_id = serializers.IntegerField()
    nombre = serializers.CharField()
    capacidad = serializers.IntegerField()
    tipo = serializers.CharField()
    disponible = serializers.BooleanField()

# --- Serializers de Grupos y Academia ---

class GrupoSerializer(serializers.ModelSerializer):
    """Serializador para la gestión de grupos."""
    curso_nombre = serializers.CharField(source='curso.nombre', read_only=True)
    docente_nombre = serializers.CharField(source='docente.nombre', read_only=True)

    class Meta:
        model = 'apps.academico.infrastructure.models.GrupoModel' # Referencia al modelo ORM
        fields = ['id', 'curso', 'docente', 'num_estudiantes', 'semestre',
                  'curso_nombre', 'docente_nombre']

# Serializadores de Reglas y Catálogos (Para la gestión de reglas)
class ReglaSerializer(serializers.ModelSerializer):
    """Serializador para las reglas de negocio."""
    class Meta:
        model = 'apps.academico.infrastructure.models.ReglaNegocioModel'
        fields = '__all__'
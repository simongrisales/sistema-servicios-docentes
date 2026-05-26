from rest_framework import viewsets, mixins
from django.conf import settings
from ..application.use_cases import UseCasesService
from .serializers import AulaOutputSerializer, GrupoSerializer

class AcademicoViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ViewSet principal que maneja la lógica de negocio académica.
    Se utiliza para exponer los casos de uso principales.
    """
    # Nota: Los permisos deben ser controlados a nivel de clase/método en producción (e.g., IsLiderDoc)

    def get_service(self):
        """Obtiene una instancia del UseCasesService con las dependencias inyectadas."""
        return UseCasesService(
            aula_repo=None, # Se debe inicializar con el repositorio concreto
            grupo_repo=None,
            curso_repo=None,
            docente_repo=None
        )

    def list(self, request):
        """Lista aulas disponibles para un bloque horario dado (Llamado desde la vista de Dashboard)."""
        # 1. Obtener el bloque horario del contexto o parámetros (ej. query params)
        horario = None # Placeholder: Debe extraerse de los parámetros de consulta

        if not horario:
            return Response({"detail": "Debe proporcionar un rango horario para la búsqueda."})

        try:
            service = self.get_service()
            # 2. Llamar al caso de uso
            aulas_dtos = service.listar_aulas_disponibles(horario)

            # 3. Serializar y devolver los resultados
            serializer_list = AulaOutputSerializer(aulas_dtos, many=True)
            return Response(serializer_list.data)

        except Exception as e:
            return Response({"detail": f"Error al listar aulas: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def execute_assignment(self, request):
        """Endpoint para ejecutar la asignación automática de un grupo."""
        # 1. Validar entrada (GrupoInputDTO y HorarioBloque)
        try:
            service = self.get_service()
            # Placeholder: Se extraen DTOs desde los datos del request body
            grupo_dto = GrupoInputDTO(group_id=request.data.get('group_id'), curso_id=1, docente_id=1, num_estudiantes=10)
            horario_bloque = HorarioBloque(dia="Lunes", hora_inicio=8.5, hora_fin=9.5) # Placeholder

            # 2. Llamar al caso de uso y recibir resultado (string o DTO)
            resultado = service.ejecutar_asignacion_automatica(grupo_output=GrupoOutputDTO(**grupo_dto.__dict__), horario=horario_bloque)
            return Response({"success": True, "message": resultado})

        except Exception as e:
            # Capturar errores de dominio y devolverlos con buen status code
            if hasattr(e, 'message'): # Si es una excepción de dominio personalizada
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": f"Error al ejecutar la asignación: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# NOTA IMPORTANTE: Estos ViewSets son conceptuales y requieren el setup de las dependencias reales (repositorios concretos, etc.)
"""
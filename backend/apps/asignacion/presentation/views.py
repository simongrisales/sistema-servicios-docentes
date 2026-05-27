from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# Importar DTOs y Use Cases del módulo application
from asignacion.application.dtos import AsignacionInputDTO, SimulacionInputDTO
from asignacion.application.use_cases import (
    EjecutarAsignacionAutomatica,
    SimularAsignacion,
    ValidarConflictos,
    VerificarCoberturaTotalGrupos
)
# Importar Serializers definidos en este mismo módulo
from .serializers import SerializacionAsignacion, SerializacionResultadoAsignacion, SerializacionCoberturaOutput

class AsignacionViewSet(viewsets.ViewSet):
    """Viewset para manejar las operaciones críticas de asignación."""

    queryset = None # No usamos queryset directamente, la lógica va en los use cases
    serializer_class = SerializacionResultadoAsignacion

    def list(self, request):
        # Este endpoint podría listar grupos o aulas para referencia rápida.
        return Response({"detail": "Endpoint de listing no implementado en esta versión."})

    def create(self, request):
        """POST /api/asignacion/ejecutar - Ejecuta la asignación automática."""
        serializer = SerializacionAsignacion(data=request.data)
        if not serializer.is_valid():
            return Response({"detail": "Datos inválidos", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. Mapear datos a DTOs
            input_dto = AsignacionInputDTO(
                grupo_id=serializer.validated_data['grupo_id'],
                semestre=serializer.validated_data['semestre'],
                fecha_inicio=serializer.validated_data['fecha_inicio'],
                fecha_fin=serializer.validated_data['fecha_fin']
            )

            # 2. Ejecutar el caso de uso
            resultado = EjecutarAsignacionAutomatica(input_dto).execute()

            # 3. Serializar y retornar resultados
            result_serializer = SerializacionResultadoAsignacion(resultado.get_result())
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Capturar excepciones de dominio como AsignacionConflictoError o DatosIncompletosError
            print(f"Error al ejecutar asignación: {e}")
            return Response({"detail": f"Error crítico en el proceso de asignación: {str(e)}"}, status=status.HTTP_409_CONFLICT)

    def perform_simulation(self, request):
        """POST /api/asignacion/simular - Simula la asignación sin afectar datos reales."""
        serializer = SerializacionAsignacion(data=request.data)
        if not serializer.is_valid():
            return Response({"detail": "Datos inválidos", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. Mapear datos a DTOs
            input_dto = AsignacionInputDTO(
                grupo_id=serializer.validated_data['grupo_id'],
                semestre=serializer.validated_data['semestre'],
                fecha_inicio=serializer.validated_data['fecha_inicio'],
                fecha_fin=serializer.validated_data['fecha_fin']
            )

            # 2. Ejecutar el caso de uso
            resultado = SimularAsignacion(input_dto).execute()

            # 3. Serializar y retornar resultados
            result_serializer = SerializacionResultadoAsignacion(resultado.get_result())
            return Response({"detail": "Simulación exitosa.", "data": result_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error al simular asignación: {e}")
            return Response({"detail": f"Error crítico en la simulación: {str(e)}"}, status=status.HTTP_409_CONFLICT)

    def verificar_cobertura(self, request):
        """GET /api/asignacion/verificar-cobertura - Verifica si todos los grupos tienen asignación."""
        try:
            # Ejecutar la validación sin DTOs de entrada
            resultado = VerificarCoberturaTotalGrupos().execute()

            serializer = SerializacionCoberturaOutput(resultado.get_result())
            return Response({"detail": "Verificación completada.", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error al verificar cobertura: {e}")
            return Response({"detail": f"Error en la verificación de cobertura: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
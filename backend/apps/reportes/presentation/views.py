# backend/apps/reportes/presentation/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from backend.apps.reportes.domain.interfaces import IReporteRepository
from backend.apps.reportes.application.use_cases import ReporteService
from .serializers import ReporteSerializer, ReporteTipoSerializer


class ReporteViewSet(viewsets.ModelViewSet):
    """ViewSet principal para la gestión de reportes."""
    # Nota: En un entorno real, esto debería filtrar por permisos de usuario (user.role)

    def get_queryset(self):
        """Permite listar todos los reportes solicitados por el usuario autenticado."""
        # Debería filtrar para mostrar solo los reportes del usuario actual
        return ReporteModel.objects.filter(usuario_solicitante=self.request.user)

    def list(self, request):
        """Lista los reportes generados por el usuario."""
        serializer = ReporteSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['post'])
    def solicitar(self, request):
        """Endpoint para iniciar la generación de un reporte asíncrono."""
        try:
            # 1. Validación de datos del cuerpo (debería usar un serializer específico DTO)
            data = request.data
            reporte_tipo_codigo = data['reporte_tipo_codigo']
            periodo_inicio = data['periodo_inicio'] # Fecha YYYY-MM-DD
            periodo_fin = data['periodo_fin']

            # 2. Obtener el repositorio inyectado o instanciarlo globalmente
            repo: IReporteRepository = self.get_serializer().reporte_repo # Asumimos que la dependencia se inyecta aquí
            service = ReporteService(repo)

            # 3. Ejecutar Caso de Uso (genera el ID y dispara Celery en background)
            input_dto = ReporteInputDTO(
                reporte_tipo_codigo=reporte_tipo_codigo,
                periodo_inicio=periodo_inicio,
                periodo_fin=periodo_fin,
                usuario_id=request.user.id # Asumiendo que el usuario está autenticado y tiene un ID
            )

            reporte_id = service.ejecutar_generacion_asincrona(input_dto)
            return Response({'message': 'Solicitud de reporte iniciada con éxito.', 'reporte_id': reporte_id}, status=status.HTTP_202_ACCEPTED)

        except TipoReporteInvalidoError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Captura de errores generales y devuelve un error 500 para el cliente
            return Response({"error": f"Error al procesar la solicitud: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=True, methods=['get'])
    def obtener_estado(self, request, pk):
        """Endpoint para verificar el estado actual de un reporte solicitado."""
        try:
            # 1. Obtener repositorio e instancia del servicio (se haría mejor con Dependency Injection)
            repo: IReporteRepository = self.get_serializer().reporte_repo
            service = ReporteService(repo)

            # 2. Ejecutar caso de uso para obtener el estado
            output_dto = service.obtener_estado_reporte(pk)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError as e:
             return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Error al obtener estado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Nota: Se necesita un mecanismo de inyección de dependencias (DI) o global para pasar el repositorio y servicio en la práctica.
# Este ejemplo muestra la lógica funcional usando suposiciones de contexto Django REST Framework.
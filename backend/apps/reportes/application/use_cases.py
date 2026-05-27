# reportes/application/use_cases.py
from datetime import date
from typing import Optional, List

# Importaciones de la capa Domain y DTOs locales
from backend.apps.reportes.domain.entities import ReporteTipo, Reporte, DatoReporteItem
from backend.apps.reportes.domain.interfaces import IReporteRepository, IReporteGenerador
from backend.apps.reportes.domain.exceptions import TipoReporteInvalidoError, DatosInsufficientError
from backend.apps.reportes.application.dtos import ReporteInputDTO, ReporteOutputDTO, SimulaciónInputDTO

class ReporteService:
    """Orquestador de casos de uso para la gestión completa de reportes."""

    def __init__(self, reporte_repo: IReporteRepository):
        self.reporte_repo = reporte_repo

    async def ejecutar_generacion_asincrona(self, dto: ReporteInputDTO) -> int:
        """
        Caso de Uso Principal: Inicia la petición de un reporte pesado en el fondo (Celery).
        Devuelve el ID del reporte solicitado.
        """
        # 1. Validar tipo y parámetros iniciales
        self._validar_reporte_tipo(dto.reporte_tipo_codigo)

        # 2. Crear la solicitud de reporte en la infraestructura (Esto crea el registro con estado PENDIENTE)
        nuevo_reporte = Reporte(
            tipo_codigo=dto.reporte_tipo_codigo,
            titulo=f"Solicitud {ReporteTipo('TBD', 'Título', 'desc').nombre_completo}", # Título provisional
            fecha_generacion=date.today(),
            periodo_inicio=dto.periodo_inicio,
            periodo_fin=dto.periodo_fin,
            descripcion_detallada="Generación de reporte a través de la API.",
            estado="PENDIENTE",
            usuario_solicitante_id=dto.usuario_id
        )

        reporte_id = self.reporte_repo.create_report_request(nuevo_reporte)

        # 3. Disparar la tarea de Celery (esto es lo que se llama en tasks.py/infraestructura)
        # from .tasks import generate_celery_report
        # generate_celery_report.delay(reporte_id) # <- Llamada real a la cola

        return reporte_id

    def obtener_estado_reporte(self, reporte_id: int) -> ReporteOutputDTO:
        """Consulta el estado de un reporte generado previamente."""
        try:
            reporte = self.reporte_repo.get_reporte_by_id(reporte_id)

            if not reporte:
                raise ValueError("Reporte no encontrado.")

            # Mapeo del objeto Reporte a DTO de salida
            return ReporteOutputDTO(
                reporte_id=reporte.reporte_id,
                titulo=reporte.titulo,
                estado=reporte.estado,
                contenido_estructurado=reporte.datos_raw if reporte.estado == "COMPLETO" else None
            )
        except ValueError as e:
            raise e

    def simular_generacion(self, dto: SimulaciónInputDTO):
        """
        Caso de Uso para simulación local (sin impactar datos reales ni disparar Celery).
        Sirve para que el frontend muestre resultados "qué pasaría si".
        """
        print("Ejecutando lógica de simulación del reporte.")
        # Aquí se llama a la lógica de negocio pura, sin tocar repositorios.

        return ReporteOutputDTO(
            reporte_id=-1, # No tiene ID real
            titulo=f"Simulación exitosa para {dto.periodo_inicio} - {dto.periodo_fin}",
            estado="SIMULADO",
            contenido_estructurado={"mensaje": "La simulación fue exitosa.", "detalles": "Ningún dato fue escrito en la BD."}
        )

    def _validar_reporte_tipo(self, codigo: str):
        """Método auxiliar para validar si el tipo de reporte es conocido."""
        # En un sistema real, se consultaría el repositorio o una tabla de configuración.
        if not ReporteTipo('TBD', 'Nombre Dummy', 'Desc').codigo == codigo: # Simplificación
            raise TipoReporteInvalidoError(f"Código de reporte '{codigo}' no es válido.")

# Nota: Los métodos reales (como el procesamiento pesado) se ejecutarán en tasks.py/Celery Worker.
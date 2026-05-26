from django.db import transaction, IntegrityError
# Importaciones del Dominio (para mapear los datos)
from ..domain.entities import Aula, Grupo, Docente, Curso, HorarioBloque
# Importaciones de Infraestructura y BaseRepository
from .models import * # Importa todos los modelos definidos en models.py
from core.repositories import BaseRepository

class AcademicoRepository(BaseRepository):
    """Clase base que agrupa la lógica de repositorio para el módulo académico."""

    # --- Aulas y Recursos Físicos ---
    def find_available_aulas(self, horario_bloque: HorarioBloque) -> List[Aula]:
        """Busca aulas disponibles en un bloque horario específico."""
        try:
            # Query a AulaModel buscando aquellas que no tienen ninguna asignación/reserva en el mismo slot.
            count_conflicto = AulaModel.objects.filter(
                bloque_horario=horario_bloque
            ).exclude(
                asignaciones__estado='CONFIRMADO'
            ).count()

            # Simplificación: solo devolvemos aulas con asignación cero en este bloque horario
            aulas_disponibles = AulaModel.objects.filter(id__in=self.get_all_aula_ids()).exclude(
                asignaciones__bloque_horario=horario_bloque,
                asignaciones__estado='CONFIRMADO'
            )

            # Mapeo de ORM a Entidad de Dominio
            return [Aula(
                id=a.id,
                nombre=a.nombre,
                capacidad=a.capacidad,
                tipo=a.tipo,
                disponible=(len(aulas_disponibles) > 0), # Simplificado: asumir disponible si no hay conflicto visible
                restricciones=list(a.restricciones) if a.restricciones else []
            ) for a in aulas_disponibles]

        except Exception as e:
             print(f"Error al buscar disponibilidad de aulas: {e}")
             return []


    # --- Grupos y Curso ---
    def get_grupos_por_curso(self, curso_id: int) -> List[Grupo]:
        """Obtiene todos los grupos asociados a un curso dado."""
        try:
            groups = GrupoModel.objects.filter(curso=curso_id).select_related('docente')
            return [Grupo(
                id=g.id,
                curso_id=g.curso.id,
                docente_id=g.docente.usuario_id,
                num_estudiantes=g.num_estudiantes,
                semestre=g.semestre
            ) for g in groups]
        except Exception as e:
             print(f"Error al obtener grupos por curso {curso_id}: {e}")
             return []

    # Métodos auxiliares (simulación de la complejidad real):
    def get_all_aula_ids(self) -> list[int]:
        """Simula obtención de todos los IDs de aula existentes."""
        try:
            return list(AulaModel.objects.values_list('id', flat=True'))
        except Exception as e:
             print(f"Error al obtener IDs de aulas: {e}")
             return []

    # --- Transacciones críticas (Ejemplo) ---
    @transaction.atomic
    def asignar_aula_transaccion(self, grupo_id: int, aula_id: int, bloque_horario: HorarioBloque):
        """Intenta asegurar la asignación de aula y prevenir conflictos."""
        try:
            # 1. Verificar si el aula ya está comprometida en ese horario por otro proceso/grupo (Integridad)
            if AulaModel.objects.filter(id=aula_id).exclude(restricciones__contains='DISPONIBLE').exists():
                raise Exception("Aula ya comprometida con restricciones.")

            # 2. Crear la asignación
            AsignacionModel.objects.create(
                grupo_id=grupo_id,
                aula_id=aula_id,
                bloque_horario=bloque_horario,
                semestre='2026-S1' # Usar semestre actual
            )
            # 3. Actualizar disponibilidad del aula (Lógica de negocio)
            AulaModel.objects.filter(id=aula_id).update(disponible=False)

        except IntegrityError as e:
            raise Exception(f"Conflicto de base de datos durante la asignación: {e}")
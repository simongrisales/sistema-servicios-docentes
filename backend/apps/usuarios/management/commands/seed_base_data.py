from datetime import time

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.academico.infrastructure.models import (
    AulaModel,
    CursoModel,
    DocenteModel,
    FacultadModel,
    GrupoModel,
    HorarioBloqueModel,
    ProgramaModel,
)
from apps.usuarios.infrastructure.models import RoleModel

ROLES = [
    ("administrador", "Administrador", "Gestion del sistema y auditoria."),
    ("lider_sd", "Lider SD", "Ejecucion y supervision de asignacion academica."),
    ("auxiliar_sd", "Auxiliar SD", "Apoyo operativo en reservas y ajustes."),
    ("facultad", "Facultad", "Envio de datos academicos al sistema."),
    ("admisiones", "Admisiones", "Actualizacion de cupos reales por grupo."),
]


class Command(BaseCommand):
    help = "Crea roles, usuarios y datos academicos base para demo."

    def handle(self, *args, **options):
        roles = self._crear_roles()
        self._crear_usuarios(roles)
        self._crear_datos_academicos()
        self.stdout.write(self.style.SUCCESS("Datos base creados correctamente."))

    def _crear_roles(self) -> dict[str, RoleModel]:
        roles = {}
        for code, name, description in ROLES:
            role, _ = RoleModel.objects.update_or_create(
                code=code,
                defaults={"name": name, "description": description},
            )
            roles[code] = role
        return roles

    def _crear_usuarios(self, roles: dict[str, RoleModel]) -> None:
        user_model = get_user_model()
        ejemplos = [
            ("admin.sds", "admin.sds@uco.edu.co", "administrador", "TI"),
            ("lider.sd", "lider.sd@uco.edu.co", "lider_sd", "Servicios Docentes"),
            (
                "auxiliar.sd",
                "auxiliar.sd@uco.edu.co",
                "auxiliar_sd",
                "Servicios Docentes",
            ),
            (
                "facultad.ing",
                "facultad.ing@uco.edu.co",
                "facultad",
                "Facultad Ingenieria",
            ),
            ("admisiones", "admisiones@uco.edu.co", "admisiones", "Admisiones"),
        ]
        for username, email, role_code, departamento in ejemplos:
            user, created = user_model.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "role": roles[role_code],
                    "departamento": departamento,
                    "cargo": roles[role_code].name,
                    "is_staff": role_code == "administrador",
                    "is_superuser": role_code == "administrador",
                },
            )
            if created:
                user.set_password("UcoDemo2026*")
                user.save()

    def _crear_datos_academicos(self) -> None:
        facultad, _ = FacultadModel.objects.update_or_create(
            codigo="ING",
            defaults={"nombre": "Facultad de Ingenieria", "activa": True},
        )
        programa, _ = ProgramaModel.objects.update_or_create(
            codigo="ISI",
            defaults={
                "nombre": "Ingenieria de Sistemas",
                "facultad": facultad,
                "activo": True,
            },
        )
        curso, _ = CursoModel.objects.update_or_create(
            codigo="ISW2",
            defaults={
                "nombre": "Ingenieria de Software II",
                "programa": programa,
                "creditos": 3,
                "activo": True,
            },
        )
        docente, _ = DocenteModel.objects.update_or_create(
            email="docente.demo@uco.edu.co",
            defaults={"nombre": "Docente Demo", "activo": True},
        )
        HorarioBloqueModel.objects.update_or_create(
            dia="lunes",
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
            defaults={"activo": True},
        )
        for nombre, capacidad, tipo in [
            ("Bloque 3 - Aula 204", 35, "aula_regular"),
            ("Laboratorio Sistemas 1", 28, "sala_sistemas"),
            ("Auditorio Principal", 120, "auditorio"),
            ("Bloque 2 - Aula 108", 45, "aula_regular"),
        ]:
            AulaModel.objects.update_or_create(
                nombre=nombre,
                defaults={
                    "capacidad": capacidad,
                    "tipo": tipo,
                    "disponible": True,
                    "activa": True,
                },
            )
        GrupoModel.objects.update_or_create(
            curso=curso,
            codigo="01",
            semestre="2026-1",
            defaults={
                "docente": docente,
                "num_estudiantes": 32,
                "activo": True,
            },
        )

        # Seed de parámetros (app: parametros)
        from apps.parametros.infrastructure.models import CatalogoParametroModel

        parametros_seed = [
            {
                "clave": "max_aulas_por_semestre",
                "valor": 10,
                "grupo": "asignacion",
                "descripcion": "Máximo de aulas por semestre (demo).",
                "activo": True,
            },
            {
                "clave": "min_capacidad_por_grupo",
                "valor": 0,
                "grupo": "asignacion",
                "descripcion": "Capacidad mínima permitida (demo).",
                "activo": True,
            },
            {
                "clave": "notificaciones_activas",
                "valor": True,
                "grupo": "notificaciones",
                "descripcion": "Control para enviar notificaciones (demo).",
                "activo": True,
            },
            {
                "clave": "seguridad_salt",
                "valor": "demo-salt",
                "grupo": "seguridad",
                "descripcion": "Semilla demo para seguridad/validaciones.",
                "activo": True,
            },
        ]

        for p in parametros_seed:
            CatalogoParametroModel.objects.update_or_create(
                clave=p["clave"],
                defaults={
                    "valor": p["valor"],
                    "grupo": p["grupo"],
                    "descripcion": p["descripcion"],
                    "activo": p["activo"],
                },
            )


from datetime import time

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.usuarios.infrastructure.models import RoleModel

ROLES = [
    ("administrador", "Administrador", "Gestion del sistema y auditoria."),
    ("lider_sd", "Lider SD", "Ejecucion y supervision de asignacion academica."),
    ("auxiliar_sd", "Auxiliar SD", "Apoyo operativo en reservas y ajustes."),
    ("facultad", "Facultad", "Envio de datos academicos al sistema."),
    ("admisiones", "Admisiones", "Actualizacion de cupos reales por grupo."),
]

FACULTADES = [
    ("ING", "Facultad de Ingeniería", "Ingeniería de Sistemas"),
    ("SOC", "Facultad de Ciencias Sociales", "Ciencias Sociales"),
    (
        "ADM",
        "Facultad de Ciencias Administrativas y Económicas",
        "Administración y Economía",
    ),
    ("DER", "Facultad de Derecho", "Derecho"),
    ("SAL", "Facultad de Ciencias de la Salud", "Ciencias de la Salud"),
    (
        "AGR",
        "Facultad de Ciencias Agrarias y Ambientales",
        "Ciencias Agrarias y Ambientales",
    ),
]

CURSOS = {
    "ING": [
        ("ING101", "Programación I"),
        ("ING102", "Programación II"),
        ("ING103", "Bases de Datos"),
        ("ING104", "Ingeniería de Software"),
        ("ING105", "Arquitectura de Software"),
        ("ING106", "Redes de Computadores"),
        ("ING107", "Sistemas Operativos"),
        ("ING108", "Inteligencia Artificial"),
    ],
    "SOC": [
        ("SOC101", "Sociología General"),
        ("SOC102", "Psicología Social"),
        ("SOC103", "Antropología Cultural"),
        ("SOC104", "Metodología de la Investigación"),
        ("SOC105", "Comunicación Organizacional"),
    ],
    "ADM": [
        ("ADM101", "Fundamentos de Administración"),
        ("ADM102", "Contabilidad General"),
        ("ADM103", "Gestión Financiera"),
        ("ADM104", "Mercadeo Estratégico"),
        ("ADM105", "Gestión del Talento Humano"),
    ],
    "DER": [
        ("DER101", "Introducción al Derecho"),
        ("DER102", "Derecho Constitucional"),
        ("DER103", "Derecho Civil"),
        ("DER104", "Derecho Laboral"),
        ("DER105", "Derecho Comercial"),
    ],
    "SAL": [
        ("SAL101", "Anatomía Humana"),
        ("SAL102", "Fisiología"),
        ("SAL103", "Bioquímica"),
        ("SAL104", "Salud Pública"),
        ("SAL105", "Enfermería Comunitaria"),
    ],
    "AGR": [
        ("AGR101", "Producción Animal"),
        ("AGR102", "Botánica General"),
        ("AGR103", "Fertilidad de Suelos"),
        ("AGR104", "Gestión Ambiental"),
        ("AGR105", "Nutrición Animal"),
    ],
}

GRUPOS_POR_CURSO = {
    "ING101": [1, 2, 3, 4],
    "ING102": [1, 2, 3],
    "ING103": [1, 2, 3],
    "ING104": [1, 2],
    "ING105": [1],
    "ING106": [1, 2],
    "ING107": [1, 2],
    "ING108": [1],
    "SOC101": [1, 2],
    "SOC102": [1],
    "SOC103": [1],
    "SOC104": [1, 2, 3],
    "SOC105": [1],
    "ADM101": [1, 2, 3],
    "ADM102": [1, 2],
    "ADM103": [1],
    "ADM104": [1, 2],
    "ADM105": [1],
    "DER101": [1, 2],
    "DER102": [1],
    "DER103": [1, 2],
    "DER104": [1],
    "DER105": [1],
    "SAL101": [1, 2],
    "SAL102": [1],
    "SAL103": [1],
    "SAL104": [1, 2],
    "SAL105": [1],
    "AGR101": [1, 2],
    "AGR102": [1],
    "AGR103": [1],
    "AGR104": [1, 2],
    "AGR105": [1],
}

AULAS = [
    *[(f"M20{i}", 35, "aula_regular", "Bloque M2") for i in range(1, 9)],
    *[(f"M30{i}", 40, "aula_regular", "Bloque M3") for i in range(1, 9)],
    *[(f"M40{i}", 45, "aula_regular", "Bloque M4") for i in range(1, 9)],
    ("Aula Multimedia", 35, "sala_sistemas", "Aulas Especiales"),
    ("Aula EDC", 30, "aula_regular", "Aulas Especiales"),
    ("Laboratorio de Química", 28, "laboratorio", "Laboratorios"),
    ("Laboratorio de Física", 28, "laboratorio", "Laboratorios"),
    ("Laboratorio de Biología", 28, "laboratorio", "Laboratorios"),
    ("Laboratorio de Zootecnia", 30, "laboratorio", "Laboratorios"),
    ("Laboratorio de Enfermería", 30, "laboratorio", "Laboratorios"),
    ("Sala de Valores InnovaMater", 25, "aula_regular", "Salas Especiales"),
    *[(f"J{i}", 32, "aula_regular", "Bloque J") for i in range(1, 16)],
    ("JPro", 24, "aula_regular", "Bloque J"),
]

HORARIOS = [
    ("lunes", time(6, 0), time(8, 0)),
    ("lunes", time(8, 0), time(10, 0)),
    ("martes", time(8, 0), time(10, 0)),
    ("miercoles", time(10, 0), time(12, 0)),
    ("jueves", time(14, 0), time(16, 0)),
    ("viernes", time(16, 0), time(18, 0)),
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
        FacultadModel = apps.get_model("academico", "FacultadModel")
        ProgramaModel = apps.get_model("academico", "ProgramaModel")
        DocenteModel = apps.get_model("academico", "DocenteModel")
        CursoModel = apps.get_model("academico", "CursoModel")
        AulaModel = apps.get_model("academico", "AulaModel")
        GrupoModel = apps.get_model("academico", "GrupoModel")
        HorarioBloqueModel = apps.get_model("academico", "HorarioBloqueModel")
        CatalogoParametroModel = apps.get_model(
            "parametros",
            "CatalogoParametroModel",
        )

        programas = {}
        cursos = {}
        for codigo, nombre, programa_nombre in FACULTADES:
            facultad, _ = FacultadModel.objects.update_or_create(
                codigo=codigo,
                defaults={"nombre": nombre, "activa": True},
            )
            programa, _ = ProgramaModel.objects.update_or_create(
                codigo=f"{codigo}-GEN",
                defaults={
                    "nombre": programa_nombre,
                    "facultad": facultad,
                    "activo": True,
                },
            )
            programas[codigo] = programa

        docentes = {}
        for codigo, nombre, _programa_nombre in FACULTADES:
            docente, _ = DocenteModel.objects.update_or_create(
                email=f"docente.{codigo.lower()}@uco.edu.co",
                defaults={
                    "nombre": f"Docente {nombre.replace('Facultad de ', '')}",
                    "activo": True,
                },
            )
            docentes[codigo] = docente

        for facultad_codigo, cursos_facultad in CURSOS.items():
            for curso_codigo, curso_nombre in cursos_facultad:
                curso, _ = CursoModel.objects.update_or_create(
                    codigo=curso_codigo,
                    defaults={
                        "nombre": curso_nombre,
                        "programa": programas[facultad_codigo],
                        "creditos": 3,
                        "activo": True,
                    },
                )
                cursos[curso_codigo] = curso

        for dia, hora_inicio, hora_fin in HORARIOS:
            HorarioBloqueModel.objects.update_or_create(
                dia=dia,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                defaults={"activo": True},
            )

        for nombre, capacidad, tipo, bloque in AULAS:
            AulaModel.objects.update_or_create(
                nombre=nombre,
                defaults={
                    "capacidad": capacidad,
                    "tipo": tipo,
                    "disponible": True,
                    "restricciones": {"bloque": bloque},
                    "activa": True,
                },
            )

        for curso_codigo, numeros_grupo in GRUPOS_POR_CURSO.items():
            facultad_codigo = curso_codigo[:3]
            for numero in numeros_grupo:
                GrupoModel.objects.update_or_create(
                    curso=cursos[curso_codigo],
                    codigo=f"{curso_codigo}-{numero:02d}",
                    semestre="2026-1",
                    defaults={
                        "docente": docentes[facultad_codigo],
                        "num_estudiantes": self._estudiantes_para_grupo(
                            curso_codigo,
                            numero,
                        ),
                        "activo": True,
                    },
                )

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

    @staticmethod
    def _estudiantes_para_grupo(curso_codigo: str, numero: int) -> int:
        base_por_facultad = {
            "ING": 30,
            "SOC": 26,
            "ADM": 34,
            "DER": 28,
            "SAL": 24,
            "AGR": 22,
        }
        base = base_por_facultad.get(curso_codigo[:3], 25)
        ajuste = (sum(ord(char) for char in curso_codigo) + numero * 7) % 12
        return base + ajuste

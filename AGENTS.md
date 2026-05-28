# AGENTS.md

## ROL Y CONTEXTO
 
Actúa como un **arquitecto de software senior y desarrollador full-stack** con experiencia en Django, arquitecturas distribuidas N-Tier y sistemas de gestión académica. Vas a guiarme paso a paso en la construcción de un sistema web real llamado **Sistema de Servicios Docentes** de la Universidad Católica de Oriente (UCO). Soy un estudiante universitario, así que necesito que expliques las decisiones técnicas con claridad, pero que el código sea de calidad profesional, siguiendo buenas prácticas desde el inicio.

---

## Proyecto: Sistema de Servicios Docentes

Aplicación web para gestión de asignación académica de aulas en la Universidad Católica de Oriente (UCO). Automatiza la asignación de espacios considerando disponibilidad, capacidad y restricciones institucionales.

**Misión**: Para el Área de Servicios Docentes de la Universidad Católica de Oriente que enfrenta conflictos y retrasos recurrentes en la asignación manual de aulas, lo que genera demoras en la definición y confirmación de espacios al inicio de cada semestre académico y afecta la eficiencia operativa del servicio, Sistema de Servicios Docentes es una aplicación web que automatiza esta asignación mediante validaciones de capacidad y disponibilidad, reduciendo de manera estimada entre un 50% y 60% el tiempo operativo de programación y disminuyendo en más del 80% los conflictos por cruces de espacios. Esto permite optimizar el uso de la infraestructura física, mejorar la eficiencia administrativa y fortalecer la confianza y la imagen institucional del servicio ante la comunidad académica. A diferencia de soluciones como uPlanner, Scientia, CELCAT, Ad Astra, 25Live, Syllabus Plus, Infosilem, PowerCampus y Banner by Ellucian, nuestro producto se especializa exclusivamente en la asignación académica de aulas bajo criterios institucionales propios, garantizando una solución ágil, contextualizada y alineada con los lineamientos internos de la universidad.

---

## Stack Tecnológico completo (Versiones Exactas - NO MODIFICAR)
> ⚠️ IMPORTANTE: Usa exactamente estas versiones. No actualices ni cambies tecnologías sin consultarme.

### Desarrollo propio
| Componente | Versión |
|---|---|
| Sistema Servicios Docentes — Backend | 0.1 |
| Sistema Servicios Docentes — Frontend | 0.1 |
 
### Plataforma de desarrollo
| Tecnología | Versión |
|---|---|
| Python | 3.13 |
| Django | 5.2 LTS |
| Django REST Framework | 3.15 |
| Gunicorn | 23 |
| django-environ | 0.11 |
| pip + requirements.txt | 24 |
| drf-spectacular | 0.27 |
| Django i18n (nativo)   | 5.2  |
 
### Frontend
| Tecnología | Versión |
|---|---|
| Django Templates | 5.2 (nativo) |
| HTMX | 2.x |
| Alpine.js | 3.14 |
| Tailwind CSS | 4.x |
| django-tailwind | 3.x |
| daisyUI | 5.x |
| Heroicons | 2.x |
 
### Infraestructura y red
| Tecnología | Versión | Rol |
|---|---|---|
| Nginx | 1.27 | DNS + CDN + WAF + API Gateway + Load Balancer |
| WhiteNoise | 6 | Archivos estáticos en desarrollo |
 
### Seguridad e identidad
| Tecnología | Versión |
|---|---|
| djangorestframework-simplejwt | 5.4 |
| Django Auth + Permissions | 5.2 (nativo) |
| django-ratelimit | 4 |
| django-environ (Key Vault dev) | 0.11 |
| HashiCorp Vault (Key Vault prod) | 1.18 |
| django-recaptcha       | 4  |
| bleach                 | 6  |
 
### Procesamiento asíncrono y tiempo real
| Tecnología | Versión | Rol |
|---|---|---|
| Valkey | 8 | Broker Celery + Caché + Channel Layer |
| Celery | 5.6 | Workers y tareas asíncronas |
| Django Channels | 4.1 | WebSocket |
| Daphne | 4 | Servidor ASGI |
| django-notifications-hq | 1.8 | Notificaciones in-app |
 
### Datos
| Tecnología | Versión |
|---|---|
| PostgreSQL | 17 |
| django-redis (apuntando a Valkey) | 5.4 |
 
### Observabilidad
| Tecnología | Versión |
|---|---|
| Prometheus | 3 |
| Grafana | 12 |
| django-prometheus | 0.3 |
| Python logging + Django logging | Stdlib |
 
### DevOps y calidad
| Tecnología | Versión |
|---|---|
| Docker + Docker Compose | 27 / 2 |
| Visual Studio Code | 1.9x |
| Git | 2.47 |
| GitHub + GitHub Actions | — |
| SonarQube Community Edition | 25 |
| pytest + pytest-django | 8 / 4 |
| coverage.py | 7 |
| Ruff + Black | 0.9 / 25 |
| OWASP ZAP              | 2.15 |

---

## Componentes con tecnologías:
- Backend del sistema	Equipo de desarrollo — UCO	Sistema Servicios Docentes — Backend
- Frontend del sistema	Equipo de desarrollo — UCO	Sistema Servicios Docentes — Frontend
- Lenguaje base	Python Software Foundation	Python
- Framework backend	Django Software Foundation	Django
- APIs REST	Comunidad DRF	Django REST Framework
- Servidor WSGI	Benoit Chesneau	Gunicorn
- Variables de entorno / Secretos (dev)	Comunidad	django-environ
- Gestor de dependencias	PyPA	pip + requirements.txt
- Documentación de APIs	OpenAPI Initiative / Comunidad	drf-spectacular
- Motor de plantillas	Django Software Foundation	Django Templates
- Interactividad servidor	Big Sky Software	HTMX
- Reactividad cliente	Caleb Porzio / Comunidad	Alpine.js
- Framework CSS	Tailwind Labs	Tailwind CSS
- Integración Django-Tailwind	Tim Kamanin	django-tailwind
- Librería de componentes UI	Pouya Saadeghi	daisyUI
- Librería de iconos	Tailwind Labs	Heroicons
- Load Balancer / DNS / CDN / WAF / API GATEWAY	F5 / NGINX Inc.	Nginx
- Archivos estáticos (CDN local)	Dave Evans	WhiteNoise
- IDP/IDM - Autenticación JWT	Jazzband	djangorestframework-simplejwt
- IDP/IDM - Control de acceso por roles	Django Software Foundation	Django Auth + Permissions
- Rate Limiter	Brendan Sterne	django-ratelimit
- Key Vault (desarrollo)	Comunidad	django-environ
- Key Vault (producción)	HashiCorp	HashiCorp Vault
- Colas de mensajes	Comunidad	Valkey + Celery
- Workers	Celery Project	Celery
- WebSocket	Comunidad Django	Django Channels
- Servidor ASGI (WebSocket)	Django / Comunidad	Daphne
- Notificaciones	Łukasz Balcerzak / Comunidad	django-notifications-hq
- Base de datos relacional	PostgreSQL Global Development Group	PostgreSQL
- Caché Distribuido	Linux Foundation / Valkey Community	Valkey + django-redis
- Recolección (Monitoreo)	Cloud Native Computing Foundation	Prometheus
- Visualización (Monitoreo)	Grafana Labs	Grafana
- Exportador Django (Monitoreo)	Comunidad	django-prometheus
- Logs	Python Software Foundation	Python logging + Django logging
- Contenedores y despliegue	Docker Inc.	Docker + Docker Compose
- IDE de desarrollo	Microsoft	Visual Studio Code
- Control de versiones	Linus Torvalds / Comunidad	Git
- Repositorio de código	Microsoft	GitHub
- Integración continua CI/CD	GitHub	GitHub Actions
- Análisis estático de código	SonarSource	SonarQube Community Edition
- Framework de pruebas	Python Software Foundation	pytest + pytest-django
- Cobertura de pruebas	Ned Batchelder	coverage.py
- Linting y formato de código	Astral / PyCQA	Ruff + Black

---

## Línea Base del Sistema (Requisitos obligatorios del profesor)

Todos estos componentes deben estar implementados y demostrables:

| # | Requisito | Tecnología | Estado |
|---|---|---|---|
| 1 | Baúl de secretos | django-environ + HashiCorp Vault | En stack |
| 2 | CI/CD | GitHub Actions | En stack |
| 3 | Análisis estático | SonarQube Community | En stack |
| 4 | Identity Provider federado | simplejwt + Django Auth | En stack |
| 5 | API Gateway | Nginx | En stack |
| 6 | WAF | Nginx | En stack |
| 7 | Monitoreo e instrumentación | Prometheus + Grafana | En stack |
| 8 | Notification Gateway | django-notifications-hq | En stack |
| 9 | Catálogo de mensajes | Valkey + Celery | En stack |
| 10 | Catálogo de parámetros | Modelo CatalogoParametro (JSONB) | Implementar |
| 11 | Catálogo de notificaciones | django-notifications-hq | En stack |
| 12 | Principios de diseño | SOLID | En stack |
| 13 | Clean Code | Ruff + Black | En stack |
| 14 | Clean Architecture | Estructura de capas | En stack |
| 15 | APIs REST | Django REST Framework | En stack |
| 16 | Swagger / OpenAPI | drf-spectacular | En stack |
| 17 | HTTPS | Nginx SSL | En stack |
| 18 | Aseguramiento APIs | simplejwt + Django permissions | En stack |
| 19 | Captcha | django-recaptcha 4.x | Agregar |
| 20 | I18N | Django i18n nativo (es-co) | Agregar |
| 21 | Git + ramificación | GitHub + feature/develop/main | En stack |
| 22 | OWASP ZAP + Sanitizer | OWASP ZAP 2.15 + bleach 6.x | Agregar |
| 23 | Caché distribuida | Valkey + django-redis | En stack |

---

## Arquitectura N-Tier Stateless

### Estilo arquitectónico
- **Arquitectura distribuida N-Tier** con separación clara de capas
- **Enfoque stateless** en todos los servicios backend
- **Modelo C4 Nivel 1-2** (contexto y contenedores)
- **Principios SOLID** aplicados a todo el código
- **Patrones de diseño**: Repository (acceso a datos), Strategy (algoritmos de asignación), Factory (creación de entidades complejas)

### Capas de la arquitectura
```
[Clientes]          PC / Laptop (navegador web)
      ↓ HTTPS
[Edge / Entrada]    DNS → CDN → WAF → API Gateway → Rate Limiter
      ↓ HTTPS
[Frontend]          Frontend sistema de servicios docentes UCO
      ↓ HTTPS
[Seguridad]         IDP/IDM  |  Key Vault
      ↓ HTTPS
[Backend]           Backend sistema de servicios docentes UCO
      ↓ TCP/IP
[Datos]             Base de datos relacional  |  Caché distribuido | Load Balancer
      ↓ AMQP
[Procesamiento]     Workers  |  WebSocket | Colas de mensajes
      ↓
[Notificaciones]    Notifications
      ↓
[Observabilidad]    Monitoreo |	Logs
```
---

**Principios clave**: Todos los servicios son **stateless**. Seguir principios SOLID y Clean Code.

---

## Patrón de Desarrollo Obligatorio

### Secuencia por App Django (Clean Architecture)
Para cada app, desarrollar en este orden estricto:
1. `domain/entities.py`
2. `domain/interfaces.py`
3. `domain/exceptions.py`
4. `application/dtos.py`
5. `application/use_cases.py`
6. `infrastructure/models.py`
7. `infrastructure/repositories.py`
8. `infrastructure/tasks.py` (si la app lo necesita)
9. `presentation/serializers.py`
10. `presentation/views.py`
11. `presentation/urls.py`
12. `tests/test_domain.py`
13. `tests/test_use_cases.py`
14. `tests/test_views.py`

### Patrones de Diseño Requeridos
- **Repository**: toda consulta a la BD va en `infrastructure/repositories.py`, 
  extendiendo `BaseRepository` de `core/`
- **Strategy**: el algoritmo de asignación debe soportar múltiples estrategias 
  intercambiables desde el día 1
- **Factory**: creación de entidades complejas que requieren lógica de construcción

---

## Arquitectura de código: Clean Architecture + Django MVT

El proyecto implementa Clean Architecture dentro de Django.
Cada app sigue esta estructura interna de 4 capas:

### Capas por app
```
sistema-servicios-docentes/
├── backend/
│   ├── apps/
│   │   ├── asignacion/                    # Asignación automática de aulas (NÚCLEO)
│   │   │   ├── domain/                    # Python puro — CERO imports de Django
│   │   │   │   ├── __init__.py
│   │   │   │   ├── entities.py            # Asignacion, ReglaAsignacion (clases Python)
│   │   │   │   ├── exceptions.py          # AsignacionConflictoError, CapacidadInsuficienteError
│   │   │   │   └── interfaces.py          # IAsignacionRepository, IAsignacionStrategy (ABCs)
│   │   │   ├── application/               # Casos de uso — orquesta el dominio
│   │   │   │   ├── __init__.py
│   │   │   │   ├── dtos.py                # AsignacionInputDTO, AsignacionOutputDTO
│   │   │   │   └── use_cases.py           # EjecutarAsignacion, SimularAsignacion, ValidarCobertura
│   │   │   ├── infrastructure/            # Django, ORM, Celery
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py              # Modelos Django ORM
│   │   │   │   ├── repositories.py        # Implementación concreta de IAsignacionRepository
│   │   │   │   ├── strategies.py          # Implementaciones concretas de IAsignacionStrategy
│   │   │   │   └── tasks.py               # Tareas Celery (asignación masiva, recálculo)
│   │   │   ├── presentation/              # Vistas, serializers, URLs, templates
│   │   │   │   ├── __init__.py
│   │   │   │   ├── serializers.py
│   │   │   │   ├── views.py
│   │   │   │   ├── urls.py
│   │   │   │   └── templates/
│   │   │   │       └── asignacion/
│   │   │   │           ├── lista.html
│   │   │   │           ├── detalle.html
│   │   │   │           └── partials/      # Fragmentos HTMX
│   │   │   └── tests/
│   │   │       ├── test_domain.py         # Tests del dominio (sin Django)
│   │   │       ├── test_use_cases.py      # Tests de casos de uso
│   │   │       └── test_views.py          # Tests de integración
│   │   │
│   │   ├── academico/                     # Cursos, grupos, docentes, horarios
│   │   │   ├── domain/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── entities.py            # Aula, Grupo, Docente, Curso, HorarioBloque
│   │   │   │   ├── exceptions.py          # AulaNoDisponibleError, GrupoSinDocenteError
│   │   │   │   └── interfaces.py          # IAulaRepository, IGrupoRepository
│   │   │   ├── application/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── dtos.py
│   │   │   │   └── use_cases.py           # CrearGrupo, ActualizarCapacidadAula, CargaMasivaGrupos
│   │   │   ├── infrastructure/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── repositories.py
│   │   │   │   └── tasks.py               # Tarea Celery para carga masiva
│   │   │   ├── presentation/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── serializers.py
│   │   │   │   ├── views.py
│   │   │   │   ├── urls.py
│   │   │   │   └── templates/
│   │   │   │       └── academico/
│   │   │   │           └── partials/
│   │   │   └── tests/
│   │   │       ├── test_domain.py
│   │   │       ├── test_use_cases.py
│   │   │       └── test_views.py
│   │   │
│   │   ├── reservas/                      # Reservas temporales de aulas
│   │   │   ├── domain/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── entities.py            # Reserva, EstadoReserva
│   │   │   │   ├── exceptions.py          # ReservaConflictoError, ReservaExpiradaError
│   │   │   │   └── interfaces.py          # IReservaRepository
│   │   │   ├── application/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── dtos.py
│   │   │   │   └── use_cases.py           # CrearReserva, ConfirmarReserva, CancelarReserva
│   │   │   ├── infrastructure/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── repositories.py
│   │   │   │   └── tasks.py               # Expiración automática de reservas
│   │   │   ├── presentation/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── serializers.py
│   │   │   │   ├── views.py
│   │   │   │   ├── urls.py
│   │   │   │   └── templates/
│   │   │   │       └── reservas/
│   │   │   │           └── partials/
│   │   │   └── tests/
│   │   │       ├── test_domain.py
│   │   │       ├── test_use_cases.py
│   │   │       └── test_views.py
│   │   │
│   │   ├── usuarios/                      # Actores, roles y autenticación
│   │   │   ├── domain/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── entities.py            # Usuario, Rol, Permiso
│   │   │   │   ├── exceptions.py          # PermisoInsuficienteError, CredencialesInvalidasError
│   │   │   │   └── interfaces.py          # IUsuarioRepository
│   │   │   ├── application/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── dtos.py
│   │   │   │   └── use_cases.py           # AutenticarUsuario, CrearUsuario, AsignarRol
│   │   │   ├── infrastructure/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   └── repositories.py
│   │   │   ├── presentation/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── serializers.py
│   │   │   │   ├── views.py
│   │   │   │   ├── urls.py
│   │   │   │   └── templates/
│   │   │   │       └── usuarios/
│   │   │   │           ├── login.html
│   │   │   │           └── perfil.html
│   │   │   └── tests/
│   │   │       ├── test_domain.py
│   │   │       └── test_views.py
│   │   │
│   │   ├── reportes/                      # Generación de reportes
│   │   │   ├── domain/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── entities.py            # Reporte, TipoReporte
│   │   │   │   └── interfaces.py          # IReporteRepository
│   │   │   ├── application/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── dtos.py
│   │   │   │   └── use_cases.py           # GenerarReporteOcupacion, GenerarReporteCobertura
│   │   │   ├── infrastructure/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── repositories.py
│   │   │   │   └── tasks.py               # Generación asíncrona de reportes pesados
│   │   │   ├── presentation/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── serializers.py
│   │   │   │   ├── views.py
│   │   │   │   ├── urls.py
│   │   │   │   └── templates/
│   │   │   │       └── reportes/
│   │   │   │           └── partials/
│   │   │   └── tests/
│   │   │       ├── test_domain.py
│   │   │       └── test_use_cases.py
│   │   │
│   │   └── notificaciones/                # django-notifications-hq + WebSocket
│   │       ├── domain/
│   │       │   ├── __init__.py
│   │       │   ├── entities.py            # Notificacion, TipoNotificacion
│   │       │   └── interfaces.py          # INotificacionRepository
│   │       ├── application/
│   │       │   ├── __init__.py
│   │       │   ├── dtos.py
│   │       │   └── use_cases.py           # EnviarNotificacion, MarcarLeida
│   │       ├── infrastructure/
│   │       │   ├── __init__.py
│   │       │   ├── models.py
│   │       │   ├── repositories.py
│   │       │   └── consumers.py           # Django Channels WebSocket consumer
│   │       ├── presentation/
│   │       │   ├── __init__.py
│   │       │   ├── views.py
│   │       │   ├── urls.py
│   │       │   └── templates/
│   │       │       └── notificaciones/
│   │       │           └── partials/
│   │       │               └── campana.html   # Fragmento HTMX del ícono de notificaciones
│   │       └── tests/
│   │           └── test_consumers.py
│   │
│   ├── config/                            # Configuración central del proyecto
│   │   ├── __init__.py
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                    # Configuración común a todos los entornos
│   │   │   ├── dev.py                     # Desarrollo local (DEBUG=True, hot-reload)
│   │   │   └── prod.py                    # Producción (Gunicorn + Daphne + Nginx)
│   │   ├── urls.py                        # URLs raíz del proyecto
│   │   ├── asgi.py                        # Punto de entrada ASGI (Daphne + WebSocket)
│   │   └── wsgi.py                        # Punto de entrada WSGI (Gunicorn)
│   │
│   ├── core/                              # Clases base reutilizables (sin lógica de negocio)
│   │   ├── __init__.py
│   │   ├── repositories.py                # BaseRepository (ABC con métodos CRUD genéricos)
│   │   ├── services.py                    # BaseService (ABC base para use_cases)
│   │   ├── exceptions.py                  # Excepciones base del sistema
│   │   └── dtos.py                        # DTOs base reutilizables
│   │
│   └── requirements/
│       ├── base.txt                       # Dependencias comunes
│       ├── dev.txt                        # base.txt + herramientas de desarrollo
│       └── prod.txt                       # base.txt + gunicorn, daphne, whitenoise
│
├── frontend/                              # Assets y templates globales
│   ├── templates/
│   │   ├── base.html                      # Layout principal (Tailwind + daisyUI + HTMX + Alpine)
│   │   ├── partials/                      # Fragmentos globales reutilizables
│   │   │   ├── navbar.html
│   │   │   ├── sidebar.html
│   │   │   └── toast.html                 # Notificaciones toast via WebSocket
│   │   └── pages/
│   │       ├── dashboard.html             # Panel principal según rol
│   │       ├── 403.html
│   │       ├── 404.html
│   │       └── 500.html
│   └── static/
│       ├── css/
│       │   └── tailwind.css               # CSS compilado por django-tailwind
│       ├── js/
│       │   ├── htmx.min.js
│       │   ├── alpine.min.js
│       │   └── ws-notifications.js        # Conexión WebSocket para notificaciones
│       └── icons/                         # Heroicons SVG
│
├── nginx/
│   └── nginx.conf                         # Proxy inverso HTTP→Gunicorn, WS→Daphne
│
├── docker-compose.yml                     # Stack completo de producción
├── docker-compose.dev.yml                 # Stack de desarrollo con hot-reload
├── .env.example                           # Variables de entorno documentadas
├── .env                                   # Variables reales (en .gitignore)
├── AGENTS.md                              # Contexto para Codex
└── .github/
    └── workflows/
        └── ci.yml                         # GitHub Actions: pytest + Ruff en cada push
```

### Regla de dependencias (NO romper esto)
- `domain/` → no importa nada de Django ni de otras capas
- `application/` → solo importa de `domain/`
- `infrastructure/` → importa de `domain/`, `application/` y Django
- `presentation/` → solo importa de `application/`

### Secuencia de desarrollo por app
1. `domain/entities.py` → `domain/interfaces.py`
2. `application/dtos.py` → `application/use_cases.py`
3. `infrastructure/models.py` → `infrastructure/repositories.py`
4. `presentation/serializers.py` → `presentation/views.py` → `presentation/urls.py`
5. `tests/` (una carpeta de tests por capa)

---

## MODELO DE DATOS PRINCIPAL (entidades clave)
 
```
Aula           → id, nombre, capacidad, tipo, disponible, restricciones
Facultad       → id, nombre, codigo
Programa       → id, nombre, facultad
Docente        → id, nombre, email, disponibilidad
Curso          → id, nombre, codigo, programa, creditos
Grupo          → id, curso, docente, num_estudiantes, semestre
HorarioBloque  → id, dia, hora_inicio, hora_fin
Asignacion     → id, grupo, aula, bloque_horario, semestre, estado
Reserva        → id, aula, bloque_horario, solicitante, estado, fecha_expiracion
ReglaNegocio   → id, nombre, tipo, parametros (JSONB), activa
CatalogoParametro → id, clave, valor, descripcion, activo
```

---

## Componentes Críticos

### Algoritmo de Asignación (app: asignacion)
- **Función crítica**: Núcleo del sistema - prioriza grupos por número de estudiantes
- **Requisitos**: Pattern Strategy desde el inicio, cobertura de pruebas unitaria obligatoria
- **Validaciones**: capacidad aula vs num_estudiantes, conflictos de horario

### Validación de Conflictos
- Detecta cruces entre asignaciones de diferentes grupos en mismo aula/horario

### WebSockets (Django Channels)
- ÚNICAMENTE para: disponibilidad de aulas en tiempo real + notificaciones in-app

---

## RESTRICCIONES IMPORTANTES
 
### De negocio
- El equipo académico y administrativo involucrado en el proyecto dispone de tiempo limitado para participar en levantamiento de requerimientos, validaciones funcionales y pruebas del sistema debido a sus responsabilidades operativas institucionales.
- El sistema debe estar disponible antes del inicio del proceso institucional de programación académica del semestre correspondiente para generar valor operativo real.
- El sistema debe garantizar el cumplimiento de la normativa colombiana relacionada con protección de datos personales (Habeas Data) y políticas institucionales de manejo de información académica.
- Existe incertidumbre respecto a futuras necesidades funcionales del sistema, como integración con otros sistemas académicos institucionales o ampliación hacia programación completa de horarios.
- El nivel de adopción tecnológica por parte de algunos usuarios administrativos puede ser bajo, generando resistencia al cambio frente a la automatización del proceso.
- El conocimiento funcional del proceso de asignación se encuentra concentrado en pocas personas dentro del área de servicios docentes.
- El sistema debe respetar **normativas institucionales internas sobre uso de infraestructura física académica**.
- El sistema debe cumplir con la **normativa colombiana de protección de datos (Habeas Data)**
- Debe respetar normativas institucionales internas sobre uso de infraestructura física
- El **presupuesto es cero** — todo debe ser 100% open source o gratuito
- El sistema debe estar listo en pocas semanas (proyecto académico universitario)
- **Disponibilidad**: 98% durante matrícula, jornada académica en regular
- **RTO/RPO**: Restablecer servicio <2 minutos tras caídas sin pérdida de datos
- **Performance**: 500 grupos <5 segundos | 50 usuarios concurrentes sin degradación
### Técnicas
- Todos los servicios deben ser **stateless**
- Seguir principios **SOLID** y **Clean Code** en todo el código
- Usar el patrón **Repository** para toda la capa de acceso a datos
- El algoritmo de asignación debe implementarse con el patrón **Strategy** (para soportar múltiples algoritmos)
- Usar patrón **Factory** para creación de entidades complejas
- Cobertura de pruebas unitarias en los componentes críticos (algoritmo de asignación, validación de conflictos)
- Ramas Git: `feature/*` → `develop` → `main`

---

## Roles del Sistema

| Rol | Permisos clave |
|---|---|
| Administrador | Usuarios, reglas configurables, logs centralizados (<1 min para identificar errores) |
| Líder DOC | Ejecutar asignación automática, supervisión del proceso, validación de datos, registra y modifica asignaciones de aulas por tiempo semestral |
| Auxiliar DOC | Registrar/modificar asignaciones de tiempo parcial (reducir errores humanos) |
| Facultad/Admisiones | Ingresa los datos académicos como: materia, grupo, profesor y horario |
| Admisiones | Ingresa la cantidad real de estudiantes por grupos de materias |

---


### Descripción escenarios de calidad
-El administrador debe poder identificar errores de asignación mediante logs centralizados en menos de 1 minuto.
-Si dos procesos intentan asignar la misma aula en el mismo horario simultáneamente, el sistema debe rechazar una de las operaciones mediante restricciones de base de datos y mantener consistencia sin corrupción de datos.
-Cuando un grupo cambia su cantidad de estudiantes antes de la asignación, el sistema debe recalcular automáticamente las opciones de aula válidas sin permitir asignaciones inconsistentes.
-El sistema debe estar disponible el 98% del tiempo durante periodos de matrícula y además en tiempos regulres, como la jornada acádemica, teniendo en cuenta, asignación de aulas (Periodos cortos), laboratorios y salas de sistemas.
-Ante una caída del servidor, conexión con base de datos, transferencia o actualización de datos el sistema debe restablecer el servicio en menos de 2 minutos sin pérdida de datos.
-El sistema debe completar la asignación de 500 grupos en menos de 5 segundos bajo condiciones normales.
-El sistema debe soportar al menos 50 usuarios concurrentes sin degradación significativa en el tiempo de respuesta.
-Si un usuario intenta acceder a funcionalidades fuera de su rol, o intenta acceder con credencial invalidas el sistema debe bloquear la acción y registrar el intento en logs de seguridad.
-Un usuario nuevo debe poder completar el proceso de asignación sin capacitación en menos de 10 minutos utilizando la interfaz.
-Cuando un líder intenta ejecutar la asignación sin datos completos, el sistema debe mostrar mensajes claros indicando exactamente qué información falta.

### Funcionalidades criticas del sistema
-Como líder de servicios docentes, necesito ejecutar el proceso de asignación automática de aulas basado en disponibilidad y capacidad, con el fin de optimizar la distribución de espacios y reducir conflictos manuales en la programación académica.
-Como sistema, debo validar automáticamente que no existan conflictos de horarios entre asignaciones de aulas para diferentes grupos, con el fin de evitar cruces que afecten la operación académica.
-Como líder de servicios docentes, necesito ejecutar simulaciones de asignación de aulas sin afectar datos reales, con el fin de evaluar diferentes escenarios antes de realizar la asignación definitiva.
-Como sistema, debo priorizar la asignación de aulas a grupos con mayor número de estudiantes, con el fin de optimizar el uso de la infraestructura institucional disponible.
-Como sistema, debo validar la integridad y consistencia de los datos registrados, como relaciones entre cursos, grupos y horarios, con el fin de evitar errores en la asignación automática.
-Como sistema, necesito recalcular automáticamente las asignaciones de aulas cuando se presenten cambios en datos críticos como cantidad de estudiantes o disponibilidad de aulas, con el fin de mantener la coherencia y validez de la programación académica.
-Como sistema, necesito gestionar múltiples solicitudes concurrentes de asignación de aulas sin generar inconsistencias en los datos, con el fin de garantizar la integridad del sistema durante periodos de alta demanda operativa.
-Como administrador del sistema, necesito definir reglas configurables para el proceso de asignación automática, con el fin de adaptar el sistema a políticas institucionales cambiantes sin necesidad de modificar el código.
-Como usuario de admisiones, necesito cargar o actualizar datos de múltiples grupos de manera masiva, con el fin de optimizar el tiempo operativo y reducir errores manuales.
-Como sistema, necesito soportar el incremento de datos como número de grupos o aulas sin degradar el rendimiento, con el fin de garantizar la sostenibilidad del sistema a largo plazo.
-Como sistema, necesito actualizar la disponibilidad de aulas en tiempo real ante cambios o reservas, con el fin de evitar inconsistencias en la información mostrada.
-Como sistema, debo verificar que todos los grupos tengan aula asignada antes de finalizar el proceso de programación académica, con el fin de garantizar la cobertura total de la operación.

---

## Funcionalidades clave del sistema
1. **Asignación automática de aulas** — algoritmo que asigna espacios a grupos según disponibilidad, capacidad y restricciones. Es el núcleo del sistema.
2. **Validación de conflictos de horario** — el sistema detecta automáticamente cruces de asignaciones entre grupos.
3. **Simulación de asignación** — permite evaluar escenarios sin afectar datos reales.
4. **Priorización por número de estudiantes** — los grupos más grandes tienen prioridad de asignación.
5. **Reglas configurables** — el administrador define reglas de asignación sin tocar el código.
6. **Reservas temporales de aulas** — con validación de conflictos en tiempo real.
7. **Carga masiva de datos** — carga de múltiples grupos de forma asíncrona.
8. **Recálculo automático** — ante cambios en datos críticos (capacidad, disponibilidad), el sistema recalcula.
9. **Disponibilidad en tiempo real** — los cambios de estado se reflejan instantáneamente via WebSocket.
10. **Verificación de cobertura total** — antes de cerrar la programación, valida que todos los grupos tengan aula.
11. **Generación de reportes** — reportes de ocupación, asignaciones y cobertura académica.
12. **Notificaciones in-app** — alertas de conflictos, confirmaciones de asignación y cambios de estado.

---

## Reglas de Oro

1. **Versiones exactas**: NUNCA modificar las versiones del stack tecnológico definidas en este archivo
2. **Clean Architecture**: respetar la dirección de dependencias — `domain` no importa nada de Django, `application` solo importa de `domain`, `infrastructure` puede usar Django, `presentation` solo llama a `application`
3. **Repository obligatorio**: ninguna vista ni caso de uso accede al ORM directamente, siempre a través del repositorio
4. **Algoritmo de asignación**: implementar con patrón Strategy + tests unitarios obligatorios desde el inicio
5. **Frontend**: Django Templates + HTMX para interacciones con servidor + Alpine.js solo para estado local de UI (modales, dropdowns, tabs) + Tailwind + daisyUI para estilos
6. **WebSockets**: usar exclusivamente para disponibilidad de aulas en tiempo real y notificaciones in-app
7. **Docker producción**: nunca usar `runserver` — siempre Gunicorn (HTTP) + Daphne (WebSocket) + Nginx
8. **Valkey único**: actúa como broker de Celery + channel layer de Django Channels + backend de caché en el mismo contenedor
9. **Antes de cualquier modelo**: mostrar el diagrama entidad-relación en texto y esperar confirmación
10. **Decisiones técnicas no obvias**: explicar antes de implementar, especialmente si implican cambios al stack
11. **Al final de cada sesión**: entregar resumen de qué se completó, qué falta y cuál es el siguiente paso

---

## Primer paso — Infraestructura base

Crea la infraestructura base del proyecto en este orden exacto.
No pases al siguiente punto sin terminar el anterior.

### 1. Estructura de carpetas
Crea todas las carpetas del proyecto según la estructura definida en este archivo.
Incluye los `__init__.py` en cada carpeta de Python.
No crees ningún archivo de lógica todavía, solo la estructura.

### 2. Archivos de dependencias
Crea `requirements/base.txt`, `requirements/dev.txt` y `requirements/prod.txt`
con las versiones exactas del stack tecnológico definido en este archivo.
Ninguna versión puede diferir de la tabla del stack.

### 3. Variables de entorno
Crea `.env.example` con todas las variables necesarias para:
PostgreSQL, Valkey, Django secret key, Celery, Prometheus, Grafana y JWT.
Crea `.gitignore` que ignore `.env`, `__pycache__`, archivos de compilación y volúmenes Docker.

### 4. Settings de Django
Crea `backend/config/settings/base.py`, `dev.py` y `prod.py`.
- `base.py`: configuración común, apps instaladas, middleware, Channels, Celery, Valkey como caché y broker
- `dev.py`: DEBUG=True, hot-reload, sin SSL
- `prod.py`: DEBUG=False, Gunicorn + Daphne, Nginx, WhiteNoise

### 5. Núcleo del sistema (core/)
Crea `backend/core/` con:
- `repositories.py`: clase abstracta `BaseRepository` con métodos genéricos (get, list, create, update, delete)
- `services.py`: clase abstracta `BaseService`
- `exceptions.py`: excepciones base del sistema
- `dtos.py`: DTOs base reutilizables

### 6. Docker Compose producción
Crea `docker-compose.yml` con estos servicios y sus versiones exactas:
- `django`: Gunicorn para HTTP + Daphne para WebSocket
- `postgres`: PostgreSQL 17
- `valkey`: Valkey 8 (broker Celery + caché + channel layer)
- `celery`: worker Celery 5.6
- `nginx`: Nginx 1.27 como proxy inverso
- `prometheus`: Prometheus 3
- `grafana`: Grafana 12

### 7. Docker Compose desarrollo
Crea `docker-compose.dev.yml` con hot-reload activado para Django y Celery.
Los volúmenes deben montar el código fuente para que los cambios se reflejen sin reconstruir la imagen.

### 8. Nginx
Crea `nginx/nginx.conf` configurado como:
- Proxy inverso HTTP → Gunicorn (puerto 8000)
- Proxy WebSocket /ws/ → Daphne (puerto 8001)
- Servir archivos estáticos directamente
- Rate limiting básico por IP

### 9. GitHub Actions
Crea `.github/workflows/ci.yml` que en cada push a cualquier rama ejecute:
- Ruff (linting)
- Black (formato)
- pytest con coverage sobre `backend/`

---

Al terminar cada punto dime qué creaste y si encontraste algún problema.
Al terminar los 9 puntos dime:
- Lista de todos los archivos creados
- Comando exacto para levantar el proyecto por primera vez
- Cuál es el siguiente módulo que construiremos (app `academico/`)

## Segundo paso — App academico/

Esta es la app base del sistema. Sin estas entidades no existe ninguna otra funcionalidad.
Construye la app `academico/` completa en este orden estricto.
No pases al siguiente punto sin terminar el anterior.

### 1. Dominio
Crea `academico/domain/` con:
- `entities.py`: Aula, Facultad, Programa, Docente, Curso, Grupo, HorarioBloque
- `interfaces.py`: IAulaRepository, IFacultadRepository, IProgramaRepository,
  IDocenteRepository, ICursoRepository, IGrupoRepository, IHorarioBloqueRepository
- `exceptions.py`: AulaNoDisponibleError, GrupoSinDocenteError, CapacidadInvalidaError

### 2. Aplicación
Crea `academico/application/` con:
- `dtos.py`: AulaInputDTO, AulaOutputDTO, GrupoInputDTO, GrupoOutputDTO,
  DocenteInputDTO, DocenteOutputDTO, CargaMasivaInputDTO
- `use_cases.py`: CrearAula, ActualizarAula, CrearGrupo, ActualizarGrupo,
  CrearDocente, CargaMasivaGrupos, ListarAulasDisponibles

### 3. Infraestructura
Crea `academico/infrastructure/` con:
- `models.py`: AulaModel, FacultadModel, ProgramaModel, DocenteModel,
  CursoModel, GrupoModel, HorarioBloqueModel
- `repositories.py`: implementación concreta de cada interfaz del dominio,
  extendiendo BaseRepository de core/
- `tasks.py`: tarea Celery para procesamiento asíncrono de carga masiva de grupos

### 4. Presentación
Crea `academico/presentation/` con:
- `serializers.py`: un serializer por entidad
- `views.py`: ViewSets para Aula, Grupo, Docente con permisos por rol
- `urls.py`: rutas REST bajo /api/academico/
- `templates/academico/`: lista y detalle para aulas y grupos con HTMX

### 5. Tests
Crea `academico/tests/` con:
- `test_domain.py`: tests de entidades sin Django (sin base de datos)
- `test_use_cases.py`: tests de casos de uso con repositorios mock
- `test_views.py`: tests de integración de endpoints REST

### 6. Migraciones
Ejecuta:
python manage.py makemigrations academico
python manage.py migrate

Al terminar este paso dime:
- Lista de archivos creados
- Si las migraciones aplicaron correctamente
- Resultado de los tests

---

## Tercer paso — App usuarios/

Sistema de autenticación y roles. Todas las vistas del sistema
dependen de esto para verificar quién está conectado y qué puede hacer.
Construye la app `usuarios/` en este orden estricto.

### 1. Dominio
Crea `usuarios/domain/` con:
- `entities.py`: Usuario, Rol, Permiso
- `interfaces.py`: IUsuarioRepository
- `exceptions.py`: CredencialesInvalidasError, PermisoInsuficienteError,
  TokenInvalidoError

### 2. Aplicación
Crea `usuarios/application/` con:
- `dtos.py`: LoginInputDTO, LoginOutputDTO, UsuarioInputDTO, UsuarioOutputDTO
- `use_cases.py`: AutenticarUsuario, CrearUsuario, AsignarRol, CambiarPassword

### 3. Infraestructura
Crea `usuarios/infrastructure/` con:
- `models.py`: extiende AbstractUser de Django con campo rol
- `repositories.py`: implementación concreta de IUsuarioRepository

### 4. Presentación
Crea `usuarios/presentation/` con:
- `serializers.py`: LoginSerializer, UsuarioSerializer, TokenSerializer
- `views.py`: LoginView (simplejwt), UsuarioViewSet con CAPTCHA en login
- `urls.py`: rutas bajo /api/usuarios/ y /api/token/
- `templates/usuarios/`: login.html con reCAPTCHA, perfil.html

### 5. Tests
Crea `usuarios/tests/` con:
- `test_domain.py`: tests de entidades y reglas de rol
- `test_views.py`: tests de login, token refresh y acceso por rol

### 6. Migraciones
python manage.py makemigrations usuarios
python manage.py migrate

Al terminar dime qué está listo y si los tests pasan.

---

## Cuarto paso — App asignacion/ (NÚCLEO DEL SISTEMA)

Esta es la funcionalidad más crítica. Requiere que academico/ y usuarios/
estén completamente terminados antes de empezar.
Antes de escribir cualquier código muéstrame el diagrama
entidad-relación de esta app en texto y espera mi confirmación.

### 1. Dominio
Crea `asignacion/domain/` con:
- `entities.py`: Asignacion, ReglaAsignacion, ResultadoAsignacion
- `interfaces.py`: IAsignacionRepository, IAsignacionStrategy
- `exceptions.py`: AsignacionConflictoError, CapacidadInsuficienteError,
  SinAulasDisponiblesError, DatosIncompletosError

### 2. Aplicación
Crea `asignacion/application/` con:
- `dtos.py`: AsignacionInputDTO, AsignacionOutputDTO,
  SimulacionInputDTO, SimulacionOutputDTO, CoberturaOutputDTO
- `use_cases.py`: EjecutarAsignacionAutomatica, SimularAsignacion,
  ValidarConflictos, VerificarCoberturaTotalGrupos, RecalcularAsignaciones

### 3. Infraestructura
Crea `asignacion/infrastructure/` con:
- `models.py`: AsignacionModel, ReglaNegocioModel, CatalogoParametroModel
- `repositories.py`: implementación concreta de IAsignacionRepository
- `strategies.py`: PrioridadEstudiantesStrategy implementando IAsignacionStrategy
- `tasks.py`: asignacion_masiva_task, recalculo_automatico_task

### 4. Presentación
Crea `asignacion/presentation/` con:
- `serializers.py`: AsignacionSerializer, ReglaSerializer, SimulacionSerializer
- `views.py`: AsignacionViewSet con endpoints para ejecutar, simular,
  verificar cobertura y recalcular
- `urls.py`: rutas bajo /api/asignacion/
- `templates/asignacion/`: dashboard principal con HTMX + WebSocket

### 5. Tests — OBLIGATORIOS
Crea `asignacion/tests/` con cobertura mínima 80%:
- `test_domain.py`: tests de Asignacion.es_valida(), conflictos,
  priorización por estudiantes
- `test_use_cases.py`: tests de EjecutarAsignacionAutomatica,
  ValidarConflictos, VerificarCobertura con mocks
- `test_views.py`: tests de integración de todos los endpoints

Al terminar dime qué está listo y los resultados de coverage.

---

## Quinto paso — App reservas/

### 1. Dominio → 2. Aplicación → 3. Infraestructura → 4. Presentación → 5. Tests
Misma secuencia. Requiere academico/ y asignacion/ terminados.
Antes de empezar muéstrame el diagrama ER y espera confirmación.

---

## Sexto paso — App notificaciones/

### 1. Dominio → 2. Aplicación → 3. Infraestructura → 4. Presentación → 5. Tests
Misma secuencia. Incluye consumers.py para Django Channels y
campana.html como partial HTMX en el navbar.
Requiere todos los pasos anteriores terminados.

---

## Séptimo paso — App reportes/

### 1. Dominio → 2. Aplicación → 3. Infraestructura → 4. Presentación → 5. Tests
Misma secuencia. Genera reportes de ocupación, asignaciones y cobertura.
La generación pesada va en tasks.py de Celery de forma asíncrona.
Requiere todos los pasos anteriores terminados.

---

## Octavo paso — Frontend global

1. `frontend/templates/base.html` con layout completo:
   Tailwind + daisyUI + HTMX + Alpine.js + campana de notificaciones
2. `frontend/templates/partials/`: navbar con roles, sidebar, toast WebSocket
3. `frontend/templates/pages/dashboard.html`: panel según rol del usuario
4. `frontend/static/js/ws-notifications.js`: conexión WebSocket a Django Channels
5. Páginas de error: 403.html, 404.html, 500.html
6. Ajustes finales de UX: mensajes de validación, estados de carga HTMX,
   confirmaciones de acciones críticas

---

Te aclaro algo: Cuando termines cada paso me dices para yo hacer un git push y luego que puedas seguir con el siguiente paso.
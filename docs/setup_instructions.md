# Guía de Instalación y Puesta en Marcha

**Sistema de Servicios Docentes — Universidad Católica de Oriente**  
Versión 0.1 | Python 3.13 | Django 5.2 LTS

---

## Requisitos Previos

Instala las siguientes herramientas antes de comenzar:

| Herramienta | Versión mínima | Instalación |
|---|---|---|
| Python | 3.13 | https://python.org/downloads |
| pip | 24 | incluido con Python |
| Git | 2.47 | https://git-scm.com |
| Docker Desktop | 27 | https://docs.docker.com/get-docker |
| Docker Compose | 2.x | incluido con Docker Desktop |

---

## Opción A — Con Docker (Recomendada) 🐳

Esta opción levanta **todos los servicios** (PostgreSQL, Valkey, Daphne, Gunicorn, Nginx, Prometheus, Grafana) con un solo comando.

### 1. Clonar el repositorio

```bash
git clone https://github.com/simongrisales/sistema-servicios-docentes.git
cd sistema-servicios-docentes
```

### 2. Configurar variables de entorno

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux / macOS
cp .env.example .env
```

Edita `.env` con valores reales si es necesario (para desarrollo el archivo de ejemplo funciona tal cual).

### 3. Levantar el stack de desarrollo

```bash
docker compose -f docker-compose.dev.yml up --build
```

Esto iniciará:
- **postgres** — Base de datos PostgreSQL 17 en el puerto `5432`
- **valkey** — Cache + broker Celery en el puerto `6379`
- **backend** — Django con hot-reload en el puerto `8000`

### 4. Aplicar migraciones (primera vez)

En otra terminal, mientras el stack está corriendo:

```bash
docker compose -f docker-compose.dev.yml exec backend python manage.py migrate
```

### 5. Crear superusuario (opcional)

```bash
docker compose -f docker-compose.dev.yml exec backend python manage.py createsuperuser
```

### 6. Acceder a la aplicación

| Servicio | URL |
|---|---|
| API REST | http://localhost:8000/api/ |
| Swagger UI | http://localhost:8000/api/docs/ |
| OpenAPI JSON | http://localhost:8000/api/schema/ |
| Admin Django | http://localhost:8000/admin/ |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 (admin / password-placeholder) |

### 7. Detener el stack

```bash
docker compose -f docker-compose.dev.yml down
```

Para eliminar también los volúmenes (base de datos):

```bash
docker compose -f docker-compose.dev.yml down -v
```

---

## Opción B — Sin Docker (Inicio rápido local) ⚡

Usa SQLite en memoria y cache local. Solo requiere Python instalado.  
**Ideal para correr tests o revisar el código rápidamente.**

> [!NOTE]
> Esta opción NO levanta PostgreSQL, Valkey ni Nginx. Solo ejecuta Django con la configuración de desarrollo que usa SQLite automáticamente durante tests.

### 1. Clonar el repositorio

```bash
git clone https://github.com/simongrisales/sistema-servicios-docentes.git
cd sistema-servicios-docentes
```

### 2. Crear entorno virtual

```bash
# Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux / macOS
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements/dev.txt
```

### 4. Configurar variables de entorno

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux / macOS
cp .env.example .env
```

> [!IMPORTANT]
> Para la Opción B (sin Docker), cambia en `.env`:
> ```
> POSTGRES_HOST=localhost
> VALKEY_HOST=localhost
> ```
> Si no tienes PostgreSQL local, los tests usarán SQLite automáticamente (configurado en `backend/config/settings/dev.py`).

### 5. Aplicar migraciones

```bash
# Asegúrate de que DJANGO_SETTINGS_MODULE esté configurado
$env:DJANGO_SETTINGS_MODULE = "config.settings.dev"   # Windows
export DJANGO_SETTINGS_MODULE=config.settings.dev      # Linux/macOS

python manage.py migrate
```

### 6. Cargar datos base de demostración

```bash
python manage.py seed_base_data
```

Este comando crea roles, usuarios demo, aulas, grupos, un docente, un curso y parámetros base.  
La contraseña de los usuarios demo es `UcoDemo2026*`.

### 7. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

Accede a: http://localhost:8000/api/docs/

---

## Ejecutar Tests

```bash
# Suite completa con cobertura
python -m pytest backend/ --cov=backend/ --cov-report=term-missing

# Solo la app de asignación
python -m pytest backend/apps/asignacion/ -v

# Con reporte HTML de cobertura
python -m pytest backend/ --cov=backend/ --cov-report=html
# Abre htmlcov/index.html en el navegador
```

---

## Verificar Calidad de Código

```bash
# Linting con Ruff
python -m ruff check backend/

# Verificar formato con Black
python -m black --check backend/

# Formatear automáticamente
python -m black backend/
```

---

## Stack Completo de Producción

Para levantar el stack completo de producción (con Nginx, Gunicorn, Daphne):

```bash
docker compose up --build
```

Servicios incluidos:
- `nginx` — Proxy inverso + WAF en puertos 80/443
- `backend` — Gunicorn (HTTP) + Daphne (WebSocket)  
- `postgres` — PostgreSQL 17
- `valkey` — Valkey 8 (Celery broker + cache)
- `celery` — Workers asíncronos
- `prometheus` — Métricas
- `grafana` — Dashboards

---

## Estructura de Ramas Git

```
main          ← Producción estable (releases etiquetados)
  └─ develop  ← Integración continua
       └─ feature/<nombre>  ← Desarrollo de features
```

**Flujo de trabajo:**
1. Crea tu rama: `git checkout -b feature/mi-feature develop`
2. Trabaja y commitea con mensajes descriptivos
3. Abre un Pull Request hacia `develop`
4. CI valida: lint, tests, cobertura ≥ 78%
5. Merge después de aprobación

---

## Resolución de Problemas Comunes

| Problema | Solución |
|---|---|
| `psycopg` no conecta a PostgreSQL | Usa la Opción B o levanta Docker primero |
| Puerto 5432 ocupado | PostgreSQL nativo de Windows usa ese puerto; usa Docker con puerto diferente o desactiva el servicio local |
| `staticfiles` no encontrado | Ejecuta `python manage.py collectstatic` o ignora la advertencia en desarrollo |
| Tests fallan con error de Valkey | Los tests usan cache en memoria automáticamente, no necesitan Valkey |
| `ruff` reporta E402 en `dev.py` | El `import sys` debe estar al principio del archivo; ya está corregido en la versión actual |

---

*Documentación del Sistema de Servicios Docentes UCO — v0.1*

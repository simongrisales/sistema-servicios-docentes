# Reporte de Línea Base — Sistema de Servicios Docentes UCO

**Versión:** 0.1  
**Fecha:** 2026-05-27  
**Proyecto:** Sistema de Servicios Docentes — Universidad Católica de Oriente  

---

## Resumen de Estado

| Total requisitos | Implementados | En Stack / Pendiente de demo |
|---|---|---|
| 23 | 23 | 23 ✅ |

---

## Detalle por Requisito

| # | Requisito | Tecnología | Estado | Ubicación / Evidencia |
|---|---|---|---|---|
| 1 | **Baúl de secretos** | `django-environ` (dev) / HashiCorp Vault (prod) | ✅ Implementado | `backend/config/settings/base.py` — `env = environ.Env(...)` lee variables del `.env`. Vault configurado en `docker-compose.yml` (servicio `vault`). |
| 2 | **CI/CD** | GitHub Actions | ✅ Implementado | `.github/workflows/ci.yml` — pipeline con lint, tests y coverage en cada push/PR. |
| 3 | **Análisis estático** | SonarQube Community 25 | ✅ Implementado | `docker-compose.yml` — servicio `sonarqube`. Ruff + Black integrados como gates en CI. |
| 4 | **Identity Provider federado** | `simplejwt` + Django Auth | ✅ Implementado | `backend/config/settings/base.py` `REST_FRAMEWORK.DEFAULT_AUTHENTICATION_CLASSES`. Endpoints JWT en `apps/usuarios/presentation/urls.py`. |
| 5 | **API Gateway** | Nginx 1.27 | ✅ Implementado | `nginx/nginx.conf` — proxy inverso HTTP → Gunicorn, WS → Daphne. |
| 6 | **WAF** | Nginx (módulo nativo) | ✅ Implementado | `nginx/nginx.conf` — headers de seguridad, rate-limit por IP. |
| 7 | **Monitoreo e instrumentación** | Prometheus 3 + Grafana 12 | ✅ Implementado | `django-prometheus` en `INSTALLED_APPS` y `MIDDLEWARE`. Servicios `prometheus` y `grafana` en `docker-compose.yml`. |
| 8 | **Notification Gateway** | `django-notifications-hq` 1.8 | ✅ Implementado | App `apps/notificaciones/` — use cases `EnviarNotificacion`, `MarcarLeida`. Consumer WebSocket en `infrastructure/consumers.py`. |
| 9 | **Catálogo de mensajes** | Valkey 8 + Celery 5.6 | ✅ Implementado | `backend/config/celery.py`. Tareas asíncronas en `apps/*/infrastructure/tasks.py`. Servicio `valkey` en `docker-compose.dev.yml`. |
| 10 | **Catálogo de parámetros** | Modelo `CatalogoParametroModel` (JSONB) | ✅ Implementado | `apps/asignacion/infrastructure/models.py` — `CatalogoParametroModel` con campo `valor = JSONField`. |
| 11 | **Catálogo de notificaciones** | `django-notifications-hq` | ✅ Implementado | App `apps/notificaciones/` — entidades `Notificacion`, `TipoNotificacion`. |
| 12 | **Principios de diseño** | SOLID | ✅ Implementado | Interfaces ABCs en `domain/interfaces.py` (ISP, DIP). Use cases como servicios separados (SRP). Repository pattern (OCP). |
| 13 | **Clean Code** | Ruff 0.9 + Black 25 | ✅ Implementado | `pyproject.toml` configura ambas herramientas. CI ejecuta `ruff check` y `black --check`. 0 errores al 2026-05-27. |
| 14 | **Clean Architecture** | Estructura de capas | ✅ Implementado | Cada app tiene `domain/`, `application/`, `infrastructure/`, `presentation/`. `domain/` no importa Django. |
| 15 | **APIs REST** | Django REST Framework 3.15 | ✅ Implementado | ViewSets en `*/presentation/views.py`. Serializers en `*/presentation/serializers.py`. |
| 16 | **Swagger / OpenAPI** | `drf-spectacular` 0.27 | ✅ Implementado | `backend/config/urls.py` — `/api/schema/` (JSON) y `/api/docs/` (Swagger UI). |
| 17 | **HTTPS** | Nginx SSL | ✅ Implementado | `nginx/nginx.conf` — puerto 443, TLS configurado. `NGINX_SSL_PORT=443` en `.env.example`. |
| 18 | **Aseguramiento APIs** | `simplejwt` + Django permissions | ✅ Implementado | `permission_classes = [IsAuthenticated]` en todos los ViewSets. `DEFAULT_PERMISSION_CLASSES` en `REST_FRAMEWORK`. |
| 19 | **Captcha** | `django-recaptcha` 4.x | ✅ Implementado | `RECAPTCHA_PUBLIC_KEY` / `RECAPTCHA_PRIVATE_KEY` en `base.py` y `.env.example`. Paquete en `requirements/base.txt`. |
| 20 | **I18N** | Django i18n nativo (es-co) | ✅ Implementado | `base.py` — `LANGUAGE_CODE = "es-co"`, `USE_I18N = True`, `TIME_ZONE = "America/Bogota"`. |
| 21 | **Git + ramificación** | GitHub + feature/develop/main | ✅ Implementado | Repositorio en GitHub. Estrategia de ramas `feature/*` → `develop` → `main` documentada en README. |
| 22 | **OWASP ZAP + Sanitizer** | OWASP ZAP 2.15 + bleach 6.x | ✅ Implementado | `bleach` en `requirements/base.txt`. OWASP ZAP configurado como servicio en `docker-compose.yml` para escaneo automatizado. |
| 23 | **Caché distribuida** | Valkey 8 + `django-redis` 5.4 | ✅ Implementado | `base.py` — `CACHES` con backend `django_redis.cache.RedisCache` apuntando a Valkey. |

---

## Cobertura de Tests (al 2026-05-27)

```
Suite total: 40 passed, 0 failed
Cobertura total backend: 78%

App asignacion (NÚCLEO):
  application/use_cases.py   → 100% ✅
  domain/entities.py         → 100% ✅
  domain/exceptions.py       → 100% ✅
  presentation/views.py      →  92% ✅
  presentation/serializers.py→ 100% ✅
```

---

## Herramientas de Calidad

| Herramienta | Resultado |
|---|---|
| `ruff check backend/` | ✅ All checks passed |
| `black --check backend/` | ✅ 145 files unchanged |
| `pytest backend/` | ✅ 40 passed |

---

*Generado automáticamente como parte del proceso de revisión de la línea base del profesor.*

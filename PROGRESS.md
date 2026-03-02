# PROGRESS.md — Estado del Proyecto Ingecon Findeter

> **Última actualización**: 2 de marzo de 2026
> **Propósito**: Este documento permite a cualquier sesión de IA (o desarrollador) entender rápidamente qué se ha hecho y qué falta por hacer.

---

## Resumen Ejecutivo

El proyecto tiene **backend funcional con 10 modelos de datos, migración Alembic, seed data, y ~30 endpoints API** incluyendo el módulo completo de Informe Semanal (generación automática, edición por secciones, transiciones de estado, snapshots de hitos, banco de fotos, y plan de acción acumulativo). **Motor de exportación Excel GES-FO-016** completamente funcional. El **frontend tiene login con JWT, dashboard conectado al API, contratos con detalle/hitos, y 7 tabs de informe semanal**. Falta: tests, Curva S, exportación PDF, y CRUD de usuarios.

---

## Lo Que Está Hecho

### 1. Infraestructura y Configuración

| Componente | Estado | Detalles |
|-----------|--------|---------|
| Docker Compose | Listo | PostgreSQL 16 + Backend + Frontend — `docker-compose.yml` |
| Backend Dockerfile | Listo | Python 3.12-slim, uvicorn con reload |
| Frontend Dockerfile | Listo | Node 22-alpine, next dev |
| `.env.example` | Listo | Backend y Frontend |
| `.gitignore` | Listo | Python, Node, IDE files |
| Alembic (config) | Listo | `alembic.ini`, `env.py`, migración `001_initial.py` con 10 tablas |
| Seed data | Listo | `backend/app/scripts/seed.py` — 7 usuarios, 1 contrato interventoría, 4 contratos de obra, 64 hitos, 22 actividades no previstas |
| pyproject.toml | Listo | Dependencies: FastAPI, SQLAlchemy, Alembic, openpyxl, passlib, python-jose |
| package.json | Listo | Next.js 16, React 19, Tailwind CSS 4 |

### 2. Backend (FastAPI) — `backend/app/`

#### Modelos SQLAlchemy (`models/`) — 10 modelos

| Modelo | Archivo | Campos principales | Relaciones |
|--------|---------|-------------------|------------|
| `Usuario` | `usuario.py` | email, nombre_completo, hashed_password, rol (7 roles), activo | — |
| `ContratoInterventoria` | `contrato.py` | numero, objeto, valor_inicial, valor_actualizado, plazo_dias, fechas, contratista, supervisor | → N contratos_obra |
| `ContratoObra` | `contrato.py` | numero, objeto, contratista, valores, plazo_dias, fechas (inicio/term/susp/reinicio) | → 1 contrato_interventoria, → N hitos, → N informes, → N fotos, → N actividades_np |
| `Hito` | `contrato.py` | numero, descripcion, fecha_programada, fecha_real, estado (enum), avance_porcentaje | → 1 contrato_obra. Property `dias_retraso` |
| `ActividadNoPrevista` | `contrato.py` | codigo (NP-01..NP-22), descripcion, fecha_programada, fecha_real | → 1 contrato_obra |
| `Foto` | `foto.py` | archivo_nombre, archivo_path, archivo_size_bytes, pie_de_foto, tipo (5 tipos), fecha_toma, lat/long | → 1 contrato_obra, → N informe_fotos |
| `InformeSemanal` | `informe.py` | numero_informe, semana_inicio/fin, estado (4 estados), avance fisico/financiero, comentarios S3/S5/S6, timestamps de transición | → 1 contrato_obra, → N snapshot_hitos, → N fotos_seleccionadas, → N acciones_plan |
| `SnapshotHito` | `informe.py` | copia inmutable del hito al momento del corte semanal, dias_retraso | → 1 informe, → 1 hito |
| `InformeFoto` | `informe.py` | tabla de unión informe↔foto, orden, pie_de_foto_override | → 1 informe, → 1 foto |
| `AccionPlan` | `informe.py` | numero, actividad, responsable, fecha_programada, fecha_cumplimiento, estado, observaciones | → 1 informe_origen |

#### Schemas Pydantic (`schemas/`)

| Archivo | Schemas |
|---------|---------|
| `contrato.py` | Create/Response para ContratoInterventoria, ContratoObra, Hito |
| `informe.py` | InformeGenerarRequest, UpdateS3/S5/S6×4, TransicionEstado, SnapshotHitoResponse, InformeSemanalList/Detail/Response |
| `usuario.py` | Create/Response para Usuario, Token, TokenPayload |
| `foto.py` | FotoCreate/Response, InformeFotoCreate/Update/Response |
| `plan_accion.py` | AccionPlanCreate/Update/Response |
| `actividad_no_prevista.py` | ActividadNoPrevistaCreate/Update/Response |

#### Endpoints API (`api/v1/endpoints/`) — ~30 endpoints

| Endpoint | Métodos | Funcionalidad |
|----------|---------|--------------|
| `/api/v1/auth/login` | POST | Login con email/password → JWT token |
| `/api/v1/dashboard` | GET | Resumen: total contratos, valor total, hitos retrasados, informes pendientes, avance general |
| `/api/v1/contratos/interventoria` | GET, POST | CRUD contrato de interventoría |
| `/api/v1/contratos/interventoria/{id}` | GET | Detalle contrato interventoría |
| `/api/v1/contratos/obra` | GET, POST | CRUD contratos de obra |
| `/api/v1/contratos/obra/{id}` | GET | Detalle contrato de obra |
| `/api/v1/contratos/obra/{id}/hitos` | GET, POST | CRUD hitos de un contrato |
| `/api/v1/contratos/obra/{id}/actividades-no-previstas` | GET, POST, PATCH | CRUD actividades no previstas |
| `/api/v1/informes/semanales` | GET | Listar informes (filtros: contrato_obra_id, estado) |
| `/api/v1/informes/semanales/{id}` | GET, PATCH | Detalle/actualizar informe |
| `/api/v1/informes/semanales/generar` | POST | Generar borrador con snapshots e indicadores |
| `/api/v1/informes/semanales/generar-todos` | POST | Generar borradores para todos los contratos activos |
| `/api/v1/informes/semanales/{id}/seccion/s3` | PATCH | Editar situaciones problemáticas |
| `/api/v1/informes/semanales/{id}/seccion/s5` | PATCH | Editar narrativa actividades no previstas |
| `/api/v1/informes/semanales/{id}/seccion/s6-*` | PATCH ×4 | Editar comentarios técnico/SST/ambiental/social |
| `/api/v1/informes/semanales/{id}/transicion` | POST | Cambiar estado (borrador→en_revision→aprobado→radicado) |
| `/api/v1/informes/semanales/{id}/snapshot-hitos` | GET | Listar snapshots de hitos |
| `/api/v1/informes/semanales/{id}/refresh-snapshot` | POST | Retomar snapshot (solo BORRADOR) |
| `/api/v1/informes/semanales/{id}/fotos` | GET, POST, PATCH, DELETE | CRUD fotos del informe |
| `/api/v1/informes/semanales/{id}/plan-accion` | GET, POST, PATCH, DELETE | CRUD plan de acción |
| `/api/v1/fotos/upload` | POST | Upload multipart de fotos |
| `/api/v1/fotos` | GET | Listar fotos por contrato/fecha/tipo |
| `/api/v1/fotos/{id}` | GET | Detalle de foto |
| `/api/v1/fotos/{id}/archivo` | GET | Servir archivo de imagen |
| `/api/v1/fotos/{id}` | DELETE | Eliminar foto (si no está en informe aprobado) |
| `/health` | GET | Health check |

#### Servicios (`services/`)

- `informe_generator.py` — Generación automática de borradores con snapshots de hitos, cálculo de indicadores, marcado de acciones vencidas, y pre-carga de fotos de la semana

#### Core (`core/`)

- `config.py` — Settings: DB URL, JWT, CORS, UPLOAD_DIR, MAX_UPLOAD_SIZE_MB, ALLOWED_IMAGE_TYPES
- `database.py` — Engine SQLAlchemy + SessionLocal + Base
- `security.py` — JWT create/verify + bcrypt hash/verify
- `deps.py` — `get_current_user` (JWT dependency), `require_roles(*roles)`

### 3. Frontend (Next.js) — `frontend/src/`

| Página/Componente | Archivo | Estado |
|-------------------|---------|--------|
| Layout principal | `app/layout.tsx` | Listo — AuthProvider + AppShell + contenido principal |
| AppShell | `components/AppShell.tsx` | Listo — Sidebar condicional (oculto en /login, visible autenticado) |
| Sidebar | `components/Sidebar.tsx` | Listo — 3 links + info de usuario + botón logout |
| Login | `app/login/page.tsx` | **Conectado al API** — Formulario email/password, JWT, redirect a /dashboard |
| Auth Context | `lib/auth.tsx` | Listo — AuthProvider, JWT en localStorage, auto-redirect, `rolLabel()` |
| Redirect raíz | `app/page.tsx` | Listo — Redirect a /dashboard |
| Dashboard | `app/dashboard/page.tsx` | **Conectado al API** — KPI cards dinámicos, hitos retrasados, avance general |
| Contratos de Obra | `app/contratos/page.tsx` | **Conectado al API** — Tabla dinámica con valores, plazos, fechas |
| Detalle Contrato | `app/contratos/[id]/page.tsx` | **Conectado al API** — Info del contrato, KPIs de hitos, tabla de hitos con avance |
| Informes Semanales | `app/informes/page.tsx` | **Conectado al API** — Selector de contrato, filtro por estado, botón generar informe, tabla dinámica |
| Detalle Informe | `app/informes/[id]/page.tsx` | **Conectado al API** — 7 tabs (S1-S7) con edición por sección, transiciones de estado |
| EstadoBadge | `components/EstadoBadge.tsx` | Listo — Badges de color para estado informe/hito/plan |
| API client | `lib/api.ts` | Listo — `apiFetch`, `apiUpload`, `apiDownload`, `fotoUrl`, auth headers, 401 redirect |
| Types | `lib/types.ts` | Listo — Interfaces TS para todos los modelos del API |

#### Tabs del Detalle de Informe (7 secciones GES-FO-016):

| Tab | Sección | Funcionalidad |
|-----|---------|--------------|
| S1 | Información General | Card read-only con datos del contrato y periodo |
| S2 | Hitos | Tabla de snapshots con semáforo, indicadores avance, botón "Actualizar Snapshot" |
| S3 | Situaciones Problemáticas | Textarea editable con autoguardado |
| S4 | Plan de Acción | Tabla interactiva con agregar/editar acciones, estados editables inline |
| S5 | Actividades No Previstas | Tabla read-only de ANP del contrato + narrativa editable |
| S6 | Comentarios Especialistas | 4 textareas (técnico, SST, ambiental, social) con guardado individual |
| S7 | Registro Fotográfico | Panel dual: banco de fotos (seleccionar) + fotos del informe (reordenar, quitar) |

### 4. Documentación

| Archivo | Propósito |
|---------|----------|
| `CLAUDE.md` | Guía completa para IA — contexto del negocio, módulos, convenciones, arquitectura |
| `docs/app-base.md` | Especificación de diseño completa — 10 módulos + 9 features IA + 4 fases |
| `docs/*.xlsx` | 5 plantillas Excel de referencia (formatos Findeter) |
| `docs/*.pdf` | 4 documentos PDF de referencia (contrato, informes ejemplo) |

### 5. Migración y Seed Data

- **`backend/alembic/versions/001_initial.py`** — Migración inicial que crea las 10 tablas con tipos, FKs, enums, y server_defaults
- **`backend/app/scripts/seed.py`** — Script ejecutable con `python -m app.scripts.seed`:
  - 7 usuarios (uno por rol, password: `Ingecon2026!`)
  - 1 contrato de interventoría (FDT-ATBOSA-I-028-2025)
  - 4 contratos de obra (CTO-703 a CTO-706)
  - 64 hitos (20 por parque vecinal, 12 por parque de bolsillo)
  - 22 actividades no previstas (NP-01 a NP-22)

---

## Lo Que FALTA Por Hacer

### Fase 1 — MVP (lo que se debe completar primero)

#### A. Infraestructura Pendiente (Prioridad: ALTA)

- [x] ~~Generar migración Alembic inicial~~
- [x] ~~Crear script de seed~~
- [x] ~~Proteger endpoints con autenticación JWT~~ — `deps.py` con `get_current_user` y `require_roles`
- [ ] **Ejecutar migración y seed en Docker** — Levantar, aplicar `alembic upgrade head`, correr seed
- [ ] **Tests backend** — 0 tests escritos. Carpeta `tests/` vacía

#### B. Backend — Módulos Faltantes (Prioridad: ALTA)

- [x] ~~Modelo `AccionPlan` (Plan de Acción S4)~~
- [x] ~~Modelo `Foto` + `InformeFoto` (Registro Fotográfico S7)~~
- [x] ~~Modelo `SnapshotHito` (Snapshots inmutables S2)~~
- [x] ~~Modelo `ActividadNoPrevista` (NP-01 a NP-22)~~
- [x] ~~Servicio de generación automática de informes~~
- [x] ~~Endpoints de edición por sección~~
- [x] ~~Endpoints de transición de estado~~
- [x] ~~Endpoints de banco de fotos~~
- [x] ~~Endpoints de plan de acción acumulativo~~
- [x] ~~Motor de exportación Excel GES-FO-016~~ — `backend/app/services/excel_export.py` + endpoint `GET /api/v1/informes/semanales/{id}/exportar`
- [x] ~~Endpoint de Curva S~~ — `GET /api/v1/informes/semanales/curva-s/{contrato_obra_id}` + `GET /api/v1/dashboard/curva-s`
- [ ] **Exportación PDF** — A partir del Excel o renderizado directo
- [ ] **CRUD Usuarios** — Solo existe login, no hay endpoint para crear/listar/editar usuarios
- [ ] **Roles y permisos por endpoint** — Los guards existen pero no están aplicados en todos los endpoints

#### C. Frontend — Funcionalidad Faltante (Prioridad: ALTA)

- [x] ~~Conectar Informes al API~~ — Lista + detalle con 7 tabs
- [x] ~~Formulario de informe semanal completo (7 secciones)~~
- [x] ~~Badges de estado con colores~~
- [x] ~~Upload de fotos y selector dual~~
- [x] ~~Conectar Dashboard al API~~ — KPI cards dinámicos, hitos retrasados, avance general
- [x] ~~Conectar Contratos al API~~ — Tabla dinámica con datos reales del backend
- [x] ~~Página de detalle de contrato~~ — `/contratos/[id]` con info del contrato y tabla de hitos
- [x] ~~Botón de exportar Excel~~ — Conectado al endpoint de exportación
- [x] ~~Login page~~ — Formulario email/password con JWT
- [x] ~~Protección de rutas~~ — AuthProvider + AppShell + redirect a /login + 401 interception
- [x] ~~Componente Curva S~~ — Recharts LineChart en Dashboard y Detalle de Contrato

#### D. IA — Fase 1 (Prioridad: MEDIA)

- [ ] **5.1 Generación de narrativas** — Integrar API de Claude para generar borradores de secciones 3, 4 y 6
- [ ] **5.2 Auditor de consistencia** — Motor de reglas de validación (30+ reglas) pre-exportación

### Fase 2 — Campo

- [ ] Modelo `InformeDiario` — Formato FR-INT-13-10
- [ ] Modelo `ChequeoSST` — Formato FDLBOSALIC 006-2024
- [ ] Modelo `ChequeoAmbiental` — Formato GES-FO-082 v2
- [ ] Modelo `ChequeoSocial` — Formato CTO 703
- [ ] Exportación Excel de cada formato
- [ ] App móvil / PWA con soporte offline
- [ ] 5.3 Alertas predictivas, 5.4 Autocompletado de chequeos

### Fase 3 — Financiero

- [ ] Modelo `ActaCorte`, `Poliza`
- [ ] Control presupuestal
- [ ] Gestión de comunicaciones
- [ ] 5.5 Mayores cantidades, 5.6 Clasificación de fotos

### Fase 4 — Valor Agregado

- [ ] Mapa interactivo, Comités, Personal en obra, PQRS
- [ ] 5.7 Actas de comité, 5.8 Chatbot RAG, 5.9 Análisis PQRS

---

## Decisiones Técnicas Tomadas

| Decisión | Detalle |
|----------|---------|
| Stack Backend | **FastAPI + SQLAlchemy 2.0 (Mapped) + Alembic + PostgreSQL** |
| Stack Frontend | **Next.js 16 + React 19 + Tailwind CSS 4** |
| Auth | **JWT con bcrypt** (python-jose + passlib) |
| Excel Engine | **openpyxl** (ya en dependencies) |
| Contenedores | **Docker Compose** con 3 servicios (db, backend, frontend) |
| API versioning | `/api/v1/` como prefijo |
| Esquema DB | Spanish column names matching domain terminology |
| Informe — Generación | Auto-genera cada lunes como borrador con datos pre-llenados |
| Informe — Edición | Cada residente edita su sección directamente en el informe |
| Informe — Hitos | Viven en módulo Contratos, informe toma snapshot inmutable al generarse |
| Informe — Fotos | Se suben durante la semana a un banco, luego se seleccionan para el informe |
| Informe — Plan Acción | Acumulativo: un registro por acción, query dinámico arrastra pendientes |

## Decisiones Pendientes

- [ ] Hosting/deployment (AWS, Azure, GCP, o on-premise)
- [ ] Storage para archivos (S3, Azure Blob, o filesystem)
- [ ] Proveedor LLM definitivo (Claude API vs GPT-4)
- [ ] App móvil nativa (React Native / Flutter) vs PWA
- [ ] Servicio de firmas digitales electrónicas
- [ ] CI/CD pipeline

---

## Próximos Pasos Recomendados (en orden)

1. **Ejecutar migración + seed en Docker** — `alembic upgrade head` + `python -m app.scripts.seed`
2. **Exportación PDF** — A partir del Excel generado
3. **Tests** — Al menos para endpoints CRUD y el motor de exportación
4. **CRUD Usuarios** — Endpoint para crear/listar/editar usuarios
5. **Roles y permisos** — Aplicar guards en todos los endpoints

---

## Cómo Levantar el Proyecto

```bash
# Opción 1: Docker Compose (recomendado)
docker-compose up --build

# Aplicar migración
docker exec -it ingecon-backend alembic upgrade head

# Ejecutar seed
docker exec -it ingecon-backend python -m app.scripts.seed

# Opción 2: Manual
# Terminal 1 — Base de datos
docker run -e POSTGRES_USER=ingecon -e POSTGRES_PASSWORD=ingecon -e POSTGRES_DB=ingecon_findeter -p 5432:5432 postgres:16-alpine

# Terminal 2 — Backend
cd backend
pip install -e .
alembic upgrade head
python -m app.scripts.seed
uvicorn app.main:app --reload --port 8000

# Terminal 3 — Frontend
cd frontend
npm install
npm run dev
```

- Backend API Docs: http://localhost:8000/docs
- Frontend: http://localhost:3000
- DB: postgresql://ingecon:ingecon@localhost:5432/ingecon_findeter

### Credenciales de prueba (seed)

| Email | Password | Rol |
|-------|----------|-----|
| director@ingecon.co | Ingecon2026! | Director de Interventoría |
| tecnico@ingecon.co | Ingecon2026! | Residente Técnico |
| sst@ingecon.co | Ingecon2026! | Residente SST |
| ambiental@ingecon.co | Ingecon2026! | Residente Ambiental |
| social@ingecon.co | Ingecon2026! | Residente Social |
| admin@ingecon.co | Ingecon2026! | Residente Administrativo |
| supervisor@findeter.gov.co | Ingecon2026! | Supervisor |

---

## Archivos Clave para Contexto

| Para entender... | Leer... |
|-----------------|---------|
| Requisitos completos del negocio | `docs/app-base.md` |
| Instrucciones para IA | `CLAUDE.md` |
| Estado actual del proyecto | `PROGRESS.md` (este archivo) |
| Modelo de datos | `backend/app/models/*.py` (10 modelos) |
| Migración | `backend/alembic/versions/001_initial.py` |
| Seed data | `backend/app/scripts/seed.py` |
| Servicio de generación | `backend/app/services/informe_generator.py` |
| Motor de exportación Excel | `backend/app/services/excel_export.py` |
| Endpoints API | `backend/app/api/v1/endpoints/*.py` |
| Páginas frontend | `frontend/src/app/*/page.tsx` |
| Template Excel más crítico | `docs/INFORME SEMANAL N° 28 CTO 703.xlsx` |

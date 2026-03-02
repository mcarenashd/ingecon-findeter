# PROGRESS.md — Estado del Proyecto Ingecon Findeter

> **Última actualización**: 2 de marzo de 2026
> **Propósito**: Este documento permite a cualquier sesión de IA (o desarrollador) entender rápidamente qué se ha hecho y qué falta por hacer.

---

## Resumen Ejecutivo

El proyecto está en una **fase de scaffolding inicial**. Se creó la estructura base del backend (FastAPI) y frontend (Next.js) con modelos de datos principales, endpoints CRUD básicos y páginas placeholder. **No hay migraciones de base de datos ejecutadas, no hay datos seed, no hay tests, y las páginas del frontend son estáticas (sin conexión real al API).**

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
| Alembic (config) | Parcial | `alembic.ini` y `env.py` existen, pero **0 migraciones generadas** |
| pyproject.toml | Listo | Dependencies: FastAPI, SQLAlchemy, Alembic, openpyxl, passlib, python-jose |
| package.json | Listo | Next.js 16, React 19, Tailwind CSS 4 |

### 2. Backend (FastAPI) — `backend/app/`

#### Modelos SQLAlchemy (`models/`)

| Modelo | Archivo | Campos principales | Relaciones |
|--------|---------|-------------------|------------|
| `ContratoInterventoria` | `contrato.py` | numero, objeto, valor_inicial, valor_actualizado, plazo_dias, fecha_inicio, fecha_terminacion, contratista, supervisor | → N contratos_obra |
| `ContratoObra` | `contrato.py` | numero, objeto, contratista, valor_inicial, adiciones, valor_actualizado, plazo_dias, fechas (inicio/term/susp/reinicio) | → 1 contrato_interventoria, → N hitos, → N informes_semanales |
| `Hito` | `contrato.py` | numero, descripcion, fecha_programada, fecha_real, estado (enum), avance_porcentaje | → 1 contrato_obra. Property `dias_retraso` calculada |
| `InformeSemanal` | `informe.py` | numero_informe, semana_inicio/fin, estado (enum: borrador/en_revision/aprobado/radicado), avance_fisico_prog/ejec, valor_acum_prog/ejec, situaciones_problematicas, actividades_no_previstas, comentarios (tecnico/sst/ambiental/social) | → 1 contrato_obra |
| `Usuario` | `usuario.py` | email, nombre_completo, hashed_password, rol (enum 7 roles), activo | Sin relaciones |

#### Schemas Pydantic (`schemas/`)

- `contrato.py` — Create/Response para ContratoInterventoria, ContratoObra, Hito
- `informe.py` — Create/Update/Response para InformeSemanal
- `usuario.py` — Create/Response para Usuario, Token, TokenPayload

#### Endpoints API (`api/v1/endpoints/`)

| Endpoint | Métodos | Funcionalidad |
|----------|---------|--------------|
| `/api/v1/auth/login` | POST | Login con email/password → JWT token |
| `/api/v1/dashboard` | GET | Resumen: total contratos, valor total, hitos retrasados, informes pendientes, avance general |
| `/api/v1/contratos/interventoria` | GET, POST | CRUD contrato de interventoría |
| `/api/v1/contratos/interventoria/{id}` | GET | Detalle contrato interventoría |
| `/api/v1/contratos/obra` | GET, POST | CRUD contratos de obra |
| `/api/v1/contratos/obra/{id}` | GET | Detalle contrato de obra |
| `/api/v1/contratos/obra/{id}/hitos` | GET, POST | CRUD hitos de un contrato |
| `/api/v1/informes/semanales` | GET, POST | Listar/crear informes semanales |
| `/api/v1/informes/semanales/{id}` | GET, PATCH | Detalle/actualizar informe semanal |
| `/health` | GET | Health check |

#### Core (`core/`)

- `config.py` — Settings con pydantic-settings (DB URL, JWT secret, CORS)
- `database.py` — Engine SQLAlchemy + SessionLocal + Base declarativa
- `security.py` — JWT create/verify + bcrypt hash/verify

### 3. Frontend (Next.js) — `frontend/src/`

| Página/Componente | Archivo | Estado |
|-------------------|---------|--------|
| Layout principal | `app/layout.tsx` | Listo — Sidebar + contenido principal |
| Sidebar | `components/Sidebar.tsx` | Listo — 3 links: Dashboard, Contratos, Informes |
| Redirect raíz | `app/page.tsx` | Listo — Redirect a /dashboard |
| Dashboard | `app/dashboard/page.tsx` | **Estático** — 4 KPI cards hardcoded, placeholders para Curva S y Semáforo de Hitos |
| Contratos de Obra | `app/contratos/page.tsx` | **Estático** — Tabla con los 4 proyectos hardcoded (datos del contrato real) |
| Informes Semanales | `app/informes/page.tsx` | **Estático** — Tabla vacía + listado de las 7 secciones del formato GES-FO-016 |
| API client | `lib/api.ts` | Listo — Función `apiFetch` genérica con manejo de errores |

### 4. Documentación

| Archivo | Propósito |
|---------|----------|
| `CLAUDE.md` | Guía completa para IA — contexto del negocio, módulos, convenciones, arquitectura |
| `docs/app-base.md` | Especificación de diseño completa — 10 módulos + 9 features IA + 4 fases |
| `docs/*.xlsx` | 5 plantillas Excel de referencia (formatos Findeter) |
| `docs/*.pdf` | 4 documentos PDF de referencia (contrato, informes ejemplo) |

---

## Lo Que FALTA Por Hacer

### Fase 1 — MVP (lo que se debe completar primero)

#### A. Infraestructura Pendiente (Prioridad: ALTA)

- [ ] **Generar migración Alembic inicial** — `alembic revision --autogenerate -m "initial"` y aplicarla
- [ ] **Crear script de seed** — Poblar la DB con: contrato de interventoría FDT-ATBOSA-I-028-2025, los 4 contratos de obra, los 20 hitos de cada parque (La Esperanza y Piamonte), usuarios iniciales (7 roles)
- [ ] **Proteger endpoints con autenticación JWT** — Los endpoints actuales NO verifican el token. Falta middleware/dependency `get_current_user`
- [ ] **Tests backend** — 0 tests escritos. Carpeta `tests/` vacía

#### B. Backend — Módulos Faltantes (Prioridad: ALTA)

- [ ] **Modelo `PlanAccion`** — Sección 4 del informe: actividad, responsable, fecha, estado (pendiente/en_proceso/cumplido/vencido)
- [ ] **Modelo `RegistroFotografico`** — Sección 7: foto (S3/blob), pie de foto, geolocalización, fecha, vinculación a informe
- [ ] **Modelo `ActividadNoPrevista`** — Ítems NP-01 a NP-22 con código, descripción, fechas
- [ ] **Endpoint de Curva S** — Generar datos de curva S a partir de avance semanal acumulado
- [ ] **Motor de exportación Excel** — **LA funcionalidad más crítica**. Generar .xlsx pixel-perfect del formato GES-FO-016 con logos, celdas combinadas, colores, fórmulas funcionales. Usar openpyxl (ya está en dependencies)
- [ ] **Exportación PDF** — A partir del Excel o renderizado directo
- [ ] **CRUD Usuarios** — Solo existe login, no hay endpoint para crear/listar/editar usuarios
- [ ] **Roles y permisos** — Verificación de rol en cada endpoint según la matriz de permisos

#### C. Frontend — Funcionalidad Real (Prioridad: ALTA)

- [ ] **Conectar Dashboard al API** — Reemplazar datos hardcoded por llamadas reales a `/api/v1/dashboard`
- [ ] **Conectar Contratos al API** — Reemplazar array estático por datos reales
- [ ] **Página de detalle de contrato** — `/contratos/[id]` con hitos, cronograma, curva S
- [ ] **Formulario de informe semanal** — Las 7 secciones editables del GES-FO-016
- [ ] **Sección 3 — Editor de texto enriquecido** — Para Situaciones Problemáticas
- [ ] **Sección 7 — Upload de fotos** — Con metadata (geolocalización, fecha)
- [ ] **Botón de exportar Excel/PDF** — Llamar al backend y descargar archivo
- [ ] **Login page** — Formulario de autenticación
- [ ] **Protección de rutas** — Redirigir a login si no hay token

#### D. IA — Fase 1 (Prioridad: MEDIA)

- [ ] **5.1 Generación de narrativas** — Integrar API de Claude/GPT para generar borradores de secciones 3, 4 y 6 del informe semanal
- [ ] **5.2 Auditor de consistencia** — Motor de reglas de validación (30+ reglas) que se ejecuta antes de exportar

### Fase 2 — Campo

- [ ] **Modelo `InformeDiario`** — Formato FR-INT-13-10 completo
- [ ] **Modelo `ChequeoSST`** — Formato FDLBOSALIC 006-2024 (6 componentes, 32 ítems)
- [ ] **Modelo `ChequeoAmbiental`** — Formato GES-FO-082 v2 (4 semanas + consolidado mensual)
- [ ] **Modelo `ChequeoSocial`** — Formato CTO 703 (10 secciones)
- [ ] **Exportación Excel** de cada formato (pixel-perfect con los templates de `docs/`)
- [ ] **App móvil / PWA** — Con soporte offline y sincronización
- [ ] **5.3 Alertas predictivas** — Regresión sobre avance semanal
- [ ] **5.4 Autocompletado de chequeos** — Precarga de valores anteriores

### Fase 3 — Financiero

- [ ] **Modelo `ActaCorte`** — Número, periodo, valor bruto, retención, valor neto, estado
- [ ] **Modelo `Poliza`** — Tipo amparo, monto, vigencia, alertas de vencimiento
- [ ] **Control presupuestal** — Balance por contrato de obra
- [ ] **Gestión de comunicaciones** — Correspondencia, consecutivos, trazabilidad
- [ ] **5.5 Mayores cantidades** — Comparador presupuesto vs ejecutado
- [ ] **5.6 Clasificación de fotos** — Modelo de visión para etiquetar fotos automáticamente

### Fase 4 — Valor Agregado

- [ ] Mapa interactivo de frentes de obra
- [ ] Módulo de comités (agendas, actas, compromisos)
- [ ] Control de personal en obra
- [ ] Gestión de PQRS
- [ ] 5.7 Actas de comité automáticas
- [ ] 5.8 Chatbot contractual (RAG)
- [ ] 5.9 Análisis de sentimiento PQRS

---

## Decisiones Técnicas Tomadas

| Decisión | Detalle |
|----------|---------|
| Stack Backend | **FastAPI + SQLAlchemy 2.0 + Alembic + PostgreSQL** |
| Stack Frontend | **Next.js 16 + React 19 + Tailwind CSS 4** |
| Auth | **JWT con bcrypt** (python-jose + passlib) |
| Excel Engine | **openpyxl** (ya en dependencies) |
| Contenedores | **Docker Compose** con 3 servicios (db, backend, frontend) |
| API versioning | `/api/v1/` como prefijo |
| Esquema DB | Spanish column names matching domain terminology |

## Decisiones Pendientes

- [ ] Hosting/deployment (AWS, Azure, GCP, o on-premise)
- [ ] Storage para archivos (S3, Azure Blob, o filesystem)
- [ ] Proveedor LLM definitivo (Claude API vs GPT-4)
- [ ] App móvil nativa (React Native / Flutter) vs PWA
- [ ] Servicio de firmas digitales electrónicas
- [ ] CI/CD pipeline

---

## Próximos Pasos Recomendados (en orden)

1. **Migración Alembic + Seed data** — Sin esto la app no funciona
2. **Auth middleware** — Proteger los endpoints existentes
3. **Conectar frontend al API** — Reemplazar datos hardcoded
4. **Página de detalle de contrato** con hitos y curva S
5. **Formulario completo del informe semanal** (las 7 secciones)
6. **Motor de exportación Excel GES-FO-016** — La funcionalidad más importante del proyecto
7. **Tests** — Al menos para los endpoints CRUD y el motor de exportación

---

## Cómo Levantar el Proyecto

```bash
# Opción 1: Docker Compose (recomendado)
docker-compose up --build

# Opción 2: Manual
# Terminal 1 — Base de datos
docker run -e POSTGRES_USER=ingecon -e POSTGRES_PASSWORD=ingecon -e POSTGRES_DB=ingecon_findeter -p 5432:5432 postgres:16-alpine

# Terminal 2 — Backend
cd backend
pip install -e .
uvicorn app.main:app --reload --port 8000

# Terminal 3 — Frontend
cd frontend
npm install
npm run dev
```

- Backend API Docs: http://localhost:8000/docs
- Frontend: http://localhost:3000
- DB: postgresql://ingecon:ingecon@localhost:5432/ingecon_findeter

---

## Archivos Clave para Contexto

| Para entender... | Leer... |
|-----------------|---------|
| Requisitos completos del negocio | `docs/app-base.md` |
| Instrucciones para IA | `CLAUDE.md` |
| Estado actual del proyecto | `PROGRESS.md` (este archivo) |
| Modelo de datos | `backend/app/models/contrato.py` + `informe.py` + `usuario.py` |
| Endpoints API | `backend/app/api/v1/endpoints/*.py` |
| Páginas frontend | `frontend/src/app/*/page.tsx` |
| Template Excel más crítico | `docs/INFORME SEMANAL N° 28 CTO 703.xlsx` |

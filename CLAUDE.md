# CLAUDE.md — Ingecon Findeter

## Project Overview

**Ingecon Findeter** is a construction oversight (interventoría) tracking application for Consorcio Infraestructura Bosa under contract FDT-ATBOSA-I-028-2025 with Findeter. The application manages oversight of public works contracts (parks, bridges, roads) in the Bosa district of Bogotá, Colombia.

The project is currently in the **design/specification phase** — no application code has been written yet. The repository contains the design proposal and reference documents that define the requirements.

### Business Context

- **Client**: Findeter (Financiera de Desarrollo Territorial)
- **Contractor**: Consorcio Infraestructura Bosa
- **Contract type**: Integral oversight — technical, administrative, financial, accounting, legal, environmental, and OHS (SST)
- **Supervised works**: Conservation and construction of public spaces, parks, bridges, and roads in Bosa, Bogotá D.C.
- **Contract values**: Oversight ~$650M COP, Works ~$4,462M COP
- **Primary language**: Spanish (all documents, UI, and business terminology)

---

## Repository Structure

```
ingecon-findeter/
├── CLAUDE.md                  # This file — AI assistant guide
└── docs/
    ├── app-base.md            # Core design document (full application specification)
    ├── *.xlsx                 # Reference Excel templates (Findeter standard formats)
    └── *.pdf                  # Reference PDF documents (contracts, reports)
```

### Key Files

| File | Purpose |
|------|---------|
| `docs/app-base.md` | **Primary design document** — Full application specification with modules, AI features, architecture, and implementation phases |
| `docs/INFORME SEMANAL N° 28 CTO 703.xlsx` | Reference: Weekly report format (6MB, most complex template) |
| `docs/7 - GESFO082...xlsx` | Reference: Environmental management checklist (GES-FO-082 v2) |
| `docs/FR-INT-13-10...xlsx` | Reference: Daily inspection report template |
| `docs/LISTA DE CHEQUEO CTO 703...xlsx` | Reference: Social checklist template |
| `docs/FDT-ATBOSA-I-028-2025...pdf` | Reference: Oversight contract document |
| `docs/INFORME SEMANAL N°24...pdf` | Reference: Sample weekly report (PDF export) |
| `docs/FR-INT-13-10...pdf` | Reference: Daily inspection report sample (PDF) |
| `docs/LISTA DE CHEQUEO GESTIÓN SST...pdf` | Reference: OHS/Environmental checklist sample |

---

## Application Modules (from design spec)

The application is designed with 10 core modules:

1. **Dashboard Ejecutivo** — Real-time KPIs, S-Curve charts, milestone traffic lights
2. **Gestión de Contratos de Obra** — Contract registry, milestones, scheduling, automatic S-Curve
3. **Informes Semanales (GES-FO-016)** — **Most critical module** — Weekly oversight reports with 7 sections
4. **Informe Diario de Inspección (FR-INT-13-10)** — Daily field inspection forms
5. **Lista de Chequeo SST y Ambiental (FDLBOSALIC 006-2024)** — OHS/Environmental checklists
6. **Lista de Chequeo Plan Manejo Ambiental (GES-FO-082 v2)** — Environmental management plan (5-tab Excel)
7. **Lista de Chequeo Social (CTO 703)** — Social compliance weekly checklists
8. **Gestión de Comunicaciones** — Correspondence tracking and document repository
9. **Bitácora de Obra** — Digital construction logbook
10. **Control Financiero** — Budget tracking, payment certificates, insurance policies

### AI Modules (9 features across 4 phases)

| Priority | Feature | LLM Required |
|----------|---------|-------------|
| High | 5.1 Automatic narrative generation for weekly reports | Yes |
| High | 5.2 Cross-consistency auditor | Partial |
| High | 5.3 Predictive delay/penalty alerts | No (statistical) |
| Medium | 5.4 Smart auto-fill for daily checklists | No |
| Medium | 5.5 Quantity variation detection | Partial |
| Medium | 5.6 Automatic photo classification | Yes (vision) |
| Low | 5.7 Committee meeting minutes generation | Yes |
| Low | 5.8 Contractual consultation chatbot (RAG) | Yes |
| Low | 5.9 PQRS sentiment analysis | Yes |

---

## Planned Technical Architecture

From the design document (`docs/app-base.md` Section 7):

- **Frontend**: React/Next.js (web) + React Native or Flutter (mobile with offline support)
- **Backend**: Node.js or Python (Django/FastAPI)
- **Database**: PostgreSQL + S3/Blob Storage for files
- **Excel Engine**: openpyxl (Python) or ExcelJS (Node) — pixel-perfect format replication is a **hard requirement**
- **AI/LLM**: Claude API (Anthropic) or GPT-4 for text generation and vision
- **Auth**: OAuth2 with role-based access per project
- **Deployment**: Cloud (AWS/Azure/GCP) or on-premise

### Data Model

```
Contrato_Interventoría (1) ── has ── (N) Contratos_Obra
Contrato_Obra (1) ── has ── (N) Hitos
Contrato_Obra (1) ── has ── (N) Informes_Semanales
Contrato_Obra (1) ── has ── (N) Informes_Diarios
Contrato_Obra (1) ── has ── (N) Chequeos_SST
Contrato_Obra (1) ── has ── (N) Chequeos_Ambientales
Contrato_Obra (1) ── has ── (N) Chequeos_Sociales
Contrato_Obra (1) ── has ── (N) Comunicaciones
Contrato_Obra (1) ── has ── (N) Actas_Corte
Contrato_Obra (1) ── has ── (N) Fotos
```

---

## Implementation Phases

| Phase | Modules | Duration |
|-------|---------|----------|
| **Phase 1 — MVP** | Dashboard + Contracts + Weekly Report + Excel Export + AI narratives + Consistency auditor | 10-12 weeks |
| **Phase 2 — Field** | Daily Report + SST/Env/Social Checklists + Mobile offline + Predictive alerts + Auto-fill | 8-10 weeks |
| **Phase 3 — Financial** | Budget control + Payment certificates + Insurance + Communications + Quantity analysis + Photo classification | 6-8 weeks |
| **Phase 4 — Value-add** | Interactive map + Committees + Personnel + PQRS + Meeting minutes + Chatbot + Sentiment analysis | 6-8 weeks |

---

## Development Conventions

### Language and Terminology

- **All UI, labels, and user-facing text must be in Spanish** — this is a Colombian government contract application
- Use the exact format codes from Findeter standards: GES-FO-016, FR-INT-13-10, GES-FO-082, FDLBOSALIC 006-2024
- Domain terms should match the contract language (interventoría, hitos, actas de corte, apremio, etc.)
- Code comments and technical documentation may be in English or Spanish — be consistent within files

### Excel Export Requirements (Critical)

The Excel export engine is the **single most important technical feature**. Every exported file must:

- Match the original Findeter template **pixel-perfectly**: merged cells, borders, colors, column widths
- Include logos (Findeter top-left, Consorcio top-right)
- Contain **working formulas** in the exported Excel files so reviewers can verify calculations
- Support export to both .xlsx and PDF
- Respect format version codes (e.g., GES-FO-016 v3, 14-Feb-2023)

### User Roles

Seven defined roles with distinct permissions:

| Role | Key Access |
|------|-----------|
| Director de Interventoría | Full access + approvals |
| Residente Técnico | Daily reports, photos |
| Residente SST | OHS checklists, incidents |
| Residente Ambiental | Environmental checklists |
| Residente Social | Community engagement, PQRS |
| Residente Administrativo/Financiero | Budget, payments, insurance |
| Supervisor (Findeter) | Read-only + approvals (VoBo) |

### Offline Support

Field personnel in Bosa parks may lack internet connectivity. The application **must support offline data entry** with sync when connectivity returns. This applies especially to:
- Daily inspection reports
- SST/Environmental checklists
- Photo capture with metadata

---

## Working with This Repository

### For AI Assistants

1. **Read `docs/app-base.md` first** — it is the authoritative design specification
2. The `.xlsx` and `.pdf` files in `docs/` are **reference templates** — the exported files from the app must match them exactly
3. No tech stack has been finalized yet — the design document suggests options but decisions are pending
4. When generating code, default to Spanish for all user-facing strings
5. Financial values use Colombian Pesos (COP) — use appropriate number formatting (dot for thousands, comma for decimals in display)
6. Date formats follow Colombian convention: DD/MM/YYYY

### Key Business Rules

- Weekly reports must be delivered on the **first business day of each week** (cutoff: Sunday)
- Monthly reports must be delivered by the **third business day of the month**
- Penalty (apremio) rate: 0.1% of contract value per day of delay (max 10%)
- OHS/Environmental checklists: scores below 90/100 require mention in weekly report
- Milestones with >30 days delay must appear in the "Situaciones Problemáticas" section
- All documents require digital signature from the Director and VoBo from the Supervisor
- Full audit trail is mandatory — who created, modified, and approved every document

### Current Project Parks

| Park | Contract | Key Detail |
|------|----------|-----------|
| La Esperanza 7-236 | 20 milestones | 147 days behind on Preliminares |
| Piamonte 7-145 | 20 milestones | Active execution |

---

## Git Workflow

- **Main branch**: `master`
- Commit messages should be descriptive and in English
- No CI/CD pipeline configured yet
- Reference documents (`.xlsx`, `.pdf`) are committed to `docs/` — keep file sizes reasonable for future additions

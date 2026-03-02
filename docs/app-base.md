# Propuesta de Diseño — Aplicación de Seguimiento de Interventoría

## Contrato FDT-ATBOSA-I-028-2025 | Consorcio Infraestructura Bosa

---

## 1. Contexto del Problema

El Consorcio Infraestructura Bosa ejecuta un contrato de interventoría integral (técnica, administrativa, financiera, contable, legal, ambiental y SST) sobre contratos de obra de conservación y construcción de espacio público, parques, puentes y malla vial en la localidad de Bosa, Bogotá D.C.

Actualmente la gestión se realiza con archivos Excel independientes, documentos Word y PDFs que se envían por correo, lo que genera duplicación de datos, errores en fechas y porcentajes, dificultad para hacer seguimiento transversal, y riesgo de incumplir los plazos de entrega de informes que el contrato exige (semanal: primer día hábil de cada semana; mensual: tercer día hábil).

---

## 2. Usuarios de la Aplicación

| Rol | Descripción | Permisos clave |
|-----|-------------|----------------|
| **Director de Interventoría** | Germán Espinel Parra. Firma informes, visión general | Todo + aprobaciones |
| **Residente Técnico** | Seguimiento diario en campo, bitácora | Crear informes diarios, cargar fotos |
| **Residente SST** | Pedro Vargas Calderón. Listas de chequeo SST | Chequeos SST, accidentes |
| **Residente Ambiental** | Adriana Neira Bustos. Chequeos ambientales | Chequeos ambientales, MAO |
| **Residente Social** | Gestión con comunidad, PQRS, punto CREA | Social, actas vecindad |
| **Residente Administrativo/Financiero** | Control presupuestal, pagos, pólizas | Módulo financiero |
| **Supervisor (Findeter)** | Dario Morales. Solo lectura + aprobaciones | Visualización, VoBo |

---

## 3. Módulos Principales

### 3.1 Dashboard Ejecutivo

Panel principal con indicadores en tiempo real de todos los contratos de obra supervisados:

- **Curva S** programado vs. ejecutado (como la del informe semanal N°24)
- Semáforo de hitos: verde (a tiempo), amarillo (riesgo), rojo (en retraso) — hoy hay 147 días de retraso en Preliminares Parque La Esperanza
- Valor programado vs. pagado vs. por pagar (Interventoría: $650M, Obra: $4.462M)
- Días transcurridos / Plazo total (172/300 interventoría, 157/240 obra)
- Alertas automáticas: informes pendientes, hitos próximos, acciones correctivas vencidas

### 3.2 Gestión de Contratos de Obra

Un módulo que registre cada contrato de obra vigilado con toda su información contractual:

- **Datos contractuales**: número, objeto, contratista, valor inicial, adiciones, valor actualizado, plazo, fechas de inicio/terminación/suspensión/reinicio
- **Hitos y cronograma**: tabla de hitos con fecha programada, fecha real de cumplimiento y cálculo automático de días de retraso (el sistema los calcula, no se digitan manualmente). Los 20 hitos del Parque La Esperanza 7-236 y los 20 del Piamonte 7-145 deben quedar precargados desde los datos contractuales
- **Actividades no previstas**: registro independiente con los ítems NP (NP-01 a NP-22 que ya existen), con su código, descripción, fecha programada y real
- **Curva S automática**: se genera con los datos de avance semanal, sin necesidad de graficar manualmente en Excel

### 3.3 Informes Semanales de Interventoría (Formato GES-FO-016)

**Este es el módulo más crítico.** El informe semanal es el producto principal del contrato y debe entregarse el primer día hábil de cada semana con corte al domingo.

La app debe replicar fielmente el formato GES-FO-016 v3 (14-Feb-2023) con estas secciones:

**Sección 1 — Información General**: se autocompleta con datos del módulo de contratos. No hay que digitarlo cada semana.

**Sección 2 — Control de Hitos**: 
- Etapa 1 (Diagnóstico): los 10 hitos (24, 25, 28, 32, 34, 41, 43, 49, 50, 52) con sus fechas
- Etapa 2 (Ejecución por parque): los 20 hitos de condiciones iniciales contractuales por cada parque
- Actividades No Previstas por parque
- **Indicadores semanales**: valor acumulado programado/ejecutado, avance físico programado/ejecutado (diagnóstico, ejecución, general), días de atraso — todos calculados automáticamente

**Sección 3 — Situaciones Problemáticas**: editor de texto enriquecido para redactar las situaciones. Posibilidad de usar plantillas o reutilizar texto de semanas anteriores con ajustes.

**Sección 4 — Plan de Acción**: tabla de actividad + responsable + fecha programada. Con seguimiento: estado (pendiente, en proceso, cumplido, vencido).

**Sección 5 — Actividades No Previstas y Mayores Cantidades**: narrativa + tabla.

**Sección 6 — Comentarios del Interventor**: campos separados para SST, Ambiental, Técnico, Social. Cada residente redacta su parte y el director consolida.

**Sección 7 — Registro Fotográfico**: carga de fotos geolocalizadas con fecha/hora automática, pie de foto, y organización en grilla de 3 columnas (como el formato actual).

**Exportación**: genera un archivo Excel (.xlsx) idéntico al formato GES-FO-016 con logos de Findeter y Consorcio, celdas combinadas, bordes, colores, etc. También permite exportar a PDF.

### 3.4 Informe Diario de Inspección (Formato FR-INT-13-10)

Formulario digital que replica exactamente el formato Findeter FR-INT-13-10 (v. 30 Ago 2013):

**Tabla superior** — Actividades Ejecutadas:
- Columnas: No | ABSC in | ABSC fi | COST | ITEM | CANTIDAD
- Columnas de Muestras para Laboratorio: TIPO | CANTIDAD

**Tabla inferior** — Detalle de Actividades Realizadas:
- Columnas: No | OBSERVACIONES

Campos de encabezado: Proyecto, Fecha, Inspector, Ing. Residente, Paginación.

**Funcionalidades extra**: 
- Llenado desde campo (móvil) sin conexión, sincronización posterior
- Vinculación automática con el presupuesto: al seleccionar un ITEM, sugiere el código COST
- Exporta a Excel manteniendo exactamente el formato original con logos

### 3.5 Lista de Chequeo SST y Ambiental (Formato FDLBOSALIC 006-2024)

Formulario digital que replica el formato de valoración del desempeño SST/Ambiental con sus 6 componentes:

- **Componente A** — SG-SST (13%): 5 ítems, ponderación 2-4
- **Componente C** — Vegetación y paisaje (8%): 2 ítems
- **Componente D** — Actividades constructivas (35%): 7 ítems, ponderación 4-6
- **Componente E** — SG-SST (39%): 17 ítems, ponderación 1-6
- **Componente F** — Demarcación y señalización (5%): 1 ítem

Para cada ítem: campo APLICA/NO APLICA, calificación 100%/0%, observaciones de texto libre.

**Cálculos automáticos**: totales por componente, total general (como el 97/100 del ejemplo), porcentajes ponderados.

**Exporta** al formato Excel exacto con la misma estructura visual.

### 3.6 Lista de Chequeo Plan de Manejo Ambiental (Formato GES-FO-082 v2)

Este formato es particularmente complejo porque tiene:

- **4 pestañas semanales** + 1 **consolidado mensual**
- Cada semana tiene 5 días de evaluación (lunes a viernes)
- 3 componentes: A (20%), B (50%), C (30%) — hay que respetar las ponderaciones exactas
- Para cada ítem: SI/NO/N.A./RESUELTO + calificación diaria 0/1 + promedio automático
- El consolidado mensual promedia las 4 semanas automáticamente

**La app debe**:
- Permitir llenar cada día individualmente (checklist rápido en campo)
- Calcular promedios semanales y mensuales automáticamente
- Generar alertas cuando un ítem baje de cierto umbral
- Exportar el Excel con las 5 pestañas exactas, fórmulas incluidas

### 3.7 Lista de Chequeo Social (Formato CTO 703)

Formato de evaluación social semanal con secciones:

- Generalidades (3 ítems)
- Información a Usuarios Beneficiarios (4 ítems)
- Divulgación (5 ítems)
- Atención al Ciudadano (3 ítems)
- Sostenibilidad (3 ítems)
- Capacitación al Personal (2 ítems)
- Apoyo Generación de Empleo (2 ítems)
- Manejo de Impactos Comerciales (3 ítems)
- Acompañamiento Social (9 ítems)
- Reportes (1 ítem)

Cada ítem: CUMPLIÓ / NO CUMPLIÓ / N/A por semana (S1-S5).

### 3.8 Gestión de Comunicaciones

Módulo para controlar toda la correspondencia contractual:

- **Registro de comunicaciones**: consecutivo, fecha, remitente, destinatario, asunto, tipo (oficio, memorando, correo, acta)
- **Trazabilidad**: vinculación con contratos de obra, con informes, con planes de acción
- **Alertas**: comunicaciones sin respuesta después de X días
- **Repositorio documental**: adjuntar archivos escaneados o digitales

### 3.9 Bitácora de Obra

Registro diario digital equivalente al libro de obra:

- Fecha, clima, personal en obra (cantidad por categoría), equipo y maquinaria
- Actividades ejecutadas (vinculadas a hitos del cronograma)
- Novedades, instrucciones, compromisos
- Registro fotográfico con geolocalización
- Firmado digital por inspector y residente

### 3.10 Control Financiero

- **Balance presupuestal** por contrato de obra: valor inicial, adiciones, valor actualizado, pagado, por pagar
- **Actas de corte / pago**: registro de cada acta con número, periodo, valor bruto, retención en garantía (10%), valor neto, estado (radicada, aprobada, pagada)
- **Flujo de caja**: programado vs. real
- **Control de pólizas**: tipo de amparo, monto, vigencia, alertas de vencimiento

---

## 4. Funcionalidades Transversales

### 4.1 Motor de Exportación de Formatos

Esta es **la funcionalidad más importante** del sistema. Los formatos NO son opcionales — son estándar contractual de Findeter y del FDLB. El motor debe:

- Generar archivos Excel (.xlsx) que sean **pixel-perfect** con los originales: mismas celdas combinadas, mismos bordes, mismos colores, mismos logos (Findeter arriba izquierda, Consorcio arriba derecha)
- Respetar códigos de formato (GES-FO-016, FR-INT-13-10, GES-FO-082, FDLBOSALIC 006-2024)
- Incluir fórmulas funcionales en los Excel exportados (para que los revisores puedan verificar cálculos)
- Exportar también a PDF para archivo formal

### 4.2 Trabajo Offline + Sincronización

El personal de campo necesita llenar formularios sin conexión a internet (los parques en Bosa no siempre tienen buena señal). La app debe funcionar en modo offline y sincronizar cuando haya conexión.

### 4.3 Registro Fotográfico Inteligente

- Captura de fotos con marca de agua automática: fecha, hora, coordenadas GPS, nombre del proyecto
- Organización automática por fecha, parque y actividad
- Vinculación con informes (una foto puede aparecer en el informe semanal y en la bitácora)

### 4.4 Alertas y Recordatorios

| Alerta | Frecuencia | Destinatario |
|--------|-----------|--------------|
| Informe semanal pendiente | Jueves de cada semana | Todo el equipo |
| Hito próximo a vencer | 15, 7 y 3 días antes | Director + Residente |
| Plan de acción vencido | Diaria | Responsable asignado |
| Póliza próxima a vencer | 30 y 15 días antes | Administrativo |
| Informe mensual pendiente | 5 días antes del cierre | Todo el equipo |
| Chequeo SST/Ambiental no diligenciado | Diaria a las 5pm | Residente SST/Ambiental |

### 4.5 Firmas Digitales

Los informes requieren firma del Director de Interventoría y VoBo del Supervisor. La app debe soportar firmas electrónicas con validez jurídica (el contrato ya reconoce firma electrónica en su Cláusula 36).

### 4.6 Auditoría y Trazabilidad

Registro de quién creó, modificó y aprobó cada documento. Esto es fundamental para la Interventoría, donde la trazabilidad es una obligación contractual.

---

## 5. Módulo de Inteligencia Artificial

La IA no se incluye como decoración ni como buzzword. Cada funcionalidad responde a un dolor específico documentado en los informes analizados. Se organizan en tres niveles de prioridad según la relación impacto/esfuerzo.

---

### 🔴 PRIORIDAD ALTA — Implementar en Fase 1-2

---

#### 5.1 Generación Automática de Narrativas del Informe Semanal

**Dolor que resuelve:** Los residentes (técnico, SST, ambiental, social) dedican entre 4 y 8 horas semanales cada uno a redactar sus secciones del informe. Los textos son técnicos, extensos y altamente repetitivos de una semana a otra. Por ejemplo, en el informe N°24, el comentario técnico tiene ~5 párrafos que esencialmente dicen "revisamos el acta de corte, la documentación está completa, hay observaciones menores". Esta redacción se repite con variaciones mínimas cada semana.

**Cómo funciona:** La IA toma como insumo los datos duros que ya están en el sistema (qué hitos avanzaron, cuáles siguen en retraso, qué chequeos se llenaron esa semana, qué fotos se tomaron, qué comunicaciones se radicaron, qué compromisos del plan de acción se cumplieron o vencieron) y genera un borrador completo para cada sección:

- **Sección 3 — Situaciones Problemáticas:** identifica automáticamente los problemas a partir de datos (ej: "Hito 1 Preliminares tiene 147 días de retraso", "Chequeo ambiental semana 4 bajó en Componente B por escombros no cubiertos") y redacta el análisis de causas con lenguaje técnico contractual.
- **Sección 4 — Plan de Acción:** propone acciones concretas vinculadas a las situaciones problemáticas identificadas, con responsables sugeridos basados en la estructura del equipo y plazos razonables.
- **Sección 6 — Comentarios del Interventor:** genera los 4 comentarios (SST, Ambiental, Técnico, Social) a partir de las actividades y novedades registradas esa semana.

El residente revisa, ajusta y aprueba. El Director consolida y firma.

**Impacto estimado:** Reducción del 60-70% del tiempo de redacción del informe semanal. Pasa de ser un proceso de 2 días a medio día entre todos los residentes.

**Implementación técnica:** API de LLM (Claude/GPT) con prompts especializados que incluyen el contexto contractual, el estilo técnico de la Interventoría y los datos de la semana como variables. Se entrena con los informes previos (N°1 al N°28 ya existentes) como ejemplos de tono y estructura.

---

#### 5.2 Auditor Automático de Consistencia Cruzada

**Dolor que resuelve:** La propia Interventoría identificó en la Sección 3 del informe N°24 que existen "inconsistencias formales en carátulas y cuadros resumen, relacionadas con errores materiales en fechas y presentación de porcentajes, atribuibles a deficiencias en el control de calidad previo a la radicación". Es decir, ellos mismos saben que el informe sale con errores porque nadie lo revisa cruzado antes de enviarlo.

**Cómo funciona:** Antes de exportar cualquier informe, la IA ejecuta un chequeo automático de más de 30 reglas de validación:

- **Consistencia numérica:** valor pagado + valor por pagar = valor actualizado. Avance físico programado de intervención ≤ 100%. Porcentajes de las listas de chequeo cuadran con las ponderaciones.
- **Consistencia de fechas:** las fechas reales de cumplimiento no son anteriores a las fechas de inicio del contrato. Los hitos marcados como "no iniciado" no tienen fecha real. El periodo del informe corresponde a la semana correcta.
- **Consistencia narrativa vs. datos:** si el avance ejecutado es menor al programado, la narrativa no puede decir "avance satisfactorio". Si hay un hito con más de 30 días de retraso, debe aparecer mencionado en situaciones problemáticas. Si un chequeo SST sacó menos de 90/100, el comentario SST debe mencionarlo.
- **Consistencia entre informes:** los valores acumulados de esta semana deben ser ≥ los de la semana anterior. El número de personal reportado es coherente con los registros de afiliación a seguridad social.
- **Completitud:** todas las secciones obligatorias están diligenciadas. El registro fotográfico tiene mínimo las fotos requeridas. Las firmas están completas.

El sistema muestra un reporte de validación con semáforo: errores bloqueantes (rojo, no deja exportar), advertencias (amarillo, deja exportar con nota), e información (verde, todo ok).

**Impacto estimado:** Eliminación del 95% de los errores formales antes de la radicación. Esto directamente mejora la relación con el Supervisor y evita devoluciones.

**Implementación técnica:** Motor de reglas deterministas (no requiere LLM) para las validaciones numéricas y de fechas. LLM solo para la validación de consistencia narrativa vs. datos, que requiere comprensión de lenguaje natural.

---

#### 5.3 Alertas Predictivas de Atraso y Riesgo de Apremio

**Dolor que resuelve:** Hoy el Consorcio se entera del nivel de retraso cuando ya ocurrió. El informe N°24 muestra 147 días de retraso en Preliminares, 129 en Excavaciones, 126 en Nivelación — pero nadie proyectó a tiempo que esto iba a pasar. El contrato establece apremio de 0.1% del valor diario (máx. 10%), lo que para un contrato de $4.462M de obra significa hasta $446M de exposición.

**Cómo funciona:** El sistema analiza la tendencia de avance de las últimas 4-8 semanas y genera:

- **Fecha estimada real de terminación** de cada hito basada en la velocidad de avance actual (no la fecha programada, que claramente no se va a cumplir en muchos casos).
- **Simulador de apremio:** muestra cuánto se acumularía en apremios si el ritmo de ejecución no cambia. "Al ritmo actual, Hito 1 terminará el 15/06/2026 (vs. programado 1/11/2025), acumulando un potencial apremio de $X".
- **Alertas tempranas:** cuando la tendencia de un hito sugiere que va a exceder la fecha programada por más de 15 días, genera una alerta al Director para que tome acción preventiva.
- **Escenarios:** permite simular "¿qué pasa si duplicamos los frentes de trabajo en Parque Piamonte?" y ver cómo afecta las proyecciones.

**Impacto estimado:** Anticipación de 2-4 semanas en la detección de problemas de cronograma. Capacidad de dimensionar la exposición financiera por apremios en tiempo real.

**Implementación técnica:** Modelos de regresión lineal y series de tiempo sobre los datos de avance semanal. No requiere LLM — es análisis estadístico clásico con buena visualización.

---

### 🟡 PRIORIDAD MEDIA — Implementar en Fase 2-3

---

#### 5.4 Autocompletado Inteligente de Chequeos Diarios

**Dolor que resuelve:** Los chequeos ambientales (GES-FO-082) tienen 26 ítems que se evalúan cada día de la semana. Los chequeos SST tienen 32 ítems. En la práctica, el 80% de los ítems no cambia de un día a otro (el cerramiento sigue instalado, las canecas siguen marcadas). El residente pierde 20-30 minutos diarios marcando lo mismo.

**Cómo funciona:** Al abrir el chequeo del día, el sistema precarga los valores del día anterior y resalta solo los ítems que históricamente cambian con más frecuencia (ej: "escombros en espacio público" y "materiales cubiertos" que en la semana 4 del chequeo ambiental bajaron a 0). El residente solo confirma con un gesto de "todo igual" o toca los ítems que cambiaron.

Adicionalmente, si el residente marca un ítem como NO CUMPLE, la IA sugiere automáticamente un texto de observación basado en observaciones anteriores para ese mismo ítem (ej: para "materiales cubiertos con lonas" sugiere "Se evidencia material sin cubrir en zona X, se requiere al contratista cubrir inmediatamente").

**Impacto estimado:** Reducción del 70% del tiempo de diligenciamiento diario de chequeos. De ~30 min a ~5 min por chequeo.

**Implementación técnica:** Lógica de precarga basada en el último registro + modelo simple de frecuencia de cambio por ítem. Para sugerencia de observaciones: búsqueda por similitud en el historial de observaciones previas.

---

#### 5.5 Asistente de Identificación de Mayores Cantidades

**Dolor que resuelve:** En la sección 5 del informe N°24, la Interventoría dedica una página entera a explicar las variaciones de cantidades. El análisis se hace manualmente comparando el presupuesto original con las cantidades certificadas en cada acta de corte. Es tedioso, propenso a errores y requiere experiencia para saber qué variaciones son normales y cuáles son preocupantes.

**Cómo funciona:** El sistema toma el presupuesto detallado del contrato de obra (con todos los ítems, unidades y cantidades originales) y lo cruza automáticamente con las cantidades acumuladas en las actas de corte. Genera:

- **Tabla de variaciones**: ítem por ítem, muestra cantidad presupuestada vs. ejecutada, diferencia absoluta y porcentual.
- **Clasificación automática**: distingue entre variaciones menores (<10%, normales de ejecución), medianas (10-25%, requieren seguimiento) y mayores (>25%, requieren justificación técnica formal).
- **Proyección de agotamiento**: para ítems con mayor ejecución que la presupuestada, estima en qué acta de corte se agotaría la cantidad contratada.
- **Borrador de justificación**: genera el párrafo técnico que explica las causas de las variaciones, adaptado al lenguaje contractual que usa la Interventoría.

**Impacto estimado:** Reducción del 80% del tiempo de análisis de cantidades. Detección temprana de ítems que se van a agotar antes de terminar la obra.

**Implementación técnica:** Cálculos deterministas para las comparaciones y proyecciones. LLM solo para la generación de la justificación narrativa.

---

#### 5.6 Clasificación Automática de Fotografías

**Dolor que resuelve:** El registro fotográfico es obligatorio en cada informe. Actualmente, cada foto se describe manualmente ("Instalación adoquín Parque La Esperanza 7-236"). Con 9+ fotos por informe semanal y fotos diarias en la bitácora, esto consume tiempo y es inconsistente.

**Cómo funciona:** Al subir una foto, la IA de visión analiza el contenido y sugiere:

- **Tipo de actividad visible**: excavación, relleno, instalación de adoquín, fundida de concreto, instalación de mobiliario, cerramiento, etc.
- **Parque/ubicación**: basado en las coordenadas GPS de la foto y los polígonos de cada parque.
- **Hito relacionado**: vincula la actividad detectada con el hito correspondiente del cronograma.
- **Pie de foto sugerido**: genera el texto descriptivo en el formato estándar ("Instalación adoquín Parque La Esperanza 7-236").

El usuario confirma o corrige la sugerencia con un toque.

**Impacto estimado:** Reducción del 50% del tiempo de gestión fotográfica. Mayor consistencia en las descripciones.

**Implementación técnica:** Modelo de visión por computador (Claude Vision o GPT-4V) con fine-tuning o prompt engineering sobre los tipos de actividad de obra civil.

---

### 🟢 PRIORIDAD BAJA — Implementar en Fase 4

---

#### 5.7 Generación Automática de Actas de Comité

**Dolor que resuelve:** Los comités de obra y seguimiento producen actas extensas con compromisos. Hoy se redactan manualmente después de cada reunión.

**Cómo funciona:** El sistema permite grabar audio del comité o tomar notas en tiempo real. La IA transcribe, identifica los temas discutidos, extrae los compromisos con responsable y plazo, y genera el borrador del acta en el formato institucional. Los compromisos se vinculan automáticamente al módulo de plan de acción del informe semanal.

**Impacto estimado:** Reducción del 90% del tiempo de elaboración de actas. Mejor captura de compromisos (no se pierde nada).

**Implementación técnica:** Whisper (OpenAI) o similar para transcripción. LLM para estructuración del acta y extracción de compromisos.

---

#### 5.8 Chatbot de Consulta Contractual

**Dolor que resuelve:** Los residentes frecuentemente necesitan consultar cláusulas específicas del contrato (plazos, obligaciones, procedimientos de apremio, requisitos de informes). Hoy abren el PDF de 32 páginas y buscan manualmente.

**Cómo funciona:** Un chatbot alimentado con el contrato FDT-ATBOSA-I-028-2025 y los términos de referencia, que responde preguntas en lenguaje natural: "¿Cuántos días tengo para entregar el informe mensual?", "¿Cuál es el procedimiento si el contratista no mantiene el personal mínimo?", "¿Qué pólizas necesito actualizar si hay una prórroga?".

**Impacto estimado:** Agilización de consultas contractuales. Especialmente útil para residentes nuevos que no conocen el contrato a fondo.

**Implementación técnica:** RAG (Retrieval-Augmented Generation) sobre los documentos contractuales. LLM con retrieval.

---

#### 5.9 Análisis de Sentimiento en PQRS y Gestión Social

**Dolor que resuelve:** El componente social registra PQRS de la comunidad y realiza socializaciones. Detectar tendencias de inconformidad tempranamente permite prevenir oposición comunitaria (que es una condición resolutoria del contrato, según la Cláusula 21).

**Cómo funciona:** La IA analiza las PQRS recibidas, los registros de asistencia a socializaciones y las actas de vecindad para identificar patrones: zonas con mayor inconformidad, temas recurrentes, ciudadanos con quejas múltiples. Genera un mapa de calor social y alertas cuando se detecta escalamiento.

**Impacto estimado:** Detección temprana de riesgos sociales que podrían escalar a oposición comunitaria formal.

**Implementación técnica:** Clasificación de texto + análisis de sentimiento con LLM. Dashboard georreferenciado.

---

### Resumen de Priorización IA

| # | Funcionalidad IA | Prioridad | Fase | Impacto en horas/semana | Requiere LLM | Complejidad |
|---|-----------------|-----------|------|------------------------|--------------|-------------|
| 5.1 | Generación de narrativas del informe semanal | 🔴 Alta | 1 | -16 a -24 hrs (todos los residentes) | Sí | Media |
| 5.2 | Auditor de consistencia cruzada | 🔴 Alta | 1 | Evita devoluciones y errores formales | Parcial | Media |
| 5.3 | Alertas predictivas de atraso y apremio | 🔴 Alta | 2 | Prevención de exposición financiera | No | Baja |
| 5.4 | Autocompletado de chequeos diarios | 🟡 Media | 2 | -5 hrs/semana (residentes SST + Amb.) | No | Baja |
| 5.5 | Identificación de mayores cantidades | 🟡 Media | 3 | -4 hrs/semana (residente técnico) | Parcial | Media |
| 5.6 | Clasificación automática de fotos | 🟡 Media | 3 | -2 hrs/semana (todos) | Sí (visión) | Media |
| 5.7 | Generación de actas de comité | 🟢 Baja | 4 | -3 hrs/comité | Sí | Alta |
| 5.8 | Chatbot contractual | 🟢 Baja | 4 | Agilización de consultas | Sí (RAG) | Media |
| 5.9 | Análisis de sentimiento PQRS | 🟢 Baja | 4 | Prevención de riesgo social | Sí | Alta |

---

## 6. Funcionalidades Extra (No-IA) que Agregan Valor

### 6.1 Mapa Interactivo de Frentes de Obra

Mapa con los parques (La Esperanza 7-236 y Piamonte 7-145) mostrando polígonos de intervención, ubicación de fotos, estado de avance por zona y ubicación de puntos CREA.

### 6.2 Módulo de Comités

Gestión de comités de obra y seguimiento: agenda, actas, compromisos con responsable, fecha límite, estado, y vinculación con el plan de acción del informe semanal.

### 6.3 Control de Personal en Obra

Registro del personal (25 directos, 10 indirectos actualmente), verificación de cumplimiento del 50% mujeres en personal calificado, control de afiliaciones a seguridad social, y vinculación de mano de obra local y población vulnerable.

### 6.4 Gestión de PQRS

Registro y seguimiento de peticiones, quejas, reclamos y sugerencias vinculado al punto CREA y al programa de atención al ciudadano.

### 6.5 Control de Ensayos de Laboratorio

Vinculado al informe diario de inspección: registro de muestras (tipo, cantidad, ubicación), seguimiento de estado (tomada → en laboratorio → resultados → evaluada), alertas cuando un resultado es desfavorable.

### 6.6 Comparador de Cantidades

Herramienta que compare cantidades presupuestadas vs. ejecutadas por ítem, detectando automáticamente mayores y menores cantidades.

---

## 7. Arquitectura Técnica Sugerida

### Stack recomendado

- **Frontend**: React/Next.js (web) + React Native o Flutter (móvil) con capacidad offline
- **Backend**: Node.js o Python (Django/FastAPI) 
- **Base de datos**: PostgreSQL + almacenamiento de archivos en S3/Blob Storage
- **Motor de Excel**: librería openpyxl (Python) o ExcelJS (Node) para generación fiel de formatos
- **IA/LLM**: API de Claude (Anthropic) o GPT-4 para generación de texto y visión
- **Autenticación**: OAuth2 con roles por proyecto
- **Despliegue**: Cloud (AWS/Azure/GCP) o en infraestructura propia

### Modelo de datos simplificado

```
Contrato_Interventoría (1) ──── tiene ──── (N) Contratos_Obra
Contrato_Obra (1) ──── tiene ──── (N) Hitos
Contrato_Obra (1) ──── tiene ──── (N) Informes_Semanales
Contrato_Obra (1) ──── tiene ──── (N) Informes_Diarios
Contrato_Obra (1) ──── tiene ──── (N) Chequeos_SST
Contrato_Obra (1) ──── tiene ──── (N) Chequeos_Ambientales
Contrato_Obra (1) ──── tiene ──── (N) Chequeos_Sociales
Contrato_Obra (1) ──── tiene ──── (N) Comunicaciones
Contrato_Obra (1) ──── tiene ──── (N) Actas_Corte
Contrato_Obra (1) ──── tiene ──── (N) Fotos
```

---

## 8. Fases de Implementación

| Fase | Módulos | IA incluida | Duración estimada |
|------|---------|-------------|-------------------|
| **Fase 1 — MVP** | Dashboard + Contratos + Informe semanal + Exportación Excel | 5.1 Narrativas + 5.2 Auditor consistencia | 10-12 semanas |
| **Fase 2 — Campo** | Informe diario + Chequeos SST/Amb./Social + App móvil offline | 5.3 Alertas predictivas + 5.4 Autocompletado chequeos | 8-10 semanas |
| **Fase 3 — Financiero** | Control presupuestal + Actas de corte + Pólizas + Comunicaciones | 5.5 Mayores cantidades + 5.6 Clasificación fotos | 6-8 semanas |
| **Fase 4 — Valor agregado** | Mapa interactivo + Comités + Personal + PQRS | 5.7 Actas comité + 5.8 Chatbot + 5.9 Sentimiento PQRS | 6-8 semanas |

---

## 9. Inventario de Formatos a Replicar

| # | Código | Nombre | Frecuencia | Formato original |
|---|--------|--------|------------|------------------|
| 1 | GES-FO-016 v3 | Informe Semanal de Interventoría | Semanal (lunes) | Excel multi-hoja |
| 2 | FR-INT-13-10 | Informe Diario de Actividades de Inspección | Diario | Excel 3 hojas |
| 3 | FDLBOSALIC 006-2024 | Lista de Chequeo Valoración SST/Ambiental | Semanal | Excel 1 hoja |
| 4 | GES-FO-082 v2 | Lista de Chequeo Plan de Manejo Ambiental | Semanal + Consolidado mensual | Excel 5 hojas |
| 5 | (Lista Chequeo Social) | Lista de Chequeo Gestión Social CTO 703 | Mensual | Excel 1 hoja |

Todos estos formatos deben exportarse con fidelidad total: mismos logos, celdas combinadas, bordes, colores, fórmulas funcionales, paginación y estructura visual.

---

## 10. Resumen de Valor

La aplicación le permitiría al Consorcio Infraestructura Bosa:

- **Reducir el tiempo de elaboración del informe semanal** de ~2 días a ~4 horas gracias a autocompletado + IA narrativa
- **Eliminar errores de transcripción** (fechas, porcentajes, valores) con el auditor automático de consistencia
- **Cumplir consistentemente los plazos de entrega** (primer día hábil) con alertas y flujo de trabajo colaborativo
- **Anticipar problemas de cronograma** con 2-4 semanas de antelación mediante alertas predictivas
- **Dimensionar la exposición financiera por apremios** en tiempo real, no después de que se materialicen
- **Reducir el tiempo de chequeos diarios en campo** de 30 minutos a 5 minutos con autocompletado inteligente
- **Tener visibilidad en tiempo real** del estado de 4 proyectos simultáneos desde un solo dashboard
- **Facilitar la auditoría y trazabilidad** que exige el contrato con registro completo de todas las acciones
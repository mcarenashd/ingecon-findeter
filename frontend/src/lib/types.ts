export type EstadoInforme = "borrador" | "en_revision" | "aprobado" | "radicado";
export type EstadoPlanAccion = "pendiente" | "en_proceso" | "cumplido" | "vencido";
export type EstadoHito = "no_iniciado" | "en_proceso" | "cumplido" | "vencido";
export type TipoFoto = "avance" | "sst" | "ambiental" | "social" | "general";

// --- Dashboard ---
export interface HitoResumen {
  id: number;
  contrato_numero: string;
  descripcion: string;
  fecha_programada: string;
  dias_retraso: number;
  estado: EstadoHito;
  avance_porcentaje: string;
}

export interface DashboardData {
  total_contratos_obra: number;
  valor_total_obra: string;
  hitos_en_retraso: HitoResumen[];
  total_informes_pendientes: number;
  avance_fisico_general: string;
}

// --- Contratos ---
export interface ContratoInterventoria {
  id: number;
  numero: string;
  objeto: string;
  valor_inicial: string;
  valor_actualizado: string;
  plazo_dias: number;
  fecha_inicio: string;
  fecha_terminacion: string;
  contratista: string;
  supervisor: string;
}

export interface Hito {
  id: number;
  contrato_obra_id: number;
  numero: number;
  descripcion: string;
  fecha_programada: string;
  fecha_real: string | null;
  estado: EstadoHito;
  avance_porcentaje: string;
  dias_retraso: number;
}

export interface ContratoObra {
  id: number;
  contrato_interventoria_id: number;
  numero: string;
  objeto: string;
  contratista: string;
  valor_inicial: string;
  adiciones: string;
  valor_actualizado: string;
  plazo_dias: number;
  fecha_inicio: string;
  fecha_terminacion: string;
  fecha_suspension: string | null;
  fecha_reinicio: string | null;
}

export interface SnapshotHito {
  id: number;
  hito_id: number;
  numero: number;
  descripcion: string;
  fecha_programada: string;
  fecha_real: string | null;
  estado: EstadoHito;
  avance_porcentaje: string;
  dias_retraso: number;
}

export interface InformeSemanalList {
  id: number;
  contrato_obra_id: number;
  numero_informe: number;
  semana_inicio: string;
  semana_fin: string;
  estado: EstadoInforme;
  avance_fisico_ejecutado: string;
  updated_at: string;
}

export interface InformeSemanalDetail {
  id: number;
  contrato_obra_id: number;
  numero_informe: number;
  semana_inicio: string;
  semana_fin: string;
  estado: EstadoInforme;
  avance_fisico_programado: string;
  avance_fisico_ejecutado: string;
  valor_acumulado_programado: string;
  valor_acumulado_ejecutado: string;
  situaciones_problematicas: string | null;
  actividades_no_previstas: string | null;
  actividades_no_previstas_narrativa: string | null;
  comentario_tecnico: string | null;
  comentario_sst: string | null;
  comentario_ambiental: string | null;
  comentario_social: string | null;
  fecha_envio_revision: string | null;
  fecha_aprobacion: string | null;
  fecha_radicacion: string | null;
  snapshot_hitos: SnapshotHito[];
  created_at: string;
  updated_at: string;
}

export interface AccionPlan {
  id: number;
  numero: number;
  informe_origen_id: number;
  actividad: string;
  responsable: string;
  responsable_usuario_id: number | null;
  fecha_programada: string;
  fecha_cumplimiento: string | null;
  estado: EstadoPlanAccion;
  observaciones: string | null;
  created_at: string;
  updated_at: string;
}

export interface Foto {
  id: number;
  contrato_obra_id: number;
  archivo_nombre: string;
  archivo_path: string;
  archivo_size_bytes: number;
  pie_de_foto: string | null;
  tipo: TipoFoto;
  fecha_toma: string;
  latitud: string | null;
  longitud: string | null;
  created_at: string;
}

export interface InformeFoto {
  id: number;
  informe_semanal_id: number;
  foto_id: number;
  orden: number;
  pie_de_foto_override: string | null;
  foto: Foto;
}

export interface ActividadNoPrevista {
  id: number;
  contrato_obra_id: number;
  codigo: string;
  descripcion: string;
  fecha_programada: string | null;
  fecha_real: string | null;
}

// --- Curva S ---
export interface CurvaSDataPoint {
  semana: number;
  semana_fin: string;
  programado: number;
  ejecutado: number;
}

export interface CurvaSResponse {
  contrato_obra_id: number;
  contrato_numero: string;
  datos: CurvaSDataPoint[];
}

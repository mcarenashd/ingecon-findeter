"use client";

import { useEffect, useState, useCallback } from "react";
import { apiFetch } from "@/lib/api";
import { useAuth, rolLabel } from "@/lib/auth";
import type { Usuario, RolUsuario } from "@/lib/types";

const ROLES: { value: RolUsuario; label: string }[] = [
  { value: "director_interventoria", label: "Director de Interventoría" },
  { value: "residente_tecnico", label: "Residente Técnico" },
  { value: "residente_sst", label: "Residente SST" },
  { value: "residente_ambiental", label: "Residente Ambiental" },
  { value: "residente_social", label: "Residente Social" },
  { value: "residente_administrativo", label: "Residente Administrativo" },
  { value: "supervisor", label: "Supervisor" },
];

const EMPTY_FORM = {
  nombre_completo: "",
  email: "",
  rol: "residente_tecnico" as RolUsuario,
  password: "",
};

export default function UsuariosPage() {
  const { user } = useAuth();
  const isDirector = user?.role === "director_interventoria";

  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // Formulario crear/editar
  const [showForm, setShowForm] = useState(false);
  const [editandoId, setEditandoId] = useState<number | null>(null);
  const [form, setForm] = useState(EMPTY_FORM);
  const [saving, setSaving] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  const loadUsuarios = useCallback(() => {
    apiFetch<Usuario[]>("/api/v1/usuarios")
      .then(setUsuarios)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    loadUsuarios();
  }, [loadUsuarios]);

  // Auto-hide success message
  useEffect(() => {
    if (successMsg) {
      const t = setTimeout(() => setSuccessMsg(null), 3000);
      return () => clearTimeout(t);
    }
  }, [successMsg]);

  const openCrear = () => {
    setEditandoId(null);
    setForm(EMPTY_FORM);
    setFormError(null);
    setShowForm(true);
  };

  const openEditar = (u: Usuario) => {
    setEditandoId(u.id);
    setForm({
      nombre_completo: u.nombre_completo,
      email: u.email,
      rol: u.rol,
      password: "",
    });
    setFormError(null);
    setShowForm(true);
  };

  const cancelar = () => {
    setShowForm(false);
    setEditandoId(null);
    setFormError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    setSaving(true);

    try {
      if (editandoId) {
        // PATCH — solo enviar campos que cambiaron
        const body: Record<string, string> = {
          nombre_completo: form.nombre_completo,
          email: form.email,
          rol: form.rol,
        };
        if (form.password) body.password = form.password;

        await apiFetch(`/api/v1/usuarios/${editandoId}`, {
          method: "PATCH",
          body: JSON.stringify(body),
        });
        setSuccessMsg("Usuario actualizado correctamente");
      } else {
        // POST — crear
        if (!form.password) {
          setFormError("La contraseña es obligatoria al crear un usuario");
          setSaving(false);
          return;
        }
        await apiFetch("/api/v1/usuarios", {
          method: "POST",
          body: JSON.stringify(form),
        });
        setSuccessMsg("Usuario creado correctamente");
      }
      setShowForm(false);
      setEditandoId(null);
      loadUsuarios();
    } catch (err: unknown) {
      setFormError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setSaving(false);
    }
  };

  const toggleActivo = async (u: Usuario) => {
    try {
      await apiFetch(`/api/v1/usuarios/${u.id}`, {
        method: "PATCH",
        body: JSON.stringify({ activo: !u.activo }),
      });
      setSuccessMsg(u.activo ? "Usuario desactivado" : "Usuario activado");
      loadUsuarios();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Error");
    }
  };

  // KPIs
  const totalActivos = usuarios.filter((u) => u.activo).length;
  const totalInactivos = usuarios.filter((u) => !u.activo).length;
  const rolesEnUso = new Set(usuarios.filter((u) => u.activo).map((u) => u.rol)).size;

  if (error && !usuarios.length) {
    return (
      <div>
        <h1 className="text-2xl font-bold text-slate-900 mb-4">
          Administración de Usuarios
        </h1>
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
          {error}
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400">
        Cargando usuarios...
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6 flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">
            Administración de Usuarios
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            {usuarios.length} usuario{usuarios.length !== 1 ? "s" : ""}{" "}
            registrado{usuarios.length !== 1 ? "s" : ""}
          </p>
        </div>
        {isDirector && (
          <button
            onClick={openCrear}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
          >
            + Nuevo Usuario
          </button>
        )}
      </div>

      {/* Messages */}
      {successMsg && (
        <div className="mb-4 p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-sm text-emerald-700">
          {successMsg}
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        <div className="bg-white rounded-xl border border-slate-200 p-4">
          <p className="text-xs font-medium text-slate-500 uppercase tracking-wide">
            Usuarios Activos
          </p>
          <p className="text-2xl font-bold text-slate-900 mt-1">{totalActivos}</p>
        </div>
        <div className="bg-white rounded-xl border border-slate-200 p-4">
          <p className="text-xs font-medium text-slate-500 uppercase tracking-wide">
            Inactivos
          </p>
          <p className="text-2xl font-bold text-slate-900 mt-1">{totalInactivos}</p>
        </div>
        <div className="bg-white rounded-xl border border-slate-200 p-4">
          <p className="text-xs font-medium text-slate-500 uppercase tracking-wide">
            Roles en Uso
          </p>
          <p className="text-2xl font-bold text-slate-900 mt-1">
            {rolesEnUso} / {ROLES.length}
          </p>
        </div>
      </div>

      {/* Formulario crear/editar */}
      {showForm && (
        <div className="bg-white rounded-xl border border-slate-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">
            {editandoId ? "Editar Usuario" : "Nuevo Usuario"}
          </h2>
          {formError && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
              {formError}
            </div>
          )}
          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">
                  Nombre Completo
                </label>
                <input
                  type="text"
                  required
                  value={form.nombre_completo}
                  onChange={(e) =>
                    setForm({ ...form, nombre_completo: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Ej: Juan Carlos Pérez"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  required
                  value={form.email}
                  onChange={(e) =>
                    setForm({ ...form, email: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="correo@ingecon.co"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">
                  Rol
                </label>
                <select
                  value={form.rol}
                  onChange={(e) =>
                    setForm({ ...form, rol: e.target.value as RolUsuario })
                  }
                  className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {ROLES.map((r) => (
                    <option key={r.value} value={r.value}>
                      {r.label}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">
                  Contraseña{editandoId ? " (dejar vacío para no cambiar)" : ""}
                </label>
                <input
                  type="password"
                  required={!editandoId}
                  value={form.password}
                  onChange={(e) =>
                    setForm({ ...form, password: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder={editandoId ? "Sin cambios" : "Contraseña segura"}
                />
              </div>
            </div>
            <div className="flex gap-3 mt-5">
              <button
                type="submit"
                disabled={saving}
                className="bg-blue-600 text-white px-5 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors disabled:opacity-50"
              >
                {saving
                  ? "Guardando..."
                  : editandoId
                    ? "Guardar Cambios"
                    : "Crear Usuario"}
              </button>
              <button
                type="button"
                onClick={cancelar}
                className="bg-slate-100 text-slate-700 px-5 py-2 rounded-lg text-sm font-medium hover:bg-slate-200 transition-colors"
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Tabla de usuarios */}
      {usuarios.length === 0 ? (
        <div className="bg-white rounded-xl border border-slate-200 p-12 text-center text-slate-400">
          No hay usuarios registrados.
        </div>
      ) : (
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200">
                <th className="text-left px-4 py-3 font-semibold text-slate-700">
                  Usuario
                </th>
                <th className="text-left px-4 py-3 font-semibold text-slate-700">
                  Email
                </th>
                <th className="text-left px-4 py-3 font-semibold text-slate-700">
                  Rol
                </th>
                <th className="text-center px-4 py-3 font-semibold text-slate-700">
                  Estado
                </th>
                {isDirector && (
                  <th className="text-center px-4 py-3 font-semibold text-slate-700">
                    Acciones
                  </th>
                )}
              </tr>
            </thead>
            <tbody>
              {usuarios.map((u) => (
                <tr
                  key={u.id}
                  className={`border-b border-slate-100 hover:bg-slate-50 ${
                    !u.activo ? "opacity-60" : ""
                  }`}
                >
                  <td className="px-4 py-3">
                    <div className="font-medium text-slate-900">
                      {u.nombre_completo}
                    </div>
                  </td>
                  <td className="px-4 py-3 text-slate-600">{u.email}</td>
                  <td className="px-4 py-3">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700">
                      {rolLabel(u.rol)}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        u.activo
                          ? "bg-emerald-50 text-emerald-700"
                          : "bg-red-50 text-red-700"
                      }`}
                    >
                      {u.activo ? "Activo" : "Inactivo"}
                    </span>
                  </td>
                  {isDirector && (
                    <td className="px-4 py-3 text-center">
                      <div className="flex items-center justify-center gap-2">
                        <button
                          onClick={() => openEditar(u)}
                          className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                        >
                          Editar
                        </button>
                        <span className="text-slate-300">|</span>
                        <button
                          onClick={() => toggleActivo(u)}
                          className={`text-sm font-medium ${
                            u.activo
                              ? "text-red-600 hover:text-red-800"
                              : "text-emerald-600 hover:text-emerald-800"
                          }`}
                        >
                          {u.activo ? "Desactivar" : "Activar"}
                        </button>
                      </div>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

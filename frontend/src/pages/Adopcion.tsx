import { useEffect, useState } from "react";
import { getAllMascotas } from "../animalService";
import { Link } from "react-router-dom";
import axios from "axios";
import "./Adopcion.css";

type Mascota = {
  id_mascota: number;
  nombre_mascota: string;
  edad?: number;
  id_especie: number;
  id_raza: number;
  fotos?: { url: string }[];
};

type Especie = {
  id_especie: number;
  nombre: string;
};

type Raza = {
  id_raza: number;
  nombre: string;
  id_especie: number;
};

export default function Adopcion() {
  const [mascotas, setMascotas] = useState<Mascota[]>([]);
  const [filtroNombre, setFiltroNombre] = useState("");
  const [especies, setEspecies] = useState<Especie[]>([]);
  const [razas, setRazas] = useState<Raza[]>([]);
  const [especieSeleccionada, setEspecieSeleccionada] = useState("");
  const [razaSeleccionada, setRazaSeleccionada] = useState("");
  const roles = JSON.parse(localStorage.getItem("roles") || "[]");

  useEffect(() => {
    getAllMascotas().then((res) => setMascotas(res.data));
    axios
      .get("http://localhost:5000/especies/")
      .then((res) => setEspecies(res.data));
    axios.get("http://localhost:5000/razas/").then((res) => setRazas(res.data));
  }, []);

  const razasFiltradas = especieSeleccionada
    ? razas.filter((r) => r.id_especie === Number(especieSeleccionada))
    : razas;

  const mascotasFiltradas = mascotas.filter((m) => {
    const coincideNombre = m.nombre_mascota
      .toLowerCase()
      .includes(filtroNombre.toLowerCase());
    const coincideEspecie =
      !especieSeleccionada || m.id_especie === Number(especieSeleccionada);
    const coincideRaza =
      !razaSeleccionada || m.id_raza === Number(razaSeleccionada);
    return coincideNombre && coincideEspecie && coincideRaza;
  });

  return (
    <div className="adopcion-container">
      <h2>Mascotas en adopción</h2>
      <div className="filtros">
        <input
          type="text"
          placeholder="Buscar por nombre"
          value={filtroNombre}
          onChange={(e) => setFiltroNombre(e.target.value)}
        />
        <select
          value={especieSeleccionada}
          onChange={(e) => {
            setEspecieSeleccionada(e.target.value);
            setRazaSeleccionada("");
          }}
        >
          <option value="">Todas las especies</option>
          {especies.map((e) => (
            <option key={e.id_especie} value={e.id_especie}>
              {e.nombre}
            </option>
          ))}
        </select>
        <select
          value={razaSeleccionada}
          onChange={(e) => setRazaSeleccionada(e.target.value)}
        >
          <option value="">Todas las razas</option>
          {razasFiltradas.map((r) => (
            <option key={r.id_raza} value={r.id_raza}>
              {r.nombre}
            </option>
          ))}
        </select>
        {(roles.includes("Administrador") || roles.includes("Voluntario")) && (
          <button
            onClick={() => {
              /* lógica para agregar mascota */
            }}
          >
            Agregar Mascota
          </button>
        )}
      </div>
      <div className="mascotas-list">
        {mascotasFiltradas.length === 0 && (
          <p>No hay mascotas que coincidan con la búsqueda.</p>
        )}
        {mascotasFiltradas.map((m) => (
          <div className="mascota-card" key={m.id_mascota}>
            <div className="mascota-img">
              <img
                src={
                  m.fotos && m.fotos.length > 0
                    ? m.fotos[0].url
                    : "/fondo_refugio.jpg"
                }
                alt={m.nombre_mascota}
              />
            </div>
            <div className="mascota-info">
              <h3>{m.nombre_mascota}</h3>
              <p className="raza">
                Raza:{" "}
                {razas.find((r) => r.id_raza === m.id_raza)?.nombre ||
                  "Sin raza"}
              </p>
              <p className="edad">
                Edad: {m.edad ? m.edad + " años" : "No especificada"}
              </p>
              {(roles.includes("Administrador") ||
                roles.includes("Voluntario")) && (
                <>
                  <button
                    onClick={() => {
                      /* lógica editar */
                    }}
                  >
                    Editar
                  </button>
                  <button
                    onClick={() => {
                      /* lógica eliminar */
                    }}
                  >
                    Eliminar
                  </button>
                </>
              )}
              {roles.includes("Usuario") && (
                <button
                  onClick={() => {
                    /* lógica para solicitar adopción */
                  }}
                >
                  Adoptar
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

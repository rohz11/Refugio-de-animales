import axios from "axios";
const API_URL = "http://localhost:5000/mascotas";

// Listar todas las mascotas
export function getAllMascotas() {
  return axios.get(`${API_URL}/`);
}

// Ver detalles de una mascota
export function getMascota(id) {
  return axios.get(`${API_URL}/${id}`);
}

// Registrar mascota (requiere token)
export function createMascota(data, token) {
  return axios.post(`${API_URL}/`, data, {
    headers: { Authorization: `Bearer ${token}` }
  });
}

// Editar mascota (requiere token)
export function updateMascota(id, data, token) {
  return axios.put(`${API_URL}/${id}`, data, {
    headers: { Authorization: `Bearer ${token}` }
  });
}

// Eliminar mascota (requiere token)
export function deleteMascota(id, token) {
  return axios.delete(`${API_URL}/${id}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
}
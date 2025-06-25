import axios from "axios";

const API_URL = "http://localhost:5000";

// Log Functions
export function registerUser(data) {
  return axios.post(`${API_URL}/usuarios/registro`, data);
}

export function loginUser(data) {
  return axios.post(`${API_URL}/usuarios/login`, data);
}

// Users functions
export function miUser() {
  return axios.get(`${API_URL}/usuarios/me`);
}

// Cambiar preguntas de seguridad
export function changeSecurityQuestions(data) {
  return axios.post(`${API_URL}/usuarios/cambiar-preguntas`, data);
}

// Cambiar nombre de usuario
export function changeUsername(data) {
  return axios.post(`${API_URL}/usuarios/cambiar-usuario`, data);
}

// Cambiar clave de usuario
export function changePassword(data) {
  return axios.put(`${API_URL}/usuarios/cambiar-clave`, data);
}

// datos Persona
// Cambiar nombre
export function changeName(data) {
  return axios.put(`${API_URL}/usuarios/cambiar-nombre`, data);
}

// Cambiar apellido
export function changeSurname(data) {
  return axios.put(`${API_URL}/usuarios/cambiar-apellido`, data);
}

// Cambiar DNI
export function changeDNI(data) {
  return axios.put(`${API_URL}/usuarios/cambiar-dni`, data);
}

// Cambiar correo
export function changeEmail(data) {
  return axios.put(`${API_URL}/usuarios/cambiar-correo`, data);
}

// Cambiar teléfono
export function changePhone(data) {
  return axios.put(`${API_URL}/usuarios/cambiar-telefono`, data);
}

// Cambiar dirección
export function changeAddress(data) {
  return axios.put(`${API_URL}/usuarios/cambiar-direccion`, data);
}

// Admin functions
// Asignar rol a un usuario
export function asignRol(data) {
  return axios.post(`${API_URL}/usuarios/asignar-rol`, data);
}

// Obtener todos los usuarios
export function getUsers() {
  return axios.get(`${API_URL}/usuarios`);
}

// Eliminar un usuario por ID
export function deleteUser(id) {
  return axios.delete(`${API_URL}/usuarios/${id}`);
}

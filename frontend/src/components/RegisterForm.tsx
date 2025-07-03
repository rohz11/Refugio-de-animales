import React, { useState } from "react";
import { registerUser } from "../userService";

const RegisterForm: React.FC = () => {
  const [form, setForm] = useState({
    nombre: "",
    apellido: "",
    dni: "",
    telefono: "",
    direccion: "",
    email: "",
    alias: "",
    clave: "",
    pregunta: "",
    respuesta: "",
  });
  const [mensaje, setMensaje] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Construir el payload según espera el backend
      const payload = {
        alias: form.alias,
        clave: form.clave,
        correo: form.email,
        pregunta_seguridad: form.pregunta,
        respuesta_seguridad: form.respuesta,
        persona: {
          nombre: form.nombre,
          apellido: form.apellido,
          dni: form.dni,
          telefono: form.telefono,
          direccion: form.direccion,
        },
      };
      await registerUser(payload);
      setMensaje("¡Registro exitoso!");
    } catch (error: any) {
      setMensaje("Error en el registro");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="nombre"
        placeholder="Nombre"
        value={form.nombre}
        onChange={handleChange}
        required
      />
      <input
        name="apellido"
        placeholder="Apellido"
        value={form.apellido}
        onChange={handleChange}
        required
      />
      <input
        name="dni"
        placeholder="DNI"
        value={form.dni}
        onChange={handleChange}
        required
      />
      <input
        name="telefono"
        placeholder="Teléfono"
        value={form.telefono}
        onChange={handleChange}
        required
      />
      <input
        name="direccion"
        placeholder="Dirección"
        value={form.direccion}
        onChange={handleChange}
        required
      />
      <input
        name="email"
        type="email"
        placeholder="Email"
        value={form.email}
        onChange={handleChange}
        required
      />
      <input
        name="alias"
        placeholder="Alias de usuario"
        value={form.alias}
        onChange={handleChange}
        required
      />
      <input
        name="clave"
        type="password"
        placeholder="Clave"
        value={form.clave}
        onChange={handleChange}
        required
      />
      <input
        name="pregunta"
        placeholder="Pregunta de seguridad"
        value={form.pregunta}
        onChange={handleChange}
        required
      />
      <input
        name="respuesta"
        placeholder="Respuesta de seguridad"
        value={form.respuesta}
        onChange={handleChange}
        required
      />
      <button type="submit">Registrarse</button>
      {mensaje && <p>{mensaje}</p>}
    </form>
  );
};

export default RegisterForm;

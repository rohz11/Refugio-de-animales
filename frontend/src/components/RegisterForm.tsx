import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../api";

export default function RegisterForm() {
  const [alias, setAlias] = useState("");
  const [clave, setClave] = useState("");
  const [pregunta, setPregunta] = useState("");
  const [respuesta, setRespuesta] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await apiFetch("/usuarios/registro", {
        method: "POST",
        body: JSON.stringify({
          alias,
          clave,
          pregunta_seguridad: pregunta,
          respuesta_seguridad: respuesta,
        }),
      });
      navigate("/login");
    } catch (err) {
      setError("Error al registrar usuario");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Registrarse</h2>
      <input
        value={alias}
        onChange={(e) => setAlias(e.target.value)}
        placeholder="Usuario"
        required
      />
      <input
        type="password"
        value={clave}
        onChange={(e) => setClave(e.target.value)}
        placeholder="Contraseña"
        required
      />
      <input
        value={pregunta}
        onChange={(e) => setPregunta(e.target.value)}
        placeholder="Pregunta de seguridad"
        required
      />
      <input
        value={respuesta}
        onChange={(e) => setRespuesta(e.target.value)}
        placeholder="Respuesta de seguridad"
        required
      />
      <button type="submit">Registrarse</button>
      {error && <div style={{ color: "red" }}>{error}</div>}
    </form>
  );
}

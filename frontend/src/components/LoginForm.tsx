import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../api";
import "./LoginForm.css";

export default function LoginForm() {
  const [alias, setAlias] = useState("");
  const [clave, setClave] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const data = await apiFetch("/usuarios/login", {
        method: "POST",
        body: JSON.stringify({ alias, clave }),
      });
      localStorage.setItem("token", data.access_token);
      navigate("/perfil");
    } catch (err) {
      setError("Credenciales incorrectas");
    }
  };

  return (
  <div className="login-bg">
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
      <h2>Iniciar sesión</h2>
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
      <button type="submit">Entrar</button>
      {error && <div style={{ color: "red" }}>{error}</div>}
      </form>
    </div> 
  </div> 
  );
}

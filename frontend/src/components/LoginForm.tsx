import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../userService";
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
      const res = await loginUser({ alias, clave });
      const { access_token } = res.data;
      // Puedes ajustar el tiempo de expiración según tu backend (ejemplo: 1 hora)
      const expiresInMinutes = 60;
      const expiresAt = Date.now() + expiresInMinutes * 60 * 1000;
      localStorage.setItem("token", access_token);
      localStorage.setItem("token_expires_at", expiresAt.toString());
      localStorage.setItem("alias", alias); 
      navigate("/home");
    } catch (err) {
      setError("Credenciales incorrectas");
    }
  };

  return (
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
  );
}

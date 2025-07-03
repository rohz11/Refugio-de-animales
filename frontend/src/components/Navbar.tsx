import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  const expiresAt = localStorage.getItem("token_expires_at");
  const alias = localStorage.getItem("alias");
  const isLoggedIn = token && expiresAt && Date.now() < Number(expiresAt);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("token_expires_at");
    localStorage.removeItem("alias");
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand">Huellitas de amor</div>
      <div className="navbar-links">
        <Link className="nav-link" to="/Home">
          Home
        </Link>
        <Link className="nav-link" to="/adopcion">
          Adopción
        </Link>
        <Link className="nav-link" to="/cuidados">
          Cuidados
        </Link>
        <div className="login-register-group">
          {isLoggedIn ? (
            <>
              <button
                className="user-alias"
                onClick={() => navigate("/perfil")}
                style={{
                  background: "none",
                  border: "none",
                  color: "#333",
                  cursor: "pointer",
                }}
              >
                👤 {alias}
              </button>
              <button className="logout-btn" onClick={handleLogout}>
                Cerrar sesión
              </button>
            </>
          ) : (
            <>
              <Link className="login-btn" to="/login">
                Iniciar sesión
              </Link>
              <Link className="register-btn" to="/register">
                Registrarse
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import "./Navbar.css";

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const toggleMobile = () => setMobileOpen((v) => !v);
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
      <div className="navbar-inner">
        <div
          className="navbar-brand"
          role="button"
          tabIndex={0}
          onClick={() => navigate("/")}
        >
          Huellitas de amor
        </div>

        <button
          className={`hamburger ${mobileOpen ? "is-active" : ""}`}
          onClick={toggleMobile}
          aria-expanded={mobileOpen}
          aria-label="Toggle navigation"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        <div className={`navbar-links ${mobileOpen ? "open" : ""}`}>
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
      </div>
    </nav>
  );
}

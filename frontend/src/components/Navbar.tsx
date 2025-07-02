import { Link } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
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
          <Link className="login-btn" to="/login">
            Iniciar sesión
          </Link>
          <Link className="register-btn" to="/register">
            Registrarse
          </Link>
        </div>
      </div>
    </nav>
  );
}

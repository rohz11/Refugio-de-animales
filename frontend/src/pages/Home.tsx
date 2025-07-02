import "./Home.css";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="home-bg">
      <div className="home-content">
        <h1 className="home-title">¿Y si el amor de tu vida tiene cuatro patas?</h1>
        <p className="home-subtitle">
          Dales un hogar. Gánate un amigo para siempre. Cada mascota tiene una historia y un corazón lleno de amor esperando por ti. Adoptar no solo cambia su vida… también cambiará la tuya. Explora, enamórate y da ese primer paso hacia una conexión única. Porque cuando adoptas, rescatas más que una vida: encuentras una amistad incondicional.
        </p>
        <Link to="/adopcion" className="adopt-btn">
          Adopta aquí
        </Link>
      </div>
    </div>
  );
}

import "./Home.css";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="home-bg">
      <div className="home-content">
        <h1 className="home-title">¿Te falta un compañero en casa?</h1>
        <p className="home-subtitle">
          Adopte un leal amigo en nuestro refugio (West Animal Side Center)
        </p>
        <Link to="/adopcion" className="adopt-btn">
          Adopta aquí
        </Link>
      </div>
    </div>
  );
}

import "./Home.css";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <main className="home-bg" role="main">
      <div className="home-content">
        <section className="hero">
          <div className="hero-text">
            <h1 className="home-title">Encuentra un amigo que te espere con la cola moviéndose</h1>
            <p className="home-subtitle">
              En nuestro refugio cada animal tiene nombre y una pequeña historia. Navega entre perfiles, conoce su personalidad y descubre cómo puedes darles una segunda oportunidad. Adoptar es un acto de amor — ven y enamórate.
            </p>
            <div className="hero-ctas">
              <Link to="/adopcion" className="adopt-btn">Adopta ahora</Link>
            </div>
          </div>
        </section>

        <section className="features" aria-label="Opciones rápidas">
          <article className="feature-card">
            <div className="card-icon">🐶</div>
            <h3 className="card-title">Adopciones</h3>
            <p className="card-text">Explora mascotas disponibles con fotos y ficha de personalidad.</p>
            <Link to="/adopcion" className="card-link">Ver mascotas</Link>
          </article>

          <article className="feature-card">
            <div className="card-icon">🤝</div>
            <h3 className="card-title">Cómo ayudar</h3>
            <p className="card-text">Voluntariado, donaciones y campañas — formas prácticas de colaborar.</p>
            <Link to="/cuidados" className="card-link">Aprende más</Link>
          </article>

          <article className="feature-card">
            <div className="card-icon">🎁</div>
            <h3 className="card-title">Dona</h3>
            <p className="card-text">Apoya con recursos para comida, medicinas y mejoras en el refugio.</p>
            <Link to="/perfil_adopcion" className="card-link">Contribuir</Link>
          </article>
        </section>
      </div>
    </main>
  );
}

import React from "react";
import "./Ayudas.css";

export default function Ayudas() {
  return (
    <main className="ayudas-page">
      <header className="ayudas-hero">
        <div className="ayudas-hero-inner container">
          <h1>Cómo puedes ayudar</h1>
          <p className="lead">
            Cada aporte cuenta: conoce las formas de apoyar al refugio y a los
            animales que necesitan un hogar.
          </p>
          <div className="hero-ctas">
            <a className="btn primary" href="#donar">
              Donar ahora
            </a>
            <a className="btn outline" href="#voluntariado">
              Ser voluntario
            </a>
          </div>
        </div>
      </header>

      <section id="donar" className="container ayudas-section">
        <h2>Donaciones</h2>
        <p>
          Las donaciones permiten pagar atención veterinaria, alimento y
          mantenimiento. Puedes donar dinero, alimento o materiales. A continuación
          encontrarás opciones seguras y transparentes.
        </p>

        <div className="donation-grid">
          <div className="card">
            <h3>Donación mensual</h3>
            <p>
              Un aporte mensual nos ayuda a planificar y cubrir necesidades
              recurrentes (alimentos, vacunas, desparasitaciones).
            </p>
            <ul>
              <li>Desde 5 USD/mes — apoyo básico</li>
              <li>Desde 20 USD/mes — apoyo veterinario</li>
            </ul>
          </div>

          <div className="card">
            <h3>Donación puntual</h3>
            <p>
              Para casos de emergencia, campañas de esterilización o campañas
              específicas. Puedes donar mediante transferencia o plataformas.
            </p>
          </div>

          <div className="card">
            <h3>Donación en especie</h3>
            <p>
              Alimento seco/húmedo, mantas, productos de limpieza, correas y
              juguetes en buen estado son siempre bienvenidos.
            </p>
          </div>
        </div>
      </section>

      <section id="voluntariado" className="container ayudas-section">
        <h2>Voluntariado</h2>
        <p>
          Convertirte en voluntario es una de las maneras más directas de ayudar.
          Acompañar, pasear, socializar y colaborar en eventos marca una gran
          diferencia.
        </p>

        <div className="vol-grid">
          <div className="card">
            <h3>Paseo y socialización</h3>
            <p>Pasea perros, socializa gatos y ayuda a reducir su estrés.</p>
          </div>
          <div className="card">
            <h3>Apoyo en eventos</h3>
            <p>Ayuda en campañas de adopción, ferias y recaudación de fondos.</p>
          </div>
          <div className="card">
            <h3>Tareas de mantenimiento</h3>
            <p>Limpieza, organización de donaciones y pequeños arreglos.</p>
          </div>
        </div>

        <p className="notes">
          Para ser voluntario debes completar una breve inscripción y asistir a
          una inducción. Contacta con nosotros para recibir más información.
        </p>
      </section>

      <section className="container ayudas-section">
        <h2>Apadrinamiento</h2>
        <p>
          Apadrinar a una mascota significa aportar una ayuda regular que se
          destina directamente a su cuidado. Recibirás actualizaciones y fotos
          del apadrinado.
        </p>
      </section>

      <section className="container ayudas-section contact">
        <h2>Contacto</h2>
        <p>
          ¿Listo para ayudar o tienes dudas? Escríbenos y te indicaremos los
          pasos: <strong>contacto@refugio.org</strong> — o llama al +34 600 000 000.
        </p>
      </section>
    </main>
  );
}

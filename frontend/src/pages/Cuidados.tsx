import React from "react";
import "./Cuidados.css";

export default function Cuidados() {
	return (
		<main className="cuidados-page">
			<header className="cuidados-hero">
				<div className="cuidados-hero-inner">
					<h1>Cuidados esenciales para nuestras mascotas</h1>
					<p className="lead">
						Consejos prácticos y cariño: todo lo que necesitas saber para darle a
						tu compañero peludo una vida sana, feliz y llena de amor.
					</p>
					<div className="hero-ctas">
						<a className="btn primary" href="#nutricion">
							Aprende sobre nutrición
						</a>
						<a className="btn outline" href="#salud">
							Salud y prevención
						</a>
					</div>
				</div>
			</header>

			<section className="cuidados-intro container">
				<h2>Por qué los cuidados importan</h2>
				<p>
					Las mascotas dependen de nosotros para sobrevivir y prosperar. Un
					cuidado consistente —alimentación adecuada, ejercicio, higiene y
					atención veterinaria— transforma su calidad de vida. Aquí encontrarás
					guías claras, fáciles de aplicar, pensadas para fomentar el vínculo
					entre tú y tu mascota.
				</p>
			</section>

			<section id="nutricion" className="container cuidados-section">
				<div className="section-grid">
					<div className="card">
						<h3>Nutrición equilibrada</h3>
						<p>
							Una dieta adecuada según la especie, edad, tamaño y estado de salud
							es la base del bienestar. Evita cambios bruscos de alimento y
							consulta al veterinario para necesidades especiales.
						</p>
						<ul>
							<li>Alimento de calidad, por porciones y horarios consistentes.</li>
							<li>Agua fresca disponible siempre.</li>
							<li>Evitar comida humana peligrosa (chocolate, cebolla, uvas).</li>
						</ul>
					</div>

					<div className="card">
						<h3>Control de peso y porciones</h3>
						<p>
							El sobrepeso acorta la vida y provoca enfermedades. Sigue las
							guías del fabricante y ajusta la ración según la actividad.
						</p>
						<ol>
							<li>Pesa a tu mascota regularmente.</li>
							<li>Reduce premios calóricos, usa snacks saludables.</li>
							<li>Haz ejercicio diario adaptado a su edad y raza.</li>
						</ol>
					</div>

					<div className="card">
						<h3>Suplementos y dietas especiales</h3>
						<p>
							Solo bajo indicación veterinaria. Algunos animales requieren dietas
							veterinarias para problemas renales, alergias o metabólicos.
						</p>
					</div>
				</div>
			</section>

			<section id="salud" className="container cuidados-section">
				<h2>Salud y prevención</h2>
				<div className="section-grid">
					<div className="card">
						<h3>Vacunas y desparasitaciones</h3>
						<p>
							Mantén el calendario de vacunas al día y desparasita según la
							recomendación local. Protege a tu mascota y a tu familia.
						</p>
					</div>

					<div className="card">
						<h3>Revisiones periódicas</h3>
						<p>
							Revisiones veterinarias anuales (o más frecuentes en animales
							mayores) permiten detectar problemas a tiempo.
						</p>
					</div>

					<div className="card">
						<h3>Primeros auxilios básicos</h3>
						<p>
							Aprende a controlar hemorragias leves, inmovilizar fracturas
							temporales y reconocer signos de urgencia (vómito persistente,
							respiración dificultosa, colapso).
						</p>
					</div>
				</div>
			</section>

			<section className="container cuidados-section">
				<h2>Higiene y bienestar diario</h2>
				<div className="tips-grid">
					<div className="tip">
						<strong>Cepillado:</strong>
						<p>Evita nudos y revisa la piel. Frecuencia según largo de pelo.</p>
					</div>
					<div className="tip">
						<strong>Baños:</strong>
						<p>No abuses: usa shampoos adecuados. Consulta por piel sensible.</p>
					</div>
					<div className="tip">
						<strong>Cuidado dental:</strong>
						<p>Cepilla los dientes o usa snacks dentales para prevenir placa.</p>
					</div>
					<div className="tip">
						<strong>Corte de uñas:</strong>
						<p>Realízalo con cuidado o acude a un profesional para evitar dolor.</p>
					</div>
				</div>
			</section>

			<section className="container cuidados-section">
				<h2>Entrenamiento y socialización</h2>
				<p>
					El entrenamiento refuerza la convivencia y reduce estrés. Premia el
					buen comportamiento, sé consistente y usa refuerzo positivo.
				</p>
				<ul className="checklist">
					<li>Rutinas de paseo diarias y ejercicio mental.</li>
					<li>Socialización temprana con personas y otros animales.</li>
					<li>Clases de obediencia si es necesario.</li>
				</ul>
			</section>

			<section className="container cuidados-section resources">
				<h2>Recursos rápidos</h2>
				<div className="resource-grid">
					<a className="resource" href="#">
						Guía de alimentación por edades
					</a>
					<a className="resource" href="#">
						Lista de control para el primer día en casa
					</a>
					<a className="resource" href="#">
						Preguntas frecuentes sobre vacunas
					</a>
					<a className="resource" href="#">
						Contacto de emergencias veterinarias
					</a>
				</div>
			</section>

			<footer className="cuidados-cta container">
				<div className="cta-inner">
					<div>
						<h3>¿Listo para brindar el mejor cuidado?</h3>
						<p>Pequeños hábitos hacen grandes diferencias. Empieza hoy.</p>
					</div>
					<div className="cta-actions">
						<button className="btn primary">Ver guía completa</button>
						<button className="btn outline">Contactar voluntarios</button>
					</div>
				</div>
			</footer>
		</main>
	);
}


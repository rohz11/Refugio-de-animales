import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import LoginForm from "./components/LoginForm";
import RegisterForm from "./components/RegisterForm";
import Home from "./pages/Home";
import Adopcion from "./pages/Adopcion";
import Cuidados from "./pages/Cuidados";
import Ayudas from "./pages/Ayudas";
<link
  href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,500,600,700&display=swap"
  rel="stylesheet"
></link>;

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/Home" element={<Home />} />
        <Route path="/Adopcion" element={<Adopcion />} />
        <Route path="/ayudas" element={<Ayudas />} />
        <Route path="/cuidados" element={<Cuidados />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/register" element={<RegisterForm />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

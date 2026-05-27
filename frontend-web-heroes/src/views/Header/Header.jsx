import "./Header.css";

export default function Header({ currentView, setCurrentView }) {
  return (
    <header className="header">
      <nav className="header-nav">
        {/* BOTÓN TABERNA */}
        <button
          className={`header-btn ${currentView === "shop" ? "active" : ""}`}
          onClick={() => setCurrentView("shop")}
        >
          Taberna
        </button>

        {/* BOTÓN LISTA DE PERSONAJES */}
        <button
          className={`header-btn ${currentView === "heroes" ? "active" : ""}`}
          onClick={() => setCurrentView("heroes")}
        >
          Lista de personajes
        </button>

        {/* BOTÓN MISIONES (INTERFAZ DE COMBATE) */}
        <button
          className={`header-btn ${currentView === "combat" ? "active" : ""}`}
          onClick={() => setCurrentView("combat")}
        >
          Misiones
        </button>

        <button className="header-btn">...</button>

        <div className="header-resources">
          <span>Recursos: Oro: 150</span>
        </div>

        <button className="header-btn logout">Cerrar sesión</button>
      </nav>
    </header>
  );
}

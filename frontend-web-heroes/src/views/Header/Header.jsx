import React, { useState } from "react";
import "./Header.css";

export default function Header({ currentView, setCurrentView }) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="header">
      <nav className="header-nav">
        {/* GRUPO IZQUIERDO: Navegación Principal */}
        <div className="nav-group-left">
          <button
            className={`header-btn ${currentView === "shop" ? "active" : ""}`}
            onClick={() => setCurrentView("shop")}
          >
            Tienda
          </button>

          <button
            className={`header-btn ${currentView === "heroes" ? "active" : ""}`}
            onClick={() => setCurrentView("heroes")}
          >
            Héroes
          </button>

          <button
            className={`header-btn ${currentView === "combat" ? "active" : ""}`}
            onClick={() => setCurrentView("combat")}
          >
            Tablón
          </button>
        </div>

        {/* GRUPO DERECHO: Recursos y Menú de Usuario */}
        <div className="nav-group-right">
          <div className="header-resources">
            <span className="resource-value">150</span>
            <span className="resource-icon">💰</span>
          </div>

          {/* Contenedor relativo para el menú desplegable */}
          <div className="user-menu-container">
            <button
              className={`header-btn hamburger-btn ${isMenuOpen ? "active" : ""}`}
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              ☰
            </button>

            {/* Menú Desplegable */}
            {isMenuOpen && (
              <div className="user-dropdown">
                <div className="dropdown-header">
                  <span className="dropdown-username">Aventurero</span>
                  <small>Nivel 1</small>
                </div>
                <div className="dropdown-divider"></div>
                <button className="dropdown-item">Mi Perfil</button>
                <button className="dropdown-item">Ajustes</button>
                <button className="dropdown-item logout">Cerrar sesión</button>
              </div>
            )}
          </div>
        </div>
      </nav>
    </header>
  );
}

import React, { useState } from "react";
import "./Header.css";
import logoWebHeroes from "./logo-web-heroes2.png";
import ItemIcon from "../BattleView/components/ItemIcon";

export default function Header({ currentView, setCurrentView, user, onLogout }) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="header">
      <nav className="header-nav">
        {/* GRUPO IZQUIERDO: Navegación Principal y Logo */}
        <div className="nav-group-left">
          {/* Contenedor del Logo */}
          <div className="header-logo-container">
            <img
              src={logoWebHeroes}
              alt="Web Heroes Logo"
              className="header-logo-img"
            />
          </div>

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
            className={`header-btn ${currentView === "missions" ? "active" : ""}`}
            onClick={() => setCurrentView("missions")}
          >
            Tablón
          </button>
        </div>

        {/* GRUPO DERECHO: Recursos y Menú de Usuario */}
        <div className="nav-group-right">
          <div className="header-resources">
            <span className="resource-value">{user?.gold ?? 0}</span>
            <ItemIcon item={{ sprite_x: 7, sprite_y: 0, name: "Moneda de oro" }} />
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
                  <span className="dropdown-username">
                    {user?.name ?? "Aventurero"}
                  </span>
                  <small>{user ? "Bienvenido" : "Invitado"}</small>
                </div>
                <div className="dropdown-divider"></div>
                <button className="dropdown-item">Mi Perfil</button>
                <button className="dropdown-item">Ajustes</button>
                <button className="dropdown-item logout" onClick={onLogout}>
                  Cerrar sesión
                </button>
              </div>
            )}
          </div>
        </div>
      </nav>
    </header>
  );
}

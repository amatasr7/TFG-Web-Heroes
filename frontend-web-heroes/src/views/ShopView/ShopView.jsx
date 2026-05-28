import React, { useState } from "react";
import "./ShopView.css";
import spriteMercader from "../../assets/sprites/Icons_15.png";

export default function ShopView() {
  const [oroJugador] = useState(150);

  // Generamos un array fijo de 25 elementos para renderizar las cuadrículas
  const slots = Array.from({ length: 25 });

  return (
    <div className="tienda-wrapper">
      <div className="tienda-container">
        {/* FILA SUPERIOR: PORTRAIT E INVENTARIOS */}
        <div className="tienda-fila-superior">
          {/* PANEL IZQUIERDO: FOTO VENDEDOR */}
          <div className="tienda-panel-vendedor">
            <div className="tienda-marco-retrato">
              <img
                src={spriteMercader}
                alt="Vendedor"
                className="tienda-retrato-img"
              />
            </div>
          </div>

          {/* PANEL DERECHO: INVENTARIOS */}
          <div className="tienda-panel-inventarios">
            {/* Inventario del Vendedor */}
            <div className="tienda-columna-inventario">
              <h3 className="tienda-inventario-titulo">Inventario Vendedor</h3>
              <div className="tienda-inventario-cuadricula">
                {slots.map((_, i) => (
                  <div key={`vendedor-slot-${i}`} className="tienda-slot">
                    {/* Renderizamos iconos de prueba en los primeros slots */}
                    {i < 2 && <span>⚔️</span>}
                  </div>
                ))}
              </div>
            </div>

            {/* Línea divisoria central */}
            <div className="tienda-divisor-vertical"></div>

            {/* Mi Inventario */}
            <div className="tienda-columna-inventario">
              <h3 className="tienda-inventario-titulo">Mi Inventario</h3>
              <div className="tienda-inventario-cuadricula">
                {slots.map((_, i) => (
                  <div key={`jugador-slot-${i}`} className="tienda-slot"></div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* FILA INFERIOR: DIÁLOGO Y CONTROLES */}
        <div className="tienda-fila-inferior">
          {/* TEXTO VENDEDOR */}
          <div className="tienda-panel-texto">
            <p className="tienda-texto-titulo">¡Bienvenido, viajero!</p>
            <p className="tienda-texto-sub">¿Qué deseas comprar hoy?</p>
          </div>

          {/* CONTROLES (DINERO Y BOTONES) */}
          <div className="tienda-panel-controles">
            {/* MI DINERO */}
            <div className="tienda-bloque-dinero">
              <span className="tienda-dinero-etiqueta">Mi Dinero</span>
              <div className="tienda-dinero-valor-contenedor">
                <span className="tienda-dinero-cantidad">{oroJugador}</span>
                <span className="tienda-dinero-icono">💰</span>
              </div>
            </div>

            {/* BOTONES DE TIENDA */}
            <div className="tienda-bloque-botones">
              <button className="tienda-btn tienda-btn-comprar">Comprar</button>
              <button className="tienda-btn tienda-btn-vender">Vender</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

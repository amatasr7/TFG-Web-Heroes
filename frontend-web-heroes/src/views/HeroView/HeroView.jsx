import React, { useState } from "react";
import "./HeroView.css";
import spriteHeroeDefault from "../../assets/sprites/Icons_01.png";

export default function HeroView() {
  const [heroes, setHeroes] = useState([
    {
      id: 1,
      nombre: "Eldrin el Valiente",
      clase: "Guerrero",
      nivel: 5,
      hp: 120,
      maxHp: 120,
      mp: 20,
      maxMp: 20,
      ataque: 24,
      defensa: 18,
      equipo: {
        cabeza: "Casco de Hierro",
        pecho: "Cota de Malla",
        mano: "Espada Bastarda",
        pies: "Botas de Cuero",
      },
    },
    {
      id: 2,
      nombre: "Lumina",
      clase: "Maga de Fuego",
      nivel: 4,
      hp: 75,
      maxHp: 75,
      mp: 110,
      maxMp: 110,
      ataque: 32,
      defensa: 8,
      equipo: {
        cabeza: "Tocado Arcano",
        pecho: "Túnica de Seda",
        mano: "Bastón de Fuego",
        pies: "Sandalias",
      },
    },
    {
      id: 3,
      nombre: "Kaelen",
      clase: "Pícaro",
      nivel: 4,
      hp: 90,
      maxHp: 90,
      mp: 40,
      maxMp: 40,
      ataque: 21,
      defensa: 12,
      equipo: {
        cabeza: "Capucha Global",
        pecho: "Chaqueta de Cuero",
        mano: "Dagas Gemelas",
        pies: "Botas Ligeras",
      },
    },
  ]);

  const [selectedHeroId, setSelectedHeroId] = useState(1);
  const heroeSeleccionado =
    heroes.find((h) => h.id === selectedHeroId) || heroes[0];

  // Slots fijos para simular el inventario general del usuario (estilo Tienda)
  const slotsInventario = Array.from({ length: 12 });

  return (
    <div className="heroe-wrapper">
      <div className="heroe-container">
        <h2 className="heroe-titulo">PANEL DE GESTIÓN DE PERSONAJES</h2>

        <div className="heroe-layout-tres-columnas">
          {/* ================= COLUMNA IZQUIERDA ================= */}
          <div className="heroe-columna">
            {/* ARRIBA: Equipo del personaje */}
            <div className="heroe-bloque heroe-bloque-superior">
              <h3 className="heroe-bloque-titulo">EQUIPO EQUIPADO</h3>
              <div className="heroe-cuadricula-equipo">
                <div className="heroe-slot-equipo">
                  <span className="heroe-slot-etiqueta">CABEZA:</span>
                  <span className="heroe-slot-item">
                    {heroeSeleccionado.equipo.cabeza}
                  </span>
                </div>
                <div className="heroe-slot-equipo">
                  <span className="heroe-slot-etiqueta">PECHO:</span>
                  <span className="heroe-slot-item">
                    {heroeSeleccionado.equipo.pecho}
                  </span>
                </div>
                <div className="heroe-slot-equipo">
                  <span className="heroe-slot-etiqueta">ARMA:</span>
                  <span className="heroe-slot-item">
                    {heroeSeleccionado.equipo.mano}
                  </span>
                </div>
                <div className="heroe-slot-equipo">
                  <span className="heroe-slot-etiqueta">PIES:</span>
                  <span className="heroe-slot-item">
                    {heroeSeleccionado.equipo.pies}
                  </span>
                </div>
              </div>
            </div>

            {/* ABAJO: Inventario del usuario */}
            <div className="heroe-bloque heroe-bloque-inferior">
              <h3 className="heroe-bloque-titulo">INVENTARIO DEL USUARIO</h3>
              <div className="heroe-inventario-cuadricula">
                {slotsInventario.map((_, i) => (
                  <div key={`inv-slot-${i}`} className="heroe-slot-vacio"></div>
                ))}
              </div>
            </div>
          </div>

          {/* ================= COLUMNA CENTRAL ================= */}
          <div className="heroe-columna">
            {/* ARRIBA: Imagen del personaje */}
            <div className="heroe-bloque heroe-bloque-superior heroe-centrado-retrato">
              <div className="heroe-marco-retrato">
                <img
                  src={spriteHeroeDefault}
                  alt={heroeSeleccionado.nombre}
                  className="heroe-retrato-img"
                />
              </div>
            </div>

            {/* ABAJO: Estadísticas */}
            <div className="heroe-bloque heroe-bloque-inferior">
              <h3 className="heroe-bloque-titulo">ESTADÍSTICAS</h3>
              <div className="heroe-stats-lista">
                <div className="heroe-stat-fila">
                  <span>NIVEL:</span>
                  <span className="heroe-stat-val font-amarillo">
                    LVL {heroeSeleccionado.nivel}
                  </span>
                </div>
                <div className="heroe-stat-fila">
                  <span>SALUD (HP):</span>
                  <span className="heroe-stat-val font-verde">
                    {heroeSeleccionado.hp} / {heroeSeleccionado.maxHp}
                  </span>
                </div>
                <div className="heroe-stat-fila">
                  <span>MANÁ (MP):</span>
                  <span className="heroe-stat-val font-azul">
                    {heroeSeleccionado.mp} / {heroeSeleccionado.maxMp}
                  </span>
                </div>
                <div className="heroe-stat-fila">
                  <span>ATAQUE:</span>
                  <span className="heroe-stat-val">
                    {heroeSeleccionado.ataque} ⚔️
                  </span>
                </div>
                <div className="heroe-stat-fila">
                  <span>DEFENSA:</span>
                  <span className="heroe-stat-val">
                    {heroeSeleccionado.defensa} 🛡️
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* ================= COLUMNA DERECHA ================= */}
          <div className="heroe-columna">
            {/* ARRIBA: Menú de opciones */}
            <div className="heroe-bloque heroe-bloque-superior">
              <h3 className="heroe-bloque-titulo">OPCIONES DE GESTIÓN</h3>
              <div className="heroe-menu-opciones">
                <button className="heroe-btn-accion btn-subir">
                  Subir de Nivel
                </button>
                <button className="heroe-btn-accion">
                  Cambiar Habilidades
                </button>
                <button className="heroe-btn-accion">Desequipar Todo</button>
              </div>
            </div>

            {/* ABAJO: Lista de personajes */}
            <div className="heroe-bloque heroe-bloque-inferior">
              <h3 className="heroe-bloque-titulo">PERSONAJES DISPONIBLES</h3>
              <div className="heroe-lista-scroll">
                {heroes.map((heroe) => (
                  <div
                    key={heroe.id}
                    className={`heroe-item-seleccion ${
                      selectedHeroId === heroe.id ? "heroe-item-activo" : ""
                    }`}
                    onClick={() => setSelectedHeroId(heroe.id)}
                  >
                    <div className="heroe-item-info">
                      <span className="heroe-item-nombre">{heroe.nombre}</span>
                      <span className="heroe-item-clase">{heroe.clase}</span>
                    </div>
                    <span className="heroe-item-lvl">LVL {heroe.nivel}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

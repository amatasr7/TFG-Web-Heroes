// HeroStats.jsx
import React from "react";

export default function HeroStats({ heroe }) {
  return (
    <div className="heroe-bloque heroe-bloque-inferior">
      <h3 className="heroe-bloque-titulo">Estadísticas:</h3>
      <div className="heroe-stats-lista">
        
        <div className="heroe-stat-fila">
          <span>Nivel:</span>
          <span className="heroe-stat-val font-amarillo">Nvl {heroe.level}</span>
        </div>

        <div className="heroe-stat-fila">
          <span>Clase:</span>
          <span className="heroe-stat-val font-amarillo">{heroe.hero_class?.name}</span>
        </div>

        <div className="heroe-stat-fila">
          <span>Salud (HP):</span>
          <span className="heroe-stat-val font-verde">
            {heroe.hp_current} / {heroe.hero_class?.base_hp_max || 10}
          </span>
        </div>

        <div className="heroe-stat-fila">
          <span>Maná (MP):</span>
          <span className="heroe-stat-val font-azul">
            {heroe.mp_current} / {heroe.hero_class?.base_mp_max || 10}
          </span>
        </div>

        <div className="heroe-stat-fila">
          <span>Energía:</span>
          <span className="heroe-stat-val font-amarillo">{heroe.energy_current}</span>
        </div>

        <div className="heroe-stat-fila">
          <span>Ataque:</span>
          <span className="heroe-stat-val font-amarillo">
            {heroe.ataque || 10}
          </span>
        </div>

        <div className="heroe-stat-fila">
          <span>Defensa:</span>
          <span className="heroe-stat-val font-amarillo">
            {heroe.defensa || 5}
          </span>
        </div>

      </div>
    </div>
  );
}
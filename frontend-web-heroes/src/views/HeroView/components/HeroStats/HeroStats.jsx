import React from "react";

export default function HeroStats({ heroe, heroItems = [] }) {
  const equippedWeapon = heroItems.find((hi) => hi.item?.type?.slug === "weapon");
  const equippedArmor = heroItems.find((hi) => hi.item?.type?.slug === "armor");

  const attackBonus = equippedWeapon?.item?.damage_bonus ?? 0;
  const defenseBonus = equippedArmor?.item?.hp_bonus ?? 0;

  const effectiveAttack = heroe.attack + attackBonus;
  const effectiveDefense = heroe.defense + defenseBonus;

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
            {effectiveAttack}
            {attackBonus > 0 && (
              <span className="heroe-stat-bonus"> (+{attackBonus})</span>
            )}
          </span>
        </div>

        <div className="heroe-stat-fila">
          <span>Defensa:</span>
          <span className="heroe-stat-val font-amarillo">
            {effectiveDefense}
            {defenseBonus > 0 && (
              <span className="heroe-stat-bonus"> (+{defenseBonus})</span>
            )}
          </span>
        </div>

      </div>
    </div>
  );
}

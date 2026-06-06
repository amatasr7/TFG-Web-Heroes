import "./AbilitiesMenu.css";

// Ability definitions per class (mirrors backend ABILITIES dict)
export const CLASS_ABILITIES = {
  guerrero: [
    {
      id: "golpe_brutal",
      name: "Golpe Brutal",
      mp_cost: 1,
      effect_type: "damage_single",
      damage_multiplier: 1.5,
      guaranteed_hit: true,
      requiresTarget: true,
      description: "Ataque garantizado con 150% del daño base",
      icon: "💥",
    },
    {
      id: "grito_de_guerra",
      name: "Grito de Guerra",
      mp_cost: 1,
      effect_type: "heavy_defend",
      guaranteed_hit: false,
      requiresTarget: false,
      description: "Postura defensiva extrema: reduce el daño recibido un 75%",
      icon: "🛡",
    },
  ],
  mago: [
    {
      id: "bola_de_fuego",
      name: "Bola de Fuego",
      mp_cost: 4,
      effect_type: "damage_all",
      flat_damage: 3,
      guaranteed_hit: true,
      requiresTarget: false,
      description: "Inflige 3 de daño a todos los enemigos vivos",
      icon: "🔥",
    },
    {
      id: "rayo_de_hielo",
      name: "Rayo de Hielo",
      mp_cost: 2,
      effect_type: "damage_pierce",
      flat_damage: 4,
      guaranteed_hit: true,
      requiresTarget: true,
      description: "Daño mágico de 4 que ignora la defensa del objetivo",
      icon: "❄",
    },
  ],
  picaro: [
    {
      id: "golpe_furtivo",
      name: "Golpe Furtivo",
      mp_cost: 2,
      effect_type: "damage_single",
      damage_multiplier: 2.0,
      guaranteed_hit: true,
      requiresTarget: true,
      description: "Ataque certero con el doble de daño base",
      icon: "🗡",
    },
    {
      id: "evasion",
      name: "Evasión",
      mp_cost: 1,
      effect_type: "evasion",
      guaranteed_hit: false,
      requiresTarget: false,
      description: "Evades completamente el próximo ataque recibido",
      icon: "💨",
    },
  ],
};

export function getAbilitiesForHero(hero) {
  const cls = (hero?.hero_class?.name ?? "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "");
  for (const [key, abilities] of Object.entries(CLASS_ABILITIES)) {
    if (cls.includes(key)) return abilities;
  }
  return [];
}

export default function AbilitiesMenu({ hero, hasSelectedEnemy, onUse, onClose }) {
  if (!hero) return null;

  const abilities = getAbilitiesForHero(hero);
  const mp = hero.mp_current ?? 0;

  return (
    <div className="modal-overlay abilities-overlay" onClick={onClose}>
      <div className="abilities-modal" onClick={(e) => e.stopPropagation()}>
        <div className="abilities-header">
          <span className="abilities-title">✨ Habilidades de {hero.name}</span>
          <span className="abilities-mp">MP: {mp}</span>
        </div>

        {abilities.length === 0 ? (
          <p className="abilities-empty">Esta clase no tiene habilidades disponibles.</p>
        ) : (
          <div className="abilities-list">
            {abilities.map((ability) => {
              const canAfford = mp >= ability.mp_cost;
              const needsTarget = ability.requiresTarget && !hasSelectedEnemy;
              const disabled = !canAfford || needsTarget;

              let tooltip = "";
              if (!canAfford) tooltip = `Necesitas ${ability.mp_cost} MP`;
              else if (needsTarget) tooltip = "Selecciona un enemigo primero";

              return (
                <button
                  key={ability.id}
                  className={`ability-btn${disabled ? " ability-btn--disabled" : ""}`}
                  onClick={() => !disabled && onUse(ability)}
                  disabled={disabled}
                  title={tooltip || ability.description}
                >
                  <span className="ability-icon">{ability.icon}</span>
                  <div className="ability-info">
                    <span className="ability-name">{ability.name}</span>
                    <span className="ability-desc">{ability.description}</span>
                  </div>
                  <span className={`ability-cost${!canAfford ? " ability-cost--low" : ""}`}>
                    {ability.mp_cost} MP
                  </span>
                </button>
              );
            })}
          </div>
        )}

        <button className="abilities-close-btn" onClick={onClose}>
          Cancelar
        </button>
      </div>
    </div>
  );
}

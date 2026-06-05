import "./CharacterStats.css";

function getHeroSprite(hero) {
  const cls = (hero?.hero_class?.name ?? "").toLowerCase();
  if (cls.includes("guerrero")) return "/sprites/Guerrero2.png";
  if (cls.includes("mago")) return "/sprites/Maga.png";
  if (cls.includes("picaro") || cls.includes("pícaro")) return "/sprites/Arquero.png";
  if (cls.includes("jefe")) return "/sprites/Orco.png";
  return "/sprites/Pelirrojo.png";
}

export default function CharacterStats({ heroes = [], currentHeroId = null }) {
  return (
    <div className="character-stats">
      {heroes.map((hero) => {
        const maxHp = hero.hp_max ?? hero.hero_class?.base_hp_max ?? 100;
        const maxMp = hero.mp_max ?? hero.hero_class?.base_mp_max ?? 50;
        const hpPct = Math.max(0, Math.min(100, (hero.hp_current / maxHp) * 100));
        const mpPct = Math.max(0, Math.min(100, (hero.mp_current / maxMp) * 100));
        const isDead = hero.hp_current <= 0;
        const isActive = hero.id === currentHeroId;
        const sprite = getHeroSprite(hero);

        return (
          <div
            key={hero.id}
            className={`hero-stat-card${isActive ? " active" : ""}${isDead ? " dead" : ""}`}
          >
            <div className="hero-stat-portrait">
              <img src={sprite} alt={hero.name} className="hero-stat-sprite" />
            </div>
            <div className="hero-stat-info">
              <div className="hero-stat-name">{hero.name}</div>
              <div className="stat-bar-row">
                <span className="stat-bar-label">HP</span>
                <div className="stat-bar-bg">
                  <div className="stat-bar-fill hp-fill" style={{ width: `${hpPct}%` }} />
                </div>
                <span className="stat-bar-value">
                  {hero.hp_current}/{maxHp}
                </span>
              </div>
              <div className="stat-bar-row">
                <span className="stat-bar-label">MP</span>
                <div className="stat-bar-bg">
                  <div className="stat-bar-fill mp-fill" style={{ width: `${mpPct}%` }} />
                </div>
                <span className="stat-bar-value">
                  {hero.mp_current}/{maxMp}
                </span>
              </div>
              {hero.isDefending && (
                <span className="defending-badge">🛡 Defendiendo</span>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

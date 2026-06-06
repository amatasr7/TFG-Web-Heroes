import { useEffect, useState } from "react";
import "./BattleMap.css";
import { getSpriteForHero, getSpriteForEnemy } from "../../../../utils/sprites";

import caveImg from "/backgrounds/Cave.jpeg";
import desertImg from "/backgrounds/Desert.jpeg";
import forestImg from "/backgrounds/Forest.jpeg";
import mineshaftImg from "/backgrounds/Mineshaft.jpeg";
import mountainImg from "/backgrounds/Mountain.jpeg";

const backgroundOptions = [caveImg, desertImg, forestImg, mineshaftImg, mountainImg];

export default function BattleMap({
  heroes = [],
  enemies = [],
  selectedEnemy = null,
  onSelectEnemy = () => {},
  currentActorId,
  currentActorType,
}) {
  const [backgroundUrl, setBackgroundUrl] = useState(null);

  useEffect(() => {
    const idx = Math.floor(Math.random() * backgroundOptions.length);
    setBackgroundUrl(backgroundOptions[idx]);
  }, []);

  return (
    <div className="battle-map">
      <div
        className="map-background"
        style={{ backgroundImage: backgroundUrl ? `url(${backgroundUrl})` : "none" }}
      >
        {/* Heroes on the LEFT */}
        <div className="combat-column heroes-side">
          {heroes.map((hero) => {
            const isDead = hero.hp_current <= 0;
            const isActive = currentActorType === "hero" && currentActorId === hero.id;
            const sprite = getSpriteForHero(hero);
            return (
              <div
                key={hero.id}
                className={`sprite-marker hero-sprite${isDead ? " dead" : ""}${isActive ? " active-turn" : ""}`}
                title={hero.name}
              >
                <img src={sprite} alt={hero.name} className="sprite-img" />
                <span className="sprite-name">{hero.name}</span>
              </div>
            );
          })}
        </div>

        {/* Enemies on the RIGHT */}
        <div className="combat-column enemies-side">
          {enemies.map((enemy) => {
            const isDead = enemy.hp_current <= 0;
            const isSelected = selectedEnemy?.id === enemy.id;
            const isActive = currentActorType === "enemy" && currentActorId === enemy.id;
            const sprite = getSpriteForEnemy(enemy);
            return (
              <div
                key={enemy.id}
                className={`sprite-marker${isDead ? " dead" : ""}${isSelected ? " selected" : ""}${isActive ? " active-turn" : ""}`}
                onClick={() => !isDead && onSelectEnemy(enemy)}
                title={isDead ? `${enemy.name} (derrotado)` : enemy.name}
              >
                <img src={sprite} alt={enemy.name} className="sprite-img" />
                <span className="sprite-name">{enemy.name}</span>
                {isDead && <span className="dead-mark">✕</span>}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

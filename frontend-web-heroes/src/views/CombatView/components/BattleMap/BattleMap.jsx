import { useEffect, useMemo, useState } from "react";
import "./BattleMap.css";

const backgroundImages = import.meta.glob(
  "../../assets/backgrounds/*.{jpg,jpeg,png}",
  {
    eager: true,
    import: "default",
  },
);

export default function BattleMap({ enemies, selectedEnemy, onSelectEnemy }) {
  const backgrounds = useMemo(
    () => Object.values(backgroundImages).filter(Boolean),
    [],
  );

  const [backgroundUrl, setBackgroundUrl] = useState(null);

  useEffect(() => {
    if (backgrounds.length > 0) {
      const randomIndex = Math.floor(Math.random() * backgrounds.length);
      setBackgroundUrl(backgrounds[randomIndex]);
    }
  }, [backgrounds]);

  return (
    <div className="battle-map">
      <div
        className="map-background"
        style={
          backgroundUrl
            ? { backgroundImage: `url(${backgroundUrl})` }
            : undefined
        }
      >
        {enemies.map((enemy) => (
          <div
            key={enemy.id}
            className={`enemy-marker ${selectedEnemy?.id === enemy.id ? "selected" : ""}`}
            onClick={() => onSelectEnemy(enemy)}
          >
            <span className="enemy-number">{enemy.id}</span>
          </div>
        ))}

        {/* Items en el mapa */}
        <div className="map-item item-green"></div>
        <div className="map-item item-purple"></div>
        <div className="map-item item-yellow"></div>
      </div>
    </div>
  );
}

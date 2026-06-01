import { useEffect, useState } from "react";
import "./BattleMap.css";

// 1. Importamos las imágenes explícitamente para que el empaquetador las reconozca
import caveImg from "/backgrounds/Cave.jpeg";
import desertImg from "/backgrounds/Desert.jpeg";
import forestImg from "/backgrounds/Forest.jpeg";
import mineshaftImg from "/backgrounds/Mineshaft.jpeg";
import mountainImg from "/backgrounds/Mountain.jpeg";

// 2. Creamos el array con las imágenes importadas
const backgroundOptions = [caveImg, desertImg, forestImg, mineshaftImg, mountainImg];

export default function BattleMap({
  enemies = [],
  heroes = [],
  selectedEnemy = null,
  onSelectEnemy = () => {},
}) {
  const [backgroundUrl, setBackgroundUrl] = useState(null);

  useEffect(() => {
    // 3. Seleccionamos aleatoriamente una vez al montar
    const randomIndex = Math.floor(Math.random() * backgroundOptions.length);
    setBackgroundUrl(backgroundOptions[randomIndex]);
  }, []);

  return (
    <div className="battle-map">
      <div
        className="map-background"
        style={{
          // 4. Aplicamos el fondo correctamente
          backgroundImage: backgroundUrl ? `url(${backgroundUrl})` : "none",
        }}
      >
        <div className="combat-column enemies-side">
          {enemies.map((enemy) => (
            <div
              key={enemy.id}
              className={`sprite-marker${selectedEnemy?.id === enemy.id ? " selected" : ""}`}
              onClick={() => onSelectEnemy(enemy)}
              title={enemy.name}
            >
              <span className="sprite-label">{enemy.name?.[0] ?? "E"}</span>
            </div>
          ))}
        </div>

        <div className="combat-column heroes-side">
          {heroes.map((hero) => (
            <div key={hero.id} className="sprite-marker hero-sprite" title={hero.name}>
              <span className="sprite-label">H</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
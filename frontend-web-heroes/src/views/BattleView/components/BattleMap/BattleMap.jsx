import { useEffect, useMemo, useState } from "react";
import "./BattleMap.css";

// FIX: import.meta.glob puede devolver un objeto vacío si no hay imágenes.
// Usamos try/catch para que el componente no explote en entornos sin assets.
let backgroundImages = {};
try {
  backgroundImages = import.meta.glob(
    "../../assets/backgrounds/*.{jpg,jpeg,png}",
    { eager: true, import: "default" }
  );
} catch {
  // Sin imágenes disponibles — el fondo quedará con el color de CSS
}

export default function BattleMap({
  enemies = [],
  heroes = [],
  selectedEnemy = null,
  onSelectEnemy = () => {},
}) {
  const backgrounds = useMemo(
    () => Object.values(backgroundImages).filter(Boolean),
    []
  );
  const [backgroundUrl, setBackgroundUrl] = useState(null);

  useEffect(() => {
    if (backgrounds.length > 0) {
      setBackgroundUrl(
        backgrounds[Math.floor(Math.random() * backgrounds.length)]
      );
    }
  }, [backgrounds]);

  return (
    // FIX: se añade la clase `.battle-map` que faltaba en el CSS
    <div className="battle-map">
      <div
        className="map-background"
        style={{
          backgroundImage: backgroundUrl ? `url(${backgroundUrl})` : undefined,
        }}
      >
        {/* Columna de Enemigos (Izquierda) */}
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

        {/* Columna de Héroes (Derecha) */}
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
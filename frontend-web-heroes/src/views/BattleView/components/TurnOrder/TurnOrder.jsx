import "./TurnOrder.css";

export default function TurnOrder({ turnQueue = [], currentIndex = 0, heroes = [], enemies = [] }) {
  const total = turnQueue.length;

  return (
    <section className="turn-order">
      <h3>Orden de Turnos</h3>
      <div className="turn-order-list">
        {turnQueue.map((actor, idx) => {
          const isCurrent = total > 0 && idx === currentIndex % total;
          const hp =
            actor.type === "hero"
              ? (heroes.find((h) => h.id === actor.id)?.hp_current ?? 0)
              : (enemies.find((e) => e.id === actor.id)?.hp_current ?? 0);
          const isDead = hp <= 0;

          return (
            <div
              key={`${actor.type}-${actor.id}-${idx}`}
              className={`turn-card ${actor.type}${isCurrent ? " current" : ""}${isDead ? " dead" : ""}`}
            >
              <span className="turn-number">{idx + 1}</span>
              <img
                src={actor.sprite}
                alt={actor.name}
                className="turn-sprite"
              />
              <span className="turn-name">{actor.name}</span>
              {isDead && <span className="turn-dead-mark">✕</span>}
            </div>
          );
        })}
      </div>
    </section>
  );
}

import "./ActionButtons.css";

export default function ActionButtons({ onAction }) {
  return (
    <div className="action-buttons">
      <button className="action-btn" onClick={() => onAction("attack")}>
        Atacar
      </button>
      <button className="action-btn" onClick={() => onAction("defend")}>
        Defender
      </button>
      <button className="action-btn" onClick={() => onAction("abilities")}>
        Habilidades
      </button>
      <button className="action-btn" onClick={() => onAction("items")}>
        Usar objeto
      </button>
    </div>
  );
}
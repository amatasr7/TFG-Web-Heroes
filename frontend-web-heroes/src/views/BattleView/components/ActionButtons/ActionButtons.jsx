import "./ActionButtons.css";

// FIX: el componente recibe `onAction`, no `onOpenInventory`.
// BattleView centraliza la lógica: cuando action === "items" abre el inventario.
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
      {/* FIX: "Usar objeto" abre el inventario a través del handler central */}
      <button className="action-btn" onClick={() => onAction("items")}>
        Usar objeto
      </button>
    </div>
  );
}
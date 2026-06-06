import ItemIcon from "../../../../components/ItemIcon";
import "./BattleInventory.css";

export default function BattleInventory({ userItems = [], heroName = "", onUse, onClose }) {
  return (
    <div className="battle-inventory-overlay" onClick={onClose}>
      <div className="battle-inventory-panel" onClick={(e) => e.stopPropagation()}>
        <div className="battle-inventory-header">
          <span className="battle-inventory-title">Bolsa de {heroName}</span>
          <button className="battle-inventory-close" onClick={onClose}>✕</button>
        </div>

        {userItems.length === 0 ? (
          <p className="battle-inventory-empty">No hay consumibles en el inventario.</p>
        ) : (
          <div className="battle-inventory-grid">
            {userItems.map((ui) => {
              const item = ui.item;
              const parts = [];
              if (item.hp_bonus > 0) parts.push(`+${item.hp_bonus} HP`);
              if (item.mp_bonus > 0) parts.push(`+${item.mp_bonus} MP`);
              const effect = parts.join(" / ");

              return (
                <button
                  key={ui.item_id}
                  className="battle-inventory-item"
                  onClick={() => onUse(ui)}
                  title={`${item.name} — ${effect}`}
                >
                  <div className="battle-inventory-icon">
                    <ItemIcon item={item} />
                    {ui.quantity > 1 && (
                      <span className="battle-inventory-qty">{ui.quantity}</span>
                    )}
                  </div>
                  <span className="battle-inventory-name">{item.name}</span>
                  {effect && (
                    <span className="battle-inventory-effect">{effect}</span>
                  )}
                </button>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

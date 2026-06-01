import './Inventory.css';

export default function Inventory({ onClose }) {
  return (
    <div className="inventory-panel">
      <h2>Inventario</h2>
      {/* Aquí tu lista de items */}
      <div className="inventory-list inventory-empty">(vacío)</div>
      <button className="action-btn" onClick={onClose}>Cerrar</button>
    </div>
  );
}
import "./ActionButtons.css";

export default function ActionButtons({ onAttack, onAbilities, onDefend, onItems }) {
  return (
    <div className="action-buttons">
      <div className="buttons-left">
        <button className="action-btn" onClick={onAttack}>Atacar</button>
        <button className="action-btn" onClick={onDefend}>Defender</button>
      </div>
      <div className="buttons-right">
        <button className="action-btn" onClick={onAbilities}>Habilidades</button>
        <button className="action-btn" onClick={onItems}>Objetos</button>
      </div>
    </div>
  );
}

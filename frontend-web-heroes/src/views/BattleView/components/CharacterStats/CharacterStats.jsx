import "./CharacterStats.css";

export default function CharacterStats({ character }) {
  return (
    <div className="character-stats" style={{ gridTemplateColumns: "1fr" }}>
      <div className="stats-row">
        {/* Barra de Vida del Héroe */}
        <div className="stat-bar">
          <div className="stat-icon diamond-blue"></div>
          <div className="stat-display">
            <div className="health-bar">
              <div 
                className="health-fill" 
                style={{ width: `${(character.hp / character.maxHp) * 100}%` }}
              ></div>
            </div>
            <span className="stat-text">{character.hp}/{character.maxHp}</span>
          </div>
        </div>

        {/* Barra de Maná del Héroe */}
        <div className="stat-bar">
          <div className="stat-icon diamond-blue"></div>
          <div className="stat-display">
            <div className="mana-bar">
              <div 
                className="mana-fill" 
                style={{ width: `${(character.mana / character.maxMana) * 100}%` }}
              ></div>
            </div>
            <span className="stat-text">{character.mana}/{character.maxMana}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
import "./CharacterStats.css";

export default function CharacterStats({ character, enemy }) {
  return (
    <div className="character-stats">
      <div className="stats-row">
        <div className="stat-bar">
          <div className="stat-icon diamond-blue"></div>
          <div className="stat-display">
            <div className="health-bar">
              <div className="health-fill" style={{ width: `${(character.hp / character.maxHp) * 100}%` }}></div>
            </div>
            <span className="stat-text">{character.hp}/{character.maxHp}</span>
          </div>
        </div>

        <div className="stat-bar">
          <div className="stat-icon diamond-blue"></div>
          <div className="stat-display">
            <div className="mana-bar">
              <div className="mana-fill" style={{ width: `${(character.mana / character.maxMana) * 100}%` }}></div>
            </div>
            <span className="stat-text">{character.mana}/{character.maxMana}</span>
          </div>
        </div>
      </div>

      <div className="stats-row">
        <div className="stat-bar">
          <div className="stat-icon diamond-red"></div>
          <div className="stat-display">
            <div className="health-bar">
              <div className="health-fill enemy" style={{ width: `${(enemy.hp / enemy.maxHp) * 100}%` }}></div>
            </div>
            <span className="stat-text">{enemy.hp}/{enemy.maxHp}</span>
          </div>
        </div>

        <div className="stat-bar">
          <div className="stat-icon diamond-red"></div>
          <div className="stat-display">
            <div className="mana-bar">
              <div className="mana-fill enemy" style={{ width: `${(enemy.mana / enemy.maxMana) * 100}%` }}></div>
            </div>
            <span className="stat-text">{enemy.mana}/{enemy.maxMana}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

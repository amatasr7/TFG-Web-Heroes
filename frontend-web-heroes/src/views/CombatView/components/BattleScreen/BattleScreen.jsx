import { useState } from "react";
import "./BattleScreen.css";
import Header from "../../../Header/Header";
import BattleMap from "../BattleMap/BattleMap";
import ItemSelection from "../ItemSelection/ItemSelection";
import CombatLog from "../CombatLog/CombatLog";
import CharacterStats from "../CharacterStats/CharacterStats";
import ActionButtons from "../ActionButtons/ActionButtons";
import TurnOrder from "../TurnOrder/TurnOrder";

export default function BattleScreen() {
  const [selectedEnemy, setSelectedEnemy] = useState(null);
  const [logs, setLogs] = useState([
    {
      timestamp: "16:41",
      message: "<4Hero> ha atacado a <Enemigo>, causando <x> puntos de daño.",
    },
    {
      timestamp: "16:45",
      message:
        "<4Héroe 1> ha lanzado <Habilidad> sobre <Héroe 2>, gastando <x> puntos de maná y curando <x> puntos de salud.",
    },
  ]);

  const [character] = useState({ hp: 85, maxHp: 100, mana: 60, maxMana: 80 });
  const [enemy, setEnemy] = useState({
    hp: 45,
    maxHp: 60,
    mana: 30,
    maxMana: 50,
  });
  const [enemies] = useState([
    { id: 1, name: "Enemigo 1", hp: 45, maxHp: 60 },
    { id: 2, name: "Enemigo 2", hp: 35, maxHp: 50 },
  ]);

  const [turnOrder] = useState([
    { id: "hero-1", name: "Aragorn", type: "hero" },
    { id: "enemy-1", name: "Guerrero enemigo", type: "enemy" },
    { id: "hero-2", name: "Morgana", type: "hero" },
    { id: "enemy-2", name: "Dragon rojo", type: "enemy" },
  ]);

  const handleAttack = () => {
    const newHp = Math.max(0, enemy.hp - 15);
    setEnemy({ ...enemy, hp: newHp });
    setLogs([
      ...logs,
      {
        timestamp: new Date().toLocaleTimeString(),
        message: "<Héroe> ha atacado a <Enemigo>, causando 15 puntos de daño.",
      },
    ]);
  };

  const handleAbilities = () => {
    setLogs([
      ...logs,
      {
        timestamp: new Date().toLocaleTimeString(),
        message: "<Héroe> usa una habilidad...",
      },
    ]);
  };

  const handleDefend = () => {
    setLogs([
      ...logs,
      {
        timestamp: new Date().toLocaleTimeString(),
        message: "<Héroe> se defiende...",
      },
    ]);
  };

  const handleItems = () => {
    setLogs([
      ...logs,
      {
        timestamp: new Date().toLocaleTimeString(),
        message: "<Héroe> usa un objeto...",
      },
    ]);
  };

  const handleFlee = () => {
    setLogs([
      ...logs,
      {
        timestamp: new Date().toLocaleTimeString(),
        message: "¡Intento de huir!",
      },
    ]);
  };

  return (
    <div className="battle-container">
      <TurnOrder actors={turnOrder} />
      <main className="battle-main">
        {/* SECCIÓN SUPERIOR: Mapa, Selección de Items y Log */}
        <div className="battle-top-section">
          <div className="map-wrapper">
            <BattleMap
              enemies={enemies}
              selectedEnemy={selectedEnemy}
              onSelectEnemy={setSelectedEnemy}
            />
          </div>
          <div className="items-wrapper">
            <ItemSelection />
          </div>
          <div className="log-wrapper">
            <CombatLog logs={logs} />
          </div>
        </div>

        {/* SECCIÓN INFERIOR: Botones de Acción, Stats y Botón Huir */}
        <div className="battle-bottom-section">
          <div className="actions-wrapper">
            <ActionButtons
              onAttack={handleAttack}
              onAbilities={handleAbilities}
              onDefend={handleDefend}
              onItems={handleItems}
            />
          </div>
          <div className="stats-wrapper">
            <CharacterStats character={character} enemy={enemy} />
          </div>
          <div className="flee-wrapper">
            <button className="flee-btn" onClick={() => {}}>
              ¡HUIR!
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

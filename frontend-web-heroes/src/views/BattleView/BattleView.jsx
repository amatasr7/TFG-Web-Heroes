import React, { useState } from "react";
import "./BattleView.css";
import BattleMap from "./components/BattleMap/BattleMap";
import TurnOrder from "./components/TurnOrder/TurnOrder";
import CombatLog from "./components/CombatLog/CombatLog";
import ActionButtons from "./components/ActionButtons/ActionButtons";
import CharacterStats from "./components/CharacterStats/CharacterStats";
import Inventory from "./components/Inventory/Inventory";

// Datos de ejemplo — reemplaza con tu estado real del juego
const INITIAL_CHARACTER = { hp: 80, maxHp: 100, mana: 40, maxMana: 50 };
const INITIAL_ENEMIES   = [{ id: 1, name: "Goblin" }, { id: 2, name: "Slime" }];
const INITIAL_HEROES    = [{ id: 1, name: "Héroe" }];
const INITIAL_ACTORS    = [
  { id: 1, name: "Héroe",  type: "hero",  initiative: 18 },
  { id: 2, name: "Goblin", type: "enemy", initiative: 12 },
  { id: 3, name: "Slime",  type: "enemy", initiative:  7 },
];
const INITIAL_LOGS = [{ timestamp: "00:00", message: "¡La batalla comienza!" }];

export default function BattleView() {
  const [isInventoryOpen, setIsInventoryOpen] = useState(false);
  const [selectedEnemy, setSelectedEnemy]     = useState(null);

  const [character] = useState(INITIAL_CHARACTER);
  const [enemies]   = useState(INITIAL_ENEMIES);
  const [heroes]    = useState(INITIAL_HEROES);
  const [actors]    = useState(INITIAL_ACTORS);
  const [logs]      = useState(INITIAL_LOGS);

  // FIX 1: un único handler de acciones que centraliza la lógica
  function handleAction(action) {
    if (action === "items") {
      setIsInventoryOpen(true);
    }
    // Aquí puedes añadir el resto de lógica (attack, defend, abilities…)
  }

  return (
    <div className="root">
      <div className="battle-view-container">
        
        <div className="view-map">
          <BattleMap /* ...props */ />
        </div>

        <div className="view-turns">
          <TurnOrder actors={actors} />
        </div>

        <div className="view-log">
          <CombatLog logs={logs} />
        </div>

        <div className="view-stats">
          <CharacterStats character={character} />
        </div>

        <div className="view-actions">
          <ActionButtons onAction={handleAction} />
        </div>

        <div className="view-inventory-slot">
          {isInventoryOpen
            ? <Inventory onClose={() => setIsInventoryOpen(false)} />
            : <div className="inventory-placeholder">Inventario</div>
          }
        </div>
      </div>
    </div>
  );
}
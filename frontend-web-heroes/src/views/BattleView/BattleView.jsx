import React, { useReducer, useEffect, useRef, useState } from "react";
import ItemIcon from "./components/ItemIcon";
import "./BattleView.css";
import BattleMap from "./components/BattleMap/BattleMap";
import TurnOrder from "./components/TurnOrder/TurnOrder";
import CombatLog from "./components/CombatLog/CombatLog";
import ActionButtons from "./components/ActionButtons/ActionButtons";
import CharacterStats from "./components/CharacterStats/CharacterStats";
import BattleInventory from "./components/BattleInventory/BattleInventory";
import AbilitiesMenu from "./components/AbilitiesMenu/AbilitiesMenu";

const API = "http://localhost:8000/api";

function ts() {
  const now = new Date();
  return `${String(now.getMinutes()).padStart(2, "0")}:${String(now.getSeconds()).padStart(2, "0")}`;
}

export function getSpriteForHero(hero) {
  if (hero?.sprite_url) return hero.sprite_url;
  const cls = (hero?.hero_class?.name ?? hero?.hero_class_name ?? "").toLowerCase();
  if (cls.includes("guerrero")) return "/sprites/Guerrero2.png";
  if (cls.includes("mago")) return "/sprites/Maga.png";
  if (cls.includes("picaro") || cls.includes("pícaro")) return "/sprites/Arquero.png";
  if (cls.includes("jefe")) return "/sprites/Orco.png";
  return "/sprites/Pelirrojo.png";
}

export function getSpriteForEnemy(enemy) {
  const name = (enemy?.name ?? "").toLowerCase();
  const cls = (enemy?.hero_class?.name ?? enemy?.hero_class_name ?? "").toLowerCase();
  if (name.includes("goblin") || cls.includes("goblin")) return "/sprites/Goblin-guerrero.png";
  if (name.includes("slime")) return "/sprites/Slime.png";
  if (name.includes("orco") || name.includes("orc")) return "/sprites/Orco.png";
  if (name.includes("lobo") || name.includes("wolf")) return "/sprites/Lobo.png";
  if (name.includes("oso") || name.includes("bear")) return "/sprites/Oso.png";
  if (name.includes("golem")) return "/sprites/Golem.png";
  if (name.includes("jabali") || name.includes("jabalí")) return "/sprites/Jabali.png";
  return "/sprites/Orco.png";
}

function enrichTurnQueue(queue, heroesState, enemiesState) {
  return queue.map((item) => ({
    ...item,
    sprite:
      item.type === "hero"
        ? getSpriteForHero(heroesState.find((h) => h.id === item.id))
        : getSpriteForEnemy(enemiesState.find((e) => e.id === item.id)),
  }));
}

const INITIAL_STATE = {
  sessionId: null,
  heroes: [],
  enemies: [],
  userItems: [],
  turnQueue: [],
  currentTurnIndex: 0,
  logs: [{ timestamp: "00:00", message: "Cargando batalla..." }],
  selectedEnemy: null,
  isAnimating: false,
  battleOver: null,
  isLoading: true,
  loadError: null,
};

function reducer(state, action) {
  switch (action.type) {
    case "LOAD":
      return {
        ...state,
        sessionId: action.sessionId,
        heroes: action.heroesState,
        enemies: action.enemiesState,
        userItems: action.userItems ?? [],
        turnQueue: enrichTurnQueue(action.turnQueue, action.heroesState, action.enemiesState),
        currentTurnIndex: action.currentTurnIndex,
        logs: action.newLogs.map((m, i) => ({ timestamp: i === 0 ? "00:00" : ts(), message: m })),
        isLoading: false,
        loadError: null,
      };

    case "LOAD_ERROR":
      return { ...state, isLoading: false, loadError: action.message };

    case "SELECT_ENEMY":
      return { ...state, selectedEnemy: action.enemy };

    case "START_ANIMATING":
      return { ...state, isAnimating: true };

    case "STOP_ANIMATING":
      return { ...state, isAnimating: false };

    case "ADD_LOG":
      return {
        ...state,
        logs: [...state.logs, { timestamp: ts(), message: action.message }],
      };

    case "BATTLE_UPDATE": {
      const newLogs = [
        ...state.logs,
        ...action.newLogs.map((m) => ({ timestamp: ts(), message: m })),
      ];
      const battleOver =
        action.status === "victory"
          ? { result: "victory" }
          : action.status === "defeat"
          ? { result: "defeat" }
          : null;
      return {
        ...state,
        heroes: action.heroesState,
        enemies: action.enemiesState,
        currentTurnIndex: action.currentTurnIndex,
        logs: newLogs,
        isAnimating: false,
        selectedEnemy: null,
        battleOver,
      };
    }

    case "UPDATE_ITEMS":
      return { ...state, userItems: action.userItems };

    default:
      return state;
  }
}

export default function BattleView({ mission, onLeave }) {
  const [state, dispatch] = useReducer(reducer, INITIAL_STATE);
  const userRef = useRef(null);
  const [isInventoryOpen, setIsInventoryOpen] = useState(false);
  const [isAbilitiesOpen, setIsAbilitiesOpen] = useState(false);
  const [missionRewards, setMissionRewards] = useState(null);

  // Load: start battle session on backend
  useEffect(() => {
    const stored = localStorage.getItem("webHeroesUser");
    userRef.current = stored ? JSON.parse(stored) : null;
    const user = userRef.current;

    async function load() {
      try {
        const [battleRes, inventoryRes] = await Promise.all([
          fetch(`${API}/combat/battle/start`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              user_id: user?.id,
              mission_id: mission?.id ?? null,
              enemy_ids: mission?.enemy_ids ?? [],
            }),
          }),
          fetch(`${API}/shop/inventory?user_id=${user?.id}`),
        ]);

        if (!battleRes.ok) {
          const err = await battleRes.json();
          dispatch({ type: "LOAD_ERROR", message: err.detail ?? "No se pudo iniciar la batalla." });
          return;
        }

        const battleData = await battleRes.json();
        const inventoryData = inventoryRes.ok ? await inventoryRes.json() : { user_items: [] };
        const userItems = (inventoryData.user_items ?? []).filter(
          (ui) => ui.item?.type?.slug === "consumable" && ui.quantity > 0
        );

        dispatch({
          type: "LOAD",
          sessionId: battleData.session_id,
          heroesState: battleData.heroes_state,
          enemiesState: battleData.enemies_state,
          turnQueue: battleData.turn_queue,
          currentTurnIndex: battleData.current_turn_index,
          newLogs: battleData.new_logs,
          userItems,
        });
      } catch (err) {
        dispatch({ type: "LOAD_ERROR", message: err.message });
      }
    }
    load();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Call mission complete on victory
  useEffect(() => {
    if (state.battleOver?.result !== "victory" || !mission?.id) return;
    const user = userRef.current;
    const heroIds = state.heroes.map((h) => h.id);
    fetch(`${API}/missions/${mission.id}/complete`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: user?.id, hero_ids: heroIds }),
    })
      .then((r) => r.json())
      .then((data) => setMissionRewards(data))
      .catch(() => {});
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state.battleOver]);

  const currentActor = state.turnQueue[state.currentTurnIndex] ?? null;
  const isPlayerTurn =
    !state.isLoading &&
    !state.isAnimating &&
    !state.battleOver &&
    currentActor?.type === "hero";

  async function sendAction(payload) {
    dispatch({ type: "START_ANIMATING" });
    try {
      const res = await fetch(`${API}/combat/battle/${state.sessionId}/action`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const err = await res.json();
        dispatch({ type: "ADD_LOG", message: err.detail ?? "Error en la acción." });
        dispatch({ type: "STOP_ANIMATING" });
        return;
      }
      const data = await res.json();
      dispatch({
        type: "BATTLE_UPDATE",
        heroesState: data.heroes_state,
        enemiesState: data.enemies_state,
        currentTurnIndex: data.current_turn_index,
        newLogs: data.new_logs,
        status: data.status,
      });
    } catch {
      dispatch({ type: "ADD_LOG", message: "Error de red." });
      dispatch({ type: "STOP_ANIMATING" });
    }
  }

  async function handleAction(action) {
    if (!isPlayerTurn) return;
    const cur = currentActor;

    if (action === "abilities") {
      setIsAbilitiesOpen(true);
      return;
    }
    if (action === "items") {
      setIsInventoryOpen(true);
      return;
    }
    if (action === "attack" && !state.selectedEnemy) {
      dispatch({ type: "ADD_LOG", message: "Selecciona un enemigo objetivo primero." });
      return;
    }

    await sendAction({
      action,
      hero_id: cur.id,
      target_enemy_id: state.selectedEnemy?.id ?? null,
    });
  }

  async function handleUseAbility(ability) {
    const cur = currentActor;
    if (!cur || cur.type !== "hero") return;
    setIsAbilitiesOpen(false);

    await sendAction({
      action: "use_ability",
      hero_id: cur.id,
      target_enemy_id: state.selectedEnemy?.id ?? null,
      ability_id: ability.id,
    });
  }

  async function handleUseItem(userItem) {
    const cur = currentActor;
    if (!cur || cur.type !== "hero") return;
    const user = userRef.current;

    try {
      const res = await fetch(`${API}/combat/battle/${state.sessionId}/action`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "use_item",
          hero_id: cur.id,
          item_id: userItem.item_id,
          user_id: user?.id,
        }),
      });
      if (!res.ok) {
        const err = await res.json();
        dispatch({ type: "ADD_LOG", message: err.detail ?? "No se pudo usar el objeto." });
        return;
      }
      const data = await res.json();
      dispatch({
        type: "BATTLE_UPDATE",
        heroesState: data.heroes_state,
        enemiesState: data.enemies_state,
        currentTurnIndex: data.current_turn_index,
        newLogs: data.new_logs,
        status: data.status,
      });
      // Refresh local item counts
      if (user?.id) {
        fetch(`${API}/shop/inventory?user_id=${user.id}`)
          .then((r) => r.json())
          .then((inv) => {
            const items = (inv.user_items ?? []).filter(
              (ui) => ui.item?.type?.slug === "consumable" && ui.quantity > 0
            );
            dispatch({ type: "UPDATE_ITEMS", userItems: items });
          })
          .catch(() => {});
      }
    } catch {
      dispatch({ type: "ADD_LOG", message: "Error al usar el objeto." });
    } finally {
      setIsInventoryOpen(false);
    }
  }

  async function handleFlee() {
    if (state.sessionId) {
      await fetch(`${API}/combat/battle/${state.sessionId}/abandon`, { method: "POST" }).catch(() => {});
    }
    onLeave();
  }

  if (state.isLoading) {
    return (
      <div className="root">
        <div className="battle-loading">Cargando batalla...</div>
      </div>
    );
  }

  if (state.loadError) {
    return (
      <div className="root">
        <div className="battle-loading">
          <p>Error: {state.loadError}</p>
          <button className="flee-btn" onClick={onLeave}>
            Volver
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="root">
      <div className="battle-view-container">
        <div className="view-header">
          <span className="battle-title">⚔ {mission?.titulo ?? "Batalla"}</span>
          <span className="turn-indicator">
            {currentActor
              ? `Turno: ${currentActor.name} ${currentActor.type === "hero" ? "⚔" : "☠"}`
              : ""}
          </span>
          <button className="flee-btn" onClick={handleFlee}>
            Huir
          </button>
        </div>

        <div className="view-map">
          <BattleMap
            heroes={state.heroes}
            enemies={state.enemies}
            selectedEnemy={state.selectedEnemy}
            onSelectEnemy={(e) => dispatch({ type: "SELECT_ENEMY", enemy: e })}
            currentActorId={currentActor?.id}
            currentActorType={currentActor?.type}
          />
        </div>

        <div className="view-turns">
          <TurnOrder
            turnQueue={state.turnQueue}
            currentIndex={state.currentTurnIndex}
            heroes={state.heroes}
            enemies={state.enemies}
          />
        </div>

        <div className="view-log">
          <CombatLog logs={state.logs} />
        </div>

        <div className="view-stats">
          <CharacterStats
            heroes={state.heroes}
            currentHeroId={currentActor?.type === "hero" ? currentActor.id : null}
          />
        </div>

        <div className="view-actions">
          <ActionButtons
            onAction={handleAction}
            isPlayerTurn={isPlayerTurn}
            hasSelectedEnemy={!!state.selectedEnemy}
            currentHero={
              currentActor?.type === "hero"
                ? state.heroes.find((h) => h.id === currentActor.id)
                : null
            }
          />
        </div>

        <div className="view-inventory-slot">
          <div className="inventory-placeholder">
            {state.userItems.length > 0
              ? `${state.userItems.length} consumible${state.userItems.length > 1 ? "s" : ""} disponible${state.userItems.length > 1 ? "s" : ""}`
              : "Sin consumibles"}
          </div>
        </div>
      </div>

      {isAbilitiesOpen && (
        <AbilitiesMenu
          hero={
            currentActor?.type === "hero"
              ? state.heroes.find((h) => h.id === currentActor.id)
              : null
          }
          hasSelectedEnemy={!!state.selectedEnemy}
          onUse={handleUseAbility}
          onClose={() => setIsAbilitiesOpen(false)}
        />
      )}

      {isInventoryOpen && (
        <BattleInventory
          userItems={state.userItems}
          heroName={currentActor?.name ?? ""}
          onUse={handleUseItem}
          onClose={() => setIsInventoryOpen(false)}
        />
      )}

      {state.battleOver && (
        <div className="battle-over-overlay">
          <div className={`battle-over-modal ${state.battleOver.result}`}>
            <h2 className="battle-over-title">
              {state.battleOver.result === "victory" ? "¡Victoria!" : "¡Derrota!"}
            </h2>
            {state.battleOver.result === "victory" && (
              <div className="battle-over-rewards">
                {missionRewards ? (
                  <>
                    <p className="battle-over-xp">+{missionRewards.xp_awarded} XP</p>
                    <p className="battle-over-gold">+{missionRewards.gold_awarded} oro</p>
                    {missionRewards.items_awarded.length > 0 && (
                      <div className="battle-over-items">
                        <p className="battle-over-items-label">Objetos obtenidos:</p>
                        <div className="battle-over-items-list">
                          {missionRewards.items_awarded.map((item) => (
                            <div key={item.id} className="battle-over-item">
                              <ItemIcon item={item} />
                              <span className="battle-over-item-name">{item.name}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </>
                ) : (
                  <p className="battle-over-sub">Calculando recompensas...</p>
                )}
              </div>
            )}
            {state.battleOver.result === "defeat" && (
              <p className="battle-over-sub">Tus héroes han caído en combate.</p>
            )}
            <button
              className="battle-over-btn"
              onClick={onLeave}
              disabled={state.battleOver.result === "victory" && !missionRewards}
            >
              Volver al Tablón
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

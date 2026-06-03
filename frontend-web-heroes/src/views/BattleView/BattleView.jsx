import React, { useReducer, useEffect, useRef, useState } from "react";
import "./BattleView.css";
import BattleMap from "./components/BattleMap/BattleMap";
import TurnOrder from "./components/TurnOrder/TurnOrder";
import CombatLog from "./components/CombatLog/CombatLog";
import ActionButtons from "./components/ActionButtons/ActionButtons";
import CharacterStats from "./components/CharacterStats/CharacterStats";
import BattleInventory from "./components/BattleInventory/BattleInventory";

const API = "http://localhost:8000/api";

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function ts() {
  const now = new Date();
  return `${String(now.getMinutes()).padStart(2, "0")}:${String(now.getSeconds()).padStart(2, "0")}`;
}

export function getSpriteForHero(hero) {
  const cls = (hero?.hero_class?.name ?? "").toLowerCase();
  if (cls.includes("guerrero")) return "/sprites/Guerrero2.png";
  if (cls.includes("mago")) return "/sprites/Maga.png";
  if (cls.includes("picaro") || cls.includes("pícaro")) return "/sprites/Arquero.png";
  if (cls.includes("jefe")) return "/sprites/Orco.png";
  return "/sprites/Pelirrojo.png";
}

export function getSpriteForEnemy(enemy) {
  const name = (enemy?.name ?? "").toLowerCase();
  const cls = (enemy?.hero_class?.name ?? "").toLowerCase();
  if (name.includes("goblin") || cls.includes("goblin")) return "/sprites/Goblin-guerrero.png";
  if (name.includes("slime")) return "/sprites/Slime.png";
  if (name.includes("orco") || name.includes("orc")) return "/sprites/Orco.png";
  if (name.includes("lobo") || name.includes("wolf")) return "/sprites/Lobo.png";
  if (name.includes("oso") || name.includes("bear")) return "/sprites/Oso.png";
  if (name.includes("golem")) return "/sprites/Golem.png";
  if (name.includes("jabali") || name.includes("jabalí")) return "/sprites/Jabali.png";
  return "/sprites/Orco.png";
}

function buildTurnQueue(heroes, enemies) {
  const sh = shuffle(heroes);
  const se = shuffle(enemies);
  const result = [];
  const maxLen = Math.max(sh.length, se.length);
  for (let i = 0; i < maxLen; i++) {
    if (i < sh.length) {
      result.push({ id: sh[i].id, name: sh[i].name, type: "hero", sprite: getSpriteForHero(sh[i]) });
    }
    if (i < se.length) {
      result.push({ id: se[i].id, name: se[i].name, type: "enemy", sprite: getSpriteForEnemy(se[i]) });
    }
  }
  return result;
}

function nextAliveIndex(queue, current, heroes, enemies) {
  const total = queue.length;
  if (total === 0) return 0;
  let next = (current + 1) % total;
  for (let i = 0; i < total; i++) {
    const actor = queue[next];
    const hp =
      actor.type === "hero"
        ? (heroes.find((h) => h.id === actor.id)?.hp_current ?? 0)
        : (enemies.find((e) => e.id === actor.id)?.hp_current ?? 0);
    if (hp > 0) return next;
    next = (next + 1) % total;
  }
  return next;
}

const INITIAL_STATE = {
  heroes: [],
  enemies: [],
  userItems: [],
  turnQueue: [],
  currentTurnIndex: 0,
  logs: [{ timestamp: "00:00", message: "¡La batalla comienza!" }],
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
        heroes: action.heroes,
        enemies: action.enemies,
        userItems: action.userItems ?? [],
        turnQueue: action.turnQueue,
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

    case "HERO_ATTACK": {
      const newHeroes = state.heroes.map((h) =>
        h.id === action.heroId ? { ...h, hp_current: action.heroHp } : h
      );
      const newEnemies = state.enemies.map((e) =>
        e.id === action.enemyId ? { ...e, hp_current: action.enemyHp } : e
      );
      const newLogs = [
        ...state.logs,
        ...action.messages.map((m) => ({ timestamp: ts(), message: m })),
      ];
      if (action.xpMessage) {
        newLogs.push({ timestamp: ts(), message: action.xpMessage });
      }
      const allEnemiesDead = newEnemies.every((e) => e.hp_current <= 0);
      const allHeroesDead = newHeroes.every((h) => h.hp_current <= 0);
      const battleOver = allEnemiesDead
        ? { result: "victory", xpGained: action.xpGained ?? 0 }
        : allHeroesDead
        ? { result: "defeat", xpGained: 0 }
        : null;
      const nextIndex = battleOver
        ? state.currentTurnIndex
        : nextAliveIndex(state.turnQueue, state.currentTurnIndex, newHeroes, newEnemies);
      return {
        ...state,
        heroes: newHeroes,
        enemies: newEnemies,
        logs: newLogs,
        isAnimating: false,
        selectedEnemy: null,
        battleOver,
        currentTurnIndex: nextIndex,
      };
    }

    case "HERO_SKIP": {
      const newHeroes = action.defend
        ? state.heroes.map((h) =>
            h.id === action.heroId ? { ...h, isDefending: true } : h
          )
        : state.heroes;
      const newLogs = [...state.logs, { timestamp: ts(), message: action.message }];
      const nextIndex = nextAliveIndex(
        state.turnQueue,
        state.currentTurnIndex,
        newHeroes,
        state.enemies
      );
      return {
        ...state,
        heroes: newHeroes,
        logs: newLogs,
        isAnimating: false,
        selectedEnemy: null,
        currentTurnIndex: nextIndex,
      };
    }

    case "ENEMY_ATTACK": {
      const target = state.heroes.find((h) => h.id === action.targetId);
      if (!target) return { ...state, isAnimating: false };

      const isDefending = target.isDefending ?? false;
      const rawDmg = action.rawDamage;
      const dmg = action.hit
        ? isDefending
          ? Math.max(1, Math.floor(rawDmg / 2))
          : rawDmg
        : 0;

      const message = !action.hit
        ? `${action.enemyName} intenta atacar a ${target.name}, ¡pero falla!`
        : isDefending
        ? `${action.enemyName} ataca a ${target.name}, ¡pero estaba defendiendo! (${dmg} daño)`
        : `${action.enemyName} ataca a ${target.name} causando ${dmg} de daño.`;

      const newHeroes = state.heroes.map((h) => {
        if (h.id !== action.targetId) return h;
        return { ...h, hp_current: Math.max(0, h.hp_current - dmg), isDefending: false };
      });
      const newLogs = [...state.logs, { timestamp: ts(), message }];
      const allHeroesDead = newHeroes.every((h) => h.hp_current <= 0);
      const battleOver = allHeroesDead ? { result: "defeat", xpGained: 0 } : null;
      const nextIndex = battleOver
        ? state.currentTurnIndex
        : nextAliveIndex(state.turnQueue, state.currentTurnIndex, newHeroes, state.enemies);
      return {
        ...state,
        heroes: newHeroes,
        logs: newLogs,
        isAnimating: false,
        battleOver,
        currentTurnIndex: nextIndex,
      };
    }

    case "USE_ITEM": {
      const newHeroes = state.heroes.map((h) =>
        h.id === action.heroId
          ? { ...h, hp_current: action.heroHp, mp_current: action.heroMp }
          : h
      );
      const newUserItems = state.userItems
        .map((ui) =>
          ui.item_id === action.itemId ? { ...ui, quantity: action.newQty } : ui
        )
        .filter((ui) => ui.quantity > 0);
      const newLogs = [...state.logs, { timestamp: ts(), message: action.message }];
      const nextIndex = nextAliveIndex(
        state.turnQueue,
        state.currentTurnIndex,
        newHeroes,
        state.enemies
      );
      return {
        ...state,
        heroes: newHeroes,
        userItems: newUserItems,
        logs: newLogs,
        isAnimating: false,
        selectedEnemy: null,
        currentTurnIndex: nextIndex,
      };
    }

    default:
      return state;
  }
}

export default function BattleView({ mission, onLeave }) {
  const [state, dispatch] = useReducer(reducer, INITIAL_STATE);
  const stateRef = useRef(state);
  const userRef = useRef(null);
  const [isInventoryOpen, setIsInventoryOpen] = useState(false);

  useEffect(() => {
    stateRef.current = state;
  }, [state]);

  useEffect(() => {
    const stored = localStorage.getItem("webHeroesUser");
    userRef.current = stored ? JSON.parse(stored) : null;
    const user = userRef.current;

    async function load() {
      try {
        const enemyIds = mission?.enemy_ids ?? [];
        const [heroRes, inventoryRes, ...enemyResArr] = await Promise.all([
          fetch(`${API}/heroes?user_id=${user?.id}`),
          fetch(`${API}/shop/inventory?user_id=${user?.id}`),
          ...enemyIds.map((id) => fetch(`${API}/enemies/${id}`)),
        ]);

        if (!heroRes.ok) throw new Error("No se pudieron cargar los héroes.");
        const heroData = await heroRes.json();
        const inventoryData = inventoryRes.ok ? await inventoryRes.json() : { user_items: [] };
        const enemyData = await Promise.all(enemyResArr.map((r) => r.json()));

        const heroes = heroData
          .filter((h) => h.hp_current > 0)
          .map((h) => ({ ...h, isDefending: false }));

        const enemies = enemyData.map((e) => ({ ...e, hp_current: e.hp_max }));
        const userItems = (inventoryData.user_items ?? []).filter(
          (ui) => ui.item?.type?.slug === "consumable" && ui.quantity > 0
        );
        const turnQueue = buildTurnQueue(heroes, enemies);
        dispatch({ type: "LOAD", heroes, enemies, userItems, turnQueue });
      } catch (err) {
        dispatch({ type: "LOAD_ERROR", message: err.message });
      }
    }
    load();
  }, []);

  // Enemy auto-turn — intentionally excludes isAnimating from deps to avoid
  // cancelling its own timer (dispatching START_ANIMATING would re-trigger the effect).
  // isAnimating is only used for hero-side API calls.
  useEffect(() => {
    if (state.isLoading || state.battleOver) return;
    const cur = state.turnQueue[state.currentTurnIndex];
    if (!cur || cur.type !== "enemy") return;

    const timer = setTimeout(() => {
      const s = stateRef.current;
      const aliveHeroes = s.heroes.filter((h) => h.hp_current > 0);
      if (aliveHeroes.length === 0) return;

      const enemy = s.enemies.find((e) => e.id === cur.id);
      const target = aliveHeroes[Math.floor(Math.random() * aliveHeroes.length)];
      const baseAtk = enemy?.hero_class?.base_attack ?? 2;
      const heroDef = target.defense ?? 0;
      const rawDmg = Math.max(1, baseAtk - heroDef);
      const hit = Math.random() < 0.6;

      dispatch({
        type: "ENEMY_ATTACK",
        targetId: target.id,
        enemyName: cur.name,
        hit,
        rawDamage: rawDmg,
      });
    }, 1500);

    return () => clearTimeout(timer);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state.currentTurnIndex, !!state.battleOver, state.isLoading]);

  const currentActor = state.turnQueue[state.currentTurnIndex] ?? null;
  const isPlayerTurn =
    !state.isLoading &&
    !state.isAnimating &&
    !state.battleOver &&
    currentActor?.type === "hero";

  async function handleAction(action) {
    if (!isPlayerTurn) return;
    const cur = currentActor;

    if (action === "attack") {
      const enemy = state.selectedEnemy;
      if (!enemy) {
        dispatch({ type: "ADD_LOG", message: "Selecciona un enemigo objetivo primero." });
        return;
      }
      dispatch({ type: "START_ANIMATING" });
      try {
        const res = await fetch(`${API}/combat/attack/${cur.id}/${enemy.id}`, {
          method: "POST",
        });
        if (!res.ok) {
          const errData = await res.json();
          dispatch({ type: "ADD_LOG", message: errData.error ?? "Error al atacar." });
          dispatch({ type: "STOP_ANIMATING" });
          return;
        }
        const data = await res.json();

        // Award XP to the whole warband when an enemy is killed
        const xpGained = data.rewards?.xp_gained ?? 0;
        if (data.enemy_status.is_dead && xpGained > 0) {
          const otherIds = state.heroes
            .filter((h) => h.id !== cur.id && h.hp_current > 0)
            .map((h) => h.id);
          if (otherIds.length > 0) {
            fetch(`${API}/combat/award-xp`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ hero_ids: otherIds, amount: xpGained }),
            }).catch(() => {});
          }
        }

        const xpMessage = xpGained > 0
          ? `¡La warband gana ${xpGained} XP!`
          : null;

        dispatch({
          type: "HERO_ATTACK",
          heroId: cur.id,
          enemyId: enemy.id,
          heroHp: data.hero_status.hp_remaining,
          enemyHp: data.enemy_status.hp_remaining,
          messages: data.combat_log,
          xpGained,
          xpMessage,
        });
      } catch {
        dispatch({ type: "ADD_LOG", message: "Error de red al atacar." });
        dispatch({ type: "STOP_ANIMATING" });
      }
    } else if (action === "defend") {
      dispatch({
        type: "HERO_SKIP",
        heroId: cur.id,
        defend: true,
        message: `${cur.name} adopta una postura defensiva.`,
      });
    } else if (action === "abilities") {
      dispatch({
        type: "HERO_SKIP",
        heroId: cur.id,
        defend: false,
        message: `${cur.name} no tiene habilidades disponibles todavía.`,
      });
    } else if (action === "items") {
      setIsInventoryOpen(true);
    }
  }

  async function handleUseItem(userItem) {
    const cur = currentActor;
    if (!cur || cur.type !== "hero") return;
    const user = userRef.current;

    try {
      const res = await fetch(`${API}/shop/use-item`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: user?.id,
          item_id: userItem.item_id,
          hero_id: cur.id,
        }),
      });
      if (!res.ok) {
        const err = await res.json();
        dispatch({ type: "ADD_LOG", message: err.detail ?? "No se pudo usar el objeto." });
        return;
      }
      const data = await res.json();
      const restoreParts = [];
      if (data.hp_restored > 0) restoreParts.push(`+${data.hp_restored} HP`);
      if (data.mp_restored > 0) restoreParts.push(`+${data.mp_restored} MP`);
      const effect = restoreParts.length > 0 ? ` (${restoreParts.join(", ")})` : "";
      dispatch({
        type: "USE_ITEM",
        heroId: cur.id,
        itemId: userItem.item_id,
        heroHp: data.hero_hp,
        heroMp: data.hero_mp,
        newQty: data.quantity_remaining,
        message: `${cur.name} usa ${data.item_name}${effect}.`,
      });
    } catch {
      dispatch({ type: "ADD_LOG", message: "Error al usar el objeto." });
    } finally {
      setIsInventoryOpen(false);
    }
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
          <button className="flee-btn" onClick={onLeave}>
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
            {state.battleOver.result === "victory" && state.battleOver.xpGained > 0 && (
              <p className="battle-over-xp">+{state.battleOver.xpGained} XP ganada</p>
            )}
            {state.battleOver.result === "defeat" && (
              <p className="battle-over-sub">Tus héroes han caído en combate.</p>
            )}
            <button className="battle-over-btn" onClick={onLeave}>
              Volver al Tablón
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

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

      const isEvading = target.isEvading ?? false;
      const isDefendingHeavy = target.isDefendingHeavy ?? false;
      const isDefending = target.isDefending ?? false;
      const rawDmg = action.rawDamage;

      let dmg = 0;
      let message = "";

      if (!action.hit || isEvading) {
        dmg = 0;
        message = isEvading
          ? `${action.enemyName} ataca a ${target.name}, ¡pero esquiva en las sombras!`
          : `${action.enemyName} intenta atacar a ${target.name}, ¡pero falla!`;
      } else if (isDefendingHeavy) {
        dmg = Math.max(1, Math.floor(rawDmg / 4));
        message = `${action.enemyName} ataca a ${target.name}, ¡Grito de Guerra lo protege! (${dmg} daño)`;
      } else if (isDefending) {
        dmg = Math.max(1, Math.floor(rawDmg / 2));
        message = `${action.enemyName} ataca a ${target.name}, ¡pero estaba defendiendo! (${dmg} daño)`;
      } else {
        dmg = rawDmg;
        message = `${action.enemyName}${action.abilityName ? ` usa ${action.abilityName} sobre` : " ataca a"} ${target.name} causando ${dmg} de daño.`;
      }

      const newHeroes = state.heroes.map((h) => {
        if (h.id !== action.targetId) return h;
        return { ...h, hp_current: Math.max(0, h.hp_current - dmg), isDefending: false, isDefendingHeavy: false, isEvading: false };
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

    case "HERO_USE_ABILITY": {
      // Update hero MP and apply any self-buff flags
      const newHeroes = state.heroes.map((h) => {
        if (h.id !== action.heroId) return h;
        return {
          ...h,
          mp_current: action.mpRemaining,
          isDefendingHeavy: action.effectType === "heavy_defend" ? true : (h.isDefendingHeavy ?? false),
          isEvading: action.effectType === "evasion" ? true : (h.isEvading ?? false),
        };
      });

      // Apply damage to enemies
      let newEnemies = state.enemies;
      if (action.effectType === "damage_single" || action.effectType === "damage_pierce") {
        newEnemies = state.enemies.map((e) =>
          e.id === action.enemyId ? { ...e, hp_current: Math.max(0, e.hp_current - action.damage) } : e
        );
      } else if (action.effectType === "damage_all") {
        newEnemies = state.enemies.map((e) =>
          e.hp_current > 0 ? { ...e, hp_current: Math.max(0, e.hp_current - action.damage) } : e
        );
      }

      const newLogs = [...state.logs, { timestamp: ts(), message: action.message }];
      const allEnemiesDead = newEnemies.every((e) => e.hp_current <= 0);
      const battleOver = allEnemiesDead ? { result: "victory", xpGained: 0 } : null;
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

    default:
      return state;
  }
}

export default function BattleView({ mission, onLeave }) {
  const [state, dispatch] = useReducer(reducer, INITIAL_STATE);
  const stateRef = useRef(state);
  const userRef = useRef(null);
  const [isInventoryOpen, setIsInventoryOpen] = useState(false);
  const [isAbilitiesOpen, setIsAbilitiesOpen] = useState(false);
  const [missionRewards, setMissionRewards] = useState(null);

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
          .map((h) => ({ ...h, isDefending: false, isDefendingHeavy: false, isEvading: false }));

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
      const enemyClass = (enemy?.hero_class?.name ?? "").toLowerCase();
      const abilityRoll = Math.random();

      let rawDmg = Math.max(1, baseAtk - heroDef);
      let hit = Math.random() < 0.6;
      let abilityName = null;

      // Enemy class abilities (client-side)
      if (enemyClass.includes("jefe") && abilityRoll < 0.35) {
        // Golpe Aplastante: 2.5x damage, guaranteed
        rawDmg = Math.max(1, Math.floor(baseAtk * 2.5) - heroDef);
        hit = true;
        abilityName = "Golpe Aplastante";
      } else if (enemyClass.includes("guerrero") && abilityRoll < 0.25) {
        // Golpe Potente: 2x damage, guaranteed
        rawDmg = Math.max(1, baseAtk * 2 - heroDef);
        hit = true;
        abilityName = "Golpe Potente";
      } else if (enemyClass.includes("mago") && abilityRoll < 0.25) {
        // Rayo Arcano: flat 3 damage, ignores defense, guaranteed
        rawDmg = 3;
        hit = true;
        abilityName = "Rayo Arcano";
      } else if (enemyClass.includes("animal") && abilityRoll < 0.30) {
        // Zarpazo Salvaje: 1.5x damage, guaranteed
        rawDmg = Math.max(1, Math.floor(baseAtk * 1.5) - heroDef);
        hit = true;
        abilityName = "Zarpazo Salvaje";
      }

      dispatch({
        type: "ENEMY_ATTACK",
        targetId: target.id,
        enemyName: cur.name,
        hit,
        rawDamage: rawDmg,
        abilityName,
      });
    }, 1500);

    return () => clearTimeout(timer);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state.currentTurnIndex, !!state.battleOver, state.isLoading]);

  // Call mission complete endpoint on victory to award gold + items
  useEffect(() => {
    if (state.battleOver?.result !== "victory" || !mission?.id) return;
    const user = userRef.current;
    const heroIds = stateRef.current.heroes.map((h) => h.id);
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
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ enemy_hp_current: enemy.hp_current }),
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
      setIsAbilitiesOpen(true);
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

  async function handleUseAbility(ability) {
    const cur = currentActor;
    if (!cur || cur.type !== "hero") return;

    const hero = state.heroes.find((h) => h.id === cur.id);
    if (!hero) return;

    dispatch({ type: "START_ANIMATING" });
    setIsAbilitiesOpen(false);

    try {
      const res = await fetch(`${API}/combat/use-ability/${cur.id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ability_id: ability.id }),
      });
      if (!res.ok) {
        const err = await res.json();
        dispatch({ type: "ADD_LOG", message: err.detail ?? "Error al usar habilidad." });
        dispatch({ type: "STOP_ANIMATING" });
        return;
      }
      const data = await res.json();

      // Compute actual damage on frontend
      let damage = 0;
      let message = "";
      const effectType = data.effect_type;

      if (effectType === "damage_single") {
        const mult = data.damage_multiplier ?? 1.0;
        damage = Math.max(1, Math.floor(hero.attack * mult));
        const enemy = state.selectedEnemy;
        message = `${cur.name} usa ${data.ability_name} sobre ${enemy?.name ?? "el enemigo"} causando ${damage} de daño.`;
      } else if (effectType === "damage_pierce") {
        damage = data.flat_damage ?? 4;
        const enemy = state.selectedEnemy;
        message = `${cur.name} lanza ${data.ability_name} sobre ${enemy?.name ?? "el enemigo"} causando ${damage} de daño mágico (ignora defensa).`;
      } else if (effectType === "damage_all") {
        damage = data.flat_damage ?? 3;
        message = `${cur.name} lanza ${data.ability_name}, causando ${damage} de daño a todos los enemigos.`;
      } else if (effectType === "heavy_defend") {
        message = `${cur.name} grita con furia. ¡Grito de Guerra activo (75% reducción de daño)!`;
      } else if (effectType === "evasion") {
        message = `${cur.name} se funde con las sombras. ¡Evasión activa!`;
      }

      // Award XP for ability kills (same pattern as regular attacks)
      if (effectType === "damage_single" || effectType === "damage_pierce") {
        const enemy = state.selectedEnemy;
        if (enemy && enemy.hp_current - damage <= 0) {
          const allIds = state.heroes.filter((h) => h.hp_current > 0).map((h) => h.id);
          if (allIds.length > 0) {
            fetch(`${API}/combat/award-xp`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ hero_ids: allIds, amount: enemy.xp_reward ?? 0 }),
            }).catch(() => {});
          }
        }
      } else if (effectType === "damage_all") {
        const killedEnemies = state.enemies.filter((e) => e.hp_current > 0 && e.hp_current - damage <= 0);
        if (killedEnemies.length > 0) {
          const totalXp = killedEnemies.reduce((sum, e) => sum + (e.xp_reward ?? 0), 0);
          const allIds = state.heroes.filter((h) => h.hp_current > 0).map((h) => h.id);
          if (totalXp > 0 && allIds.length > 0) {
            fetch(`${API}/combat/award-xp`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ hero_ids: allIds, amount: totalXp }),
            }).catch(() => {});
          }
        }
      }

      dispatch({
        type: "HERO_USE_ABILITY",
        heroId: cur.id,
        mpRemaining: data.mp_remaining,
        effectType,
        damage,
        enemyId: state.selectedEnemy?.id ?? null,
        message,
      });
    } catch {
      dispatch({ type: "ADD_LOG", message: "Error de red al usar habilidad." });
      dispatch({ type: "STOP_ANIMATING" });
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
            currentHero={currentActor?.type === "hero" ? state.heroes.find((h) => h.id === currentActor.id) : null}
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
          hero={currentActor?.type === "hero" ? state.heroes.find((h) => h.id === currentActor.id) : null}
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
                {state.battleOver.xpGained > 0 && (
                  <p className="battle-over-xp">+{state.battleOver.xpGained} XP (combate)</p>
                )}
                {missionRewards ? (
                  <>
                    <p className="battle-over-xp">+{missionRewards.xp_awarded} XP (misión)</p>
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

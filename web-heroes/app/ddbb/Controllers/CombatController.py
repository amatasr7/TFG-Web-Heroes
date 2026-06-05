"""
Combat business logic: battle sessions, enemy AI, turn management, ability damage.
Moves all game logic previously in BattleView.jsx to the backend.
"""
import random
import unicodedata
from typing import Optional

from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.orm.attributes import flag_modified

from app.crud.heroes import add_experience as crud_add_experience, get_hero as crud_get_hero
from app.crud.items import get_item
from app.crud.user_items import get_user_item, update_user_item_quantity
from app.ddbb.Models import Enemy, Hero, HeroItem, Item
from app.ddbb.Models.Ability import Ability
from app.ddbb.Models.BattleSession import BattleSession
from app.ddbb.Models.Warband import Warband
from app.ddbb.Models.WarbandHero import WarbandHero


def _normalize(text: str) -> str:
    return unicodedata.normalize("NFD", text.lower()).encode("ascii", "ignore").decode()


# ── State builders ─────────────────────────────────────────────────────────────

def _hero_total_attack(hero: Hero) -> int:
    return hero.attack + sum(hi.item.damage_bonus for hi in hero.hero_items if hi.item)


def _build_heroes_state(heroes: list[Hero]) -> list[dict]:
    states = []
    for hero in heroes:
        hp_max = hero.hero_class.base_hp_max + hero.hp_bonus
        mp_max = hero.hero_class.base_mp_max + hero.mp_bonus
        states.append({
            "id": hero.id,
            "name": hero.name,
            "sprite_url": hero.sprite_url,
            "hp_current": hero.hp_current,
            "hp_max": hp_max,
            "mp_current": hero.mp_current,
            "mp_max": mp_max,
            "attack": _hero_total_attack(hero),
            "defense": hero.defense,
            "hero_class_name": hero.hero_class.name,
            "hero_class": {"name": hero.hero_class.name},
            "is_defending": False,
            "is_defending_heavy": False,
            "is_evading": False,
        })
    return states


def _build_enemies_state(enemies: list[Enemy]) -> list[dict]:
    return [
        {
            "id": enemy.id,
            "name": enemy.name,
            "hp_current": enemy.hp_max,
            "hp_max": enemy.hp_max,
            "base_attack": enemy.hero_class.base_attack,
            "hero_class_name": enemy.hero_class.name,
            "hero_class": {"name": enemy.hero_class.name},
            "xp_reward": enemy.xp_reward,
        }
        for enemy in enemies
    ]


def _build_turn_queue(heroes_state: list[dict], enemies_state: list[dict]) -> list[dict]:
    h = [{"id": s["id"], "name": s["name"], "type": "hero"} for s in heroes_state]
    e = [{"id": s["id"], "name": s["name"], "type": "enemy"} for s in enemies_state]
    random.shuffle(h)
    random.shuffle(e)
    queue: list[dict] = []
    for i in range(max(len(h), len(e))):
        if i < len(h):
            queue.append(h[i])
        if i < len(e):
            queue.append(e[i])
    return queue


# ── Turn helpers ───────────────────────────────────────────────────────────────

def _next_alive_index(session: BattleSession) -> int:
    queue = session.turn_queue
    total = len(queue)
    if total == 0:
        return 0
    start = (session.current_turn_index + 1) % total
    for i in range(total):
        idx = (start + i) % total
        actor = queue[idx]
        if actor["type"] == "hero":
            hp = next((h["hp_current"] for h in session.heroes_state if h["id"] == actor["id"]), 0)
        else:
            hp = next((e["hp_current"] for e in session.enemies_state if e["id"] == actor["id"]), 0)
        if hp > 0:
            return idx
    return start


def _check_battle_status(session: BattleSession) -> str:
    if all(e["hp_current"] <= 0 for e in session.enemies_state):
        return "victory"
    if all(h["hp_current"] <= 0 for h in session.heroes_state):
        return "defeat"
    return "active"


def _persist_session(session: BattleSession, db: Session) -> None:
    flag_modified(session, "heroes_state")
    flag_modified(session, "enemies_state")
    flag_modified(session, "turn_queue")
    db.commit()
    db.refresh(session)


# ── Enemy AI ───────────────────────────────────────────────────────────────────

def _process_enemy_turn(session: BattleSession) -> list[str]:
    queue = session.turn_queue
    current = queue[session.current_turn_index]

    enemy_state = next((e for e in session.enemies_state if e["id"] == current["id"]), None)
    if enemy_state is None or enemy_state["hp_current"] <= 0:
        return []

    alive_heroes = [h for h in session.heroes_state if h["hp_current"] > 0]
    if not alive_heroes:
        return []

    target = random.choice(alive_heroes)
    base_atk = enemy_state.get("base_attack", 2)
    enemy_class = _normalize(enemy_state.get("hero_class_name", ""))
    hero_def = target["defense"]

    ability_roll = random.random()
    raw_dmg = max(1, base_atk - hero_def)
    hit = random.random() < 0.6
    ability_name = None

    if "jefe" in enemy_class and ability_roll < 0.35:
        raw_dmg = max(1, int(base_atk * 2.5) - hero_def)
        hit = True
        ability_name = "Golpe Aplastante"
    elif "guerrero" in enemy_class and ability_roll < 0.25:
        raw_dmg = max(1, base_atk * 2 - hero_def)
        hit = True
        ability_name = "Golpe Potente"
    elif "mago" in enemy_class and ability_roll < 0.25:
        raw_dmg = 3
        hit = True
        ability_name = "Rayo Arcano"
    elif "animal" in enemy_class and ability_roll < 0.30:
        raw_dmg = max(1, int(base_atk * 1.5) - hero_def)
        hit = True
        ability_name = "Zarpazo Salvaje"

    is_evading = target.get("is_evading", False)
    is_defending_heavy = target.get("is_defending_heavy", False)
    is_defending = target.get("is_defending", False)

    logs: list[str] = []
    dmg = 0

    if not hit or is_evading:
        if is_evading:
            logs.append(f"{current['name']} ataca a {target['name']}, ¡pero esquiva en las sombras!")
        else:
            logs.append(f"{current['name']} intenta atacar a {target['name']}, ¡pero falla!")
    elif is_defending_heavy:
        dmg = max(1, raw_dmg // 4)
        logs.append(f"{current['name']} ataca a {target['name']}, ¡Grito de Guerra lo protege! ({dmg} daño)")
    elif is_defending:
        dmg = max(1, raw_dmg // 2)
        logs.append(f"{current['name']} ataca a {target['name']}, ¡pero estaba defendiendo! ({dmg} daño)")
    else:
        dmg = raw_dmg
        if ability_name:
            logs.append(f"{current['name']} usa {ability_name} sobre {target['name']} causando {dmg} de daño.")
        else:
            logs.append(f"{current['name']} ataca a {target['name']} causando {dmg} de daño.")

    session.heroes_state = [
        {
            **h,
            "hp_current": max(0, h["hp_current"] - dmg),
            "is_defending": False,
            "is_defending_heavy": False,
            "is_evading": False,
        } if h["id"] == target["id"] else h
        for h in session.heroes_state
    ]

    return logs


def _auto_process_enemy_turns(session: BattleSession, logs: list[str], db: Session) -> None:
    """Process consecutive enemy turns until a hero's turn or battle ends."""
    while session.status == "active":
        queue = session.turn_queue
        if not queue:
            break
        current = queue[session.current_turn_index]
        if current["type"] != "enemy":
            break
        enemy_state = next((e for e in session.enemies_state if e["id"] == current["id"]), None)
        if enemy_state and enemy_state["hp_current"] > 0:
            logs.extend(_process_enemy_turn(session))
        session.status = _check_battle_status(session)
        if session.status != "active":
            break
        session.current_turn_index = _next_alive_index(session)


# ── Hero actions ───────────────────────────────────────────────────────────────

def _hero_attack_action(session: BattleSession, hero_id: int, target_enemy_id: int, db: Session) -> list[str]:
    hero_state = next((h for h in session.heroes_state if h["id"] == hero_id), None)
    enemy_state = next((e for e in session.enemies_state if e["id"] == target_enemy_id), None)

    if hero_state is None:
        return ["Error: héroe no encontrado en la sesión."]
    if enemy_state is None or enemy_state["hp_current"] <= 0:
        return ["Ese enemigo ya está derrotado."]

    logs: list[str] = []
    enemy_new_hp = enemy_state["hp_current"]

    if random.randint(1, 100) <= 80:
        cls = _normalize(hero_state.get("hero_class_name", ""))
        dmg = 3 if "guerrero" in cls else 2
        enemy_new_hp = max(0, enemy_new_hp - dmg)
        logs.append(f"{hero_state['name']} ataca a {enemy_state['name']}.")
    else:
        logs.append(f"{hero_state['name']} intenta atacar, pero {enemy_state['name']} esquiva el golpe.")

    session.enemies_state = [
        {**e, "hp_current": enemy_new_hp} if e["id"] == target_enemy_id else e
        for e in session.enemies_state
    ]

    if enemy_new_hp <= 0:
        xp = enemy_state.get("xp_reward", 0)
        logs.append(f"¡El grupo ha derrotado a {enemy_state['name']}!")
        if xp > 0:
            logs.append(f"¡La warband gana {xp} XP!")
            for h_state in session.heroes_state:
                if h_state["hp_current"] > 0:
                    hero = crud_get_hero(db, h_state["id"])
                    if hero:
                        crud_add_experience(db, hero, xp)

    return logs


def _hero_defend_action(session: BattleSession, hero_id: int) -> list[str]:
    hero_state = next((h for h in session.heroes_state if h["id"] == hero_id), None)
    if hero_state is None:
        return []
    session.heroes_state = [
        {**h, "is_defending": True} if h["id"] == hero_id else h
        for h in session.heroes_state
    ]
    return [f"{hero_state['name']} adopta una postura defensiva."]


def _hero_use_ability_action(
    session: BattleSession,
    hero_id: int,
    ability_id: str,
    target_enemy_id: int | None,
    db: Session,
) -> list[str]:
    hero_state = next((h for h in session.heroes_state if h["id"] == hero_id), None)
    if hero_state is None:
        raise ValueError("Héroe no encontrado en la sesión.")

    ability = db.query(Ability).filter(Ability.slug == ability_id).first()
    if ability is None:
        raise ValueError(f"Habilidad desconocida: {ability_id}")

    if _normalize(hero_state.get("hero_class_name", "")) != _normalize(ability.class_name):
        raise ValueError(f"{hero_state['name']} no puede usar esa habilidad.")

    if hero_state["mp_current"] < ability.mp_cost:
        raise ValueError(f"Maná insuficiente. Necesitas {ability.mp_cost} MP.")

    new_mp = hero_state["mp_current"] - ability.mp_cost
    session.heroes_state = [
        {**h, "mp_current": new_mp} if h["id"] == hero_id else h
        for h in session.heroes_state
    ]
    hero_state = {**hero_state, "mp_current": new_mp}

    effect_type = ability.effect_type
    logs: list[str] = []

    if effect_type in ("damage_single", "damage_pierce"):
        if target_enemy_id is None:
            raise ValueError("Selecciona un enemigo objetivo.")
        enemy_state = next((e for e in session.enemies_state if e["id"] == target_enemy_id), None)
        if enemy_state is None or enemy_state["hp_current"] <= 0:
            raise ValueError("Objetivo no válido.")

        if effect_type == "damage_single":
            dmg = max(1, int(hero_state["attack"] * (ability.damage_multiplier or 1.0)))
        else:
            dmg = ability.flat_damage or 4

        new_enemy_hp = max(0, enemy_state["hp_current"] - dmg)
        session.enemies_state = [
            {**e, "hp_current": new_enemy_hp} if e["id"] == target_enemy_id else e
            for e in session.enemies_state
        ]
        logs.append(f"{hero_state['name']} usa {ability.name} sobre {enemy_state['name']} causando {dmg} de daño.")

        if new_enemy_hp <= 0:
            xp = enemy_state.get("xp_reward", 0)
            logs.append(f"¡El grupo ha derrotado a {enemy_state['name']}!")
            if xp > 0:
                logs.append(f"¡La warband gana {xp} XP!")
                for h_state in session.heroes_state:
                    hero = crud_get_hero(db, h_state["id"])
                    if hero:
                        crud_add_experience(db, hero, xp)

    elif effect_type == "damage_all":
        dmg = ability.flat_damage or 3
        total_xp = 0
        new_enemies = []
        for e in session.enemies_state:
            if e["hp_current"] > 0:
                new_hp = max(0, e["hp_current"] - dmg)
                new_enemies.append({**e, "hp_current": new_hp})
                if new_hp <= 0:
                    total_xp += e.get("xp_reward", 0)
                    logs.append(f"¡{e['name']} ha sido derrotado!")
            else:
                new_enemies.append(e)
        session.enemies_state = new_enemies
        logs.insert(0, f"{hero_state['name']} lanza {ability.name}, causando {dmg} de daño a todos los enemigos.")
        if total_xp > 0:
            logs.append(f"¡La warband gana {total_xp} XP!")
            for h_state in session.heroes_state:
                hero = crud_get_hero(db, h_state["id"])
                if hero:
                    crud_add_experience(db, hero, total_xp)

    elif effect_type == "heavy_defend":
        session.heroes_state = [
            {**h, "is_defending_heavy": True} if h["id"] == hero_id else h
            for h in session.heroes_state
        ]
        logs.append(f"{hero_state['name']} grita con furia. ¡Grito de Guerra activo (75% reducción de daño)!")

    elif effect_type == "evasion":
        session.heroes_state = [
            {**h, "is_evading": True} if h["id"] == hero_id else h
            for h in session.heroes_state
        ]
        logs.append(f"{hero_state['name']} se funde con las sombras. ¡Evasión activa!")

    # Persist MP cost to hero DB record
    hero_db = crud_get_hero(db, hero_id)
    if hero_db:
        hero_db.mp_current = new_mp
        db.commit()

    return logs


def _hero_use_item_action(
    session: BattleSession,
    hero_id: int,
    item_id: int,
    user_id: int,
    db: Session,
) -> list[str]:
    hero_state = next((h for h in session.heroes_state if h["id"] == hero_id), None)
    if hero_state is None:
        raise ValueError("Héroe no encontrado.")

    user_item = get_user_item(db, user_id, item_id)
    if not user_item or user_item.quantity <= 0:
        raise ValueError("No tienes ese objeto.")

    item = get_item(db, item_id)
    if item is None or item.type.slug != "consumable":
        raise ValueError("Este objeto no es consumible.")

    hp_max = hero_state["hp_max"]
    mp_max = hero_state["mp_max"]
    hp_restored = min(item.hp_bonus, hp_max - hero_state["hp_current"])
    mp_restored = min(item.mp_bonus, mp_max - hero_state["mp_current"])
    new_hp = min(hp_max, hero_state["hp_current"] + item.hp_bonus)
    new_mp = min(mp_max, hero_state["mp_current"] + item.mp_bonus)

    session.heroes_state = [
        {**h, "hp_current": new_hp, "mp_current": new_mp} if h["id"] == hero_id else h
        for h in session.heroes_state
    ]

    hero_db = crud_get_hero(db, hero_id)
    if hero_db:
        hero_db.hp_current = new_hp
        hero_db.mp_current = new_mp
    update_user_item_quantity(db, user_item, user_item.quantity - 1)
    db.commit()

    restore_parts = []
    if hp_restored > 0:
        restore_parts.append(f"+{hp_restored} HP")
    if mp_restored > 0:
        restore_parts.append(f"+{mp_restored} MP")
    effect = f" ({', '.join(restore_parts)})" if restore_parts else ""

    return [f"{hero_state['name']} usa {item.name}{effect}."]


# ── Public API ─────────────────────────────────────────────────────────────────

def start_battle(
    db: Session,
    user_id: int,
    mission_id: int | None,
    enemy_ids: list[int],
) -> tuple[BattleSession, list[str]]:
    warband = db.query(Warband).filter(Warband.user_id == user_id).first()
    if not warband:
        raise ValueError("No tienes una banda de guerra configurada. Configura tu banda desde la vista de héroes.")

    warband_hero_ids = [
        entry.hero_id
        for entry in db.query(WarbandHero).filter(WarbandHero.warband_id == warband.id).all()
    ]

    heroes = (
        db.query(Hero)
        .options(
            joinedload(Hero.hero_class),
            selectinload(Hero.hero_items).joinedload(HeroItem.item),
        )
        .filter(Hero.id.in_(warband_hero_ids), Hero.hp_current > 0)
        .all()
    )
    if not heroes:
        raise ValueError("Ningún héroe de tu banda de guerra está disponible para el combate.")

    enemies = (
        db.query(Enemy)
        .options(joinedload(Enemy.hero_class))
        .filter(Enemy.id.in_(enemy_ids))
        .all()
    )
    if not enemies:
        raise ValueError("No se encontraron los enemigos de la misión.")

    heroes_state = _build_heroes_state(heroes)
    enemies_state = _build_enemies_state(enemies)
    turn_queue = _build_turn_queue(heroes_state, enemies_state)

    session = BattleSession(
        user_id=user_id,
        mission_id=mission_id,
        turn_queue=turn_queue,
        current_turn_index=0,
        heroes_state=heroes_state,
        enemies_state=enemies_state,
        status="active",
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    logs: list[str] = ["¡La batalla comienza!"]
    _auto_process_enemy_turns(session, logs, db)
    _persist_session(session, db)

    return session, logs


def get_session(db: Session, session_id: int) -> Optional[BattleSession]:
    return db.get(BattleSession, session_id)


def process_hero_action(
    db: Session,
    session: BattleSession,
    action: str,
    hero_id: int,
    target_enemy_id: int | None = None,
    ability_id: str | None = None,
    item_id: int | None = None,
    user_id: int | None = None,
) -> tuple[dict, list[str]]:
    if session.status != "active":
        raise ValueError("La batalla ya ha terminado.")

    queue = session.turn_queue
    if not queue:
        raise ValueError("La cola de turnos está vacía.")

    current = queue[session.current_turn_index]
    if current["type"] != "hero" or current["id"] != hero_id:
        raise ValueError("No es el turno de ese héroe.")

    logs: list[str] = []

    if action == "attack":
        if target_enemy_id is None:
            raise ValueError("Selecciona un enemigo objetivo.")
        logs.extend(_hero_attack_action(session, hero_id, target_enemy_id, db))
    elif action == "defend":
        logs.extend(_hero_defend_action(session, hero_id))
    elif action == "use_ability":
        if not ability_id:
            raise ValueError("Habilidad no especificada.")
        logs.extend(_hero_use_ability_action(session, hero_id, ability_id, target_enemy_id, db))
    elif action == "use_item":
        if item_id is None or user_id is None:
            raise ValueError("item_id y user_id son requeridos.")
        logs.extend(_hero_use_item_action(session, hero_id, item_id, user_id, db))
    else:
        raise ValueError(f"Acción desconocida: {action}")

    session.status = _check_battle_status(session)
    if session.status == "active":
        session.current_turn_index = _next_alive_index(session)
        _auto_process_enemy_turns(session, logs, db)

    _persist_session(session, db)

    return {
        "session_id": session.id,
        "status": session.status,
        "turn_queue": session.turn_queue,
        "current_turn_index": session.current_turn_index,
        "heroes_state": session.heroes_state,
        "enemies_state": session.enemies_state,
    }, logs


def abandon_battle(db: Session, session: BattleSession) -> BattleSession:
    session.status = "abandoned"
    db.commit()
    db.refresh(session)
    return session

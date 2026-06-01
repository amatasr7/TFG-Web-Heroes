import random

from app.ddbb.database import SessionLocal
from app.ddbb.models import Enemy, Hero, HeroClass, Item, ItemType, Mission, User

HERO_CLASSES = [
    {
        "name": "Guerrero",
        "is_playable": True,
        "default_race": "Orco",
        "adjectives": ["Bruto", "Cicatrizado", "Acorazado", ""],
        "base_hp_max": 10,
        "base_mp_max": 2,
    },
    {
        "name": "Mago",
        "is_playable": True,
        "default_race": "Chaman",
        "adjectives": ["Oscuro", "Ascendente", "Malvado", ""],
        "base_hp_max": 6,
        "base_mp_max": 10,
    },
    {
        "name": "Picaro",
        "is_playable": True,
        "default_race": "Goblin",
        "adjectives": ["Astuto", "Acechante", "Ratero", ""],
        "base_hp_max": 8,
        "base_mp_max": 5,
    },
    {
        "name": "Jefe",
        "is_playable": False,
        "default_race": "Dragon",
        "adjectives": ["Rojo", "Azul", "Negro", ""],
        "base_hp_max": 30,
        "base_mp_max": 15,
    },
]

ITEMS = [
    {"name": "Daga de hierro", "type": "weapon", "sprite_x": 0, "sprite_y": 0, "damage": 1, "hp": 0},
    {"name": "Daga encantada", "type": "weapon", "sprite_x": 0, "sprite_y": 1, "damage": 3, "hp": 0},
    {"name": "Daga bendita", "type": "weapon", "sprite_x": 0, "sprite_y": 2, "damage": 5, "hp": 0},
    {"name": "Daga infernal", "type": "weapon", "sprite_x": 0, "sprite_y": 3, "damage": 7, "hp": 0},
    {"name": "Espada de hierro", "type": "weapon", "sprite_x": 1, "sprite_y": 0, "damage": 2, "hp": 0},
    {"name": "Espada encantada", "type": "weapon", "sprite_x": 1, "sprite_y": 1, "damage": 4, "hp": 0},
    {"name": "Espada bendita", "type": "weapon", "sprite_x": 1, "sprite_y": 2, "damage": 6, "hp": 0},
    {"name": "Espada infernal", "type": "weapon", "sprite_x": 1, "sprite_y": 3, "damage": 8, "hp": 0},
    {"name": "Maza de hierro", "type": "weapon", "sprite_x": 2, "sprite_y": 0, "damage": 2, "hp": 0},
    {"name": "Maza encantada", "type": "weapon", "sprite_x": 2, "sprite_y": 1, "damage": 3, "hp": 0},
    {"name": "Maza bendita", "type": "weapon", "sprite_x": 2, "sprite_y": 2, "damage": 5, "hp": 0},
    {"name": "Maza infernal", "type": "weapon", "sprite_x": 2, "sprite_y": 3, "damage": 7, "hp": 0},
    {"name": "Hacha de hierro", "type": "weapon", "sprite_x": 3, "sprite_y": 0, "damage": 3, "hp": 0},
    {"name": "Hacha encantada", "type": "weapon", "sprite_x": 3, "sprite_y": 1, "damage": 5, "hp": 0},
    {"name": "Hacha bendita", "type": "weapon", "sprite_x": 3, "sprite_y": 2, "damage": 7, "hp": 0},
    {"name": "Hacha infernal", "type": "weapon", "sprite_x": 3, "sprite_y": 3, "damage": 9, "hp": 0},
    {"name": "Lanza de hierro", "type": "weapon", "sprite_x": 4, "sprite_y": 0, "damage": 3, "hp": 0},
    {"name": "Lanza encantada", "type": "weapon", "sprite_x": 4, "sprite_y": 1, "damage": 5, "hp": 0},
    {"name": "Lanza bendita", "type": "weapon", "sprite_x": 4, "sprite_y": 2, "damage": 7, "hp": 0},
    {"name": "Lanza infernal", "type": "weapon", "sprite_x": 4, "sprite_y": 3, "damage": 9, "hp": 0},
    {"name": "Escudo de hierro", "type": "armor", "sprite_x": 5, "sprite_y": 0, "damage": 0, "hp": 2},
    {"name": "Escudo encantado", "type": "armor", "sprite_x": 5, "sprite_y": 1, "damage": 0, "hp": 4},
    {"name": "Escudo bendito", "type": "armor", "sprite_x": 5, "sprite_y": 2, "damage": 0, "hp": 6},
    {"name": "Escudo infernal", "type": "armor", "sprite_x": 5, "sprite_y": 3, "damage": 0, "hp": 8},
    {"name": "Arco de hierro", "type": "weapon", "sprite_x": 6, "sprite_y": 0, "damage": 2, "hp": 0},
    {"name": "Arco encantado", "type": "weapon", "sprite_x": 6, "sprite_y": 1, "damage": 3, "hp": 0},
    {"name": "Arco bendito", "type": "weapon", "sprite_x": 6, "sprite_y": 2, "damage": 5, "hp": 0},
    {"name": "Arco infernal", "type": "weapon", "sprite_x": 6, "sprite_y": 3, "damage": 6, "hp": 0},
    {"name": "Ballesta de hierro", "type": "weapon", "sprite_x": 7, "sprite_y": 0, "damage": 3, "hp": 0},
    {"name": "Ballesta encantada", "type": "weapon", "sprite_x": 7, "sprite_y": 1, "damage": 5, "hp": 0},
    {"name": "Ballesta bendita", "type": "weapon", "sprite_x": 7, "sprite_y": 2, "damage": 7, "hp": 0},
    {"name": "Ballesta infernal", "type": "weapon", "sprite_x": 7, "sprite_y": 3, "damage": 9, "hp": 0},
    {"name": "Armadura de cuero", "type": "armor", "sprite_x": 5, "sprite_y": 6, "damage": 0, "hp": 3},
    {"name": "Armadura de hierro", "type": "armor", "sprite_x": 5, "sprite_y": 7, "damage": 0, "hp": 5},
    {"name": "Armadura de placas", "type": "armor", "sprite_x": 7, "sprite_y": 6, "damage": 0, "hp": 5},
    {"name": "Pocion de Energia", "type": "consumable", "sprite_x": 4, "sprite_y": 0, "damage": 0, "hp": 25},
    {"name": "Pocion de Salud", "type": "consumable", "sprite_x": 5, "sprite_y": 0, "damage": 0, "hp": 25},
    {"name": "Pocion de Mana", "type": "consumable", "sprite_x": 6, "sprite_y": 0, "damage": 0, "mp": 25},
    {"name": "Moneda de oro", "type": "currency", "sprite_x": 7, "sprite_y": 0, "damage": 0, "hp": 0, "value": 1},
    {"name": "Saco de monedas de oro", "type": "currency", "sprite_x": 4, "sprite_y": 5, "damage": 0, "hp": 0, "value_min": 5, "value_max": 20},
    {"name": "Cofre lleno de oro", "type": "container", "sprite_x": 5, "sprite_y": 5, "damage": 0, "hp": 0, "value_min": 10, "value_max": 50},
]


def seed_database() -> None:
    db = SessionLocal()
    try:
        if db.query(HeroClass).first():
            return

        user = User(
            name="Test User",
            email="test@example.com",
            password="",
            is_admin=True,
        )
        db.add(user)

        classes: dict[str, HeroClass] = {}
        for data in HERO_CLASSES:
            hero_class = HeroClass(**data)
            db.add(hero_class)
            classes[data["name"]] = hero_class

        db.flush()

        type_cache: dict[str, ItemType] = {}
        for item_data in ITEMS:
            slug = item_data.get("type", "consumable")
            if slug not in type_cache:
                item_type = ItemType(name=slug.capitalize(), slug=slug)
                db.add(item_type)
                db.flush()
                type_cache[slug] = item_type

            value = item_data.get("value", 0)
            if "value_min" in item_data and "value_max" in item_data:
                value = random.randint(item_data["value_min"], item_data["value_max"])

            db.add(
                Item(
                    name=item_data["name"],
                    item_type_id=type_cache[slug].id,
                    sprite_x=item_data.get("sprite_x", 0),
                    sprite_y=item_data.get("sprite_y", 0),
                    damage_bonus=item_data.get("damage", 0),
                    hp_bonus=item_data.get("hp", 0),
                    mp_bonus=item_data.get("mp", 0),
                    price=item_data.get("price", 0),
                    value=value,
                )
            )

        hero_seeds = [
            ("Aragorn", "Guerrero", 10, 2, 10),
            ("Morgana", "Mago", 6, 10, 10),
            ("Sombra", "Picaro", 8, 5, 10),
        ]
        for name, class_name, hp, mp, energy in hero_seeds:
            db.add(
                Hero(
                    user_id=user.id,
                    hero_class_id=classes[class_name].id,
                    name=name,
                    hp_current=hp,
                    mp_current=mp,
                    energy_current=energy,
                )
            )

        enemies = [
            Enemy(
                name="Guerrero enemigo",
                hero_class_id=classes["Guerrero"].id,
                level=1,
                hp_max=8,
                hp_current=8,
                xp_reward=20,
                is_boss=False,
            ),
            Enemy(
                name="Chaman enemigo",
                hero_class_id=classes["Mago"].id,
                level=1,
                hp_max=6,
                hp_current=6,
                xp_reward=25,
                is_boss=False,
            ),
            Enemy(
                name="Dragon rojo",
                hero_class_id=classes["Jefe"].id,
                level=5,
                hp_max=30,
                hp_current=30,
                xp_reward=100,
                is_boss=True,
            ),
        ]

        db.add_all(enemies)
        db.flush()

        mission_seeds = [
            {
                "name": "Plaga en el Sótano",
                "description": "El tabernero del 'Pony Pisador' pide ayuda para limpiar las raíces de una plaga de roedores gigantes que han invadido su almacén.",
                "enemy_ids": [enemies[0].id],
                "xp_reward": 50,
                "gold_reward": 55,
            },
            {
                "name": "Emboscada en el Camino",
                "description": "Un grupo de bandidos ha bloqueado la ruta hacia el este y la caravana necesita protección para llegar sana y salva.",
                "enemy_ids": [enemies[1].id],
                "xp_reward": 120,
                "gold_reward": 105,
            },
            {
                "name": "El Despertar del Dragón",
                "description": "Una cría de dragón ha sido avistada cerca de la aldea y se teme que atraiga a otras bestias de fuego.",
                "enemy_ids": [enemies[2].id],
                "xp_reward": 450,
                "gold_reward": 220,
            },
        ]

        for mission_data in mission_seeds:
            db.add(Mission(**mission_data))

        db.commit()
    finally:
        db.close()

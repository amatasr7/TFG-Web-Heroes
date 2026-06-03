"""Seeder for Mission table. Every mission assigns exactly 2 enemies."""

from sqlalchemy.orm import Session

from app.ddbb.Models import Enemy, Item, Mission


# enemy_indexes reference ENEMY_SEEDS order in EnemySeeder.py:
# 0=Goblin Guerrero, 1=Goblin Arquero, 2=Slime Verde,
# 3=Orco Guerrero,   4=Orco Chamán,    5=Lobo Salvaje,
# 6=Lobo Alfa,       7=Oso Pardo,      8=Jabalí Furioso,
# 9=Golem de Piedra, 10=Dragon Rojo

# item_reward_indexes reference ITEMS order in ItemSeeder.py:
# 0=Daga de hierro,      4=Espada de hierro,   8=Maza de hierro,
# 12=Hacha de hierro,   20=Escudo de hierro,  32=Armadura de cuero,
# 33=Armadura de hierro, 35=Pocion de Energia, 36=Pocion de Salud,
# 37=Pocion de Mana
MISSION_SEEDS = [
    {
        "name": "Plaga en el Sótano",
        "description": "El tabernero del 'Pony Pisador' pide ayuda para limpiar los sótanos de una plaga de criaturas que han invadido su almacén.",
        "xp_reward": 50,
        "gold_reward": 55,
        "enemy_indexes": [0, 2],        # Goblin Guerrero + Slime Verde
        "item_reward_indexes": [36],    # Pocion de Salud
    },
    {
        "name": "Emboscada en el Camino",
        "description": "Un grupo de goblins ha bloqueado la ruta hacia el este. La caravana necesita protección para llegar sana y salva.",
        "xp_reward": 65,
        "gold_reward": 70,
        "enemy_indexes": [0, 1],        # Goblin Guerrero + Goblin Arquero
        "item_reward_indexes": [35],    # Pocion de Energia
    },
    {
        "name": "Cacería de Bestias",
        "description": "Los granjeros reportan ataques nocturnos al ganado. Se necesita eliminar a las bestias que merodean por los alrededores.",
        "xp_reward": 110,
        "gold_reward": 100,
        "enemy_indexes": [5, 8],        # Lobo Salvaje + Jabalí Furioso
        "item_reward_indexes": [36, 35],  # Pocion de Salud + Energia
    },
    {
        "name": "La Horda Orca",
        "description": "Un campamento orco ha aparecido cerca del poblado. Hay que neutralizarlo antes de que se organicen.",
        "xp_reward": 135,
        "gold_reward": 120,
        "enemy_indexes": [3, 4],        # Orco Guerrero + Orco Chamán
        "item_reward_indexes": [0],     # Daga de hierro
    },
    {
        "name": "La Manada del Bosque",
        "description": "Una manada de lobos liderada por un alfa ha tomado el control de los senderos del bosque.",
        "xp_reward": 120,
        "gold_reward": 110,
        "enemy_indexes": [5, 6],        # Lobo Salvaje + Lobo Alfa
        "item_reward_indexes": [36, 37],  # Pocion de Salud + Mana
    },
    {
        "name": "Amenaza en las Montañas",
        "description": "Viajeros heridos informan de bestias gigantescas en los pasos de montaña que bloquean la ruta comercial.",
        "xp_reward": 160,
        "gold_reward": 150,
        "enemy_indexes": [6, 7],        # Lobo Alfa + Oso Pardo
        "item_reward_indexes": [4],     # Espada de hierro
    },
    {
        "name": "El Despertar del Golem",
        "description": "Un antiguo golem de piedra ha despertado en las ruinas y un orco guerrero lo custodia. La región entera está en peligro.",
        "xp_reward": 260,
        "gold_reward": 220,
        "enemy_indexes": [9, 3],        # Golem de Piedra + Orco Guerrero
        "item_reward_indexes": [4, 20],  # Espada de hierro + Escudo de hierro
    },
    {
        "name": "Guarida del Dragón",
        "description": "Un dragón rojo ha anidado en las cuevas junto a un golem que actúa como guardián. La misión más peligrosa del Tablón.",
        "xp_reward": 480,
        "gold_reward": 400,
        "enemy_indexes": [10, 9],       # Dragon Rojo + Golem de Piedra
        "item_reward_indexes": [33, 12],  # Armadura de hierro + Hacha de hierro
    },
]


def seed_missions(db: Session, enemies: list[Enemy]) -> None:
    items: list[Item] = db.query(Item).order_by(Item.id).all()

    for mission_data in MISSION_SEEDS:
        data = dict(mission_data)
        enemy_indexes = data.pop("enemy_indexes")
        item_reward_indexes = data.pop("item_reward_indexes")

        enemy_ids = [enemies[i].id for i in enemy_indexes]
        item_reward_ids = [items[i].id for i in item_reward_indexes if i < len(items)]

        db.add(Mission(enemy_ids=enemy_ids, item_reward_ids=item_reward_ids, **data))
    db.flush()

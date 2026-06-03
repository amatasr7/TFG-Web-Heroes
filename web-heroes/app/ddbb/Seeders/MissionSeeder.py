"""Seeder for Mission table. Every mission assigns exactly 2 enemies."""

from sqlalchemy.orm import Session

from app.ddbb.Models import Enemy, Mission


# enemy_indexes reference ENEMY_SEEDS order in EnemySeeder.py:
# 0=Goblin Guerrero, 1=Goblin Arquero, 2=Slime Verde,
# 3=Orco Guerrero,   4=Orco Chamán,    5=Lobo Salvaje,
# 6=Lobo Alfa,       7=Oso Pardo,      8=Jabalí Furioso,
# 9=Golem de Piedra, 10=Dragon Rojo
MISSION_SEEDS = [
    {
        "name": "Plaga en el Sótano",
        "description": "El tabernero del 'Pony Pisador' pide ayuda para limpiar los sótanos de una plaga de criaturas que han invadido su almacén.",
        "xp_reward": 50,
        "gold_reward": 55,
        "enemy_indexes": [0, 2],  # Goblin Guerrero + Slime Verde
    },
    {
        "name": "Emboscada en el Camino",
        "description": "Un grupo de goblins ha bloqueado la ruta hacia el este. La caravana necesita protección para llegar sana y salva.",
        "xp_reward": 65,
        "gold_reward": 70,
        "enemy_indexes": [0, 1],  # Goblin Guerrero + Goblin Arquero
    },
    {
        "name": "Cacería de Bestias",
        "description": "Los granjeros reportan ataques nocturnos al ganado. Se necesita eliminar a las bestias que merodean por los alrededores.",
        "xp_reward": 110,
        "gold_reward": 100,
        "enemy_indexes": [5, 8],  # Lobo Salvaje + Jabalí Furioso
    },
    {
        "name": "La Horda Orca",
        "description": "Un campamento orco ha aparecido cerca del poblado. Hay que neutralizarlo antes de que se organicen.",
        "xp_reward": 135,
        "gold_reward": 120,
        "enemy_indexes": [3, 4],  # Orco Guerrero + Orco Chamán
    },
    {
        "name": "La Manada del Bosque",
        "description": "Una manada de lobos liderada por un alfa ha tomado el control de los senderos del bosque.",
        "xp_reward": 120,
        "gold_reward": 110,
        "enemy_indexes": [5, 6],  # Lobo Salvaje + Lobo Alfa
    },
    {
        "name": "Amenaza en las Montañas",
        "description": "Viajeros heridos informan de bestias gigantescas en los pasos de montaña que bloquean la ruta comercial.",
        "xp_reward": 160,
        "gold_reward": 150,
        "enemy_indexes": [6, 7],  # Lobo Alfa + Oso Pardo
    },
    {
        "name": "El Despertar del Golem",
        "description": "Un antiguo golem de piedra ha despertado en las ruinas y un orco guerrero lo custodia. La región entera está en peligro.",
        "xp_reward": 260,
        "gold_reward": 220,
        "enemy_indexes": [9, 3],  # Golem de Piedra + Orco Guerrero
    },
    {
        "name": "Guarida del Dragón",
        "description": "Un dragón rojo ha anidado en las cuevas junto a un golem que actúa como guardián. La misión más peligrosa del Tablón.",
        "xp_reward": 480,
        "gold_reward": 400,
        "enemy_indexes": [10, 9],  # Dragon Rojo + Golem de Piedra
    },
]


def seed_missions(db: Session, enemies: list[Enemy]) -> None:
    for mission_data in MISSION_SEEDS:
        data = dict(mission_data)
        enemy_indexes = data.pop("enemy_indexes")
        enemy_ids = [enemies[i].id for i in enemy_indexes]
        db.add(Mission(enemy_ids=enemy_ids, **data))
    db.flush()

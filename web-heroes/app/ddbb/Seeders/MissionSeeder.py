"""Seeder for Mission table."""

from sqlalchemy.orm import Session

from app.ddbb.Models import Enemy, Mission


MISSION_SEEDS = [
    {
        "name": "Plaga en el Sótano",
        "description": "El tabernero del 'Pony Pisador' pide ayuda para limpiar las raíces de una plaga de roedores gigantes que han invadido su almacén.",
        "xp_reward": 50,
        "gold_reward": 55,
        "enemy_indexes": [0],
    },
    {
        "name": "Emboscada en el Camino",
        "description": "Un grupo de bandidos ha bloqueado la ruta hacia el este y la caravana necesita protección para llegar sana y salva.",
        "xp_reward": 120,
        "gold_reward": 105,
        "enemy_indexes": [1],
    },
    {
        "name": "El Despertar del Dragón",
        "description": "Una cría de dragón ha sido avistada cerca de la aldea y se teme que atraiga a otras bestias de fuego.",
        "xp_reward": 450,
        "gold_reward": 220,
        "enemy_indexes": [2],
    },
    {
        "name": "Caza de Bestias",
        "description": "Los granjeros locales han reportado avistamientos de criaturas salvajes que atacan su ganado. Se necesita un héroe para investigar y eliminar la amenaza.",
        "xp_reward": 200,
        "gold_reward": 150,
        "enemy_indexes": [0, 1],
    },
    {
        "name": "Defensa de la Aldea",
        "description": "Una horda de enemigos se acerca a la aldea y los habitantes necesitan ayuda para defenderse.",
        "xp_reward": 500,
        "gold_reward": 300,
        "enemy_indexes": [0, 1, 2],
    },
    {
        "name": "Misión de Prueba",
        "description": "Una misión de prueba para verificar el funcionamiento del sistema.",
        "xp_reward": 100,
        "gold_reward": 50,
        "enemy_indexes": [0],
    },
    {
        "name": "Misión de Prueba Avanzada",
        "description": "Una misión de prueba más difícil para verificar el funcionamiento del sistema con múltiples enemigos.",
        "xp_reward": 200,
        "gold_reward": 100,
        "enemy_indexes": [0, 1],
    }
]


def seed_missions(db: Session, enemies: list[Enemy]) -> None:
    """
    Seed missions table.
    
    Args:
        db: Database session
        enemies: List of created Enemy instances
    """
    for mission_data in MISSION_SEEDS:
        enemy_indexes = mission_data.pop("enemy_indexes")
        enemy_ids = [enemies[i].id for i in enemy_indexes]
        
        db.add(
            Mission(
                enemy_ids=enemy_ids,
                **mission_data
            )
        )
    
    db.flush()

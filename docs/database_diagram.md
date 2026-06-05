# Diagrama Entidad-Relación — Web Heroes

```mermaid
erDiagram
    users {
        int id PK
        string name
        string email UK
        string password
        boolean is_admin
        int gold
        datetime created_at
        datetime updated_at
    }

    heroes {
        int id PK
        int user_id FK
        int hero_class_id FK
        string name
        string sprite_url
        int hp_current
        int mp_current
        int energy_current
        int hp_bonus
        int mp_bonus
        int attack
        int defense
        int experience
        int level
        datetime last_regen_at
        datetime last_action_at
        datetime created_at
        datetime updated_at
    }

    hero_classes {
        int id PK
        string name UK
        int base_hp_max
        int base_mp_max
        int base_attack
        int base_defense
        string default_race
        json adjectives
        boolean is_playable
        datetime created_at
        datetime updated_at
    }

    enemies {
        int id PK
        int hero_class_id FK
        string name UK
        int level
        int hp_max
        int xp_reward
        boolean is_boss
        datetime created_at
        datetime updated_at
    }

    abilities {
        int id PK
        string slug UK
        string name
        string class_name
        int mp_cost
        string effect_type
        float damage_multiplier
        int flat_damage
        boolean guaranteed_hit
        datetime created_at
        datetime updated_at
    }

    items {
        int id PK
        int item_type_id FK
        string name
        int sprite_x
        int sprite_y
        int hp_bonus
        int mp_bonus
        int damage_bonus
        int price
        int value
        string thumbnail_url
        datetime created_at
        datetime updated_at
    }

    item_types {
        int id PK
        string name
        string slug UK
        datetime created_at
        datetime updated_at
    }

    hero_items {
        int id PK
        int hero_id FK
        int item_id FK
        int item_type_id FK
        datetime created_at
        datetime updated_at
    }

    shop_items {
        int id PK
        int item_id UK "FK"
        int quantity
        datetime created_at
        datetime updated_at
    }

    user_items {
        int id PK
        int user_id FK
        int item_id FK
        int quantity
        datetime created_at
        datetime updated_at
    }

    warbands {
        int id PK
        int user_id UK "FK"
        string name
        datetime created_at
        datetime updated_at
    }

    warband_heroes {
        int id PK
        int warband_id FK
        int hero_id FK
        int slot
        datetime created_at
        datetime updated_at
    }

    missions {
        int id PK
        string name
        string description
        json enemy_ids
        json item_reward_ids
        int xp_reward
        int gold_reward
        datetime created_at
        datetime updated_at
    }

    user_missions {
        int id PK
        int user_id FK
        int mission_id FK
        datetime completed_at
    }

    battle_sessions {
        int id PK
        int user_id FK
        int mission_id FK
        json turn_queue
        int current_turn_index
        json heroes_state
        json enemies_state
        string status
        datetime created_at
        datetime updated_at
    }

    %% --- Relaciones de Usuario ---
    users ||--o{ heroes          : "posee"
    users ||--o| warbands        : "tiene"
    users ||--o{ user_items      : "inventario"
    users ||--o{ user_missions   : "completa"
    users ||--o{ battle_sessions : "juega"

    %% --- Relaciones de Héroe ---
    heroes }o--||  hero_classes  : "pertenece a"
    heroes ||--o{  hero_items    : "equipa"
    heroes ||--o|  warband_heroes: "forma parte de"

    %% --- Clases comparten plantilla con Enemigos ---
    hero_classes ||--o{ enemies  : "define aspecto"

    %% --- Relaciones de Ítem ---
    items }o--||   item_types    : "categorizado por"
    items ||--o{   hero_items    : "equipado vía"
    items ||--o|   shop_items    : "vendido en tienda"
    items ||--o{   user_items    : "en inventario vía"

    %% --- Slot de equipo se valida por tipo ---
    item_types ||--o{ hero_items : "restringe slot"

    %% --- Warband ---
    warbands ||--o{ warband_heroes : "contiene"

    %% --- Misiones ---
    missions ||--o{ user_missions   : "completada vía"
    missions ||--o{ battle_sessions : "combatida en"
```

---

## Resumen de relaciones clave

| Tabla pivote / asociación | Entidades que une | Restricción |
|---|---|---|
| `heroes` | `users` ↔ `hero_classes` | Un héroe pertenece a un único usuario y una clase |
| `hero_items` | `heroes` ↔ `items` ↔ `item_types` | UNIQUE(hero_id, item_type_id) — un héroe solo puede equipar un ítem por slot |
| `user_items` | `users` ↔ `items` | UNIQUE(user_id, item_id) — inventario del usuario |
| `shop_items` | `items` (tienda global) | UNIQUE(item_id) — cada ítem aparece una sola vez en la tienda |
| `warbands` | `users` | 1-to-1 — cada usuario tiene exactamente una warband |
| `warband_heroes` | `warbands` ↔ `heroes` | UNIQUE(warband_id, slot) y UNIQUE(warband_id, hero_id) |
| `user_missions` | `users` ↔ `missions` | UNIQUE(user_id, mission_id) — registro de misiones completadas |
| `battle_sessions` | `users` ↔ `missions` | Estado serializado en JSON (turn_queue, heroes_state, enemies_state) |
| `enemies` | `hero_classes` | Los enemigos reusan la plantilla de clase para stats base |

## Notas de diseño

- **`missions`**: Las referencias a enemigos y recompensas de ítems se guardan como JSON (`enemy_ids`, `item_reward_ids`) en lugar de tablas pivote — facilita la composición flexible de misiones.
- **`battle_sessions`**: El estado de combate completo (cola de turnos, HP actual de cada participante) se serializa como JSON para permitir persistencia y reanudación de batallas.
- **`abilities`**: No tiene FK a `hero_classes`; el campo `class_name` actúa como identificador textual para asociar habilidades a clases.
- **`hero_classes` / `enemies`**: Los enemigos heredan la plantilla visual y de stats de `hero_classes`, permitiendo reusar assets y lógica entre jugadores y enemigos.

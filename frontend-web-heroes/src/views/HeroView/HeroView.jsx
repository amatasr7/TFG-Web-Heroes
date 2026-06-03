import React, { useState, useEffect } from "react";
import "./HeroView.css";

import HeroEquipment from "./components/HeroEquipment/HeroEquipment";
import UserInventory from "./components/UserInventory/UserInventory";
import HeroPortrait from "./components/HeroPortrait/HeroPortrait";
import HeroStats from "./components/HeroStats/HeroStats";
import ManagementOptions from "./components/ManagementOptions/ManagementOptions";
import HeroList from "./components/HeroList/HeroList";

const API = "http://localhost:8000/api";

export default function HeroView({ user, onUserUpdate }) {
  const [heroes, setHeroes] = useState([]);
  const [selectedHeroId, setSelectedHeroId] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userItems, setUserItems] = useState([]);

  useEffect(() => {
    if (!user) {
      setHeroes([]);
      setIsLoading(false);
      return;
    }

    const fetchHeroes = async () => {
      try {
        const response = await fetch(`${API}/heroes?user_id=${user.id}`);
        if (!response.ok) {
          throw new Error(`Error en el servidor: Código de estado ${response.status}`);
        }
        const data = await response.json();
        setHeroes(data);
        if (data.length > 0) {
          setSelectedHeroId(data[0].id);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    const fetchUserInventory = async () => {
      try {
        const res = await fetch(`${API}/shop/inventory?user_id=${user.id}`);
        if (res.ok) {
          const data = await res.json();
          setUserItems(data.user_items || []);
          onUserUpdate((prev) => ({ ...prev, gold: data.user.gold }));
        }
      } catch {
        // silently ignore
      }
    };

    fetchHeroes();
    fetchUserInventory();
  }, [user?.id]);

  const handleEquip = async (entry, typeSlug) => {
    const hero = heroes.find((h) => h.id === selectedHeroId);
    if (!hero) return;

    const existing = (hero.hero_items ?? []).find(
      (hi) => hi.item.type.slug === typeSlug
    );

    if (existing) {
      await fetch(`${API}/hero-items/${existing.id}`, { method: "DELETE" });
    }

    const res = await fetch(`${API}/hero-items`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        hero_id: selectedHeroId,
        item_id: entry.item_id,
        item_type_id: entry.item.type.id,
      }),
    });

    if (res.ok) {
      const newHeroItem = await res.json();
      setHeroes((prev) =>
        prev.map((h) => {
          if (h.id !== selectedHeroId) return h;
          const filtered = (h.hero_items ?? []).filter(
            (hi) => hi.item.type.slug !== typeSlug
          );
          return { ...h, hero_items: [...filtered, newHeroItem] };
        })
      );
    }
  };

  const handleUnequip = async (heroItemId, typeSlug) => {
    const res = await fetch(`${API}/hero-items/${heroItemId}`, {
      method: "DELETE",
    });
    if (res.ok) {
      setHeroes((prev) =>
        prev.map((h) => {
          if (h.id !== selectedHeroId) return h;
          return {
            ...h,
            hero_items: (h.hero_items ?? []).filter((hi) => hi.id !== heroItemId),
          };
        })
      );
    }
  };

  const heroeSeleccionado = heroes.find((h) => h.id === selectedHeroId) || heroes[0];

  return (
    <div className="heroe-wrapper">
      <div className="heroe-container">

        {isLoading && (
          <div className="heroe-aviso-estado">
            <h3 className="font-amarillo">Invocando héroes desde la base de datos...</h3>
          </div>
        )}

        {error && (
          <div className="heroe-aviso-estado heroe-error-contenedor">
            <h3 style={{ color: "#ff4a4a" }}>No se pudo conectar con la base de datos:</h3>
            <p style={{ color: "#eee", marginTop: "5px" }}>{error}</p>
          </div>
        )}

        {!isLoading && !error && heroes.length === 0 && (
          <div className="heroe-aviso-estado">
            <h3>No se encontraron héroes en tu cuenta. ¡Crea uno nuevo!</h3>
          </div>
        )}

        {!isLoading && !error && heroes.length > 0 && (
          <div className="heroe-layout-tres-columnas">

            {/* ================= COLUMNA IZQUIERDA ================= */}
            <div className="heroe-columna">
              <HeroEquipment
                heroItems={heroeSeleccionado.hero_items ?? []}
                onEquip={handleEquip}
                onUnequip={handleUnequip}
              />
              <UserInventory items={userItems} />
            </div>

            {/* ================= COLUMNA CENTRAL ================= */}
            <div className="heroe-columna">
              <HeroPortrait heroe={heroeSeleccionado} />
              <HeroStats
                heroe={heroeSeleccionado}
                heroItems={heroeSeleccionado.hero_items ?? []}
              />
            </div>

            {/* ================= COLUMNA DERECHA ================= */}
            <div className="heroe-columna">
              <ManagementOptions />
              <HeroList
                heroes={heroes}
                selectedHeroId={selectedHeroId}
                onSelectHero={setSelectedHeroId}
              />
            </div>

          </div>
        )}
      </div>
    </div>
  );
}

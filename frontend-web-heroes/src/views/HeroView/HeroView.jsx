import React, { useState, useEffect } from "react";
import "./HeroView.css";

// Importamos los subcomponentes modulares
import HeroEquipment from "./components/HeroEquipment/HeroEquipment";
import UserInventory from "./components/UserInventory/UserInventory";
import HeroPortrait from "./components/HeroPortrait/HeroPortrait";
import HeroStats from "./components/HeroStats/HeroStats";
import ManagementOptions from "./components/ManagementOptions/ManagementOptions";
import HeroList from "./components/HeroList/HeroList";

export default function HeroView({ user }) {
  const [heroes, setHeroes] = useState([]);
  const [selectedHeroId, setSelectedHeroId] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!user) {
      setHeroes([]);
      setIsLoading(false);
      return;
    }

    const fetchHeroes = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/heroes?user_id=${user.id}`);
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

    fetchHeroes();
  }, [user]);

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
            <h3 style={{ color: "#ff4a4a" }}> No se pudo conectar con la base de datos:</h3>
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
              <HeroEquipment equipo={heroeSeleccionado.equipo} />
              <UserInventory />
            </div>

            {/* ================= COLUMNA CENTRAL ================= */}
            <div className="heroe-columna">
              <HeroPortrait heroe={heroeSeleccionado} />
              <HeroStats heroe={heroeSeleccionado} />
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
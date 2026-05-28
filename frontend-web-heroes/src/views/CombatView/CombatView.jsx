import React, { useState } from "react";
import "./CombatView.css";
import BattleScreen from "./components/BattleScreen/BattleScreen";

export default function CombatView() {
  // Estado para guardar la misión que el jugador acepta
  const [activeMission, setActiveMission] = useState(null);

  // Lista de misiones de prueba (puedes ampliarla o modificarla a tu gusto)
  const misionesDisponibles = [
    {
      id: 1,
      titulo: "Plaga en el Sótano",
      dificultad: "Fácil",
      enemigo: "Rata Gigante",
      recompensa: 50,
    },
    {
      id: 2,
      titulo: "Emboscada en el Camino",
      dificultad: "Media",
      enemigo: "Goblino Asaltante",
      recompensa: 120,
    },
    {
      id: 3,
      titulo: "El Despertar del Dragón",
      dificultad: "Difícil",
      enemigo: "Cría de Dragón",
      recompensa: 450,
    },
  ];

  // SI EL USUARIO HA ACEPTADO UNA MISIÓN:
  // Renderizamos la pantalla de combate real pasándole la misión actual y una función para volver.
  if (activeMission) {
    return (
      <BattleScreen
        mission={activeMission}
        onLeave={() => setActiveMission(null)}
      />
    );
  }

  // SI NO HAY MISIÓN SELECCIONADA:
  // Renderizamos el Tablón de Anuncios medieval/retro
  return (
    <div className="tablon-wrapper">
      <div className="tablon-container">
        <h2 className="tablon-titulo">📜 TABLÓN DE ANUNCIOS DEL GREMIO 📜</h2>
        <p className="tablon-subtitulo">
          Elige un contrato firmado con sangre para iniciar la batalla
        </p>

        <div className="tablon-cuadricula">
          {misionesDisponibles.map((mision) => (
            <div key={mision.id} className="mision-card">
              <h3 className="mision-card-titulo">{mision.titulo}</h3>

              <div className="mision-detalles">
                <p>
                  ⚠️ Enemigo:{" "}
                  <span className="mision-val">{mision.enemigo}</span>
                </p>
                <p>
                  ⚡ Dificultad:{" "}
                  <span
                    className={`mision-diff diff-${mision.dificultad.toLowerCase()}`}
                  >
                    {mision.dificultad}
                  </span>
                </p>
                <p>
                  💰 Recompensa:{" "}
                  <span className="mision-oro">{mision.recompensa} oro</span>
                </p>
              </div>

              <button
                className="tablon-btn"
                onClick={() => setActiveMission(mision)}
              >
                Aceptar Contrato
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

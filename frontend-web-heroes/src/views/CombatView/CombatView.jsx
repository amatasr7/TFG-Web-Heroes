import React, { useState } from "react";
import "./CombatView.css";
import BattleScreen from "./components/BattleScreen/BattleScreen";
// Importamos el sprite del encargado del gremio (ajusta la ruta y el archivo a tu gusto)
import spriteContratista from "../../assets/sprites/Icons_14.png";

export default function CombatView() {
  const [activeMission, setActiveMission] = useState(null);

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

  if (activeMission) {
    return (
      <BattleScreen
        mission={activeMission}
        onLeave={() => setActiveMission(null)}
      />
    );
  }

  return (
    <div className="tablon-wrapper">
      <div className="tablon-container">
        {/* FILA SUPERIOR: CONTRATISTA Y TABLÓN */}
        <div className="tablon-fila-superior">
          {/* PANEL IZQUIERDO: RETRATO DEL ENCARGADO */}
          <div className="tablon-panel-contratista">
            <div className="tablon-marco-retrato">
              <img
                src={spriteContratista}
                alt="Contratista del Gremio"
                className="tablon-retrato-img"
              />
            </div>
          </div>

          {/* PANEL DERECHO: EL TABLÓN DE MADERA CON PERGAMINOS */}
          <div className="tablon-panel-misiones">
            <h2 className="tablon-titulo">
              Recompensas ofrecidas por El Gremio
            </h2>
            <div className="tablon-cuadricula">
              {misionesDisponibles.map((mision) => (
                <div key={mision.id} className="mision-card">
                  <h3 className="mision-card-titulo">{mision.titulo}</h3>

                  <div className="mision-detalles">
                    <p>
                      Enemigo:{" "}
                      <span className="mision-val">{mision.enemigo}</span>
                    </p>
                    <p>
                      Dificultad:{" "}
                      <span
                        className={`mision-diff diff-${mision.dificultad.toLowerCase()}`}
                      >
                        {mision.dificultad}
                      </span>
                    </p>
                    <p>
                      Recompensa:{" "}
                      <span className="mision-oro">
                        {mision.recompensa} oro
                      </span>
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

        {/* FILA INFERIOR: TEXTO DE DIÁLOGO Y PANEL DE CONTROL SIMÉTRICO */}
        <div className="tablon-fila-inferior">
          {/* DIÁLOGO DEL CONTRATISTA */}
          <div className="tablon-panel-texto">
            <p className="tablon-texto-titulo">Contratista del Gremio</p>
            <p className="tablon-texto-sub">
              ¿Te atreves con alguna recompensa, viajero?
            </p>
          </div>

          {/* PANEL DERECHO INFERIOR (Simétrico al de la tienda, libre para medallas o stats) */}
          <div className="tablon-panel-controles">
            <div className="tablon-bloque-decorativo">
              <span className="tablon-decorativo-etiqueta">
                Rango del Gremio
              </span>
              <span className="tablon-decorativo-valor">FAMA: 0 ★</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

import React, { useState } from "react";
import "./CombatView.css";
import BattleScreen from "./components/BattleScreen/BattleScreen";
// Importamos el sprite del encargado del gremio (ajusta la ruta y el archivo a tu gusto)
import spriteContratista from "../../assets/sprites/Icons_14.png";

export default function CombatView() {
  const [activeMission, setActiveMission] = useState(null);
  const [viewingDetails, setViewingDetails] = useState(null);

  const misionesDisponibles = [
    {
      id: 1,
      titulo: "Plaga en el Sótano",
      dificultad: "Fácil",
      enemigo: "Rata Gigante",
      recompensa: 50,
      descripcion:
        "El tabernero del 'Pony Pisador' se queja de ruidos extraños bajo los barriles de cerveza. Resulta que una rata de tamaño descomunal se ha asentado allí y está devorando los suministros de queso. ¡Sácala antes de que se beba todo el hidromiel!",
    },
    {
      id: 2,
      titulo: "Emboscada en el Camino",
      dificultad: "Media",
      enemigo: "Goblino Asaltante",
      recompensa: 120,
      descripcion:
        "Varios comerciantes reportan que un pequeño grupo de goblins maliciosos ha montado una barricada en el camino del este. Asaltan a los carromatos usando flechas rudimentarias. Despeja la ruta comercial para restaurar el orden.",
    },
    {
      id: 3,
      titulo: "El Despertar del Dragón",
      dificultad: "Difícil",
      enemigo: "Cría de Dragón",
      recompensa: 450,
      descripcion:
        "En las profundidades de las cavernas de azufre, un huevo ancestral ha eclosionado. Aunque es solo una cría, su aliento de fuego ya ha calcinado dos granjas cercanas. Es extremadamente peligrosa. Ve con tu mejor equipo.",
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
                    Aceptar contrato
                  </button>
                  <br></br>
                  <button
                    className="tablon-btn btn-detalles"
                    onClick={() => setViewingDetails(mision)}
                  >
                    Ver detalles
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
              <span className="tablon-decorativo-etiqueta">Fama: 0</span>
              <span className="tablon-decorativo-valor">
                Rango del Gremio: 0 ★
              </span>
            </div>
          </div>
        </div>
      </div>
      {viewingDetails && (
        <div
          className="tablon-modal-overlay"
          onClick={() => setViewingDetails(null)}
        >
          <div
            className="tablon-modal-content"
            onClick={(e) => e.stopPropagation()}
          >
            <h3 className="tablon-modal-titulo">{viewingDetails.titulo}</h3>

            <div className="tablon-modal-info">
              <p>
                Objetivo:{" "}
                <span className="mision-val">{viewingDetails.enemigo}</span>
              </p>
              <p>
                Dificultad:{" "}
                <span
                  className={`mision-diff diff-${viewingDetails.dificultad.toLowerCase()}`}
                >
                  {viewingDetails.dificultad}
                </span>
              </p>
              <p>
                Recompensa:{" "}
                <span className="mision-oro">
                  {viewingDetails.recompensa} oro
                </span>
              </p>
              <p className="tablon-modal-descripcion">
                {viewingDetails.descripcion}
              </p>
            </div>

            <div className="tablon-modal-botones">
              <button
                className="tablon-btn btn-aceptar"
                onClick={() => {
                  setActiveMission(viewingDetails);
                  setViewingDetails(null);
                }}
              >
                Iniciar Combate
              </button>
              <button
                className="tablon-btn btn-cerrar"
                onClick={() => setViewingDetails(null)}
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

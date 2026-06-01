import React, { useEffect, useState } from "react";
import "./MissionView.css";
import BattleView from "../BattleView/BattleView";
import spriteContratista from "/sprites/Contratista.png";

const PAGE_SIZE = 4;

function mapMissionFromApi(mission) {
  const dificultad = mission.xp_reward < 150 ? "Fácil" : mission.xp_reward < 300 ? "Media" : "Difícil";
  const enemigo = mission.enemy_ids.length
    ? mission.enemy_ids.length === 1
      ? `Enemigo ${mission.enemy_ids[0]}`
      : `${mission.enemy_ids.length} enemigos`
    : "Sin enemigos";

  return {
    id: mission.id,
    titulo: mission.name,
    descripcion: mission.description,
    recompensa: mission.gold_reward,
    enemigo,
    dificultad,
    enemy_ids: mission.enemy_ids,
    xp_reward: mission.xp_reward,
    gold_reward: mission.gold_reward,
  };
}

export default function MissionView() {
  const [activeMission, setActiveMission] = useState(null);
  const [viewingDetails, setViewingDetails] = useState(null);
  const [missions, setMissions] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMissions = async () => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await fetch(
          `http://localhost:8000/api/missions?page=${page}&page_size=${PAGE_SIZE}`
        );

        if (!response.ok) {
          throw new Error(`Error en el servidor: Código ${response.status}`);
        }

        const data = await response.json();
        setMissions(data.missions.map(mapMissionFromApi));
        setTotalPages(Math.max(1, Math.ceil(data.total / PAGE_SIZE)));
      } catch (err) {
        setError(err.message);
        setMissions([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchMissions();
  }, [page]);

  const misionesDisponibles = missions;

  if (activeMission) {
    return (
      <BattleView
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
            {isLoading && (
              <div className="tablon-cargando">
                <p>Cargando misiones desde la base de datos...</p>
              </div>
            )}
            {error && (
              <div className="tablon-error">
                <p>Error cargando misiones:</p>
                <p>{error}</p>
              </div>
            )}
            {!isLoading && !error && misionesDisponibles.length === 0 && (
              <div className="tablon-aviso">
                <p>No hay misiones disponibles en este momento.</p>
              </div>
            )}
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
            <div className="pagination-controls">
              <button
                className="tablon-btn page-button"
                onClick={() => setPage((current) => Math.max(current - 1, 1))}
                disabled={page <= 1}
              >
                Anterior
              </button>
              <span className="page-info">Página {page} de {totalPages}</span>
              <button
                className="tablon-btn page-button"
                onClick={() => setPage((current) => Math.min(current + 1, totalPages))}
                disabled={page >= totalPages}
              >
                Siguiente
              </button>
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

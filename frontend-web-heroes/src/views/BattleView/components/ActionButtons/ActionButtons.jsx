import "./ActionButtons.css";

export default function ActionButtons({
  onAction,
  isPlayerTurn = false,
  hasSelectedEnemy = false,
  currentHero = null,
}) {
  const canAct = isPlayerTurn;
  const mp = currentHero?.mp_current ?? 0;

  return (
    <div className="action-buttons">
      <button
        className={`action-btn attack-btn${!canAct ? " disabled" : ""}${canAct && !hasSelectedEnemy ? " needs-target" : ""}`}
        onClick={() => canAct && onAction("attack")}
        disabled={!canAct}
        title={
          !canAct
            ? "No es tu turno"
            : !hasSelectedEnemy
              ? "Haz clic en un enemigo primero"
              : "Atacar"
        }
      >
        <span className="btn-icon"></span>
        <span className="btn-label">Atacar</span>
        {canAct && !hasSelectedEnemy && (
          <span className="btn-hint">↑ Elige objetivo</span>
        )}
      </button>

      <button
        className={`action-btn defend-btn${!canAct ? " disabled" : ""}`}
        onClick={() => canAct && onAction("defend")}
        disabled={!canAct}
        title={
          !canAct
            ? "No es tu turno"
            : "Adoptar postura defensiva (reduce daño 50%)"
        }
      >
        <span className="btn-icon"></span>
        <span className="btn-label">Defender</span>
      </button>

      <button
        className={`action-btn abilities-btn${!canAct ? " disabled" : ""}`}
        onClick={() => canAct && onAction("abilities")}
        disabled={!canAct}
        title={!canAct ? "No es tu turno" : `Usar habilidades (MP: ${mp})`}
      >
        <span className="btn-icon"></span>
        <span className="btn-label">Habilidades</span>
        {canAct && <span className="btn-mp">{mp} MP</span>}
      </button>

      <button
        className={`action-btn items-btn${!canAct ? " disabled" : ""}`}
        onClick={() => canAct && onAction("items")}
        disabled={!canAct}
        title={!canAct ? "No es tu turno" : "Usar un objeto"}
      >
        <span className="btn-icon"></span>
        <span className="btn-label">Usar objeto</span>
      </button>
    </div>
  );
}

import "./CombatLog.css";

export default function CombatLog({ logs }) {
  return (
    <div className="combat-log">
      <h3>Log de actividad del combate:</h3>
      <div className="log-content">
        {logs.map((log, index) => (
          <p key={index} className="log-entry">
            {log.timestamp} {log.message}
          </p>
        ))}
      </div>
    </div>
  );
}

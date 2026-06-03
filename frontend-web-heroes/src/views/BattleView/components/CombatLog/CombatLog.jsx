import { useEffect, useRef } from "react";
import "./CombatLog.css";

export default function CombatLog({ logs = [] }) {
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  return (
    <div className="combat-log">
      <h3>Registro de Combate</h3>
      <div className="log-content">
        {logs.map((log, i) => (
          <p key={i} className="log-entry">
            <span className="log-time">[{log.timestamp}]</span> {log.message}
          </p>
        ))}
        <div ref={endRef} />
      </div>
    </div>
  );
}

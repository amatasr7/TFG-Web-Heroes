import React, { useState, useEffect } from "react";
import { API } from "../../../../utils/api";

const STAT_OPTIONS = [
  { key: "hp",      label: "Salud Máx. +2",  desc: "Aumenta tu vida máxima" },
  { key: "mp",      label: "Maná Máx. +2",   desc: "Aumenta tu maná máximo" },
  { key: "attack",  label: "Ataque +1",       desc: "Más daño en combate" },
  { key: "defense", label: "Defensa +1",      desc: "Más resistencia al daño" },
];

const CLASS_ACTIONS = {
  guerrero: { label: "Entrenar",  desc: "Defensa permanente +1",   action: "train",    icon: "⚔", cooldownMin: 60 },
  mago:     { label: "Meditar",   desc: "Recupera todo el maná",   action: "meditate", icon: "✦", cooldownMin: 30 },
  "pícaro": { label: "Robar",     desc: "Consigue 5–15 de oro",    action: "steal",    icon: "⚡", cooldownMin: 30 },
  picaro:   { label: "Robar",     desc: "Consigue 5–15 de oro",    action: "steal",    icon: "⚡", cooldownMin: 30 },
};

function formatRemaining(minutes) {
  if (minutes >= 60) return `${Math.floor(minutes / 60)}h ${minutes % 60}min`;
  return `${minutes} min`;
}

function getCooldownRemaining(lastActionAt, cooldownMin) {
  if (!lastActionAt || !cooldownMin) return 0;
  const lastMs = new Date(lastActionAt + "Z").getTime();
  const elapsedMin = (Date.now() - lastMs) / 60000;
  return Math.max(0, Math.ceil(cooldownMin - elapsedMin));
}

export default function ManagementOptions({ hero, user, onHeroUpdate, onGoldUpdate }) {
  const [showLevelModal, setShowLevelModal] = useState(false);
  const [message, setMessage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [, tick] = useState(0);

  // Refresh countdown every 30 seconds
  useEffect(() => {
    const id = setInterval(() => tick((n) => n + 1), 30_000);
    return () => clearInterval(id);
  }, []);

  if (!hero) return null;

  const canLevelUp = hero.experience >= 100;
  const energyFull = hero.energy_current >= 10;
  const className = (hero.hero_class?.name ?? "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  const classAction = CLASS_ACTIONS[hero.hero_class?.name?.toLowerCase()] ?? CLASS_ACTIONS[className] ?? null;

  const cooldownRemaining = classAction
    ? getCooldownRemaining(hero.last_action_at, classAction.cooldownMin)
    : 0;
  const actionOnCooldown = cooldownRemaining > 0;

  const flash = (text, isError = false) => {
    setMessage({ text, isError });
    setTimeout(() => setMessage(null), 3500);
  };

  const handleRest = async () => {
    setIsLoading(true);
    try {
      const res = await fetch(`${API}/heroes/${hero.id}/rest`, { method: "POST" });
      if (!res.ok) throw new Error("Error al descansar.");
      onHeroUpdate(await res.json());
      flash(`${hero.name} descansa y recupera toda su energía.`);
    } catch (e) {
      flash(e.message, true);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLevelUp = async (stat) => {
    setIsLoading(true);
    try {
      const res = await fetch(`${API}/heroes/${hero.id}/level-up`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ stat }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail ?? "Error al subir de nivel.");
      }
      const updated = await res.json();
      onHeroUpdate(updated);
      const label = STAT_OPTIONS.find((s) => s.key === stat)?.label ?? stat;
      flash(`¡${hero.name} sube al nivel ${updated.level}! ${label}`);
      setShowLevelModal(false);
    } catch (e) {
      flash(e.message, true);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClassAction = async () => {
    if (!classAction || actionOnCooldown) return;
    setIsLoading(true);
    try {
      const body = { action: classAction.action };
      if (classAction.action === "steal") body.user_id = user?.id;
      const res = await fetch(`${API}/heroes/${hero.id}/action`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail ?? "Error en la acción.");
      }
      const data = await res.json();
      onHeroUpdate(data.hero);
      if (data.gold_gained != null && onGoldUpdate) onGoldUpdate(data.new_gold);
      flash(data.message);
    } catch (e) {
      flash(e.message, true);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <div className="heroe-bloque heroe-bloque-superior">
        <h3 className="heroe-bloque-titulo">Opciones de Gestión</h3>
        <div className="heroe-menu-opciones">

          <button
            className="heroe-btn-accion"
            onClick={handleRest}
            disabled={isLoading || energyFull}
            title={energyFull ? "El héroe ya está descansado" : "Restaurar energía al máximo"}
          >
            💤 Descansar
            <span className="heroe-btn-sub">Energía: {hero.energy_current}/10</span>
          </button>

          <button
            className={`heroe-btn-accion btn-subir${canLevelUp ? " btn-ready" : ""}`}
            onClick={() => canLevelUp && setShowLevelModal(true)}
            disabled={isLoading || !canLevelUp}
            title={canLevelUp ? "¡Listo para subir de nivel!" : `XP: ${hero.experience}/100`}
          >
            ⬆ Subir de Nivel
            <span className="heroe-btn-sub">XP: {hero.experience}/100</span>
          </button>

          {classAction && (
            <button
              className={`heroe-btn-accion btn-clase${actionOnCooldown ? " btn-cooldown" : ""}`}
              onClick={handleClassAction}
              disabled={isLoading || actionOnCooldown}
              title={
                actionOnCooldown
                  ? `En recarga — disponible en ${formatRemaining(cooldownRemaining)}`
                  : classAction.desc
              }
            >
              {actionOnCooldown ? "⏳" : classAction.icon} {classAction.label}
              <span className="heroe-btn-sub">
                {actionOnCooldown
                  ? `Disponible en ${formatRemaining(cooldownRemaining)}`
                  : classAction.desc}
              </span>
            </button>
          )}
        </div>

        {message && (
          <p className={`heroe-accion-msg${message.isError ? " heroe-accion-msg-error" : ""}`}>
            {message.text}
          </p>
        )}
      </div>

      {showLevelModal && (
        <div className="modal-overlay heroe-modal-overlay" onClick={() => setShowLevelModal(false)}>
          <div className="heroe-modal" onClick={(e) => e.stopPropagation()}>
            <h3 className="heroe-modal-titulo">¡Nivel {hero.level + 1}!</h3>
            <p className="heroe-modal-sub">Elige qué estadística mejorar:</p>
            <div className="heroe-modal-stats">
              {STAT_OPTIONS.map((opt) => (
                <button
                  key={opt.key}
                  className="heroe-modal-stat-btn"
                  onClick={() => handleLevelUp(opt.key)}
                  disabled={isLoading}
                >
                  <span className="heroe-modal-stat-label">{opt.label}</span>
                  <span className="heroe-modal-stat-desc">{opt.desc}</span>
                </button>
              ))}
            </div>
            <button className="heroe-btn-accion" style={{ marginTop: 8 }} onClick={() => setShowLevelModal(false)}>
              Cancelar
            </button>
          </div>
        </div>
      )}
    </>
  );
}

import React from "react";

export default function HeroList({
  heroes,
  selectedHeroId,
  onSelectHero,
  warbandHeroIds,
  onToggleWarband,
  isSavingWarband,
  onSaveWarband,
}) {
  const WARBAND_MAX = 3;
  const warbandCount = warbandHeroIds.length;

  return (
    <div className="heroe-bloque heroe-bloque-inferior" style={{ height: "auto", minHeight: "340px" }}>

      {/* ── Cabecera warband ── */}
      <div className="warband-cabecera">
        <h3 className="heroe-bloque-titulo" style={{ margin: 0, border: "none", padding: 0 }}>
          Personajes disponibles:
        </h3>
        <div className="warband-status">
          <span className={`warband-contador ${warbandCount === WARBAND_MAX ? "warband-completo" : ""}`}>
            Banda: {warbandCount}/{WARBAND_MAX}
          </span>
          <button
            className={`heroe-btn-accion warband-guardar-btn ${warbandCount === WARBAND_MAX ? "btn-ready" : ""}`}
            onClick={onSaveWarband}
            disabled={warbandCount !== WARBAND_MAX || isSavingWarband}
          >
            {isSavingWarband ? "Guardando..." : "Guardar banda"}
          </button>
        </div>
      </div>

      {/* ── Hint ── */}
      <p className="warband-hint">
        Selecciona 3 héroes para tu banda de guerra
      </p>

      {/* ── Lista de héroes ── */}
      <div className="heroe-lista-scroll" style={{ marginTop: 8 }}>
        {heroes.map((heroe) => {
          const slotIndex = warbandHeroIds.indexOf(heroe.id);
          const enWarband = slotIndex !== -1;
          const warbandLlena = warbandCount >= WARBAND_MAX && !enWarband;

          return (
            <div
              key={heroe.id}
              className={`heroe-item-seleccion ${selectedHeroId === heroe.id ? "heroe-item-activo" : ""}`}
              onClick={() => onSelectHero(heroe.id)}
            >
              <div className="heroe-item-info">
                <span className="heroe-item-nombre">{heroe.name}</span>
                <span className="heroe-item-clase">{heroe.hero_class?.name || "Sin Clase"}</span>
              </div>

              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span className="heroe-item-lvl">LVL {heroe.level}</span>

                <button
                  className={`warband-slot-btn ${enWarband ? `warband-slot-activo warband-slot-${slotIndex + 1}` : "warband-slot-libre"}`}
                  onClick={(e) => {
                    e.stopPropagation();
                    onToggleWarband(heroe.id);
                  }}
                  disabled={warbandLlena}
                  title={
                    enWarband
                      ? `Slot ${slotIndex + 1} — quitar de la banda`
                      : warbandLlena
                      ? "La banda ya está completa"
                      : "Añadir a la banda"
                  }
                >
                  {enWarband ? `${slotIndex + 1}` : "+"}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

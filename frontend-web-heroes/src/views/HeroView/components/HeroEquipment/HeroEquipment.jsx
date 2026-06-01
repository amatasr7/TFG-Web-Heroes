import React from "react";

export default function HeroEquipment({ equipo }) {
  return (
    <div className="heroe-bloque heroe-bloque-superior">
      <h3 className="heroe-bloque-titulo">Objetos equipados:</h3>
      <div className="heroe-cuadricula-equipo">
        <div className="heroe-slot-equipo">
          <span className="heroe-slot-etiqueta">Armadura:</span>
          <span className="heroe-slot-item">{equipo?.pecho || "Vacío"}</span>
        </div>
        <div className="heroe-slot-equipo">
          <span className="heroe-slot-etiqueta">Arma:</span>
          <span className="heroe-slot-item">{equipo?.mano || "Vacío"}</span>
        </div>
        <div className="heroe-slot-equipo">
          <span className="heroe-slot-etiqueta">Consumible:</span>
          <span className="heroe-slot-item">{equipo?.pies || "Vacío"}</span>
        </div>
      </div>
    </div>
  );
}
import React from "react";

export default function UserInventory() {
  const slotsInventario = Array.from({ length: 12 });

  return (
    <div className="heroe-bloque heroe-bloque-inferior">
      <h3 className="heroe-bloque-titulo">Inventario del usuario:</h3>
      <div className="heroe-inventario-cuadricula">
        {slotsInventario.map((_, i) => (
          <div key={`inv-slot-${i}`} className="heroe-slot-vacio"></div>
        ))}
      </div>
    </div>
  );
}
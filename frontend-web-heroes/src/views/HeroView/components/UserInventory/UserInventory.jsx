import React, { useState } from "react";
import ItemIcon from "../../../../components/ItemIcon";

const SLOTS = 12;
const EQUIPABLE_SLUGS = ["weapon", "armor"];

export default function UserInventory({ items = [] }) {
  const [selected, setSelected] = useState(null);
  const slots = Array.from({ length: SLOTS }, (_, i) => items[i] ?? null);

  const handleClick = (entry) => {
    if (!entry) return;
    setSelected((prev) => (prev?.item_id === entry.item_id ? null : entry));
  };

  return (
    <div className="heroe-bloque heroe-bloque-inferior">
      <h3 className="heroe-bloque-titulo">Inventario del usuario:</h3>
      <div className="heroe-inventario-cuadricula">
        {slots.map((entry, i) => {
          const isDraggable =
            !!entry && EQUIPABLE_SLUGS.includes(entry.item?.type?.slug);
          const isSelected = selected?.item_id === entry?.item_id;

          return (
            <div
              key={`inv-slot-${i}`}
              className={[
                "heroe-slot-vacio",
                entry ? "heroe-slot-ocupado" : "",
                isDraggable ? "heroe-inventario-draggable" : "",
                isSelected ? "heroe-inventario-seleccionado" : "",
              ]
                .filter(Boolean)
                .join(" ")}
              draggable={isDraggable}
              onDragStart={(e) => {
                if (entry) {
                  e.dataTransfer.setData("text/plain", JSON.stringify(entry));
                }
              }}
              onClick={() => handleClick(entry)}
              title={
                entry
                  ? `${entry.item.name}${entry.quantity > 1 ? ` x${entry.quantity}` : ""}${isDraggable ? " — arrastra para equipar" : ""}`
                  : ""
              }
            >
              {entry && <ItemIcon item={entry.item} />}
              {entry && entry.quantity > 1 && (
                <span className="heroe-slot-cantidad">{entry.quantity}</span>
              )}
            </div>
          );
        })}
      </div>
      {selected && (
        <div className="heroe-inventario-info">
          <span className="heroe-inventario-info-nombre">{selected.item.name}</span>
          {selected.item.damage_bonus > 0 && (
            <span className="heroe-inventario-info-stat font-amarillo">
              +{selected.item.damage_bonus} ATK
            </span>
          )}
          {selected.item.hp_bonus > 0 && selected.item.type?.slug === "armor" && (
            <span className="heroe-inventario-info-stat font-verde">
              +{selected.item.hp_bonus} DEF
            </span>
          )}
          {EQUIPABLE_SLUGS.includes(selected.item.type?.slug) && (
            <span className="heroe-inventario-info-hint">Arrastra al slot de equipo</span>
          )}
        </div>
      )}
    </div>
  );
}

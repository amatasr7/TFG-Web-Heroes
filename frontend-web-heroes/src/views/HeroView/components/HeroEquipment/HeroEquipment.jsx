import React, { useState } from "react";
import ItemIcon from "../../../BattleView/components/ItemIcon";

export default function HeroEquipment({ heroItems, onEquip, onUnequip }) {
  const [dragOver, setDragOver] = useState(null);

  const equippedWeapon = heroItems.find((hi) => hi.item.type.slug === "weapon");
  const equippedArmor = heroItems.find((hi) => hi.item.type.slug === "armor");

  const handleDragOver = (e, typeSlug) => {
    e.preventDefault();
    setDragOver(typeSlug);
  };

  const handleDragLeave = () => setDragOver(null);

  const handleDrop = (e, typeSlug) => {
    e.preventDefault();
    setDragOver(null);
    try {
      const entry = JSON.parse(e.dataTransfer.getData("text/plain"));
      if (entry?.item?.type?.slug === typeSlug) {
        onEquip(entry, typeSlug);
      }
    } catch {}
  };

  const renderSlot = (label, typeSlug, equipped) => (
    <div className="heroe-slot-equipo">
      <span className="heroe-slot-etiqueta">{label}</span>
      <div
        className={[
          "heroe-equipo-drop-zone",
          equipped ? "heroe-equipo-ocupado" : "",
          dragOver === typeSlug ? "heroe-equipo-drag-over" : "",
        ]
          .filter(Boolean)
          .join(" ")}
        onDragOver={(e) => handleDragOver(e, typeSlug)}
        onDragLeave={handleDragLeave}
        onDrop={(e) => handleDrop(e, typeSlug)}
        onClick={() => equipped && onUnequip(equipped.id, typeSlug)}
        title={
          equipped
            ? `${equipped.item.name} — click para desequipar`
            : `Arrastra ${typeSlug === "weapon" ? "un arma" : "una armadura"} aquí`
        }
      >
        {equipped ? (
          <ItemIcon item={equipped.item} />
        ) : (
          <span className="heroe-equipo-placeholder">+</span>
        )}
      </div>
      {equipped && (
        <span className="heroe-equipo-nombre">{equipped.item.name}</span>
      )}
    </div>
  );

  return (
    <div className="heroe-bloque heroe-bloque-superior">
      <h3 className="heroe-bloque-titulo">Objetos equipados:</h3>
      <div className="heroe-cuadricula-equipo">
        {renderSlot("Arma", "weapon", equippedWeapon)}
        {renderSlot("Armadura", "armor", equippedArmor)}
      </div>
    </div>
  );
}

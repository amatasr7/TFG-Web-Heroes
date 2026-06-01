import React from "react";

export default function HeroList({ heroes, selectedHeroId, onSelectHero }) {
    return (
        <div className="heroe-bloque heroe-bloque-inferior">
        <h3 className="heroe-bloque-titulo">Personajes disponibles:</h3>
        <div className="heroe-lista-scroll">
            {heroes.map((heroe) => (
            <div
                key={heroe.id}
                className={`heroe-item-seleccion ${selectedHeroId === heroe.id ? "heroe-item-activo" : ""}`}
                onClick={() => onSelectHero(heroe.id)}
            >
                <div className="heroe-item-info">
                <span className="heroe-item-nombre">{heroe.name}</span>
                <span className="heroe-item-clase">{heroe.hero_class?.name || "Sin Clase"}</span>
                </div>
                <span className="heroe-item-lvl">LVL {heroe.level}</span>
            </div>
            ))}
        </div>
        </div>
    );
}
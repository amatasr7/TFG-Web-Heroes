import React from "react";

export default function ManagementOptions() {
    return (
        <div className="heroe-bloque heroe-bloque-superior">
        <h3 className="heroe-bloque-titulo">OPCIONES DE GESTIÓN</h3>
        <div className="heroe-menu-opciones">
            <button className="heroe-btn-accion btn-subir">Subir de Nivel</button>
            <button className="heroe-btn-accion">Cambiar Habilidades</button>
            <button className="heroe-btn-accion">Desequipar Todo</button>
        </div>
        </div>
    );
}
import React from "react";
import spriteHeroeDefault from "/sprites/Pelirrojo.png";

const EmblemaClaseFondo = ({ clase }) => {
  const claseNormalizada = clase.toLowerCase();

  // Guerrero -> Espada
  if (claseNormalizada.includes("guerrero")){
    return (
      <svg className="heroe-svg-emblema" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M50 10L54 32H46L50 10Z" fill="currentColor" />
        <path d="M48 32H52V72H48V32Z" fill="currentColor" />
        <path d="M38 72H62V76H38V72Z" fill="currentColor" />
        <path d="M47 76H53V84H47V76Z" fill="currentColor" />
      </svg>
    );
  }

  // Mago -> Bastón
  if (claseNormalizada.includes("mago")) {
    return (
      <svg className="heroe-svg-emblema" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M48 28H52V85H48V28Z" fill="currentColor" />
        <circle cx="50" cy="18" r="7" fill="currentColor" />
        <path d="M40 18C40 12.5 44.5 8 50 8" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
        <path d="M60 18C60 23.5 55.5 28 50 28" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
      </svg>
    );
  }

  // Pícaro -> Arco
  if (claseNormalizada.includes("pícaro")) {
    return (
      <svg className="heroe-svg-emblema" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M35 20C58 20 68 32 68 50C68 68 58 80 35 80" stroke="currentColor" strokeWidth="3.5" fill="none" strokeLinecap="round" />
        <line x1="35" y1="20" x2="35" y2="80" stroke="currentColor" strokeWidth="1" strokeDasharray="3,3" />
        <line x1="28" y1="50" x2="62" y2="50" stroke="currentColor" strokeWidth="2.5" />
        <path d="M65 50L56 45V55L65 50Z" fill="currentColor" />
      </svg>
    );
  }
};

export default function HeroPortrait({ heroe }) {
  const nombreClase = heroe?.hero_class?.name || "Desconocido";

  return (
    <div className="heroe-bloque heroe-bloque-superior heroe-centrado-retrato">
      <div className="heroe-marco-retrato" style={{ position: "relative" }}>
        
        <EmblemaClaseFondo clase={nombreClase} />
        
        <img 
          src={spriteHeroeDefault} 
          alt={heroe?.name || "Héroe"} 
          className="heroe-retrato-img" 
          style={{ position: "relative", zIndex: 2 }}
        />
        
      </div>
    </div>
  );
}
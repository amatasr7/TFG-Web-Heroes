import itemsSheet from "../../../assets/sprites/Inventory_Spritesheet.png";

const ItemIcon = ({ item }) => {
  const TAMAÑO_CASILLA = 32;

  // Calculamos la posición en píxeles basándonos en los índices de la BD
  // Multiplicamos por el tamaño y lo ponemos en negativo para desplazar la hoja
  const posX = -(item.sprite_x * TAMAÑO_CASILLA);
  const posY = -(item.sprite_y * TAMAÑO_CASILLA);

  const style = {
    width: `${TAMAÑO_CASILLA}px`,
    height: `${TAMAÑO_CASILLA}px`,
    backgroundImage: `url(${itemsSheet})`,
    backgroundPosition: `${posX}px ${posY}px`,
    backgroundRepeat: "no-repeat",
    imageRendering: "pixelated", // Hace que los píxeles se vean bien
    display: "inline-block",
  };

  return <div className="item-icon" style={style} title={item.name} />;
};

export default ItemIcon;

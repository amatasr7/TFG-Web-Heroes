import itemsSheet from "/sprites/Inventory_Spritesheet.png";

const TILE_SIZE = 32;

const ItemIcon = ({ item }) => {
  const posX = -(item.sprite_x * TILE_SIZE);
  const posY = -(item.sprite_y * TILE_SIZE);

  const style = {
    width: `${TILE_SIZE}px`,
    height: `${TILE_SIZE}px`,
    backgroundImage: `url(${itemsSheet})`,
    backgroundPosition: `${posX}px ${posY}px`,
    backgroundRepeat: "no-repeat",
    imageRendering: "pixelated",
    display: "inline-block",
  };

  return <div className="item-icon" style={style} title={item.name} />;
};

export default ItemIcon;

import React, { useState, useEffect } from "react";
import "./ShopView.css";
import { API } from "../../utils/api";
import spriteMercader from "/sprites/Mercader.png";
import ItemIcon from "../../components/ItemIcon";

const VENDOR_MESSAGES = {
  idle: "¡Bienvenido, viajero! ¿Qué deseas hoy?",
  noGold: "No tienes suficiente oro para eso...",
  noStock: "No me queda stock de ese ítem.",
};

export default function ShopView({ user, onUserUpdate }) {
  const [inventory, setInventory] = useState(null);
  const [gold, setGold] = useState(0);
  const [selected, setSelected] = useState(null); // { origin: 'shop'|'user', item_id, item }
  const [message, setMessage] = useState(VENDOR_MESSAGES.idle);
  const [loading, setLoading] = useState(false);

  const fetchInventory = async () => {
    try {
      const res = await fetch(`${API}/shop/inventory?user_id=${user.id}`);
      if (res.ok) {
        const data = await res.json();
        setInventory(data);
        setGold(data.user.gold);
        onUserUpdate((prev) => ({ ...prev, gold: data.user.gold }));
      }
    } catch {
      setMessage("Error al conectar con el servidor.");
    }
  };

  useEffect(() => {
    fetchInventory();
  }, [user.id]);

  const handleSelectShopItem = (shopItem) => {
    if (shopItem.quantity <= 0) return;
    setSelected({ origin: "shop", item_id: shopItem.item_id, item: shopItem.item });
    setMessage(`${shopItem.item.name} — Precio: ${shopItem.item.value} de oro`);
  };

  const handleSelectUserItem = (userItem) => {
    setSelected({ origin: "user", item_id: userItem.item_id, item: userItem.item });
    setMessage(`Vender ${userItem.item.name} por ${userItem.item.value} de oro`);
  };

  const handleBuy = async () => {
    if (!selected || selected.origin !== "shop" || loading) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/shop/buy`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: user.id, item_id: selected.item_id, quantity: 1 }),
      });
      const data = await res.json();
      if (res.ok) {
        setInventory(data);
        setGold(data.user.gold);
        onUserUpdate((prev) => ({ ...prev, gold: data.user.gold }));
        setSelected(null);
        setMessage(`¡Trato hecho! Compraste ${selected.item.name}.`);
      } else {
        setMessage(data.detail || "No se pudo completar la compra.");
      }
    } catch {
      setMessage("Error al conectar con el servidor.");
    }
    setLoading(false);
  };

  const handleSell = async () => {
    if (!selected || selected.origin !== "user" || loading) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/shop/sell`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: user.id, item_id: selected.item_id, quantity: 1 }),
      });
      const data = await res.json();
      if (res.ok) {
        setInventory(data);
        setGold(data.user.gold);
        onUserUpdate((prev) => ({ ...prev, gold: data.user.gold }));
        setSelected(null);
        setMessage(`¡Vendido! Recibiste ${selected.item.value} de oro.`);
      } else {
        setMessage(data.detail || "No se pudo completar la venta.");
      }
    } catch {
      setMessage("Error al conectar con el servidor.");
    }
    setLoading(false);
  };

  const SLOTS = 25;
  const shopSlots = Array.from({ length: SLOTS }, (_, i) => inventory?.shop_items[i] ?? null);
  const userSlots = Array.from({ length: SLOTS }, (_, i) => inventory?.user_items[i] ?? null);

  const canBuy = selected?.origin === "shop";
  const canSell = selected?.origin === "user";

  return (
    <div className="tienda-wrapper">
      <div className="tienda-container">
        {/* FILA SUPERIOR: PORTRAIT E INVENTARIOS */}
        <div className="tienda-fila-superior">
          {/* PANEL IZQUIERDO: FOTO VENDEDOR */}
          <div className="tienda-panel-vendedor">
            <div className="tienda-marco-retrato">
              <img src={spriteMercader} alt="Vendedor" className="tienda-retrato-img" />
            </div>
          </div>

          {/* PANEL DERECHO: INVENTARIOS */}
          <div className="tienda-panel-inventarios">
            {/* Inventario del Vendedor */}
            <div className="tienda-columna-inventario">
              <h3 className="tienda-inventario-titulo">Inventario Vendedor</h3>
              <div className="tienda-inventario-cuadricula">
                {shopSlots.map((shopItem, i) => {
                  const isSelected = canBuy && selected.item_id === shopItem?.item_id;
                  return (
                    <div
                      key={`vendedor-slot-${i}`}
                      className={`tienda-slot${shopItem ? " tienda-slot-ocupado" : ""}${isSelected ? " tienda-slot-seleccionado" : ""}`}
                      onClick={() => shopItem && handleSelectShopItem(shopItem)}
                      title={shopItem ? `${shopItem.item.name} (${shopItem.item.value} oro)` : ""}
                    >
                      {shopItem && (
                        <>
                          <ItemIcon item={shopItem.item} />
                          {shopItem.quantity > 1 && (
                            <span className="tienda-slot-cantidad">{shopItem.quantity}</span>
                          )}
                        </>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Línea divisoria central */}
            <div className="tienda-divisor-vertical" />

            {/* Mi Inventario */}
            <div className="tienda-columna-inventario">
              <h3 className="tienda-inventario-titulo">Mi Inventario</h3>
              <div className="tienda-inventario-cuadricula">
                {userSlots.map((userItem, i) => {
                  const isSelected = canSell && selected.item_id === userItem?.item_id;
                  return (
                    <div
                      key={`jugador-slot-${i}`}
                      className={`tienda-slot${userItem ? " tienda-slot-ocupado" : ""}${isSelected ? " tienda-slot-seleccionado" : ""}`}
                      onClick={() => userItem && handleSelectUserItem(userItem)}
                      title={userItem ? `${userItem.item.name} (vender: ${userItem.item.value} oro)` : ""}
                    >
                      {userItem && (
                        <>
                          <ItemIcon item={userItem.item} />
                          {userItem.quantity > 1 && (
                            <span className="tienda-slot-cantidad">{userItem.quantity}</span>
                          )}
                        </>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>

        {/* FILA INFERIOR: DIÁLOGO Y CONTROLES */}
        <div className="tienda-fila-inferior">
          {/* TEXTO VENDEDOR */}
          <div className="tienda-panel-texto">
            <p className="tienda-texto-titulo">Mercader</p>
            <p className="tienda-texto-sub">{message}</p>
          </div>

          {/* CONTROLES (DINERO Y BOTONES) */}
          <div className="tienda-panel-controles">
            {/* MI DINERO */}
            <div className="tienda-bloque-dinero">
              <span className="tienda-dinero-etiqueta">Mi Dinero</span>
              <div className="tienda-dinero-valor-contenedor">
                <span className="tienda-dinero-cantidad">{gold}</span>
                <ItemIcon item={{ sprite_x: 7, sprite_y: 0, name: "Moneda de oro" }} />
              </div>
            </div>

            {/* BOTONES DE TIENDA */}
            <div className="tienda-bloque-botones">
              <button
                className={`tienda-btn tienda-btn-comprar${!canBuy ? " tienda-btn-inactivo" : ""}`}
                onClick={handleBuy}
                disabled={loading || !canBuy}
              >
                Comprar
              </button>
              <button
                className={`tienda-btn tienda-btn-vender${!canSell ? " tienda-btn-inactivo" : ""}`}
                onClick={handleSell}
                disabled={loading || !canSell}
              >
                Vender
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

import "./ItemSelection.css";
import { useEffect, useState } from "react";
import ItemIcon from "../ItemIcon";

export default function ItemSelection() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiBase = import.meta.env.VITE_API_URL ?? "";
    const apiUrl = apiBase ? `${apiBase}/api/items` : "/api/items";

    fetch(apiUrl)
      .then((res) => res.json())
      .then((data) => {
        setItems(data);
      })
      .catch((err) => {
        console.error("Error fetching items:", err);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="item-selection">
      <div className="items-list">
        {loading && <div className="loading">Cargando ítems…</div>}

        {!loading && items.length === 0 && (
          <div className="no-items">No hay ítems para mostrar</div>
        )}

        {items.map((item) => (
          <div key={item.id} className="item-slot">
            <ItemIcon item={item} />
          </div>
        ))}

        <div className="items-more">
          <span>•••</span>
        </div>
      </div>
    </div>
  );
}

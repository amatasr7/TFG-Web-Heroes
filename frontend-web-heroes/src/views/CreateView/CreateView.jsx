import { useState, useEffect } from "react";
import "./CreateView.css";
import { API } from "../../utils/api";

const CLASES_JUGABLES = [
  {
    name: "Guerrero",
    desc: "Maestro del combate cuerpo a cuerpo. Alta defensa y vida.",
    sprite: "/sprites/Guerrero2.png",
    color: "#ef4444",
  },
  {
    name: "Mago",
    desc: "Manipulador de energías arcanas. Alto maná y habilidades poderosas.",
    sprite: "/sprites/Maga.png",
    color: "#a78bfa",
  },
  {
    name: "Picaro",
    desc: "Experto en las sombras. Alto ataque y habilidades de sigilo.",
    sprite: "/sprites/Arquero.png",
    color: "#10b981",
  },
];

const SPRITES_DISPONIBLES = [
  { url: "/sprites/Guerrero.png", label: "Guerrero" },
  { url: "/sprites/Guerrero2.png", label: "Guerrero II" },
  { url: "/sprites/Barbaro.png", label: "Bárbaro" },
  { url: "/sprites/Maga.png", label: "Maga" },
  { url: "/sprites/Chaman.png", label: "Chamán" },
  { url: "/sprites/Arquero.png", label: "Arquero" },
  { url: "/sprites/Arquero2.png", label: "Arquero II" },
  { url: "/sprites/Campesina.png", label: "Campesina" },
  { url: "/sprites/Pelirrojo.png", label: "Pelirrojo" },
];

export default function CreateView({ user, onUserUpdate, onNavigate }) {
  const [clases, setClases] = useState([]);
  const [contratos, setContratos] = useState(0);
  const [contratoItemId, setContratoItemId] = useState(null);

  const [nombre, setNombre] = useState("");
  const [claseSeleccionada, setClaseSeleccionada] = useState(null);
  const [spriteSeleccionado, setSpriteSeleccionado] = useState(
    SPRITES_DISPONIBLES[0].url,
  );

  const [isLoading, setIsLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  const [error, setError] = useState(null);
  const [exito, setExito] = useState(false);

  useEffect(() => {
    if (!user) return;

    const fetchData = async () => {
      setIsLoading(true);
      try {
        const [clasesRes, inventarioRes] = await Promise.all([
          fetch(`${API}/hero-classes`),
          fetch(`${API}/shop/inventory?user_id=${user.id}`),
        ]);

        if (clasesRes.ok) {
          const data = await clasesRes.json();
          setClases(data.filter((c) => c.is_playable));
        }

        if (inventarioRes.ok) {
          const inv = await inventarioRes.json();
          const contratoEntry = (inv.user_items || []).find(
            (ui) => ui.item?.name === "Contrato de heroe",
          );
          setContratos(contratoEntry?.quantity ?? 0);
          setContratoItemId(contratoEntry?.item?.id ?? null);
          onUserUpdate((prev) => ({ ...prev, gold: inv.user.gold }));
        }
      } catch {
        // silently ignore
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [user?.id]);

  // Sync sprite with class selection default
  const handleSelectClase = (clase) => {
    setClaseSeleccionada(clase);
    const match = CLASES_JUGABLES.find((c) => c.name === clase.name);
    if (match) setSpriteSeleccionado(match.sprite);
  };

  const handleCrear = async () => {
    if (!nombre.trim()) {
      setError("El nombre no puede estar vacío.");
      return;
    }
    if (!claseSeleccionada) {
      setError("Debes seleccionar una clase.");
      return;
    }
    if (contratos < 1) {
      setError("Necesitas un Contrato de héroe para crear un héroe.");
      return;
    }

    setIsCreating(true);
    setError(null);

    try {
      const res = await fetch(`${API}/heroes/create-with-contract`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: user.id,
          hero_class_id: claseSeleccionada.id,
          name: nombre.trim(),
          sprite_url: spriteSeleccionado,
        }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Error al crear el héroe.");
      }

      setContratos((prev) => prev - 1);
      setExito(true);
      setNombre("");
      setClaseSeleccionada(null);
      setSpriteSeleccionado(SPRITES_DISPONIBLES[0].url);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsCreating(false);
    }
  };

  if (isLoading) {
    return (
      <div className="create-wrapper">
        <div className="create-aviso">
          <h3 className="font-amarillo">Cargando datos...</h3>
        </div>
      </div>
    );
  }

  if (exito) {
    return (
      <div className="create-wrapper">
        <div className="create-exito-panel">
          <div className="create-exito-icono">⚔</div>
          <h2 className="create-exito-titulo">¡Héroe reclutado!</h2>
          <p className="create-exito-sub">
            Tu nuevo compañero ha sido añadido a tu lista de héroes.
          </p>
          <div className="create-exito-botones">
            <button
              className="create-btn create-btn-primario"
              onClick={() => onNavigate("heroes")}
            >
              Ver héroes
            </button>
            <button
              className="create-btn create-btn-secundario"
              onClick={() => setExito(false)}
            >
              Crear otro
            </button>
          </div>
        </div>
      </div>
    );
  }

  const clasesParaMostrar = CLASES_JUGABLES.map((cLocal) => {
    const cBackend = clases.find(
      (c) => c.name.toLowerCase() === cLocal.name.toLowerCase(),
    );
    return { ...cLocal, id: cBackend?.id, ...(cBackend ?? {}) };
  });

  return (
    <div className="create-wrapper">
      <div className="create-container">
        {/* ── CABECERA ── */}
        <div className="create-cabecera">
          <h2 className="create-titulo">Reclutamiento de héroes</h2>
          <div
            className={`create-contratos ${contratos === 0 ? "create-contratos-vacio" : ""}`}
          >
            <span>
              {contratos > 0
                ? `Contratos disponibles: ${contratos}`
                : "Sin contratos — cómpralos en la tienda"}
            </span>
          </div>
        </div>

        {contratos === 0 && (
          <div className="create-aviso-sin-contrato">
            <p>
              Necesitas al menos un <strong>Contrato de héroe</strong> para
              reclutar un nuevo miembro.
            </p>
            <button
              className="create-btn create-btn-secundario"
              onClick={() => onNavigate("shop")}
            >
              Ir a la tienda
            </button>
          </div>
        )}

        <div className="create-layout">
          {/* ── COLUMNA IZQUIERDA: Formulario ── */}
          <div className="create-columna">
            {/* Nombre */}
            <div className="create-bloque">
              <h3 className="create-bloque-titulo">Nombre del héroe</h3>
              <input
                className="create-input-nombre"
                type="text"
                placeholder="Escribe un nombre..."
                maxLength={40}
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                disabled={contratos === 0}
              />
            </div>

            {/* Clase */}
            <div className="create-bloque">
              <h3 className="create-bloque-titulo">Selecciona la clase</h3>
              <div className="create-clases-grid">
                {clasesParaMostrar.map((clase) => (
                  <button
                    key={clase.name}
                    className={`create-clase-card ${claseSeleccionada?.name === clase.name ? "create-clase-activa" : ""}`}
                    style={{ "--clase-color": clase.color }}
                    onClick={() => handleSelectClase(clase)}
                    disabled={contratos === 0}
                  >
                    <img
                      src={clase.sprite}
                      alt={clase.name}
                      className="create-clase-sprite"
                    />
                    <span className="create-clase-nombre">{clase.name}</span>
                    <span className="create-clase-desc">{clase.desc}</span>
                    {clase.base_hp_max && (
                      <div className="create-clase-stats">
                        <span className="stat-hp">HP {clase.base_hp_max}</span>
                        <span className="stat-mp">MP {clase.base_mp_max}</span>
                        <span className="stat-atk">
                          ATK {clase.base_attack}
                        </span>
                        <span className="stat-def">
                          DEF {clase.base_defense}
                        </span>
                      </div>
                    )}
                  </button>
                ))}
              </div>
            </div>

            {/* Botón crear */}
            {error && <p className="create-error">{error}</p>}

            <button
              className="create-btn create-btn-primario create-btn-grande"
              onClick={handleCrear}
              disabled={
                contratos === 0 ||
                isCreating ||
                !nombre.trim() ||
                !claseSeleccionada
              }
            >
              {isCreating ? "Reclutando..." : "⚔ Reclutar héroe"}
            </button>
          </div>

          {/* ── COLUMNA DERECHA: Preview + Sprites ── */}
          <div className="create-columna">
            {/* Preview del personaje */}
            <div className="create-bloque create-preview-bloque">
              <h3 className="create-bloque-titulo">Vista previa</h3>
              <div className="create-preview-retrato">
                <img
                  src={spriteSeleccionado}
                  alt="Vista previa"
                  className="create-preview-img"
                />
              </div>
              <div className="create-preview-info">
                <span className="create-preview-nombre">
                  {nombre || "Sin nombre"}
                </span>
                <span className="create-preview-clase">
                  {claseSeleccionada?.name || "Sin clase"}
                </span>
              </div>
            </div>

            {/* Selector de sprite */}
            <div className="create-bloque">
              <h3 className="create-bloque-titulo">Apariencia</h3>
              <div className="create-sprites-grid">
                {SPRITES_DISPONIBLES.map((s) => (
                  <button
                    key={s.url}
                    className={`create-sprite-slot ${spriteSeleccionado === s.url ? "create-sprite-activo" : ""}`}
                    onClick={() => setSpriteSeleccionado(s.url)}
                    disabled={contratos === 0}
                    title={s.label}
                  >
                    <img
                      src={s.url}
                      alt={s.label}
                      className="create-sprite-img"
                    />
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

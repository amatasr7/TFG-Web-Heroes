import "./TurnOrder.css";

export default function TurnOrder({ actors }) {
  return (
    <section className="turn-order">
      <h3>Orden de Turnos</h3>
      <div className="turn-order-list">
        {actors?.map((actor, index) => (
          <div key={actor.id} className={`turn-order-card ${actor.type}`}>
            <div className="turn-order-index">{index + 1}</div>
            <div className="turn-order-name">{actor.name}</div>
          </div>
        ))}
      </div>
    </section>
  );
}

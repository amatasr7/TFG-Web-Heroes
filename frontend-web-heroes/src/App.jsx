import { useState } from "react";
import Header from "./views/Header/Header";
import HeroView from "./views/HeroView/HeroView";
import ShopView from "./views/ShopView/ShopView";
import CombatView from "./views/CombatView/CombatView";

export default function App() {
  // El "cerebro" que sabe en qué pantalla estamos
  const [currentView, setCurrentView] = useState("heroes");

  // Elige qué cuerpo renderizar según el estado
  const renderView = () => {
    switch (currentView) {
      case "heroes":
        return <HeroView />;
      case "shop":
        return <ShopView />;
      case "combat":
        return <CombatView />;
      default:
        return <HeroView />;
    }
  };

  return (
    <div className="shell">
      <Header currentView={currentView} setCurrentView={setCurrentView} />

      <main className="content" style={{ marginTop: "20px" }}>
        {renderView()}
      </main>
    </div>
  );
}

import { useState } from "react";
import Header from "./views/Header/Header";
import HeroView from "./views/HeroView/HeroView";
import ShopView from "./views/ShopView/ShopView";
import MissionView from "./views/MissionView/MissionView";

export default function App() {
  const [currentView, setCurrentView] = useState("heroes");

  const renderView = () => {
    switch (currentView) {
      case "heroes":
        return <HeroView />;
      case "shop":
        return <ShopView />;
      case "missions":
        return <MissionView />;
      default:
        return <HeroView />;
    }
  };

  return (
    <div
      className="shell"
      style={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}
    >
      <Header currentView={currentView} setCurrentView={setCurrentView} />

      <main className="content" style={{ flexGrow: 1 }}>
        {renderView()}
      </main>
    </div>
  );
}

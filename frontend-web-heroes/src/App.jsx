import { useEffect, useState } from "react";
import Header from "./views/Header/Header";
import HeroView from "./views/HeroView/HeroView";
import ShopView from "./views/ShopView/ShopView";
import MissionView from "./views/MissionView/MissionView";
import AuthView from "./views/AuthView/AuthView";

export default function App() {
  const [currentView, setCurrentView] = useState("heroes");
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem("webHeroesUser");
    return stored ? JSON.parse(stored) : null;
  });

  useEffect(() => {
    if (user) {
      localStorage.setItem("webHeroesUser", JSON.stringify(user));
    } else {
      localStorage.removeItem("webHeroesUser");
    }
  }, [user]);

  const handleLogout = () => {
    setUser(null);
    setCurrentView("heroes");
  };

  const renderView = () => {
    if (!user) {
      return <AuthView onLogin={(user) => { setUser(user); setCurrentView("heroes"); }} />;
    }

    switch (currentView) {
      case "heroes":
        return <HeroView user={user} onUserUpdate={setUser} />;
      case "shop":
        return <ShopView user={user} onUserUpdate={setUser} />;
      case "missions":
        return <MissionView user={user} />;
      default:
        return <HeroView user={user} />;
    }
  };

  return (
    <div
      className="shell"
      style={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}
    >
      {user && (
        <Header
          currentView={currentView}
          setCurrentView={setCurrentView}
          user={user}
          onLogout={handleLogout}
        />
      )}

      <main className="content" style={{ flexGrow: 1 }}>
        {renderView()}
      </main>
    </div>
  );
}

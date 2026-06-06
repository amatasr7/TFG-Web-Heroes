export function getSpriteForHero(hero) {
  if (hero?.sprite_url) return hero.sprite_url;
  const cls = (hero?.hero_class?.name ?? hero?.hero_class_name ?? "").toLowerCase();
  if (cls.includes("guerrero")) return "/sprites/Guerrero2.png";
  if (cls.includes("mago")) return "/sprites/Maga.png";
  if (cls.includes("picaro") || cls.includes("pícaro")) return "/sprites/Arquero.png";
  if (cls.includes("jefe")) return "/sprites/Orco.png";
  return "/sprites/Pelirrojo.png";
}

export function getSpriteForEnemy(enemy) {
  const name = (enemy?.name ?? "").toLowerCase();
  const cls = (enemy?.hero_class?.name ?? enemy?.hero_class_name ?? "").toLowerCase();
  if (name.includes("goblin") || cls.includes("goblin")) return "/sprites/Goblin-guerrero.png";
  if (name.includes("slime")) return "/sprites/Slime.png";
  if (name.includes("orco") || name.includes("orc")) return "/sprites/Orco.png";
  if (name.includes("lobo") || name.includes("wolf")) return "/sprites/Lobo.png";
  if (name.includes("oso") || name.includes("bear")) return "/sprites/Oso.png";
  if (name.includes("golem")) return "/sprites/Golem.png";
  if (name.includes("jabali") || name.includes("jabalí")) return "/sprites/Jabali.png";
  return "/sprites/Orco.png";
}

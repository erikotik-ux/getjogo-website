// GETJOGO catalog. Cover art is hotlinked from Steam's public CDN
// (validated live). Each listing is one pre-owned license on one platform.
// score = GETJOGO community score out of 10.
const COVER = (appid) =>
  `https://cdn.cloudflare.steamstatic.com/steam/apps/${appid}/library_600x900.jpg`;

const GAMES = [
  {
    id: "elden-ring", appid: 1245620, title: "Elden Ring",
    platform: "PS5", retail: 59.99, price: 32.99,
    publisher: "Bandai Namco", developer: "FromSoftware",
    released: "2022-02-25", genre: "Action RPG", rating: "M", score: 9.5,
    desc: "A vast dark-fantasy world where every ruin hides a boss and every death teaches you something.",
    tags: ["trending", "top", "best", "aaa"], special: "Best Deal"
  },
  {
    id: "baldurs-gate-3", appid: 1086940, title: "Baldur's Gate 3",
    platform: "PC", retail: 59.99, price: 38.99,
    publisher: "Larian Studios", developer: "Larian Studios",
    released: "2023-08-03", genre: "RPG", rating: "M", score: 9.7,
    desc: "The deepest party RPG in years. Every playthrough goes somewhere different, usually somewhere absurd.",
    tags: ["trending", "top", "best", "aaa"]
  },
  {
    id: "cyberpunk-2077", appid: 1091500, title: "Cyberpunk 2077",
    platform: "PC", retail: 59.99, price: 24.99,
    publisher: "CD Projekt", developer: "CD Projekt Red",
    released: "2020-12-10", genre: "Action RPG", rating: "M", score: 9.0,
    desc: "Night City at full density. After years of updates this is one of the best open worlds on PC.",
    tags: ["trending", "best", "aaa"]
  },
  {
    id: "red-dead-redemption-2", appid: 1174180, title: "Red Dead Redemption 2",
    platform: "Xbox", retail: 59.99, price: 26.99,
    publisher: "Rockstar Games", developer: "Rockstar Games",
    released: "2018-10-26", genre: "Action Adventure", rating: "M", score: 9.3,
    desc: "A slow-burn outlaw epic with a world so detailed it still embarrasses newer releases.",
    tags: ["best", "aaa"]
  },
  {
    id: "witcher-3", appid: 292030, title: "The Witcher 3: Wild Hunt",
    platform: "Switch", retail: 39.99, price: 12.99,
    publisher: "CD Projekt", developer: "CD Projekt Red",
    released: "2015-05-18", genre: "Action RPG", rating: "M", score: 9.6,
    desc: "Two hundred hours of monster contracts and hard choices, and it runs in your hands.",
    tags: ["top", "best", "aaa", "trending"]
  },
  {
    id: "god-of-war", appid: 1593500, title: "God of War",
    platform: "PC", retail: 49.99, price: 22.99,
    publisher: "PlayStation Publishing", developer: "Santa Monica Studio",
    released: "2022-01-14", genre: "Action Adventure", rating: "M", score: 9.4,
    desc: "Kratos does quiet parenting between mythological beatdowns. The single-shot camera still impresses.",
    tags: ["top", "aaa"]
  },
  {
    id: "horizon-zero-dawn", appid: 1151640, title: "Horizon Zero Dawn",
    platform: "PC", retail: 49.99, price: 18.99,
    publisher: "PlayStation Publishing", developer: "Guerrilla Games",
    released: "2020-08-07", genre: "Action RPG", rating: "T", score: 8.8,
    desc: "Hunt robot dinosaurs with a bow in a post-post-apocalypse that looks better than it has any right to.",
    tags: ["aaa"]
  },
  {
    id: "sekiro", appid: 814380, title: "Sekiro: Shadows Die Twice",
    platform: "Xbox", retail: 59.99, price: 29.99,
    publisher: "Activision", developer: "FromSoftware",
    released: "2019-03-22", genre: "Action", rating: "M", score: 9.2,
    desc: "Pure sword-fighting rhythm. The hardest game on this list and the most satisfying to finish.",
    tags: ["top", "aaa"]
  },
  {
    id: "resident-evil-4", appid: 2050650, title: "Resident Evil 4",
    platform: "PS5", retail: 59.99, price: 27.99,
    publisher: "Capcom", developer: "Capcom",
    released: "2023-03-24", genre: "Survival Horror", rating: "M", score: 9.3,
    desc: "The remake that got everything right. Tense, gorgeous, and generous with its scares.",
    tags: ["trending", "top", "aaa"]
  },
  {
    id: "hogwarts-legacy", appid: 990080, title: "Hogwarts Legacy",
    platform: "Switch", retail: 59.99, price: 25.99,
    publisher: "Warner Bros. Games", developer: "Avalanche Software",
    released: "2023-02-10", genre: "Open World RPG", rating: "T", score: 8.7,
    desc: "The castle is the star. Explore, fly, and duel your way through a fully realized wizarding world.",
    tags: ["best", "aaa"]
  },
  {
    id: "starfield", appid: 1716740, title: "Starfield",
    platform: "Xbox", retail: 69.99, price: 31.99,
    publisher: "Bethesda Softworks", developer: "Bethesda Game Studios",
    released: "2023-09-06", genre: "Space RPG", rating: "M", score: 7.4,
    desc: "A thousand planets of Bethesda jank and wonder. Best enjoyed with mods and low expectations.",
    tags: ["aaa"]
  },
  {
    id: "monster-hunter-world", appid: 582010, title: "Monster Hunter: World",
    platform: "PC", retail: 29.99, price: 11.99,
    publisher: "Capcom", developer: "Capcom",
    released: "2018-08-09", genre: "Action RPG", rating: "T", score: 8.9,
    desc: "Fight giant monsters, turn them into hats, repeat. The co-op loop that ate a million evenings.",
    tags: ["under20", "aaa"]
  },
  {
    id: "armored-core-6", appid: 1888160, title: "Armored Core VI: Fires of Rubicon",
    platform: "PS5", retail: 59.99, price: 28.99,
    publisher: "Bandai Namco", developer: "FromSoftware",
    released: "2023-08-25", genre: "Mech Action", rating: "T", score: 8.8,
    desc: "Build a mech, lose to a helicopter, rebuild the mech. Fast, precise, and endlessly tunable.",
    tags: ["aaa"]
  },
  {
    id: "ghost-of-tsushima", appid: 2215430, title: "Ghost of Tsushima Director's Cut",
    platform: "PS5", retail: 59.99, price: 34.99,
    publisher: "PlayStation Publishing", developer: "Sucker Punch Productions",
    released: "2021-08-20", genre: "Action Adventure", rating: "M", score: 9.1,
    desc: "A samurai film you can play. Wind guides you, standoffs stop time, and the photo mode ruins your evening.",
    tags: ["trending", "aaa"]
  },
  {
    id: "doom-eternal", appid: 782330, title: "DOOM Eternal",
    platform: "PC", retail: 39.99, price: 14.99,
    publisher: "Bethesda Softworks", developer: "id Software",
    released: "2020-03-20", genre: "FPS", rating: "M", score: 9.0,
    desc: "A first-person shooter played at the speed of panic. Rip, tear, chain-swap weapons, repeat.",
    tags: ["under20", "aaa"]
  },
  {
    id: "spider-man-remastered", appid: 1817070, title: "Marvel's Spider-Man Remastered",
    platform: "PC", retail: 59.99, price: 27.99,
    publisher: "PlayStation Publishing", developer: "Insomniac Games",
    released: "2022-08-12", genre: "Action Adventure", rating: "T", score: 9.0,
    desc: "The swing alone is worth the price. Everything else is a very good superhero story on top.",
    tags: ["best", "aaa"]
  },
  {
    id: "hades", appid: 1145360, title: "Hades",
    platform: "Switch", retail: 24.99, price: 11.99,
    publisher: "Supergiant Games", developer: "Supergiant Games",
    released: "2020-09-17", genre: "Roguelike", rating: "T", score: 9.4,
    desc: "Die, flirt with Greek gods, get stronger, die better. The roguelike that converted everyone.",
    tags: ["under20", "top", "indie", "best"]
  },
  {
    id: "hollow-knight", appid: 367520, title: "Hollow Knight",
    platform: "Switch", retail: 14.99, price: 6.49,
    publisher: "Team Cherry", developer: "Team Cherry",
    released: "2017-02-24", genre: "Metroidvania", rating: "E10+", score: 9.5,
    desc: "A haunted bug kingdom with more content than most AAA releases, at a tenth of the price.",
    tags: ["under20", "top", "indie"], special: "Best Deal"
  },
  {
    id: "celeste", appid: 504230, title: "Celeste",
    platform: "PC", retail: 19.99, price: 7.99,
    publisher: "Maddy Makes Games", developer: "Maddy Makes Games",
    released: "2018-01-25", genre: "Platformer", rating: "E10+", score: 9.2,
    desc: "A precision platformer about climbing a mountain and everything the mountain stands for.",
    tags: ["under20", "indie"]
  },
  {
    id: "stardew-valley", appid: 413150, title: "Stardew Valley",
    platform: "Switch", retail: 14.99, price: 7.49,
    publisher: "ConcernedApe", developer: "ConcernedApe",
    released: "2016-02-26", genre: "Farming Sim", rating: "E10+", score: 9.6,
    desc: "Inherit a farm, meet the town, lose four hundred hours. The coziest game ever made by one person.",
    tags: ["under20", "top", "indie", "best"]
  },
  {
    id: "dead-cells", appid: 588650, title: "Dead Cells",
    platform: "PC", retail: 24.99, price: 9.99,
    publisher: "Motion Twin", developer: "Motion Twin",
    released: "2018-08-07", genre: "Roguelike", rating: "T", score: 9.0,
    desc: "Combat so fluid it feels autocompleted. Every run remixes the castle and your build.",
    tags: ["under20", "indie"]
  },
  {
    id: "disco-elysium", appid: 632470, title: "Disco Elysium: The Final Cut",
    platform: "PC", retail: 39.99, price: 13.99,
    publisher: "ZA/UM", developer: "ZA/UM",
    released: "2019-10-15", genre: "RPG", rating: "M", score: 9.3,
    desc: "A detective RPG where your own skills argue with you. The best writing in the medium.",
    tags: ["under20", "top", "indie"]
  },
  {
    id: "outer-wilds", appid: 753640, title: "Outer Wilds",
    platform: "PC", retail: 24.99, price: 12.99,
    publisher: "Annapurna Interactive", developer: "Mobius Digital",
    released: "2020-06-18", genre: "Adventure", rating: "E10+", score: 9.4,
    desc: "A 22-minute solar system stuck in a loop. Go in blind. Do not read anything about it.",
    tags: ["under20", "top", "indie"]
  },
  {
    id: "vampire-survivors", appid: 1794680, title: "Vampire Survivors",
    platform: "PC", retail: 4.99, price: 2.49,
    publisher: "poncle", developer: "poncle",
    released: "2022-10-20", genre: "Roguelike", rating: "E10+", score: 8.9,
    desc: "Walk around, mow down thousands of monsters, tell yourself one more run. It is never one more run.",
    tags: ["under20", "indie", "best"]
  },
  {
    id: "dave-the-diver", appid: 1868140, title: "Dave the Diver",
    platform: "Switch", retail: 19.99, price: 9.49,
    publisher: "MINTROCKET", developer: "MINTROCKET",
    released: "2023-06-28", genre: "Adventure Sim", rating: "E10+", score: 9.0,
    desc: "Catch fish by day, run a sushi bar by night, get ambushed by a new mechanic every hour.",
    tags: ["under20", "indie", "recent"]
  },
  {
    id: "slay-the-spire", appid: 646570, title: "Slay the Spire",
    platform: "PC", retail: 24.99, price: 8.99,
    publisher: "MegaCrit", developer: "MegaCrit",
    released: "2019-01-23", genre: "Deckbuilder", rating: "E10+", score: 9.2,
    desc: "The card game that spawned a genre. Every defeat is your fault, which is why you keep playing.",
    tags: ["under20", "indie"]
  },
  {
    id: "cuphead", appid: 268910, title: "Cuphead",
    platform: "Xbox", retail: 19.99, price: 8.99,
    publisher: "StudioMDHR", developer: "StudioMDHR",
    released: "2017-09-29", genre: "Run and Gun", rating: "E10+", score: 9.1,
    desc: "A 1930s cartoon that fights back. Hand-drawn bosses and a jazz record of a soundtrack.",
    tags: ["under20", "indie"]
  },
  {
    id: "lies-of-p", appid: 1627720, title: "Lies of P",
    platform: "Xbox", retail: 59.99, price: 26.99,
    publisher: "Neowiz", developer: "Neowiz / Round8 Studio",
    released: "2023-09-19", genre: "Action RPG", rating: "M", score: 8.7,
    desc: "Pinocchio as a soulslike, and somehow it works. Sharp combat in a rain-slicked belle epoque city.",
    tags: ["recent", "aaa"]
  },
  {
    id: "black-myth-wukong", appid: 2358720, title: "Black Myth: Wukong",
    platform: "PS5", retail: 59.99, price: 39.99,
    publisher: "Game Science", developer: "Game Science",
    released: "2024-08-20", genre: "Action RPG", rating: "M", score: 9.0,
    desc: "Journey to the West as a blockbuster boss gauntlet. One of the best looking games ever shipped.",
    tags: ["new", "trending", "recent", "aaa"]
  },
  {
    id: "silent-hill-2", appid: 2124490, title: "Silent Hill 2",
    platform: "PS5", retail: 69.99, price: 41.99,
    publisher: "Konami", developer: "Bloober Team",
    released: "2024-10-08", genre: "Survival Horror", rating: "M", score: 8.9,
    desc: "The remake nobody trusted and everybody needed. Fog, guilt, and the best audio design of 2024.",
    tags: ["new", "recent", "aaa"]
  },
  {
    id: "kingdom-come-2", appid: 1771300, title: "Kingdom Come: Deliverance II",
    platform: "PC", retail: 59.99, price: 38.99,
    publisher: "Deep Silver", developer: "Warhorse Studios",
    released: "2025-02-04", genre: "Historical RPG", rating: "M", score: 9.0,
    desc: "Medieval Bohemia without the fantasy. Realistic, stubborn, and completely absorbing.",
    tags: ["new", "trending", "recent", "aaa"]
  },
  {
    id: "clair-obscur", appid: 1903340, title: "Clair Obscur: Expedition 33",
    platform: "PS5", retail: 49.99, price: 33.99,
    publisher: "Kepler Interactive", developer: "Sandfall Interactive",
    released: "2025-04-24", genre: "Turn-Based RPG", rating: "M", score: 9.6,
    desc: "A painterly French RPG where turn-based combat has timing and style. 2025's breakout hit.",
    tags: ["new", "trending", "top", "recent", "aaa"], special: "Best Deal"
  },
  {
    id: "hades-2", appid: 1145350, title: "Hades II",
    platform: "Switch", retail: 29.99, price: 19.99,
    publisher: "Supergiant Games", developer: "Supergiant Games",
    released: "2025-09-25", genre: "Roguelike", rating: "T", score: 9.3,
    desc: "The witch of the underworld picks up where her brother left off. Bigger, meaner, just as replayable.",
    tags: ["new", "top", "indie", "recent"]
  },
  {
    id: "doom-dark-ages", appid: 3017860, title: "DOOM: The Dark Ages",
    platform: "Xbox", retail: 69.99, price: 44.99,
    publisher: "Bethesda Softworks", developer: "id Software",
    released: "2025-05-15", genre: "FPS", rating: "M", score: 8.8,
    desc: "The Slayer goes medieval. Shield saw, mech dragons, and the heaviest shotgun in the series.",
    tags: ["new", "recent", "aaa"]
  }
];

// Customer reviews shown in the testimonial section (sample content).
const REVIEWS = [
  {
    name: "Marcus T.", detail: "Bought Elden Ring (PS5)", stars: 5,
    text: "Honestly expected a scam at these prices. License landed in my library about 40 seconds after checkout. Converted."
  },
  {
    name: "Priya S.", detail: "Bought Hades (Switch)", stars: 5,
    text: "The ownership history on each listing is a great touch. You can see exactly what you are buying before you pay."
  },
  {
    name: "Jonas K.", detail: "Bought Cyberpunk 2077 (PC)", stars: 4,
    text: "One transfer took a few hours because the seller was asleep. Support kept me updated the whole time and the game works perfectly."
  },
  {
    name: "Elena R.", detail: "Bought Stardew Valley (Switch)", stars: 5,
    text: "Paid half price for a verified license and it activated instantly. My whole wishlist is coming from here now."
  }
];

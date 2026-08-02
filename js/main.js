// ============ helpers ============
const fmt = (n) => "$" + n.toFixed(2);
const savePct = (g) => Math.round((1 - g.price / g.retail) * 100);
const year = (g) => g.released.slice(0, 4);

const starIcon = `<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2l2.92 6.26 6.58.8-4.86 4.73 1.15 6.71L12 17.77 6.21 20.5l1.15-6.71L2.5 9.06l6.58-.8L12 2z"/></svg>`;
const shieldIcon = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>`;
const boltIcon = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"/></svg>`;

const PLATFORM_CLASS = { PC: "pf-pc", PS5: "pf-ps", Xbox: "pf-xbox", Switch: "pf-switch" };

// ============ card component ============
function gameCard(g) {
  return `
    <article class="g-card">
      <a href="#trending" class="g-cover-wrap" aria-label="${g.title}, ${g.platform}, ${fmt(g.price)}, save ${savePct(g)} percent">
        <img src="${COVER(g.appid)}" alt="${g.title} cover art" width="600" height="900" loading="lazy" decoding="async">
        <span class="badge-save">-${savePct(g)}%</span>
        ${g.special ? `<span class="badge-special">${g.special}</span>` : ""}
        <div class="g-overlay">
          <p class="g-desc">${g.desc}</p>
          <dl class="g-facts">
            <div><dt>Developer</dt><dd>${g.developer}</dd></div>
            <div><dt>Publisher</dt><dd>${g.publisher}</dd></div>
            <div><dt>Released</dt><dd>${g.released}</dd></div>
          </dl>
        </div>
      </a>
      <div class="g-body">
        <h3 class="g-title">${g.title}</h3>
        <div class="g-chips">
          <span class="chip ${PLATFORM_CLASS[g.platform]}">${g.platform}</span>
          <span class="chip chip-rating" title="ESRB rating">${g.rating}</span>
          <span class="g-score">${starIcon}${g.score.toFixed(1)}</span>
        </div>
        <p class="g-sub">${g.genre} &middot; ${year(g)}</p>
        <p class="g-verified"><span>${shieldIcon}Verified License</span><span>${boltIcon}Instant Delivery</span></p>
        <div class="g-price-row">
          <span class="g-retail">${fmt(g.retail)}</span>
          <span class="g-price">${fmt(g.price)}</span>
        </div>
        <a href="#trending" class="btn btn-primary btn-sm g-buy" aria-label="Buy ${g.title} for ${fmt(g.price)}">Buy Now</a>
      </div>
    </article>`;
}

// ============ hero spotlight ============
function spotlight(g) {
  return `
    <div class="spot-card">
      <span class="spot-sparkles" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span>
      <span class="spot-label">${boltIcon}Deal of the day</span>
      <div class="spot-inner">
        <div class="spot-cover">
          <img src="${COVER(g.appid)}" alt="${g.title} cover art" width="600" height="900" fetchpriority="high" decoding="async">
          <div class="spot-price">
            <span class="spot-price-top"><span class="badge-save">-${savePct(g)}%</span><s>${fmt(g.retail)}</s></span>
            <strong>${fmt(g.price)}</strong>
          </div>
        </div>
        <div class="spot-meta">
          <h2 class="spot-title">${g.title}</h2>
          <p class="spot-sub">${g.genre} &middot; ${g.platform} &middot; ${starIcon}${g.score.toFixed(1)}</p>
          <p class="spot-desc">${g.desc}</p>
          <a href="#trending" class="btn btn-primary g-buy">Buy Now</a>
          <p class="spot-verified">${shieldIcon}Verified license, transfers in under a minute</p>
        </div>
      </div>
    </div>`;
}

// ============ sections ============
const byTag = (tag) => GAMES.filter((g) => g.tags.includes(tag));
const SHELVES = {
  "shelf-trending": byTag("trending"),
  "shelf-new": byTag("new").sort((a, b) => b.released.localeCompare(a.released)),
  "shelf-top": GAMES.filter((g) => g.score >= 9.2).sort((a, b) => b.score - a.score),
  "shelf-best": byTag("best"),
  "shelf-aaa": byTag("aaa"),
  "shelf-indie": byTag("indie"),
  "shelf-recent": byTag("recent").sort((a, b) => b.released.localeCompare(a.released))
};

Object.entries(SHELVES).forEach(([id, games]) => {
  document.getElementById(id).innerHTML = games.map(gameCard).join("");
});

document.getElementById("grid-under20").innerHTML =
  GAMES.filter((g) => g.price < 20).sort((a, b) => a.price - b.price).map(gameCard).join("");

document.getElementById("spotlight").innerHTML =
  spotlight(GAMES.find((g) => g.id === "clair-obscur"));

// ============ customer reviews ============
function reviewCard(r) {
  const stars = Array.from({ length: 5 }, (_, i) =>
    `<span class="rv-star ${i < r.stars ? "on" : ""}">${starIcon}</span>`
  ).join("");
  return `
    <figure class="review-card">
      <div class="rv-stars" role="img" aria-label="${r.stars} out of 5 stars">${stars}</div>
      <blockquote>${r.text}</blockquote>
      <figcaption><strong>${r.name}</strong><span>${r.detail}</span></figcaption>
    </figure>`;
}
document.getElementById("reviews-grid").innerHTML = REVIEWS.map(reviewCard).join("");

// ============ shelf arrows ============
document.querySelectorAll(".shelf-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    const track = document.getElementById(btn.dataset.target);
    const card = track.querySelector(".g-card");
    const step = card ? (card.offsetWidth + 24) * 2 : 480;
    track.scrollBy({ left: step * Number(btn.dataset.dir), behavior: "smooth" });
  });
});

// ============ mobile nav ============
const navToggle = document.querySelector(".nav-toggle");
const navMenu = document.getElementById("nav-menu");
navToggle.addEventListener("click", () => {
  const open = navToggle.getAttribute("aria-expanded") === "true";
  navToggle.setAttribute("aria-expanded", String(!open));
  navMenu.classList.toggle("is-open", !open);
});
navMenu.addEventListener("click", (e) => {
  if (e.target.closest("a")) {
    navToggle.setAttribute("aria-expanded", "false");
    navMenu.classList.remove("is-open");
  }
});

// ============ typography: no single-word last lines ============
// `text-wrap: pretty` handles most blocks; where it cannot, tie the final
// two words with a non-breaking space. Skipped when that pair is long
// enough to risk overflowing a narrow column.
function bindLastWords(scope) {
  scope.querySelectorAll("p, li, blockquote, figcaption, .spot-desc, .g-desc").forEach((el) => {
    const texts = [...el.childNodes].filter((n) => n.nodeType === 3 && n.textContent.trim());
    const last = texts[texts.length - 1];
    if (!last || last !== el.lastChild) return;
    const t = last.textContent.replace(/\s+$/, "");
    const i = t.lastIndexOf(" ");
    if (i <= 0) return;
    const pair = t.slice(t.lastIndexOf(" ", i - 1) + 1);
    if (pair.length > 24) return;
    last.textContent = t.slice(0, i) + " " + t.slice(i + 1);
  });
}
bindLastWords(document);

// ============ header: scrim over the hero, solid once scrolled ============
const siteHeader = document.querySelector(".site-header");
if (siteHeader) {
  let stuck = null;
  const sync = () => {
    const next = window.scrollY > 24;
    if (next === stuck) return;           // only touch the DOM on a change
    stuck = next;
    siteHeader.classList.toggle("is-stuck", next);
  };
  addEventListener("scroll", sync, { passive: true });
  sync();
}

// ============ hero scene: pause while off-screen ============
const heroScene = document.querySelector(".hero-scene");
let sceneVisible = true;
if (heroScene && "IntersectionObserver" in window) {
  const sceneIO = new IntersectionObserver(
    ([entry]) => {
      sceneVisible = entry.isIntersecting;
      heroScene.classList.toggle("is-paused", !sceneVisible);
    },
    { threshold: 0 }
  );
  sceneIO.observe(document.querySelector(".hero"));
}

// ============ 16-bit mascot ============
// One sprite sheet, four rows: 0 roll(12) 1 uncurl(6) 2 run(8) 3 idle(8).
// A phase list drives both the frame and the position, so the choreography
// stays readable: roll in, uncurl, run under the Deal card, look up and
// blink, curl back up, roll off. Runs once per LOOP_MS.
const hogSprite = document.querySelector(".hog-sprite");
if (hogSprite && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  const LOOP_MS = 19000;
  const easeOut = (t) => 1 - Math.pow(1 - t, 3);
  const easeIn = (t) => t * t * t;

  const PHASES = [
    { dur: 1700, row: 0, fps: 28, from: -0.14, to: 0.30, ease: easeOut },
    { dur: 420,  row: 1, fps: 0,  from: 0.30,  to: 0.30, ramp: 6 },
    { dur: 1750, row: 2, fps: 16, from: 0.30,  to: 0.68 },
    // look up at the card, hold, blink, twitch an ear, settle
    { dur: 3600, row: 3, fps: 0,  from: 0.68,  to: 0.68,
      script: [0, 1, 2, 2, 2, 3, 2, 2, 4, 2, 5, 5, 6, 5, 5, 7, 7, 7] },
    { dur: 400,  row: 1, fps: 0,  from: 0.68,  to: 0.68, ramp: 6, reverse: true },
    { dur: 1500, row: 0, fps: 28, from: 0.68,  to: 1.16, ease: easeIn },
  ];
  const ACTIVE = PHASES.reduce((n, p) => n + p.dur, 0);
  const LOOK_PHASE = PHASES[3];

  const unit = () => parseFloat(getComputedStyle(heroScene).getPropertyValue("--px-unit")) || 4;
  const dealCard = document.querySelector(".spot-card");
  const buyBtn = dealCard && dealCard.querySelector(".g-buy");
  let t0 = performance.now();
  let lastCell = "";
  let noticing = false;

  // the card reacts while the mascot is stopped underneath looking up
  function setNoticed(on) {
    if (on === noticing) return;
    noticing = on;
    if (dealCard) dealCard.classList.toggle("is-noticed", on);
    if (on && buyBtn) {
      buyBtn.classList.remove("is-pulsing");
      void buyBtn.offsetWidth;                 // restart the one-shot pulse
      buyBtn.classList.add("is-pulsing");
    }
  }

  function frame(now) {
    requestAnimationFrame(frame);
    if (!sceneVisible) { t0 = now; return; }

    let t = (now - t0) % LOOP_MS;
    if (t > ACTIVE) {                      // resting between passes
      if (hogSprite.style.opacity !== "0") hogSprite.style.opacity = "0";
      setNoticed(false);
      return;
    }
    if (hogSprite.style.opacity !== "1") hogSprite.style.opacity = "1";

    let ph = PHASES[0];
    for (const p of PHASES) {
      if (t < p.dur) { ph = p; break; }
      t -= p.dur;
    }
    const prog = t / ph.dur;
    setNoticed(ph === LOOK_PHASE);

    let col;
    if (ph.script) {
      col = ph.script[Math.min(ph.script.length - 1, Math.floor(prog * ph.script.length))];
    } else if (ph.ramp) {
      const i = Math.min(ph.ramp - 1, Math.floor(prog * ph.ramp));
      col = ph.reverse ? ph.ramp - 1 - i : i;
    } else {
      const n = ph.row === 0 ? 12 : 8;
      col = Math.floor((t / 1000) * ph.fps) % n;
    }

    const u = unit();
    const cell = `${-col * 48 * u}px ${-ph.row * 34 * u}px`;
    if (cell !== lastCell) { hogSprite.style.backgroundPosition = cell; lastCell = cell; }

    const e = ph.ease ? ph.ease(prog) : prog;
    const x = (ph.from + (ph.to - ph.from) * e) * heroScene.clientWidth;
    hogSprite.style.transform = `translate3d(${Math.round(x)}px,0,0)`;
  }
  requestAnimationFrame(frame);
}

// ============ gentle parallax on the hero layers ============
const parallaxLayers = [
  [document.querySelector(".scene-sky"), 0.06],
  [document.querySelector(".scene-clouds"), 0.10],
  [document.querySelector(".scene-pines"), 0.17],
].filter(([el]) => el);
if (parallaxLayers.length && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  let queued = false;
  addEventListener("scroll", () => {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => {
      queued = false;
      const y = window.scrollY;
      if (y > window.innerHeight) return;
      for (const [el, rate] of parallaxLayers) {
        el.style.transform = `translate3d(0,${(y * rate).toFixed(1)}px,0)`;
      }
    });
  }, { passive: true });
}

// ============ scroll reveal ============
const revealEls = document.querySelectorAll(".g-card, .step-card, .trust-card, .review-card");
if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  revealEls.forEach((el) => el.classList.add("reveal"));
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          entry.target.style.transitionDelay = `${Math.min(i * 40, 200)}ms`;
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );
  revealEls.forEach((el) => io.observe(el));
} else {
  revealEls.forEach((el) => el.classList.add("is-visible"));
}

// ============ reusable card components ============
const fmt = (n) => "$" + n.toFixed(2);
const discountPct = (g) => Math.round((1 - g.price / g.priceOriginal) * 100);
const coverGradient = (g) =>
  `linear-gradient(135deg, hsl(${g.hues[0]} 45% 22%), hsl(${g.hues[1]} 55% 38%))`;

const shieldIcon = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>`;
const boltIcon = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"/></svg>`;

function ownersLabel(g) {
  return g.owners === 1 ? "1 previous owner" : `${g.owners} previous owners`;
}

function gameCard(g, { tag = null } = {}) {
  return `
    <article class="game-card reveal">
      <div class="game-cover" style="background:${coverGradient(g)}">
        <span class="discount-badge">-${discountPct(g)}%</span>
        <span class="cover-title">${g.title}</span>
      </div>
      <div class="game-body">
        ${tag ? `<span class="deal-tag">${boltIcon}${tag}</span>` : ""}
        <div class="game-meta-row">
          <h3 class="game-title-sm">${g.title}</h3>
          <span class="platform-badge">${g.platform}</span>
        </div>
        <span class="license-status">${shieldIcon}${g.condition} &middot; ${ownersLabel(g)}</span>
        <div class="price-row">
          <span class="price-original">${fmt(g.priceOriginal)}</span>
          <span class="price-current">${fmt(g.price)}</span>
        </div>
        <a href="#featured" class="btn btn-primary btn-sm" aria-label="Buy and download ${g.title} for ${fmt(g.price)}">Buy &amp; Download</a>
      </div>
    </article>`;
}

function heroCard(g) {
  return `
    <div class="hero-card">
      <span class="mini-cover" style="background:${coverGradient(g)}">${g.title.charAt(0)}</span>
      <div class="hero-card-meta">
        <span class="hc-title">${g.title}</span>
        <span class="hc-platform">${g.platform} &middot; ${g.condition}</span>
        <span class="hc-price"><s>${fmt(g.priceOriginal)}</s>${fmt(g.price)}</span>
      </div>
    </div>`;
}

// ============ render ============
document.getElementById("featured-grid").innerHTML = GAMES.map((g) => gameCard(g)).join("");
document.getElementById("deals-grid").innerHTML = DEALS.map((g) => gameCard(g, { tag: g.tag })).join("");
document.getElementById("hero-cards").innerHTML = GAMES.slice(0, 3).map(heroCard).join("");

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

// ============ weekly deals countdown ============
const countdownEl = document.getElementById("deals-countdown");
function nextMondayMidnight() {
  const now = new Date();
  const d = new Date(now);
  d.setDate(now.getDate() + ((8 - now.getDay()) % 7 || 7));
  d.setHours(0, 0, 0, 0);
  return d;
}
const dealsEnd = nextMondayMidnight();
function tick() {
  const ms = Math.max(0, dealsEnd - Date.now());
  const h = Math.floor(ms / 3600000);
  const m = Math.floor((ms % 3600000) / 60000);
  const s = Math.floor((ms % 60000) / 1000);
  const pad = (n) => String(n).padStart(2, "0");
  countdownEl.textContent = `${pad(h)}:${pad(m)}:${pad(s)}`;
}
tick();
setInterval(tick, 1000);

// ============ scroll reveal ============
const revealEls = document.querySelectorAll(".reveal, .step-card, .trust-card");
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
    { threshold: 0.12 }
  );
  revealEls.forEach((el) => io.observe(el));
} else {
  revealEls.forEach((el) => el.classList.add("is-visible"));
}

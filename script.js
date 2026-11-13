document.getElementById("year").textContent = new Date().getFullYear();

// Mobile navigation
const menu = document.querySelector(".menu-button");
const navs = document.querySelectorAll(".nav");
const setMenu = open => {
  menu.setAttribute("aria-expanded", String(open));
  navs.forEach(n => n.classList.toggle("open", open));
};
menu.addEventListener("click", () => setMenu(menu.getAttribute("aria-expanded") !== "true"));
navs.forEach(n => n.querySelectorAll("a").forEach(a => a.addEventListener("click", () => setMenu(false))));

// Journal filters
const filters = document.querySelectorAll(".filter");
const cards = [...document.querySelectorAll(".journal-card")];
const grid = document.querySelector(".journal-grid");
// Masonry that keeps reading order left-to-right: each photo goes into the shortest column
let colCount = 0;
const layout = (force) => {
  const n = innerWidth <= 760 ? 2 : innerWidth <= 1000 ? 3 : 4;
  if (n === colCount && !force) return;
  colCount = n;
  const cols = Array.from({ length: n }, () => { const c = document.createElement("div"); c.className = "journal-col"; return c; });
  const heights = new Array(n).fill(0);
  cards.forEach(card => {
    if (card.hidden) { cols[0].appendChild(card); return; }
    const img = card.querySelector("img");
    const i = heights.indexOf(Math.min(...heights));
    cols[i].appendChild(card);
    heights[i] += img.height / img.width + 0.12;
  });
  grid.replaceChildren(...cols);
  grid.classList.add("is-masonry");
};
const applyFilter = type => {
  filters.forEach(b => b.classList.toggle("is-active", b.dataset.filter === type));
  cards.forEach(card => { card.hidden = type !== "all" && card.dataset.kind !== type; });
  layout(true);
};
layout(true);
addEventListener("resize", () => layout(false));
filters.forEach(b => b.addEventListener("click", () => applyFilter(b.dataset.filter)));

// "View the edit" links open the journal filtered to that edit
document.querySelectorAll("[data-show]").forEach(a => a.addEventListener("click", () => applyFilter(a.dataset.show)));

// Lightbox
const lb = document.getElementById("lightbox");
const lbImg = lb.querySelector("img");
let current = 0, lastFocus = null;
const visible = () => cards.filter(c => !c.hidden);
const show = i => {
  const list = visible();
  current = (i + list.length) % list.length;
  const card = list[current], img = card.querySelector("img");
  lbImg.src = img.dataset.full || img.src; lbImg.alt = img.alt;
  lb.querySelector(".lb-kind").textContent = card.querySelector("figcaption span").textContent;
  lb.querySelector(".lb-title").textContent = card.querySelector("figcaption b").textContent;
  lb.querySelector(".lb-count").textContent = String(current + 1).padStart(2, "0") + " / " + String(list.length).padStart(2, "0");
};
const open = card => {
  lastFocus = document.activeElement;
  show(visible().indexOf(card));
  lb.hidden = false; document.body.classList.add("no-scroll");
  lb.querySelector(".lb-close").focus();
};
const close = () => {
  lb.hidden = true; document.body.classList.remove("no-scroll");
  if (lastFocus) lastFocus.focus();
};
cards.forEach(card => {
  card.addEventListener("click", () => open(card));
  card.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(card); } });
});
lb.querySelector(".lb-close").addEventListener("click", close);
lb.querySelector(".lb-prev").addEventListener("click", () => show(current - 1));
lb.querySelector(".lb-next").addEventListener("click", () => show(current + 1));
lb.addEventListener("click", e => { if (e.target === lb || e.target.tagName === "FIGURE") close(); });
document.addEventListener("keydown", e => {
  if (lb.hidden) return;
  if (e.key === "Escape") close();
  if (e.key === "ArrowLeft") show(current - 1);
  if (e.key === "ArrowRight") show(current + 1);
});

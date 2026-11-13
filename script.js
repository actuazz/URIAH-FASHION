(() => {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const isDesktop = () => matchMedia("(min-width: 761px)").matches;
  document.querySelectorAll("[data-year]").forEach(n => (n.textContent = new Date().getFullYear()));

  /* ---------- header: transparent over the hero, solid after ---------- */
  const header = document.querySelector("[data-header]");
  const hero = document.querySelector(".hero");
  const setHeader = () => { if (!header.classList.contains("is-fixed-solid")) header.classList.toggle("is-solid", !hero || scrollY > hero.offsetHeight - 90); };

  /* ---------- menu ---------- */
  const menu = document.querySelector("[data-menu]");
  const openBtn = document.querySelector("[data-menu-open]");
  const toggleMenu = open => {
    menu.hidden = !open;
    openBtn.setAttribute("aria-expanded", String(open));
    document.body.classList.toggle("is-locked", open);
    if (open) menu.querySelector("a").focus(); else openBtn.focus();
  };
  openBtn.addEventListener("click", () => toggleMenu(true));
  menu.querySelector("[data-menu-close]").addEventListener("click", () => toggleMenu(false));
  menu.querySelectorAll("a").forEach(a => a.addEventListener("click", () => toggleMenu(false)));

  /* ---------- reveal on scroll ---------- */
  const io = new IntersectionObserver(entries => entries.forEach(en => {
    if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
  }), { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
  document.querySelectorAll(".reveal").forEach(n => io.observe(n));

  /* ---------- parallax depth + horizontal sequence ---------- */
  const floaters = [...document.querySelectorAll("[data-speed]")];
  const bleeds = [...document.querySelectorAll("[data-bleed]")];
  const hSections = [...document.querySelectorAll("[data-hscroll]")].map(sec => ({
    sec, track: sec.querySelector("[data-htrack]"), bar: sec.querySelector("[data-hprogress]"), dist: 0
  }));
  const sizeHorizontal = () => hSections.forEach(h => {
    if (!isDesktop() || reduce) { h.sec.style.height = ""; h.track.style.transform = ""; return; }
    h.dist = Math.max(0, h.track.scrollWidth - innerWidth);
    h.sec.style.height = `${innerHeight + h.dist}px`;
  });

  let ticking = false;
  const frame = () => {
    ticking = false;
    setHeader();
    const vh = innerHeight;
    if (!reduce) {
      for (const el of floaters) {
        const r = el.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) continue;
        const offset = (r.top + r.height / 2 - vh / 2) * -parseFloat(el.dataset.speed);
        el.style.translate = `0 ${offset.toFixed(1)}px`;
      }
      for (const el of bleeds) {
        const r = el.parentElement.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) continue;
        el.style.transform = `translate3d(0, ${((r.top / vh) * -6).toFixed(2)}%, 0)`;
      }
    }
    for (const h of hSections) {
      if (!h.dist) continue;
      const r = h.sec.getBoundingClientRect();
      const p = Math.min(1, Math.max(0, -r.top / h.dist));
      h.track.style.transform = `translate3d(${(-p * h.dist).toFixed(1)}px, 0, 0)`;
      if (h.bar) h.bar.style.width = `${(p * 100).toFixed(2)}%`;
    }
  };
  const request = () => { if (!ticking) { ticking = true; requestAnimationFrame(frame); } };
  addEventListener("scroll", request, { passive: true });
  addEventListener("resize", () => { sizeHorizontal(); request(); });
  addEventListener("load", () => { sizeHorizontal(); request(); });
  sizeHorizontal();
  frame();

  /* ---------- signature viewer: drag to turn ---------- */
  const stage = document.querySelector("[data-sig]");
  if (stage) {
    const frames = [...stage.querySelectorAll(".sig-frame")];
    const stops = [...document.querySelectorAll(".sig-stop")];
    const label = document.querySelector("[data-sig-label]");
    const count = document.querySelector("[data-sig-count]");
    const bar = document.querySelector("[data-sig-progress]");
    const last = frames.length - 1;
    let pos = 0, target = 0, dragging = false, startX = 0, startTarget = 0, touched = false, raf = 0, auto = 0, autoDir = 1, inView = false;
    const pad = n => String(n).padStart(2, "0");

    const render = () => {
      frames.forEach((f, i) => {
        const d = Math.abs(pos - i);
        const o = Math.max(0, 1 - d);
        f.style.opacity = o.toFixed(3);
        f.style.transform = `scale(${(1 + d * 0.025).toFixed(4)})`;
        f.style.zIndex = o > 0 ? Math.round(o * 10) : 0;
      });
      const nearest = Math.round(pos);
      label.textContent = frames[nearest].dataset.label;
      count.textContent = `${pad(nearest + 1)} / ${pad(frames.length)}`;
      stage.setAttribute("aria-valuenow", nearest + 1);
      stops.forEach((s, i) => s.classList.toggle("is-on", i <= nearest));
      bar.style.width = `${(pos / last) * 100}%`;
    };
    const loop = () => {
      // until someone touches it, the look turns by itself: rest on a view, then move on
      if (!dragging && !touched && inView && !reduce && performance.now() - auto > 2600) {
        auto = performance.now();
        if (target + autoDir > last || target + autoDir < 0) autoDir *= -1;
        target += autoDir;
      }
      pos += (target - pos) * (dragging ? 0.35 : 0.075);
      if (Math.abs(target - pos) < 0.0005) pos = target;
      render();
      raf = requestAnimationFrame(loop);
    };
    const touch = () => { if (!touched) { touched = true; stage.classList.add("is-touched"); } };
    const snap = () => { target = Math.min(last, Math.max(0, Math.round(target))); };

    stage.addEventListener("pointerdown", ev => {
      dragging = true; touch(); startX = ev.clientX; startTarget = target;
      stage.setPointerCapture(ev.pointerId); stage.classList.add("is-dragging");
    });
    stage.addEventListener("pointermove", ev => {
      if (!dragging) return;
      const per = stage.clientWidth / Math.max(1, last) * 0.9;
      target = Math.min(last, Math.max(0, startTarget - (ev.clientX - startX) / per));
    });
    const end = () => { if (!dragging) return; dragging = false; stage.classList.remove("is-dragging"); snap(); };
    stage.addEventListener("pointerup", end);
    stage.addEventListener("pointercancel", end);
    stage.addEventListener("keydown", ev => {
      if (ev.key === "ArrowRight" || ev.key === "ArrowLeft") {
        ev.preventDefault(); touch();
        target = Math.min(last, Math.max(0, Math.round(target) + (ev.key === "ArrowRight" ? 1 : -1)));
      }
    });
    stops.forEach((s, i) => s.addEventListener("click", () => { touch(); target = i; }));
    new IntersectionObserver(([en]) => {
      inView = en.isIntersecting;
      if (inView && !raf) raf = requestAnimationFrame(loop);
      if (!inView && raf) { cancelAnimationFrame(raf); raf = 0; }
    }, { threshold: 0.25 }).observe(stage);
    // warm the cache so turning never flickers
    frames.forEach(f => { f.loading = "eager"; });
    render();
  }

  /* ---------- collection: masonry that keeps reading order + chapter filters ---------- */
  const grids = [...document.querySelectorAll("[data-masonry]")].map(g => ({ g, cards: [...g.children], n: 0 }));
  const layoutGrids = force => grids.forEach(m => {
    const n = innerWidth <= 760 ? 2 : innerWidth <= 1100 ? 3 : 4;
    if (n === m.n && !force) return;
    m.n = n;
    const cols = Array.from({ length: n }, () => Object.assign(document.createElement("div"), { className: "cat-col" }));
    const h = new Array(n).fill(0);
    m.cards.forEach(card => {
      const im = card.querySelector("img");
      const i = h.indexOf(Math.min(...h));
      cols[i].appendChild(card);
      h[i] += im.height / im.width + 0.15;
    });
    m.g.replaceChildren(...cols);
  });
  if (grids.length) { layoutGrids(true); addEventListener("resize", () => layoutGrids(false)); }

  const filterBar = document.querySelector("[data-filters]");
  if (filterBar) {
    const chapters = [...document.querySelectorAll("[data-chapter].cat-chapter")];
    const buttons = [...filterBar.querySelectorAll(".filter")];
    const apply = (key, scroll) => {
      if (!buttons.some(b => b.dataset.filter === key)) key = "all";
      buttons.forEach(b => b.classList.toggle("is-active", b.dataset.filter === key));
      chapters.forEach(c => { c.hidden = key !== "all" && c.dataset.chapter !== key; });
      chapters.forEach(c => c.querySelectorAll(".reveal").forEach(r => r.classList.add("is-in")));
      if (scroll) scrollTo({ top: filterBar.offsetTop - 70, behavior: reduce ? "auto" : "smooth" });
    };
    buttons.forEach(b => b.addEventListener("click", () => {
      apply(b.dataset.filter, true);
      history.replaceState(null, "", b.dataset.filter === "all" ? location.pathname : `#ch-${b.dataset.filter}`);
    }));
    const fromHash = () => { const k = location.hash.replace("#ch-", ""); if (location.hash.startsWith("#ch-")) apply(k, true); };
    addEventListener("hashchange", fromHash);
    fromHash();
  }

  /* ---------- lightbox ---------- */
  const lb = document.querySelector("[data-lightbox]");
  const lbImg = lb.querySelector("[data-lb-img]");
  let items = [], cur = 0, lastFocus = null;
  const collect = () => {
    const seen = new Set();
    items = [...document.querySelectorAll(".piece[data-full]")]
      .filter(p => p.offsetParent !== null && !seen.has(p.dataset.full) && seen.add(p.dataset.full));
  };
  const show = i => {
    cur = (i + items.length) % items.length;
    const p = items[cur], im = p.querySelector("img");
    lbImg.src = p.dataset.full; lbImg.alt = im.alt;
    lb.querySelector("[data-lb-title]").textContent = p.dataset.title;
    lb.querySelector("[data-lb-chapter]").textContent = p.dataset.chapter;
    lb.querySelector("[data-lb-count]").textContent = `${String(cur + 1).padStart(2, "0")} / ${String(items.length).padStart(2, "0")}`;
  };
  const open = p => { collect(); lastFocus = document.activeElement; show(items.findIndex(x => x.dataset.full === p.dataset.full)); lb.hidden = false; document.body.classList.add("is-locked"); lb.querySelector("[data-lb-close]").focus(); };
  const close = () => { lb.hidden = true; document.body.classList.remove("is-locked"); lastFocus && lastFocus.focus(); };
  document.querySelectorAll(".piece[data-full]").forEach(p => {
    p.addEventListener("click", () => open(p));
    p.addEventListener("keydown", ev => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); open(p); } });
  });
  lb.querySelector("[data-lb-close]").addEventListener("click", close);
  lb.querySelector("[data-lb-prev]").addEventListener("click", () => show(cur - 1));
  lb.querySelector("[data-lb-next]").addEventListener("click", () => show(cur + 1));
  lb.addEventListener("click", ev => { if (ev.target === lb || ev.target.classList.contains("lb-figure")) close(); });
  document.addEventListener("keydown", ev => {
    if (!menu.hidden && ev.key === "Escape") toggleMenu(false);
    if (lb.hidden) return;
    if (ev.key === "Escape") close();
    if (ev.key === "ArrowLeft") show(cur - 1);
    if (ev.key === "ArrowRight") show(cur + 1);
  });
})();

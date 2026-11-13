(() => {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.querySelectorAll("[data-year]").forEach(n => (n.textContent = new Date().getFullYear()));

  /* header: transparent over the opening photo, solid after */
  const header = document.querySelector("[data-header]");
  const hero = document.querySelector(".hero");
  if (!hero) document.body.classList.add("page-plain");
  const setHeader = () => {
    if (header.classList.contains("is-fixed-solid")) return;
    header.classList.toggle("is-solid", !hero || scrollY > hero.offsetHeight - 90);
  };
  addEventListener("scroll", setHeader, { passive: true });
  setHeader();

  /* menu */
  const menu = document.querySelector("[data-menu]");
  const openBtn = document.querySelector("[data-menu-open]");
  const setMenu = open => {
    menu.hidden = !open;
    openBtn.setAttribute("aria-expanded", String(open));
    document.body.classList.toggle("is-locked", open);
    (open ? menu.querySelector("a") : openBtn).focus();
  };
  openBtn.addEventListener("click", () => setMenu(true));
  menu.querySelector("[data-menu-close]").addEventListener("click", () => setMenu(false));
  menu.querySelectorAll("a").forEach(a => a.addEventListener("click", () => setMenu(false)));

  /* gentle fade-in */
  if (reduce || !("IntersectionObserver" in window)) {
    document.querySelectorAll(".reveal").forEach(n => n.classList.add("is-in"));
  } else {
    const io = new IntersectionObserver(entries => entries.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
    }), { rootMargin: "0px 0px -6% 0px" });
    document.querySelectorAll(".reveal").forEach(n => io.observe(n));
  }

  /* the looks: a sliding strip that drifts on its own, can be swiped or dragged, and paused */
  const frame = document.querySelector("[data-strip]");
  if (frame) {
    const strip = frame.querySelector("[data-strip-scroll]");
    const toggle = frame.querySelector("[data-strip-toggle]");
    let paused = reduce, hover = false, holdUntil = 0, last = 0, acc = 0;
    const setPaused = v => {
      paused = v; frame.classList.toggle("is-paused", v);
      toggle.setAttribute("aria-pressed", String(v));
      toggle.setAttribute("aria-label", v ? "Play the sliding photographs" : "Pause the sliding photographs");
    };
    setPaused(paused);
    toggle.addEventListener("click", () => setPaused(!paused));
    strip.addEventListener("mouseenter", () => { hover = true; });
    strip.addEventListener("mouseleave", () => { hover = false; });
    const hold = () => { holdUntil = performance.now() + 2500; };
    strip.addEventListener("touchstart", hold, { passive: true });
    strip.addEventListener("wheel", hold, { passive: true });
    // drag with the mouse
    let down = false, startX = 0, startLeft = 0, moved = false;
    strip.addEventListener("mousedown", ev => { down = true; moved = false; startX = ev.clientX; startLeft = strip.scrollLeft; strip.classList.add("is-dragging"); ev.preventDefault(); });
    addEventListener("mousemove", ev => { if (!down) return; const dx = ev.clientX - startX; if (Math.abs(dx) > 4) moved = true; strip.scrollLeft = startLeft - dx; hold(); });
    addEventListener("mouseup", () => { down = false; strip.classList.remove("is-dragging"); });
    strip.addEventListener("click", ev => { if (moved) { ev.preventDefault(); moved = false; } }, true);
    const loop = t => {
      const dt = last ? Math.min(64, t - last) : 0; last = t;
      const half = strip.scrollWidth / 2;
      if (!paused && !hover && !down && t > holdUntil) {
        acc += dt * 0.045;                 // about 45 px per second
        const step = Math.floor(acc); acc -= step;
        if (step) strip.scrollLeft += step;
      }
      if (half && strip.scrollLeft >= half) strip.scrollLeft -= half;
      if (strip.scrollLeft <= 0 && half) strip.scrollLeft += half;
      requestAnimationFrame(loop);
    };
    strip.scrollLeft = 1;
    requestAnimationFrame(loop);
  }

  /* journal: masonry that keeps reading order, plus look filters */
  const grid = document.querySelector("[data-masonry]");
  if (grid) {
    const cards = [...grid.children];
    let cols = 0;
    const layout = force => {
      const w = document.documentElement.clientWidth;
      const n = w <= 760 ? 2 : w <= 1100 ? 3 : 4;
      if (n === cols && !force) return;
      cols = n;
      const columns = Array.from({ length: n }, () => Object.assign(document.createElement("div"), { className: "journal-col" }));
      const h = new Array(n).fill(0);
      cards.forEach(card => {
        if (card.hidden) { columns[0].appendChild(card); return; }
        const im = card.querySelector("img");
        const i = h.indexOf(Math.min(...h));
        columns[i].appendChild(card);
        h[i] += im.height / im.width + 0.16;
      });
      grid.replaceChildren(...columns);
    };
    const buttons = [...document.querySelectorAll("[data-filters] .filter")];
    const panels = [...document.querySelectorAll("[data-panel]")];
    const apply = key => {
      if (!buttons.some(b => b.dataset.filter === key)) key = "all";
      buttons.forEach(b => b.classList.toggle("is-active", b.dataset.filter === key));
      panels.forEach(p => { p.hidden = p.dataset.panel !== key; });
      cards.forEach(c => { c.hidden = key !== "all" && c.dataset.kind !== key; });
      layout(true);
    };
    buttons.forEach(b => b.addEventListener("click", () => {
      apply(b.dataset.filter);
      history.replaceState(null, "", b.dataset.filter === "all" ? location.pathname : `#${b.dataset.filter}`);
    }));
    addEventListener("hashchange", () => apply(location.hash.slice(1)));
    addEventListener("resize", () => layout(false));
    addEventListener("load", () => layout(true));
    apply(location.hash.slice(1));
  }

  /* lightbox: the full photograph, among those currently shown */
  const lb = document.querySelector("[data-lightbox]");
  const lbImg = lb.querySelector("[data-lb-img]");
  let items = [], cur = 0, lastFocus = null;
  const show = i => {
    cur = (i + items.length) % items.length;
    const t = items[cur];
    lbImg.src = t.dataset.full; lbImg.alt = t.querySelector("img").alt;
    lb.querySelector("[data-lb-kicker]").textContent = t.dataset.kicker || "";
    lb.querySelector("[data-lb-title]").textContent = t.dataset.title || "";
    lb.querySelector("[data-lb-count]").textContent = `${String(cur + 1).padStart(2, "0")} / ${String(items.length).padStart(2, "0")}`;
  };
  const open = t => {
    items = [...document.querySelectorAll("[data-full]")].filter(x => !x.hidden);
    lastFocus = document.activeElement; show(items.indexOf(t));
    lb.hidden = false; document.body.classList.add("is-locked"); lb.querySelector("[data-lb-close]").focus();
  };
  const close = () => { lb.hidden = true; document.body.classList.remove("is-locked"); if (lastFocus) lastFocus.focus(); };
  document.querySelectorAll("[data-full]").forEach(t => {
    t.addEventListener("click", () => open(t));
    t.addEventListener("keydown", ev => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); open(t); } });
  });
  lb.querySelector("[data-lb-close]").addEventListener("click", close);
  lb.querySelector("[data-lb-prev]").addEventListener("click", () => show(cur - 1));
  lb.querySelector("[data-lb-next]").addEventListener("click", () => show(cur + 1));
  lb.addEventListener("click", ev => { if (ev.target === lb || ev.target.classList.contains("lb-figure")) close(); });
  document.addEventListener("keydown", ev => {
    if (!menu.hidden && ev.key === "Escape") setMenu(false);
    if (lb.hidden) return;
    if (ev.key === "Escape") close();
    if (ev.key === "ArrowLeft") show(cur - 1);
    if (ev.key === "ArrowRight") show(cur + 1);
  });
})();

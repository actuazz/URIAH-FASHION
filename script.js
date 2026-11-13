(() => {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.querySelectorAll("[data-year]").forEach(n => (n.textContent = new Date().getFullYear()));

  // a hairline under the header once the page moves
  const header = document.querySelector(".site-header");
  const onScroll = () => header.classList.toggle("is-scrolled", scrollY > 8);
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // gentle fade-in as sections arrive
  if (reduce || !("IntersectionObserver" in window)) {
    document.querySelectorAll(".reveal").forEach(n => n.classList.add("is-in"));
  } else {
    const io = new IntersectionObserver(entries => entries.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
    }), { rootMargin: "0px 0px -6% 0px" });
    document.querySelectorAll(".reveal").forEach(n => io.observe(n));
  }

  // lightbox: the full, uncropped photograph
  const lb = document.querySelector("[data-lightbox]");
  const tiles = [...document.querySelectorAll("[data-full]")];
  if (!lb || !tiles.length) return;
  const lbImg = lb.querySelector("[data-lb-img]");
  let cur = 0, lastFocus = null;
  const show = i => {
    cur = (i + tiles.length) % tiles.length;
    const t = tiles[cur];
    lbImg.src = t.dataset.full;
    lbImg.alt = t.querySelector("img").alt;
    lb.querySelector("[data-lb-caption]").textContent = t.dataset.caption || "";
    lb.querySelector("[data-lb-count]").textContent = `${cur + 1} / ${tiles.length}`;
  };
  const open = i => { lastFocus = document.activeElement; show(i); lb.hidden = false; document.body.classList.add("is-locked"); lb.querySelector("[data-lb-close]").focus(); };
  const close = () => { lb.hidden = true; document.body.classList.remove("is-locked"); if (lastFocus) lastFocus.focus(); };
  tiles.forEach((t, i) => {
    t.addEventListener("click", () => open(i));
    t.addEventListener("keydown", ev => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); open(i); } });
  });
  lb.querySelector("[data-lb-close]").addEventListener("click", close);
  lb.querySelector("[data-lb-prev]").addEventListener("click", () => show(cur - 1));
  lb.querySelector("[data-lb-next]").addEventListener("click", () => show(cur + 1));
  lb.addEventListener("click", ev => { if (ev.target === lb || ev.target.classList.contains("lb-figure")) close(); });
  document.addEventListener("keydown", ev => {
    if (lb.hidden) return;
    if (ev.key === "Escape") close();
    if (ev.key === "ArrowLeft") show(cur - 1);
    if (ev.key === "ArrowRight") show(cur + 1);
  });
})();

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

  /* the looks collage: glide in on arrival; pause/play */
  const collage = document.querySelector("[data-collage]");
  if (collage) {
    const toggle = collage.querySelector("[data-collage-toggle]");
    toggle.addEventListener("click", () => {
      const paused = collage.classList.toggle("is-paused");
      toggle.setAttribute("aria-pressed", String(paused));
      toggle.setAttribute("aria-label", paused ? "Play the moving photographs" : "Pause the moving photographs");
    });
    if (reduce || !("IntersectionObserver" in window)) collage.classList.add("is-in");
    else new IntersectionObserver(([en], obs) => { if (en.isIntersecting) { collage.classList.add("is-in"); obs.disconnect(); } }, { threshold: 0.2 }).observe(collage);
  }

  /* looks page: a vertical mood board (balanced columns, reading order kept) with look filters */
  const grid = document.querySelector("[data-masonry]");
  if (grid) {
    const cards = [...grid.children];
    let cols = 0;
    const ratio = el => el.dataset.ratio ? parseFloat(el.dataset.ratio) : (() => { const im = el.querySelector("img"); return im.height / im.width; })();
    const layout = force => {
      const w = document.documentElement.clientWidth;
      const n = w <= 760 ? 2 : w <= 1100 ? 3 : 4;
      if (n === cols && !force) return;
      cols = n;
      const columns = Array.from({ length: n }, () => Object.assign(document.createElement("div"), { className: "board-col" }));
      const h = new Array(n).fill(0);
      cards.forEach(card => {
        if (card.hidden) { columns[0].appendChild(card); return; }
        const i = h.indexOf(Math.min(...h));
        columns[i].appendChild(card);
        h[i] += ratio(card) + 0.03;
      });
      grid.replaceChildren(...columns);
    };
    addEventListener("resize", () => layout(false));
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

/* EMBLEM (placeholder, to be redesigned): an animated URIAH monogram field behind the signature quote */
(() => {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const va = new Image(); va.src = "assets/va-black.png";
  let paused = reduce;
  const tinted = {};
  function tint(color){                      // the monogram drawn in any colour
    if (tinted[color]) return tinted[color];
    const c = document.createElement("canvas"); c.width = va.width; c.height = va.height;
    const x = c.getContext("2d"); x.drawImage(va,0,0); x.globalCompositeOperation="source-in"; x.fillStyle=color; x.fillRect(0,0,c.width,c.height);
    return (tinted[color] = c);
  }
  function field(canvas, pal, alpha, threads){
    const ctx = canvas.getContext("2d");
    const GAP = 116;                         // lattice spacing in CSS px
    let w=0,h=0,dpr=1,items=[],t0=performance.now(),drift=0;
    const ptr = {x:-1e4,y:-1e4,on:false}, ripples=[];
    function layout(){
      dpr = Math.min(2, devicePixelRatio||1);
      w = canvas.clientWidth; h = canvas.clientHeight;
      canvas.width = Math.round(w*dpr); canvas.height = Math.round(h*dpr);
      items = [];
      const cols = Math.ceil(w/GAP)+3, rows = Math.ceil(h/(GAP*.5))+3;
      for (let r=-1;r<rows;r++) for (let c=-1;c<cols;c++){
        const kind = ((r%3)+3)%3===0 ? 0 : (((r+c)%2===0) ? 1 : 2);   // rows of monograms, then diamonds and points
        items.push({bx:c*GAP+(r%2?GAP/2:0), by:r*GAP*.5, kind, rot:0, s:1, a:0});
      }
    }
    function draw(now){
      const dt = Math.min(50, now - t0); t0 = now;
      if (!paused) drift = (drift + dt*0.012) % GAP;               // slow diagonal drift
      ctx.setTransform(dpr,0,0,dpr,0,0); ctx.clearRect(0,0,w,h);
      for (const rp of ripples) rp.r += dt*0.45;
      while (ripples.length && ripples[0].r > Math.hypot(w,h)) ripples.shift();
      if (threads){                                   // fine diagonal threads that weave through the lattice
        ctx.save(); ctx.globalAlpha = alpha*0.9; ctx.lineWidth = 0.6;
        const off = drift % GAP;
        for (let k=-Math.ceil(h/GAP)-2; k<Math.ceil(w/GAP)+3; k++){
          const x0 = k*GAP + off;
          ctx.strokeStyle = k%2 ? pal.diamond : pal.mono;
          ctx.beginPath(); ctx.moveTo(x0, -GAP); ctx.lineTo(x0 + h + 2*GAP, h + GAP); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(x0 + h + GAP, -GAP); ctx.lineTo(x0 - GAP, h + GAP); ctx.stroke();
        }
        ctx.restore();
      }
      for (const it of items){
        const x = (it.bx + drift) % (Math.ceil(w/GAP+2)*GAP) - GAP, y = (it.by + drift*.5) % (Math.ceil(h/(GAP*.5)+2)*GAP*.5) - GAP*.5;
        const d = Math.hypot(x-ptr.x, y-ptr.y);
        const near = ptr.on ? Math.max(0, 1 - d/170) : 0;
        let wave = 0; for (const rp of ripples){ const k = 1 - Math.abs(Math.hypot(x-rp.x,y-rp.y) - rp.r)/60; if (k>0) wave = Math.max(wave, k*(1-rp.r/900)); }
        const lift = Math.max(near, wave);
        const ease = paused && !ptr.on && !ripples.length ? 1 : 0.12;
        it.rot += ((it.kind===1 ? lift*Math.PI/2 : lift*0.35) - it.rot)*ease;
        it.s   += ((1 + lift*0.35) - it.s)*ease;
        it.a   += ((alpha + lift*alpha*2.6) - it.a)*ease;
        ctx.save(); ctx.translate(x,y); ctx.rotate(it.rot); ctx.scale(it.s,it.s); ctx.globalAlpha = Math.min(1,it.a);
        if (it.kind===0 && va.complete){ const img = tint(pal.mono), W=30, H=W*img.height/img.width; ctx.drawImage(img,-W/2,-H/2,W,H); }
        else if (it.kind===1){ ctx.strokeStyle=pal.diamond; ctx.lineWidth=1.1; ctx.beginPath(); ctx.moveTo(0,-9); ctx.lineTo(7,0); ctx.lineTo(0,9); ctx.lineTo(-7,0); ctx.closePath(); ctx.stroke(); }
        else { ctx.fillStyle=pal.dot; ctx.beginPath(); ctx.arc(0,0,1.6,0,Math.PI*2); ctx.fill(); }
        ctx.restore();
      }
      requestAnimationFrame(draw);
    }
    canvas.addEventListener("pointermove", e => { const r = canvas.getBoundingClientRect(); ptr.x=e.clientX-r.left; ptr.y=e.clientY-r.top; ptr.on=true; });
    canvas.addEventListener("pointerleave", () => { ptr.on=false; });
    canvas.addEventListener("pointerdown", e => { const r = canvas.getBoundingClientRect(); if (!reduce) ripples.push({x:e.clientX-r.left, y:e.clientY-r.top, r:0}); });
    addEventListener("resize", layout);
    const go = () => { layout(); requestAnimationFrame(draw); };
    va.complete ? go() : va.addEventListener("load", go, { once: true });
  }
  const sec=document.querySelector("#signature"); if (!sec) return; sec.style.position="relative"; sec.style.overflow="hidden";
  const cv=document.createElement("canvas"); cv.style.cssText="position:absolute;inset:0;width:100%;height:100%;display:block;z-index:0";
  sec.prepend(cv); [...sec.children].forEach(c=>{ if(c!==cv){ c.style.position="relative"; c.style.zIndex="1"; }});
  field(cv, {mono:"#16233f", diamond:"#b8603d", dot:"#5c2b4b"}, 0.15, false);
})();

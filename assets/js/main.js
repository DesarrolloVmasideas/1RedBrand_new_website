/* =========================================================
   1RedBrand Home — hilo rojo, parallax, 3D y secciones horizontales
   ========================================================= */
(() => {
  "use strict";
  const RB = window.RB;
  const html = document.documentElement;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = matchMedia("(hover: hover) and (pointer: fine)").matches;
  const G = window.gsap, ST = window.ScrollTrigger;
  const motion = !!(G && ST) && !reduce;
  if (G && ST) G.registerPlugin(ST);

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const t = (o) => (typeof o === "string" ? o : `<span lang="es">${o.es}</span><span lang="en">${o.en}</span>`);
  const bi = (es, en) => t({ es, en });
  const isDesk = () => innerWidth >= 960;

  /* ---------------- idioma ---------------- */
  try {
    const saved = localStorage.getItem("rb-lang");
    if (saved === "es" || saved === "en") { html.dataset.lang = saved; html.lang = saved; }
  } catch (e) {}
  const setLang = (l) => {
    html.dataset.lang = l; html.lang = l;
    try { localStorage.setItem("rb-lang", l); } catch (e) {}
    refreshAll();
  };
  $$("[data-lang-toggle]").forEach((b) =>
    b.addEventListener("click", () => setLang(html.dataset.lang === "es" ? "en" : "es")));

  /* ---------------- render de contenido ---------------- */
  // ciclo
  const nodesG = $("[data-nodes]");
  const NS = "http://www.w3.org/2000/svg";
  RB.steps.forEach((s, i) => {
    const a = (-90 + i * 72) * Math.PI / 180;
    const x = 200 + 150 * Math.cos(a), y = 200 + 150 * Math.sin(a);
    const g = document.createElementNS(NS, "g");
    g.setAttribute("class", "node");
    g.innerHTML = `<circle cx="${x}" cy="${y}" r="17"/><text x="${x}" y="${y}">${i + 1}</text>`;
    nodesG.appendChild(g);
  });
  $("[data-steps]").innerHTML = RB.steps.map((s, i) => `
    <li class="step"><span class="step__n">${i + 1}</span>
      <span class="step__t">${bi(s.es, s.en)}</span>
      <span class="step__m">${t(s.m)}</span></li>`).join("");

  // módulos
  const track = $("[data-track]");
  // el HTML trae una versión estática (para buscadores y motores de IA); se reemplaza aquí
  $$("[data-pre]", track).forEach((n) => n.remove());
  track.insertAdjacentHTML("beforeend", RB.modules.map((m, i) => `
    <article class="mod${m.feature ? " mod--feature" : ""}" id="mod-${m.id}" aria-label="${i + 1} / ${RB.modules.length}">
      <svg class="mod__glyph" viewBox="0 0 100 100" aria-hidden="true"><path d="${m.glyph}"/></svg>
      <h3 class="mod__name">${t(m.name)}</h3>
      <p class="mod__promise">${t(m.promise)}</p>
      <ol class="mod__how">${m.how.es.map((s, k) => `<li>${bi(s, m.how.en[k])}</li>`).join("")}</ol>
      <a class="mod__cta" href="/plataforma/${m.id}/">${t(m.cta)}</a>
    </article>`).join(""));
  const mods = $$(".mod", track);
  const dotsEl = $("[data-dots]");
  dotsEl.innerHTML = RB.modules.map((m, i) =>
    `<button class="dot" type="button" role="tab" aria-selected="${i === 0}" aria-label="${m.name.es}"></button>`).join("");
  const dots = $$(".dot", dotsEl);

  // industrias
  const rail = $("[data-ind-rail]");
  const curls = [
    "M10,190 C40,60 90,170 120,80 S190,10 170,110 C160,160 120,150 130,120",
    "M190,190 C160,90 100,160 80,90 C60,20 140,10 150,70 C160,130 40,140 20,60",
    "M20,40 C80,10 120,90 70,120 C30,145 60,190 120,170 S190,110 180,60"
  ];
  rail.innerHTML = RB.industries.map((d, i) => `
    <article class="ind" id="ind-${d.id}">
      <svg class="ind__bg" viewBox="0 0 200 200" aria-hidden="true"><path d="${curls[i % 3]}"/></svg>
      <h3 class="ind__name">${t(d.name)}</h3>
      <p class="ind__pain">${t(d.pain)}</p>
      <ul class="ind__mods">${d.mods.map((m) => `<li>${t(m)}</li>`).join("")}</ul>
      <a class="ind__cta" href="/industrias/${d.id}/">${bi("Ver " + d.name.es, "See " + d.name.en)}</a>
    </article>`).join("") + `
    <article class="ind ind--more" id="ind-mas">
      <span class="ind__plus" aria-hidden="true">+</span>
      <h3 class="ind__name">${bi("Y más", "And more")}</h3>
      <p class="ind__pain">${bi("Grupos hospitalarios, plazas comerciales y cualquier organización con identidad propia, en una ubicación o en muchas.",
        "Hospital groups, shopping centers and any organization with its own identity, in one location or many.")}</p>
      <a class="ind__cta" href="#demo">${bi("Cuéntanos de tu operación", "Tell us about your operation")}</a>
    </article>`;
  const inds = $$(".ind", rail);

  // footer
  $("[data-foot-modules]").innerHTML = RB.modules.map((m) => `<li><a href="/plataforma/${m.id}/">${t(m.name)}</a></li>`).join("");
  $("[data-foot-ind]").innerHTML = RB.industries.map((d) => `<li><a href="/industrias/${d.id}/">${t(d.name)}</a></li>`).join("");

  // título del hero en palabras (para la entrada orquestada)
  $$(".hero__title > span").forEach((s) => {
    s.innerHTML = s.textContent.trim().split(/\s+/).map((w) => `<span class="w">${w}</span>`).join(" ");
  });

  /* ---------------- header + menú ---------------- */
  const header = $(".site-header"), nav = $("#nav"), burger = $("[data-burger]");
  const closeMenu = () => {
    nav.classList.remove("is-open"); burger.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  };
  burger.addEventListener("click", () => {
    const open = !nav.classList.contains("is-open");
    nav.classList.toggle("is-open", open); burger.setAttribute("aria-expanded", String(open));
    document.body.style.overflow = open ? "hidden" : "";
  });
  $$("a", nav).forEach((a) => a.addEventListener("click", closeMenu));
  addEventListener("keydown", (e) => { if (e.key === "Escape") closeMenu(); });
  let lastY = scrollY;
  addEventListener("scroll", () => {
    const y = scrollY;
    header.classList.toggle("is-scrolled", y > 20);
    if (!nav.classList.contains("is-open"))
      header.classList.toggle("is-hidden", y > lastY && y > 300);
    lastY = y;
  }, { passive: true });

  /* =========================================================
     HILO ROJO
     Cada sección dibuja su tramo: entra por el carril izquierdo,
     pasa por sus anclas y sale donde entra la siguiente sección,
     así todos los tramos se leen como una sola línea continua.
     ========================================================= */
  const threads = new Map();
  const lane = () => (isDesk() ? Math.max(22, innerWidth * 0.035) : 12);

  // pulso de trazo a mano: oscilación pequeña que nunca sale del margen
  function sway(p) {
    const amp0 = isDesk() ? Math.min(16, lane() * 0.4) : 4;
    const out = [p[0]];
    for (let i = 1; i < p.length; i++) {
      const a = p[i - 1], b = p[i];
      const dx = b[0] - a[0], dy = b[1] - a[1], len = Math.hypot(dx, dy);
      if (len > 320) {
        const n = Math.min(4, Math.floor(len / 320));
        for (let k = 1; k <= n; k++) {
          const f = k / (n + 1), amp = amp0 * (k % 2 ? 1 : -1);
          out.push([a[0] + dx * f + (-dy / len) * amp, a[1] + dy * f + (dx / len) * amp]);
        }
      }
      out.push(b);
    }
    return out;
  }
  function crPath(p) {
    if (p.length < 2) return "";
    let d = `M${p[0][0].toFixed(1)},${p[0][1].toFixed(1)}`;
    for (let i = 0; i < p.length - 1; i++) {
      const p0 = p[i - 1] || p[i], p1 = p[i], p2 = p[i + 1], p3 = p[i + 2] || p2;
      const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
      const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
      d += ` C${c1[0].toFixed(1)},${c1[1].toFixed(1)} ${c2[0].toFixed(1)},${c2[1].toFixed(1)} ${p2[0].toFixed(1)},${p2[1].toFixed(1)}`;
    }
    return d;
  }
  const trackSvg = $("[data-track-thread]");
  let trackSeg = null;
  function anchorPts(el, base, L) {
    const r = el.getBoundingClientRect();
    const x = r.left - base.left, y = r.top - base.top;
    const at = el.dataset.at || "center";
    if (at === "trackline") {
      const t = trackSvg.getBoundingClientRect();
      return [[L, t.top - base.top + t.height - 20]];
    }
    if (at === "tail") { // remate: baja por el margen y subraya los botones
      const yy = y + r.height + 30;
      return [[L, yy - 70], [L + 30, yy], [x + r.width * 0.5, yy + 2], [x + r.width, yy]];
    }
    return [[x + r.width / 2, y + r.height / 2]];
  }
  function mkGroup(svg) {
    const g = document.createElementNS(NS, "g");
    const paths = ["t-shadow", "t-main", "t-hi"].map((c) => {
      const p = document.createElementNS(NS, "path"); p.setAttribute("class", c); g.appendChild(p); return p;
    });
    svg.appendChild(g);
    return { g, paths, len: 0 };
  }
  function setD(seg, d) {
    seg.paths.forEach((p) => p.setAttribute("d", d));
    seg.len = seg.paths[1].getTotalLength() || 1;
    seg.paths.forEach((p) => { p.style.strokeDasharray = `${seg.len} ${seg.len}`; });
  }
  function drawSeg(seg, p) {
    if (!seg) return;
    p = clamp(p);
    const off = seg.len * (1 - p);
    seg.paths.forEach((x) => { x.style.strokeDashoffset = off; });
    seg.g.style.opacity = p > 0.002 ? 1 : 0;
  }

  /* El hilo es una sola línea continua: cada sección entra en x=S y sale
     en x=E, y la siguiente entra exactamente donde terminó la anterior.
     Viaja por el margen izquierdo; solo deja el margen en zonas vacías. */
  function buildSection(sec, idx, S, E) {
    let svg = $(":scope > svg.thread", sec);
    if (!svg) {
      svg = document.createElementNS(NS, "svg");
      svg.setAttribute("class", "thread"); svg.setAttribute("aria-hidden", "true");
      sec.appendChild(svg);
    }
    svg.innerHTML = "";
    const base = sec.getBoundingClientRect();
    const w = sec.offsetWidth, h = sec.offsetHeight, L = lane();
    svg.setAttribute("viewBox", `0 0 ${w} ${h}`);

    const anchors = $$("[data-anchor]", sec).filter((el) => el.closest("[data-thread]") === sec && !el.closest("[data-track]"));
    const names = [...new Set(anchors.map((el) => el.dataset.seg || "a"))];
    if (!names.length) names.push("a");

    let gradId = null;
    if (sec.dataset.threadColor === "light") {
      gradId = `tg-${idx}`;
      const e = 70 / h, f = 100 / h;
      svg.insertAdjacentHTML("afterbegin", `<defs><linearGradient id="${gradId}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="${h}">
        <stop offset="0" stop-color="#de0b17"/><stop offset="${e}" stop-color="#de0b17"/><stop offset="${f}" stop-color="#fff"/>
        <stop offset="${1 - f}" stop-color="#fff"/><stop offset="${1 - e}" stop-color="#de0b17"/><stop offset="1" stop-color="#de0b17"/></linearGradient></defs>`);
    }

    let segPts;
    if (sec.dataset.threadStart === "origin") {
      // nace en el remate inferior del "1" del logotipo
      const m = $(".stage__mark", sec).getBoundingClientRect();
      const ox = m.left - base.left + m.width * 0.97, oy = m.top - base.top + m.height * 0.925;
      if (isDesk()) {
        segPts = [[[ox, oy], [ox + 16, oy + 22], [(ox + E) / 2 + 30, oy + (h - oy) * 0.55], [E, h - 40], [E, h + 1]]];
      } else {
        const c = $(".hero__ctas", sec).getBoundingClientRect();
        const gy = c.bottom - base.top + 46, R = w - 16;
        segPts = [[[ox, oy], [R, oy + 34], [R, gy - 60], [w * 0.55, gy], [L + 24, gy + 24], [L, gy + 80], [L, h + 1]]];
      }
    } else {
      segPts = names.map((name, i) => {
        const pts = [];
        if (i === 0) {
          if (Math.abs(S - L) > 4) {
            if (sec.dataset.threadIn === "ring") pts.push([S, 0], [S, 24]);
            else pts.push([S, 0], [S, 16], [(S + L) / 2, 44], [L, 82]); // vuelve al margen dentro del padding superior
          } else pts.push([L, 0], [L, 30]);
        }
        anchors.filter((el) => (el.dataset.seg || "a") === name).forEach((el) => {
          const ap = anchorPts(el, base, L);
          // en móvil el hilo baja por el margen y solo entra junto a su ancla
          const last = pts[pts.length - 1];
          if (!isDesk() && last && ap[0][1] - last[1] > 140 && ap[0][0] - L > 40) pts.push([L, ap[0][1] - 56]);
          pts.push(...ap);
        });
        if (i === names.length - 1 && sec.dataset.threadEnd !== "stop") pts.push([E, h - 30], [E, h + 1]);
        return pts;
      });
    }
    const segs = segPts.map((pts) => {
      const seg = mkGroup(svg);
      setD(seg, crPath(sway(pts)));
      if (gradId) seg.paths[1].style.stroke = `url(#${gradId})`;
      return seg;
    });
    const st = threads.get(sec) || { p: 0, apply: null };
    st.segs = segs;
    threads.set(sec, st);
    return st;
  }
  function drawSection(sec, p) {
    const st = threads.get(sec); if (!st) return;
    st.p = p;
    const total = st.segs.reduce((a, s) => a + s.len, 0);
    let acc = 0;
    st.segs.forEach((s) => { drawSeg(s, (p * total - acc) / s.len); acc += s.len; });
  }

  // tramo horizontal bajo las tarjetas de módulos: una onda suave, sin nudos
  function buildTrack() {
    const w = track.scrollWidth, h = track.offsetHeight + 46;
    trackSvg.setAttribute("width", w); trackSvg.setAttribute("height", h);
    trackSvg.setAttribute("viewBox", `0 0 ${w} ${h}`);
    trackSvg.innerHTML = "";
    trackSeg = mkGroup(trackSvg);
    const y = h - 20, pts = [[0, y]];
    mods.forEach((m, i) => pts.push([m.offsetLeft + m.offsetWidth / 2, y + (i % 2 ? 7 : -7)]));
    pts.push([w, y]);
    setD(trackSeg, crPath(pts));
  }

  function buildAll() {
    buildTrack();
    const secs = $$("[data-thread]"), L = lane();
    const rr = $("[data-ring]").getBoundingClientRect();
    const ringX = rr.left + rr.width / 2;
    // fronteras: en escritorio el hilo baja del hero al anillo y del anillo a módulos
    const bx = secs.map((s, i) => {
      const next = secs[i + 1];
      if (!isDesk() || !next) return L;
      if (next.dataset.threadIn === "ring" || s.dataset.threadIn === "ring") return ringX;
      return L;
    });
    secs.forEach((s, i) => buildSection(s, i, i ? bx[i - 1] : L, bx[i]));
    threads.forEach((st, sec) => (st.apply ? st.apply() : drawSection(sec, st.p)));
    if (trackApply) trackApply();
  }
  let trackApply = null;

  function refreshAll() {
    if (G && ST) ST.refresh(); else buildAll();
  }

  /* =========================================================
     CICLO (anclado: el anillo se dibuja y activa cada paso)
     ========================================================= */
  const ring = $("[data-ring]");
  const ringPaths = $$(".ring__draw path", ring);
  const ringLen = ringPaths[1].getTotalLength();
  ringPaths.forEach((p) => { p.style.strokeDasharray = `${ringLen} ${ringLen}`; });
  const nodeEls = $$(".node", ring), stepEls = $$(".step"), ringN = $("[data-ring-n]"), ringT = $("[data-ring-t]");
  let activeStep = -1;
  function setStep(i) {
    if (i === activeStep) return;
    activeStep = i;
    nodeEls.forEach((n, k) => n.classList.toggle("is-on", k <= i));
    stepEls.forEach((n, k) => n.classList.toggle("is-on", k === i));
    const s = RB.steps[Math.max(0, i)];
    ringN.textContent = `${Math.max(0, i) + 1}/5`;
    ringT.innerHTML = `${bi(s.es, s.en)}<br><small style="opacity:.7;font-size:.65em">${t(s.m)}</small>`;
  }
  function drawRing(p) {
    const off = ringLen * (1 - clamp(p));
    ringPaths.forEach((x) => { x.style.strokeDashoffset = off; });
    $(".ring__draw", ring).style.opacity = p > 0.002 ? 1 : 0;
  }
  setStep(0);

  /* =========================================================
     MÓDULOS: arco 3D (cilindro) + navegación horizontal
     ========================================================= */
  const hscroll = $("[data-hscroll]");
  const modSec = $(".modules");
  let trackX = 0;
  function arc() {
    if (reduce) return;
    const left = hscroll.getBoundingClientRect().left + trackX - hscroll.scrollLeft;
    const half = innerWidth / 2;
    let best = 0, bestD = 1e9;
    mods.forEach((m, i) => {
      const c = left + m.offsetLeft + m.offsetWidth / 2;
      const d = clamp((c - half) / half, -1.7, 1.7);
      if (Math.abs(d) < bestD) { bestD = Math.abs(d); best = i; }
      m.style.transform = `translate3d(0,${(d * d * 34).toFixed(1)}px,${(-Math.abs(d) * 170).toFixed(1)}px) rotateY(${(-d * 30).toFixed(2)}deg)`;
    });
    dots.forEach((b, i) => b.setAttribute("aria-selected", String(i === best)));
  }
  let pinST = null;
  dots.forEach((b, i) => b.addEventListener("click", () => {
    if (pinST && isDesk()) {
      const y = pinST.start + (pinST.end - pinST.start) * (i / (mods.length - 1));
      scrollTo({ top: y, behavior: reduce ? "auto" : "smooth" });
    } else {
      const m = mods[i];
      hscroll.scrollTo({ left: m.offsetLeft - (hscroll.clientWidth - m.offsetWidth) / 2, behavior: reduce ? "auto" : "smooth" });
    }
  }));
  hscroll.addEventListener("scroll", () => {
    arc();
    if (!pinST) {
      const max = hscroll.scrollWidth - hscroll.clientWidth;
      drawSeg(trackSeg, 0.12 + 0.88 * (max > 0 ? hscroll.scrollLeft / max : 1));
    }
  }, { passive: true });

  /* =========================================================
     INDUSTRIAS: paneles inclinados en perspectiva
     ========================================================= */
  const bar = $("[data-ind-bar]");
  function tiltRail() {
    const pad = parseFloat(getComputedStyle(rail).paddingLeft);
    inds.forEach((c) => {
      const d = (c.offsetLeft - rail.scrollLeft - pad) / rail.clientWidth;
      if (reduce) return;
      const dd = clamp(d, -1, 1.3);
      const rot = dd > 0 ? -dd * 26 : -dd * 18;
      c.style.transform = `rotateY(${rot.toFixed(2)}deg) translateZ(${(-Math.abs(dd) * 110).toFixed(1)}px)`;
      c.style.opacity = dd < -0.4 ? String(clamp(1 + (dd + 0.4) * 1.6, 0.25, 1)) : "1";
    });
    bar.style.transform = `scaleX(${clamp((rail.clientWidth + rail.scrollLeft) / rail.scrollWidth, 0.1, 1)})`;
  }
  rail.addEventListener("scroll", tiltRail, { passive: true });
  const step = () => (inds[0].offsetWidth + 22);
  $("[data-ind-prev]").addEventListener("click", () => rail.scrollBy({ left: -step(), behavior: reduce ? "auto" : "smooth" }));
  $("[data-ind-next]").addEventListener("click", () => rail.scrollBy({ left: step(), behavior: reduce ? "auto" : "smooth" }));
  rail.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") { e.preventDefault(); rail.scrollBy({ left: step(), behavior: "smooth" }); }
    if (e.key === "ArrowLeft") { e.preventDefault(); rail.scrollBy({ left: -step(), behavior: "smooth" }); }
  });

  /* =========================================================
     CONTADORES
     ========================================================= */
  const fmt = (el, v) => {
    const dec = +(el.dataset.dec || 0);
    const n = dec ? v.toFixed(dec) : Math.round(v).toLocaleString("en-US");
    el.textContent = `${el.dataset.prefix || ""}${n}${el.dataset.suffix || ""}`;
  };
  const counters = $$("[data-count]");

  /* =========================================================
     SIN MOVIMIENTO: todo visible y estático
     ========================================================= */
  if (!motion) {
    const still = () => {
      buildAll();
      threads.forEach((st, sec) => drawSection(sec, 1));
      drawSeg(trackSeg, 1); drawRing(1);
      stepEls.forEach((s) => s.classList.add("is-on")); nodeEls.forEach((n) => n.classList.add("is-on"));
    };
    counters.forEach((el) => fmt(el, +el.dataset.count));
    addEventListener("load", still); addEventListener("resize", still);
    tiltRail(); arc();
    return;
  }

  /* =========================================================
     CON MOVIMIENTO (GSAP + ScrollTrigger)
     ========================================================= */
  html.style.scrollBehavior = "smooth";
  ST.config({ ignoreMobileResize: true });

  // --- entrada orquestada: palabras + primer trazo desde el "1" ---
  const hero = $(".hero");
  const heroSt = { intro: 0, s: 0 };
  const heroApply = () => drawSection(hero, heroSt.intro * 0.42 + heroSt.s * 0.58);
  threads.set(hero, { p: 0, segs: [], apply: heroApply });
  G.from(".hero__title .w", { yPercent: 70, opacity: 0, rotate: 3, duration: 1, ease: "expo.out", stagger: 0.035, delay: 0.15 });
  G.from(".hero__sub, .hero__ctas, .proof", { y: 24, opacity: 0, duration: 0.9, ease: "power3.out", stagger: 0.1, delay: 0.55 });
  G.from(".stage__mark", { opacity: 0, rotateY: -35, z: -200, duration: 1.4, ease: "expo.out" });
  G.from(".tile", { opacity: 0, scale: 0.9, duration: 1, ease: "expo.out", stagger: 0.09, delay: 0.5 });
  G.to(heroSt, { intro: 1, duration: 1.8, ease: "power2.inOut", delay: 0.6, onUpdate: heroApply });
  G.to(heroSt, { s: 1, ease: "none", onUpdate: heroApply,
    scrollTrigger: { trigger: hero, start: "top top", end: "bottom 72%", scrub: 0.6 } });

  // --- escenario 3D del hero: profundidad por puntero y por scroll ---
  const inner = $("[data-stage-inner]");
  $$(".tile", inner).forEach((tl) => G.set(tl, { z: parseFloat(tl.style.getPropertyValue("--z")) || 0 }));
  if (finePointer) {
    addEventListener("pointermove", (e) => {
      G.to(inner, { rotateY: (e.clientX / innerWidth - 0.5) * 8, rotateX: (e.clientY / innerHeight - 0.5) * -5, duration: 0.9, ease: "power3.out" });
    }, { passive: true });
  }
  $$(".tile", inner).forEach((tl) => {
    const z = parseFloat(tl.style.getPropertyValue("--z")) || 60;
    G.to(tl, { y: -z * 0.9, ease: "none", scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: true } });
  });

  // --- secciones genéricas: el hilo avanza con el scroll ---
  $$("[data-thread]").forEach((sec) => {
    if (sec === hero || sec.dataset.pin) return;
    const pr = { p: 0 };
    const st = threads.get(sec) || { p: 0, segs: [] };
    st.apply = () => drawSection(sec, pr.p);
    threads.set(sec, st);
    G.to(pr, { p: 1, ease: "none", onUpdate: st.apply,
      scrollTrigger: { trigger: sec, start: "top 72%", end: "bottom 72%", scrub: 0.6 } });
  });

  // --- ciclo anclado ---
  const cyc = $(".cycle");
  const cy = { a: 0, p: 0 };
  const cycApply = () => {
    const segs = threads.get(cyc)?.segs || [];
    drawSeg(segs[0], cy.a);
    const r = clamp((cy.p - 0.04) / 0.82);
    drawRing(r);
    setStep(Math.min(4, Math.floor(r * 4.999)));
    drawSeg(segs[1], (cy.p - 0.88) / 0.12);
  };
  threads.set(cyc, { p: 0, segs: [], apply: cycApply });
  G.to(cy, { a: 1, ease: "none", onUpdate: cycApply, scrollTrigger: { trigger: cyc, start: "top 72%", end: "top top", scrub: 0.5 } });
  G.to(cy, { p: 1, ease: "none", onUpdate: cycApply,
    scrollTrigger: { trigger: cyc, start: "top top", end: "+=240%", pin: true, scrub: 0.6, anticipatePin: 1 } });

  // --- módulos: horizontal anclado en escritorio, swipe nativo en móvil ---
  const mm = G.matchMedia();
  const md = { a: 0, p: 0, m: 0 };
  const modApply = () => {
    const segs = threads.get(modSec)?.segs || [];
    if (pinST) {
      drawSeg(segs[0], md.a);
      drawSeg(segs[1], (md.p - 0.9) / 0.1);
    } else {
      drawSection(modSec, md.m);
    }
  };
  threads.set(modSec, { p: 0, segs: [], apply: modApply });
  mm.add("(min-width: 960px)", () => {
    modSec.classList.add("is-pinned-h");
    const dist = () => Math.max(0, track.scrollWidth - innerWidth);
    const a = G.to(md, { a: 1, ease: "none", onUpdate: modApply, scrollTrigger: { trigger: modSec, start: "top 72%", end: "top top", scrub: 0.5 } });
    const tw = G.to(md, {
      p: 1, ease: "none",
      onUpdate: () => {
        trackX = -dist() * md.p;
        track.style.transform = `translate3d(${trackX}px,0,0)`;
        arc(); drawSeg(trackSeg, 0.1 + 0.9 * md.p); modApply();
      },
      scrollTrigger: { trigger: modSec, start: "top top", end: () => "+=" + dist() * 1.15, pin: true, scrub: 0.7, invalidateOnRefresh: true, anticipatePin: 1 }
    });
    pinST = tw.scrollTrigger;
    trackApply = () => { drawSeg(trackSeg, 0.1 + 0.9 * md.p); arc(); };
    return () => {
      modSec.classList.remove("is-pinned-h");
      pinST = null; trackX = 0; track.style.transform = "";
      a.scrollTrigger && a.scrollTrigger.kill(); a.kill();
      tw.scrollTrigger && tw.scrollTrigger.kill(); tw.kill();
    };
  });
  mm.add("(max-width: 959px)", () => {
    const tw = G.to(md, { m: 1, ease: "none", onUpdate: modApply, scrollTrigger: { trigger: modSec, start: "top 72%", end: "bottom 72%", scrub: 0.6 } });
    trackApply = () => {
      const max = hscroll.scrollWidth - hscroll.clientWidth;
      drawSeg(trackSeg, 0.12 + 0.88 * (max > 0 ? hscroll.scrollLeft / max : 1)); arc();
    };
    return () => { tw.scrollTrigger && tw.scrollTrigger.kill(); tw.kill(); };
  });

  // --- industrias: el carril entra deslizándose al hacer scroll ---
  G.fromTo(rail, { x: 120 }, { x: 0, ease: "none", scrollTrigger: { trigger: ".industries", start: "top bottom", end: "top 25%", scrub: 0.6 } });

  // --- parallax por capas ---
  $$("[data-speed]").forEach((el) => {
    if (el.hasAttribute("data-anchor")) return; // los anclajes del hilo se quedan quietos
    const sp = +el.dataset.speed;
    G.fromTo(el, { y: 50 * sp }, { y: -50 * sp, ease: "none",
      scrollTrigger: { trigger: el.closest("section"), start: "top bottom", end: "bottom top", scrub: true } });
  });
  G.fromTo(".result", { y: 50 }, { y: -30, ease: "none", scrollTrigger: { trigger: ".results", start: "top bottom", end: "bottom top", scrub: true } });
  G.fromTo(".final h2", { scale: 0.92, opacity: 0.3 }, { scale: 1, opacity: 1, ease: "none", transformOrigin: "left center",
    scrollTrigger: { trigger: ".final", start: "top 85%", end: "top 30%", scrub: true } });

  // --- contadores ---
  counters.forEach((el) => {
    const o = { v: 0 };
    ST.create({ trigger: el, start: "top 85%", once: true,
      onEnter: () => G.to(o, { v: +el.dataset.count, duration: 2, ease: "power3.out", onUpdate: () => fmt(el, o.v) }) });
  });

  // --- reconstruir el hilo cada vez que cambia el layout ---
  ST.addEventListener("refresh", buildAll);
  buildAll(); tiltRail(); arc();
  addEventListener("load", () => ST.refresh());
  document.fonts && document.fonts.ready.then(() => ST.refresh());
})();

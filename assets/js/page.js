/* =========================================================
   1RedBrand — páginas interiores (sin dependencias)
   Hilo único: nace en el glifo del hero, cruza en el espacio
   vacío bajo el hero, baja por el margen, enhebra los nodos
   [data-node] y termina subrayando [data-tail].
   ========================================================= */
(() => {
  "use strict";
  const html = document.documentElement;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
  const isDesk = () => innerWidth >= 960;
  const NS = "http://www.w3.org/2000/svg";

  /* ---------- idioma ---------- */
  try {
    const saved = localStorage.getItem("rb-lang");
    if (saved === "es" || saved === "en") { html.dataset.lang = saved; html.lang = saved; }
  } catch (e) {}
  $$("[data-lang-toggle]").forEach((b) => b.addEventListener("click", () => {
    const l = html.dataset.lang === "es" ? "en" : "es";
    html.dataset.lang = l; html.lang = l;
    try { localStorage.setItem("rb-lang", l); } catch (e) {}
    schedule();
  }));

  /* ---------- header y menú ---------- */
  const header = $(".site-header"), nav = $("#nav"), burger = $("[data-burger]");
  const closeMenu = () => { nav.classList.remove("is-open"); burger.setAttribute("aria-expanded", "false"); document.body.style.overflow = ""; };
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
    if (!nav.classList.contains("is-open")) header.classList.toggle("is-hidden", y > lastY && y > 300);
    lastY = y;
  }, { passive: true });

  /* ---------- hilo ---------- */
  const main = $("main");
  const svg = document.createElementNS(NS, "svg");
  svg.setAttribute("class", "page-thread"); svg.setAttribute("aria-hidden", "true");
  main.prepend(svg);
  let paths = [], total = 1, samples = [], nodes = [], intro = reduce ? 1 : 0;

  function crPath(p) {
    let d = `M${p[0][0].toFixed(1)},${p[0][1].toFixed(1)}`;
    for (let i = 0; i < p.length - 1; i++) {
      const p0 = p[i - 1] || p[i], p1 = p[i], p2 = p[i + 1], p3 = p[i + 2] || p2;
      // asas limitadas al largo del tramo: evita rizos cuando el siguiente punto está lejos
      const seg = Math.hypot(p2[0] - p1[0], p2[1] - p1[1]);
      const cap = (v) => { const l = Math.hypot(v[0], v[1]), m = seg * 0.42; return l > m ? [v[0] * m / l, v[1] * m / l] : v; };
      const v1 = cap([(p2[0] - p0[0]) / 6, (p2[1] - p0[1]) / 6]);
      const v2 = cap([(p3[0] - p1[0]) / 6, (p3[1] - p1[1]) / 6]);
      const c1 = [p1[0] + v1[0], p1[1] + v1[1]];
      const c2 = [p2[0] - v2[0], p2[1] - v2[1]];
      d += ` C${c1[0].toFixed(1)},${c1[1].toFixed(1)} ${c2[0].toFixed(1)},${c2[1].toFixed(1)} ${p2[0].toFixed(1)},${p2[1].toFixed(1)}`;
    }
    return d;
  }

  function build() {
    const base = main.getBoundingClientRect();
    const w = main.offsetWidth, h = main.offsetHeight;
    const L = isDesk() ? Math.max(22, innerWidth * 0.035) : 24;
    svg.setAttribute("width", w); svg.setAttribute("height", h);
    svg.setAttribute("viewBox", `0 0 ${w} ${h}`);
    const rel = (r) => ({ x: r.left - base.left, y: r.top - base.top, w: r.width, h: r.height });
    const pts = [];

    // origen: final del trazo del glifo, o remate del "1"
    const hero = $(".ph");
    const hr = rel(hero.getBoundingClientRect());
    const glyph = $(".ph__glyph .t-main");
    const mark = $(".ph__mark");
    let o;
    if (glyph) {
      const len = glyph.getTotalLength();
      const pt = glyph.getPointAtLength(len);
      const m = glyph.getScreenCTM();
      const sp = new DOMPoint(pt.x, pt.y).matrixTransform(m);
      o = [sp.x - base.left, sp.y - base.top];
    } else if (mark) {
      const m = rel(mark.getBoundingClientRect());
      o = [m.x + m.w * 0.97, m.y + m.h * 0.925];
    } else o = [w - 40, hr.y + 120];
    pts.push(o);
    // cruza al margen por la franja vacía al pie del hero
    const gy = hr.y + hr.h - (isDesk() ? 62 : 52);
    const R = w - (isDesk() ? 30 : 12);
    if (!isDesk()) pts.push([R, o[1] + 40], [R, gy - 50]);
    else pts.push([Math.min(R, o[0] + 30), gy - 40]);
    pts.push([w * 0.48, gy + 6], [L, gy + 64]);

    // nodos en orden de documento; entre grupos vuelve al margen
    nodes = $$("[data-node]").filter((n) => n.offsetParent);
    let prevGroup = null, last = pts[pts.length - 1];
    nodes.forEach((n) => {
      const r = rel(n.getBoundingClientRect());
      const c = [r.x + r.w / 2, r.y + r.h / 2];
      const g = n.closest("[data-node-group]");
      // entradas y salidas en diagonal larga y suave: sin curvas cerradas
      if (g !== prevGroup) {
        if (prevGroup) pts.push([last[0], last[1] + 70], [L, last[1] + 230]);
        pts.push([L, c[1] - 200], [c[0], c[1] - 60]);
        prevGroup = g;
      }
      pts.push(c); last = c;
    });
    if (prevGroup) pts.push([last[0], last[1] + 70], [L, last[1] + 230]);

    // remate: subraya el CTA final
    const tail = $("[data-tail]");
    if (tail) {
      const r = rel(tail.getBoundingClientRect());
      const yy = r.y + r.h + 24;
      pts.push([L, yy - 70], [L + 30, yy], [r.x + r.w * 0.5, yy + 2], [r.x + r.w, yy]);
    } else pts.push([L, h - 40]);

    svg.innerHTML = "";
    const g = document.createElementNS(NS, "g");
    const d = crPath(pts);
    paths = ["t-shadow", "t-main", "t-hi"].map((c) => {
      const p = document.createElementNS(NS, "path"); p.setAttribute("class", c); p.setAttribute("d", d); g.appendChild(p); return p;
    });
    svg.appendChild(g);
    total = paths[1].getTotalLength() || 1;
    paths.forEach((p) => { p.style.strokeDasharray = `${total} ${total}`; });

    // muestras (longitud → y) para dibujar según el scroll
    samples = [];
    let maxY = -1e9;
    for (let s = 0; s <= total; s += 10) {
      maxY = Math.max(maxY, paths[1].getPointAtLength(s).y);
      samples.push([s, maxY]);
    }
    samples.push([total, Math.max(maxY, paths[1].getPointAtLength(total).y)]);
    draw();
  }

  function lenAtY(y) {
    let lo = 0, hi = samples.length - 1;
    if (!samples.length || y <= samples[0][1]) return 0;
    while (lo < hi) { const mid = (lo + hi + 1) >> 1; if (samples[mid][1] <= y) lo = mid; else hi = mid - 1; }
    return samples[lo][0];
  }
  function draw() {
    if (!paths.length) return;
    const top = main.getBoundingClientRect().top;
    const atBottom = innerHeight + scrollY >= document.documentElement.scrollHeight - 4;
    const target = atBottom ? total : lenAtY(-top + innerHeight * 0.74);
    const len = reduce ? total : target * intro;
    const off = total - len;
    paths.forEach((p) => { p.style.strokeDashoffset = off; });
    // los nodos se encienden cuando el hilo los alcanza
    const tipY = -top + innerHeight * 0.74;
    nodes.forEach((n) => {
      const r = n.getBoundingClientRect();
      const host = n.closest(".how__step, .tl-item");
      if (host) host.classList.toggle("is-on", reduce || (intro >= 1 && r.top - top + r.height / 2 <= tipY));
    });
  }

  let raf = 0;
  addEventListener("scroll", () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(draw); }, { passive: true });
  let tmr = 0;
  function schedule() { clearTimeout(tmr); tmr = setTimeout(build, 140); }
  addEventListener("resize", schedule);
  if ("ResizeObserver" in window) new ResizeObserver(schedule).observe(main);
  addEventListener("load", build);
  document.fonts && document.fonts.ready.then(build);
  build();

  // entrada: el hilo sale del glifo cuando el glifo termina de dibujarse
  if (!reduce) {
    const t0 = performance.now() + 1300, dur = 1400;
    const tick = (t) => {
      intro = clamp((t - t0) / dur);
      intro = intro < 0.5 ? 2 * intro * intro : 1 - Math.pow(-2 * intro + 2, 2) / 2;
      draw();
      if (t < t0 + dur) requestAnimationFrame(tick); else { intro = 1; draw(); }
    };
    requestAnimationFrame(tick);
  }

  /* ---------- carriles horizontales con puntos ---------- */
  $$("[data-rail]").forEach((rail) => {
    const items = $$(":scope > *", rail);
    const dotsEl = rail.parentElement.querySelector("[data-rail-dots]");
    if (!dotsEl) return;
    dotsEl.innerHTML = items.map((it, i) =>
      `<button type="button" aria-label="${i + 1} / ${items.length}" aria-current="${i === 0}"></button>`).join("");
    const dots = $$("button", dotsEl);
    dots.forEach((b, i) => b.addEventListener("click", () =>
      rail.scrollTo({ left: items[i].offsetLeft - parseFloat(getComputedStyle(rail).paddingLeft), behavior: reduce ? "auto" : "smooth" })));
    rail.addEventListener("scroll", () => {
      const pad = parseFloat(getComputedStyle(rail).paddingLeft);
      let best = 0, bd = 1e9;
      items.forEach((it, i) => { const d = Math.abs(it.offsetLeft - pad - rail.scrollLeft); if (d < bd) { bd = d; best = i; } });
      if (rail.scrollLeft + rail.clientWidth >= rail.scrollWidth - 4) best = items.length - 1;
      dots.forEach((b, i) => b.setAttribute("aria-current", String(i === best)));
    }, { passive: true });
  });

  /* ---------- mockup: profundidad con el puntero y el scroll ---------- */
  const mock = $(".mock");
  if (mock && !reduce) {
    const st = { rx: 6, ry: -10, px: 0, py: 0 };
    const apply = () => { mock.style.transform = `rotateX(${(st.rx + st.py).toFixed(2)}deg) rotateY(${(st.ry + st.px).toFixed(2)}deg)`; };
    addEventListener("scroll", () => {
      const r = mock.getBoundingClientRect();
      const k = clamp((r.top + r.height / 2) / innerHeight, 0, 1.2) - 0.5;
      st.rx = 6 * k * 2; st.ry = -10 * k * 2; apply();
    }, { passive: true });
    if (fine) {
      mock.parentElement.addEventListener("pointermove", (e) => {
        const r = mock.getBoundingClientRect();
        st.px = ((e.clientX - r.left) / r.width - 0.5) * 8;
        st.py = ((e.clientY - r.top) / r.height - 0.5) * -6; apply();
      });
      mock.parentElement.addEventListener("pointerleave", () => { st.px = 0; st.py = 0; apply(); });
    }
    mock.style.transition = "transform 400ms cubic-bezier(.23,1,.32,1)";
    apply();
  }

  /* ---------- contadores ---------- */
  $$("[data-count]").forEach((el) => {
    const to = +el.dataset.count;
    const show = (v) => { el.textContent = Math.round(v).toLocaleString("en-US"); };
    if (reduce || !("IntersectionObserver" in window)) return show(to);
    show(0);
    const io = new IntersectionObserver(([en]) => {
      if (!en.isIntersecting) return;
      io.disconnect();
      const t0 = performance.now();
      const step = (t) => { const p = clamp((t - t0) / 1800); show(to * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
      requestAnimationFrame(step);
    }, { threshold: 0.6 });
    io.observe(el);
  });
})();

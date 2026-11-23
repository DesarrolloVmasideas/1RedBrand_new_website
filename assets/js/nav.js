/* =========================================================
   Menú desplegable "Módulos" (patrón de divulgación accesible)
   - Escritorio: abre con clic, o al pasar el puntero (con pequeña demora).
   - Móvil: acordeón dentro del menú a pantalla completa.
   - Esc cierra y devuelve el foco al botón; clic fuera o foco fuera cierran.
   ========================================================= */
(() => {
  "use strict";
  // Guarda el origen de campaña (utm_*, gclid…) de la primera página vista en la sesión,
  // para adjuntarlo al formulario de contacto aunque el visitante navegue a otra página.
  try {
    const q = new URLSearchParams(location.search);
    const keys = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "gbraid", "wbraid", "fbclid", "msclkid"];
    const found = {};
    keys.forEach((k) => { const v = q.get(k); if (v) found[k] = v.slice(0, 150); });
    if (Object.keys(found).length && !sessionStorage.getItem("rb-attr")) sessionStorage.setItem("rb-attr", JSON.stringify(found));
  } catch (e) {}

  const header = document.querySelector(".site-header");
  const hover = matchMedia("(hover: hover) and (pointer: fine) and (min-width: 960px)");
  document.querySelectorAll("[data-dd]").forEach((dd) => {
    const btn = dd.querySelector(".nav__btn");
    const panel = dd.querySelector(".dd");
    let tOpen = 0, tClose = 0;

    const set = (open) => {
      btn.setAttribute("aria-expanded", String(open));
      dd.classList.toggle("is-open", open);
      header && header.classList.toggle("has-dd", open && innerWidth >= 960);
    };
    const isOpen = () => btn.getAttribute("aria-expanded") === "true";

    btn.addEventListener("click", () => { clearTimeout(tOpen); clearTimeout(tClose); set(!isOpen()); });

    dd.addEventListener("pointerenter", () => {
      if (!hover.matches) return;
      clearTimeout(tClose); tOpen = setTimeout(() => set(true), 90);
    });
    dd.addEventListener("pointerleave", () => {
      if (!hover.matches) return;
      clearTimeout(tOpen); tClose = setTimeout(() => set(false), 220);
    });

    dd.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && isOpen()) { e.stopPropagation(); set(false); btn.focus(); }
    });
    dd.addEventListener("focusout", (e) => {
      if (innerWidth >= 960 && !dd.contains(e.relatedTarget)) set(false);
    });
    document.addEventListener("click", (e) => { if (isOpen() && !dd.contains(e.target) && innerWidth >= 960) set(false); });
    panel.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => set(false)));
    addEventListener("resize", () => { if (isOpen() && innerWidth >= 960) header && header.classList.add("has-dd"); });
  });
})();

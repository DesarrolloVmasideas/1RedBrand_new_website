/* =========================================================
   Idioma inicial según el país del visitante.
   Se carga en el <head>, antes del CSS, para que la página se pinte
   directamente en el idioma correcto (sin parpadeo).

   Orden de prioridad:
   1. ?lang=es | ?lang=en en la URL (se guarda como elección).
   2. Elección manual guardada (botón ES/EN → localStorage "rb-lang").
   3. Buscadores y rastreadores: siempre español (versión principal).
   4. País por IP: cookie "rb-geo" que pone el servidor (nginx + GeoIP2,
      o Cloudflare). País hispanohablante → español; cualquier otro → inglés,
      salvo que el navegador esté configurado en español.
   5. Sin cookie de país (por ejemplo, en local): idioma del navegador.
   ========================================================= */
(() => {
  "use strict";
  const html = document.documentElement;
  const ES_COUNTRIES = ["MX", "ES", "AR", "BO", "CL", "CO", "CR", "CU", "DO", "EC", "SV", "GQ",
                        "GT", "HN", "NI", "PA", "PY", "PE", "PR", "UY", "VE"];
  const BOT = /bot|crawl|spider|slurp|bingpreview|facebookexternalhit|embedly|quora|whatsapp|telegram|preview|lighthouse|headless/i;
  const set = (l) => { html.dataset.lang = l; html.lang = l; };
  const browserEs = () => {
    const first = (navigator.languages && navigator.languages[0]) || navigator.language || "";
    return /^es\b/i.test(first);
  };

  try {
    const q = new URLSearchParams(location.search).get("lang");
    if (q === "es" || q === "en") {
      try { localStorage.setItem("rb-lang", q); } catch (e) {}
      return set(q);
    }
    let saved = null;
    try { saved = localStorage.getItem("rb-lang"); } catch (e) {}
    if (saved === "es" || saved === "en") return set(saved);

    if (BOT.test(navigator.userAgent || "")) return set("es");

    const m = document.cookie.match(/(?:^|;\s*)rb-geo=([A-Za-z]{2})/);
    if (m) return set(ES_COUNTRIES.includes(m[1].toUpperCase()) || browserEs() ? "es" : "en");

    set(browserEs() ? "es" : (navigator.language ? "en" : "es"));
  } catch (e) {
    set("es");
  }
})();

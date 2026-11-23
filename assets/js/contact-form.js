/* =========================================================
   Formulario de contacto — validación accesible, bilingüe.
   Destino: hello@1redbrand.com
   - Sin servidor: abre el cliente de correo con el mensaje armado (mailto).
   - En servidor: poner data-endpoint="/ruta" en el <form> y se envía por POST (JSON).
   - Captcha: montar el widget en [data-captcha] y añadir su token en getCaptchaToken().
   ========================================================= */
(() => {
  "use strict";
  const forms = document.querySelectorAll("[data-contact-form]");
  if (!forms.length) return;

  // Origen de la visita para SEM (utm_*, gclid, fbclid). nav.js lo guarda al llegar al sitio.
  const ATTR_KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "gbraid", "wbraid", "fbclid", "msclkid"];
  const readAttribution = () => {
    let saved = {};
    try { saved = JSON.parse(sessionStorage.getItem("rb-attr") || "{}"); } catch (e) {}
    const q = new URLSearchParams(location.search);
    const out = {};
    ATTR_KEYS.forEach((k) => {
      const v = q.get(k) || saved[k];
      if (v) out[k] = String(v).slice(0, 150);
    });
    return out;
  };

  const lang = () => (document.documentElement.dataset.lang === "en" ? "en" : "es");
  const M = {
    es: {
      required: "Este campo es obligatorio.",
      name: "Escribe tu nombre (solo letras, de 2 a 80 caracteres).",
      email: "Escribe un correo válido, por ejemplo nombre@empresa.com.",
      emailTypo: (d) => `¿Quisiste decir ${d}?`,
      country: "Elige tu país.",
      city: "Escribe tu ciudad (de 2 a 80 caracteres).",
      phone: "Escribe un teléfono de 7 a 15 dígitos. Puedes usar +, espacios y guiones.",
      message: "Cuéntanos un poco más (mínimo 10 caracteres).",
      messageMax: "El mensaje no puede pasar de 2,000 caracteres.",
      consent: "Necesitamos tu autorización para responderte.",
      summary: (n) => (n === 1 ? "Revisa 1 campo antes de enviar:" : `Revisa ${n} campos antes de enviar:`),
      sending: "Enviando…",
      sent: "Gracias. Recibimos tu mensaje y te responderemos pronto.",
      mailto: "Abrimos tu aplicación de correo con el mensaje listo para hello@1redbrand.com. Solo presiona Enviar.",
      fail: "No pudimos enviar el mensaje. Inténtalo de nuevo o escríbenos a hello@1redbrand.com.",
      choose: "Elige un país",
      chars: (n) => `${n} / 2,000`,
      subject: (n) => `Contacto desde 1redbrand.com: ${n}`
    },
    en: {
      required: "This field is required.",
      name: "Enter your name (letters only, 2 to 80 characters).",
      email: "Enter a valid email, for example name@company.com.",
      emailTypo: (d) => `Did you mean ${d}?`,
      country: "Choose your country.",
      city: "Enter your city (2 to 80 characters).",
      phone: "Enter a phone number with 7 to 15 digits. You can use +, spaces and dashes.",
      message: "Tell us a bit more (at least 10 characters).",
      messageMax: "The message can't exceed 2,000 characters.",
      consent: "We need your consent to reply to you.",
      summary: (n) => (n === 1 ? "Check 1 field before sending:" : `Check ${n} fields before sending:`),
      sending: "Sending…",
      sent: "Thank you. We got your message and will reply soon.",
      mailto: "We opened your email app with the message ready for hello@1redbrand.com. Just press Send.",
      fail: "We couldn't send your message. Try again or write to hello@1redbrand.com.",
      choose: "Choose a country",
      chars: (n) => `${n} / 2,000`,
      subject: (n) => `Contact from 1redbrand.com: ${n}`
    }
  };

  const TYPOS = { "gmial.com": "gmail.com", "gmai.com": "gmail.com", "gmail.co": "gmail.com", "gamil.com": "gmail.com",
    "hotmial.com": "hotmail.com", "hotmai.com": "hotmail.com", "hotmail.co": "hotmail.com", "outlok.com": "outlook.com",
    "yahoo.co": "yahoo.com", "yaho.com": "yahoo.com", "icloud.co": "icloud.com" };

  const NAME_RE = /^[\p{L}][\p{L}\p{M}'’ .-]{1,79}$/u;
  const EMAIL_RE = /^[^\s@]+@[^\s@.]+(\.[^\s@.]+)*\.[A-Za-z]{2,}$/;
  const PHONE_RE = /^\+?[\d\s().-]+$/;

  const rules = {
    name: (v) => (!v ? "required" : NAME_RE.test(v) ? null : "name"),
    email: (v) => (!v ? "required" : v.length <= 254 && EMAIL_RE.test(v) ? null : "email"),
    country: (v) => (v ? null : "country"),
    city: (v) => (!v ? "required" : v.length >= 2 && v.length <= 80 && /\p{L}/u.test(v) ? null : "city"),
    phone: (v) => {
      if (!v) return "required";
      const d = v.replace(/\D/g, "").length;
      return PHONE_RE.test(v) && d >= 7 && d <= 15 ? null : "phone";
    },
    message: (v) => (!v ? "required" : v.length < 10 ? "message" : v.length > 2000 ? "messageMax" : null),
    consent: (v) => (v ? null : "consent")
  };

  // países: códigos ISO, nombres en el idioma activo vía Intl
  const CODES = "AF AL DZ AD AO AG AR AM AU AT AZ BS BH BD BB BY BE BZ BJ BT BO BA BW BR BN BG BF BI CV KH CM CA CF TD CL CN CO KM CG CD CR CI HR CU CY CZ DK DJ DM DO EC EG SV GQ ER EE SZ ET FJ FI FR GA GM GE DE GH GR GD GT GN GW GY HT HN HK HU IS IN ID IR IQ IE IL IT JM JP JO KZ KE KI KW KG LA LV LB LS LR LY LI LT LU MO MG MW MY MV ML MT MH MR MU MX FM MD MC MN ME MA MZ MM NA NR NP NL NZ NI NE NG KP MK NO OM PK PW PS PA PG PY PE PH PL PT PR QA RO RU RW KN LC VC WS SM ST SA SN RS SC SL SG SK SI SB SO ZA KR SS ES LK SD SR SE CH SY TW TJ TZ TH TL TG TO TT TN TR TM TV UG UA AE GB US UY UZ VU VA VE VN YE ZM ZW".split(" ");
  const PINNED = ["MX", "US", "CO", "ES"];
  function fillCountries(sel) {
    const l = lang(), prev = sel.value;
    let dn = null;
    try { dn = new Intl.DisplayNames([l], { type: "region" }); } catch (e) {}
    const name = (c) => (dn ? dn.of(c) : c) || c;
    const rest = CODES.filter((c) => !PINNED.includes(c)).map((c) => [c, name(c)])
      .sort((a, b) => a[1].localeCompare(b[1], l));
    const opt = ([c, n]) => `<option value="${c}">${n}</option>`;
    sel.innerHTML = `<option value="">${M[l].choose}</option>` +
      `<optgroup label="—">${PINNED.map((c) => opt([c, name(c)])).join("")}</optgroup>` +
      `<optgroup label="${l === "es" ? "Todos los países" : "All countries"}">${rest.map(opt).join("")}</optgroup>`;
    sel.value = prev;
  }

  forms.forEach((form) => {
    const fields = [...form.querySelectorAll("[data-rule]")];
    const summary = form.querySelector("[data-summary]");
    const status = form.querySelector("[data-status]");
    const counter = form.querySelector("[data-counter]");
    const btn = form.querySelector("[type=submit]");
    const country = form.querySelector("select[name=country]");
    const touched = new Set();
    let busy = false;

    const val = (el) => (el.type === "checkbox" ? el.checked : el.value.trim());
    const errEl = (el) => form.querySelector(`#${el.getAttribute("aria-describedby").split(" ")[0]}`);

    function check(el, show = true) {
      const key = rules[el.dataset.rule](val(el));
      let hint = "";
      if (!key && el.name === "email") {
        const dom = el.value.trim().split("@")[1]?.toLowerCase();
        if (TYPOS[dom]) hint = M[lang()].emailTypo(el.value.trim().split("@")[0] + "@" + TYPOS[dom]);
      }
      if (show) {
        const e = errEl(el);
        el.setAttribute("aria-invalid", key ? "true" : "false");
        el.closest(".f").classList.toggle("is-bad", !!key);
        e.textContent = key ? M[lang()][key] : hint;
        e.classList.toggle("is-hint", !key && !!hint);
      }
      return key;
    }

    fields.forEach((el) => {
      const ev = el.type === "checkbox" || el.tagName === "SELECT" ? "change" : "blur";
      el.addEventListener(ev, () => { touched.add(el); check(el); });
      // tras el primer error, valida mientras escribe para confirmar la corrección
      el.addEventListener("input", () => { if (touched.has(el) && el.getAttribute("aria-invalid") === "true") check(el); });
    });

    // teléfono: solo caracteres permitidos
    const tel = form.querySelector("input[name=phone]");
    tel && tel.addEventListener("input", () => {
      const clean = tel.value.replace(/[^\d\s()+.-]/g, "");
      if (clean !== tel.value) tel.value = clean;
    });

    const msg = form.querySelector("textarea[name=message]");
    const updCount = () => { if (counter) counter.textContent = M[lang()].chars(msg.value.length); };
    msg && msg.addEventListener("input", updCount);

    function relabel() {
      if (country) fillCountries(country);
      updCount();
      fields.forEach((el) => { if (touched.has(el)) check(el); });
    }
    relabel();
    new MutationObserver(relabel).observe(document.documentElement, { attributes: true, attributeFilter: ["data-lang"] });

    // si el formulario cambia de alto (errores, avisos), el hilo se recalcula
    if ("ResizeObserver" in window) {
      let h = form.offsetHeight, tmr = 0;
      new ResizeObserver(() => {
        if (Math.abs(form.offsetHeight - h) < 2) return;
        h = form.offsetHeight; clearTimeout(tmr);
        tmr = setTimeout(() => (window.ScrollTrigger ? ScrollTrigger.refresh() : dispatchEvent(new Event("resize"))), 120);
      }).observe(form);
    }

    function getCaptchaToken() {
      // Cuando el sitio esté en servidor: devolver aquí el token del captcha (reCAPTCHA, hCaptcha o Turnstile).
      return null;
    }

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (busy) return;
      status.textContent = "";
      const bad = fields.filter((el) => { touched.add(el); return check(el); });
      if (bad.length) {
        summary.hidden = false;
        summary.innerHTML = `<p>${M[lang()].summary(bad.length)}</p><ul>${bad.map((el) =>
          `<li><a href="#${el.id}">${form.querySelector(`label[for="${el.id}"] .f__l [lang="${lang()}"]`)?.textContent.trim() || el.name}</a></li>`).join("")}</ul>`;
        summary.querySelectorAll("a").forEach((a) => a.addEventListener("click", (ev) => {
          ev.preventDefault(); form.querySelector(a.getAttribute("href")).focus();
        }));
        summary.focus();
        return;
      }
      summary.hidden = true; summary.innerHTML = "";

      // trampa para bots: si el campo oculto viene lleno, se descarta en silencio
      if (form.querySelector("input[name=website]")?.value) { status.textContent = M[lang()].sent; form.reset(); return; }

      const f = (n) => val(form.elements.namedItem(n));
      const data = {
        name: f("name"), email: f("email"),
        country: country.options[country.selectedIndex].text, countryCode: country.value,
        city: f("city"), phone: f("phone"), message: f("message"),
        lang: lang(), page: location.href, captcha: getCaptchaToken(),
        attribution: readAttribution()
      };

      busy = true; btn.disabled = true; btn.setAttribute("aria-busy", "true");
      const endpoint = form.dataset.endpoint;
      try {
        if (endpoint) {
          status.textContent = M[lang()].sending;
          const r = await fetch(endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
          if (!r.ok) throw new Error(r.status);
          status.textContent = M[lang()].sent;
          form.reset(); touched.clear(); updCount();
          fields.forEach((el) => { el.removeAttribute("aria-invalid"); el.closest(".f").classList.remove("is-bad"); errEl(el).textContent = ""; });
        } else {
          let body = [
            `${lang() === "es" ? "Nombre" : "Name"}: ${data.name}`,
            `${lang() === "es" ? "Correo" : "Email"}: ${data.email}`,
            `${lang() === "es" ? "País" : "Country"}: ${data.country}`,
            `${lang() === "es" ? "Ciudad" : "City"}: ${data.city}`,
            `${lang() === "es" ? "Teléfono" : "Phone"}: ${data.phone}`,
            "", data.message
          ];
          const src = Object.entries(data.attribution).map(([k, v]) => `${k}=${v}`).join(" · ");
          if (src) body.push("", `${lang() === "es" ? "Origen" : "Source"}: ${src}`);
          body = body.join("\n");
          location.href = `mailto:${form.dataset.mailto}?subject=${encodeURIComponent(M[lang()].subject(data.name))}&body=${encodeURIComponent(body)}`;
          status.textContent = M[lang()].mailto;
        }
      } catch (err) {
        status.textContent = M[lang()].fail;
      } finally {
        busy = false; btn.disabled = false; btn.removeAttribute("aria-busy");
      }
    });
  });
})();

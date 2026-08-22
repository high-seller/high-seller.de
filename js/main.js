/* ==========================================================================
   Highseller Immobilien & Finanzen — main.js
   Loader · Header · Mobile-Menü · Reveal · FAQ · Maps · Cookies · Formular
   ========================================================================== */
(function () {
  "use strict";
  var doc = document;
  var $  = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var on = function (el, ev, fn) { if (el) el.addEventListener(ev, fn); };

  /* ==========================================================================
     Zentrale Link-Konfiguration
     --------------------------------------------------------------------------
     Einzige Quelle der Wahrheit für die offiziellen Highseller-Profile und den
     direkten Google-Bewertungslink. Änderungen bitte AUSSCHLIESSLICH hier
     vornehmen – die Werte werden beim Laden automatisch auf alle passenden
     Elemente ([data-portal-link], [data-review-link]) angewendet und die
     Sicherheitsattribute (target/rel) erzwungen. Die identischen URLs sind
     zusätzlich statisch im HTML hinterlegt, damit die Links auch ohne
     JavaScript funktionieren.
     ========================================================================== */
  var HS_LINKS = {
    portals: {
      immoscout: "https://www.immobilienscout24.de/anbieter/profil/highseller-immobilien-und-finanzen",
      immowelt: "https://www.immowelt.de/profil/156e7c6439c042c6a6bc0f736075b070",
      kleinanzeigen: "https://www.kleinanzeigen.de/pro/Highseller-Immobilien-Baris-Oelmez"
    },
    googlePlaceId: "ChIJee8v30G_8IQRtnGkH8lyO3Y",
    // Direkter Link zum Abgeben einer Google-Bewertung (öffnet das Bewertungsfenster)
    googleReviewUrl: "https://search.google.com/local/writereview?placeid=ChIJee8v30G_8IQRtnGkH8lyO3Y"
  };
  window.HS_LINKS = HS_LINKS;

  function applyCentralLinks() {
    // Portal-Links (ImmoScout24, Immowelt, Kleinanzeigen) zentral setzen.
    $$("[data-portal-link]").forEach(function (a) {
      var key = a.getAttribute("data-portal-link");
      var url = HS_LINKS.portals[key];
      if (url) a.setAttribute("href", url);
      a.setAttribute("target", "_blank");
      a.setAttribute("rel", "noopener noreferrer");
    });
    // Direkter Google-Bewertungsbutton zentral setzen.
    $$("[data-review-link]").forEach(function (a) {
      if (HS_LINKS.googleReviewUrl) a.setAttribute("href", HS_LINKS.googleReviewUrl);
      a.setAttribute("target", "_blank");
      a.setAttribute("rel", "noopener noreferrer");
    });
  }

  /* ---- sicherer Storage (bricht in Sandboxes nicht) ---- */
  var store = {
    get: function (k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { window.localStorage.setItem(k, v); } catch (e) {} }
  };

  /* ---- Loader ---- */
  function hideLoader() {
    var l = $("#loader");
    if (l) l.classList.add("hide");
  }
  if (doc.readyState === "complete") setTimeout(hideLoader, 200);
  else on(window, "load", function () { setTimeout(hideLoader, 250); });
  // Fallback, falls load nicht feuert
  setTimeout(hideLoader, 2600);

  doc.addEventListener("DOMContentLoaded", function () {
    /* ---- Jahr im Footer ---- */
    $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

    /* ---- Zentrale Links (Portale, Google-Bewertung) anwenden ---- */
    applyCentralLinks();

    /* ---- Header beim Scrollen ---- */
    var header = $(".header");
    var onScroll = function () { if (header) header.classList.toggle("scrolled", window.scrollY > 12); };
    on(window, "scroll", onScroll, { passive: true }); onScroll();

    /* ---- Mobile-Menü ---- */
    var burger = $(".hamburger");
    on(burger, "click", function () {
      var open = doc.body.classList.toggle("nav-open");
      burger.setAttribute("aria-label", open ? "Menü schließen" : "Menü öffnen");
    });
    $$(".mobile-menu a").forEach(function (a) {
      on(a, "click", function () { doc.body.classList.remove("nav-open"); });
    });
    /* Mobile Untermenüs aufklappen */
    $$(".m-group > button").forEach(function (btn) {
      on(btn, "click", function () {
        var g = btn.parentNode;
        var open = g.classList.contains("open");
        $$(".m-group").forEach(function (x) { x.classList.remove("open"); });
        g.classList.toggle("open", !open);
      });
    });
    on(doc, "keydown", function (e) { if (e.key === "Escape") doc.body.classList.remove("nav-open"); });

    /* ---- Reveal-Animationen ----
       Drei Sicherungen, weil unsichtbarer Inhalt schlimmer ist als ein
       fehlender Effekt: kein Observer verfuegbar, Nutzer moechte weniger
       Bewegung, oder der Observer feuert wider Erwarten nicht. */
    var revealEls = $$(".reveal");
    function alleZeigen() { revealEls.forEach(function (el) { el.classList.add("in"); }); }
    var wenigerBewegung = window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (wenigerBewegung || !("IntersectionObserver" in window) || !revealEls.length) {
      alleZeigen();
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
        });
      }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
      revealEls.forEach(function (el) { io.observe(el); });
      // Rueckfall: Was nach drei Sekunden noch verborgen ist, wird gezeigt.
      setTimeout(alleZeigen, 3000);
    }

    /* ---- Kontaktleiste unten (Handy) ----
       Erst ab 600 px Scrolltiefe einblenden: Im Hero stehen dieselben Aufrufe
       bereits gross, dort waere die Leiste nur verdeckte Flaeche. Ohne JS
       bleibt sie sichtbar - die Verschiebung haengt im CSS an .js. */
    var leiste = doc.querySelector(".mobile-bar");
    if (leiste) {
      var SCHWELLE = 600;
      var leisteZeigen = function () {
        leiste.classList.toggle("is-in", (window.pageYOffset || doc.documentElement.scrollTop) > SCHWELLE);
      };
      leisteZeigen();
      /* Bewusst nicht ueber on(): dort fehlt der dritte Parameter, und
         passive:true haelt das Scrollen auf schwachen Geraeten fluessig. */
      window.addEventListener("scroll", leisteZeigen, { passive: true });
      /* Klicks messen - gtag existiert nur nach Einwilligung als echtes Tag,
         davor ist es die Warteschlange und der Aufruf bleibt folgenlos. */
      on(leiste, "click", function (e) {
        var a = e.target.closest ? e.target.closest("a") : null;
        if (!a || typeof window.gtag !== "function") return;
        window.gtag("event", "kontaktleiste_klick", {
          ziel: a.className || "", link_text: (a.textContent || "").trim()
        });
      });
    }

    /* ---- FAQ: Accordion ---- */
    $$(".faq-q").forEach(function (btn) {
      on(btn, "click", function () {
        var expanded = btn.getAttribute("aria-expanded") === "true";
        // andere im selben Container schließen (sauberes Akkordeon)
        $$(".faq-q").forEach(function (b) { if (b !== btn) b.setAttribute("aria-expanded", "false"); });
        btn.setAttribute("aria-expanded", expanded ? "false" : "true");
      });
    });
    /* ---- FAQ: Kategorie-Filter ---- */
    $$(".faq-cat").forEach(function (tab) {
      on(tab, "click", function () {
        var cat = tab.getAttribute("data-cat");
        $$(".faq-cat").forEach(function (t) { t.classList.toggle("active", t === tab); });
        $$(".faq-item").forEach(function (item) {
          var show = cat === "all" || item.getAttribute("data-cat") === cat;
          item.classList.toggle("hidden", !show);
          if (!show) { var q = $(".faq-q", item); if (q) q.setAttribute("aria-expanded", "false"); }
        });
      });
    });

    /* ---- Google Maps: erst nach Klick ODER nach Marketing-Einwilligung laden ---- */
    $$("[data-map-load]").forEach(function (btn) {
      on(btn, "click", function () {
        var wrap = btn.closest(".map-wrap");
        loadMap(wrap);
        // Ein bewusster Klick auf „Karte laden“ gilt als Einwilligung für externe
        // Medien und wird gespeichert (jederzeit über Cookie-Einstellungen widerrufbar).
        Consent.grant("marketing");
      });
    });

    /* ---- Cookie-Consent (Ablehnung als Standard) ---- */
    initCookies();

    /* ---- Kontaktformulare ---- */
    $$("form[data-contact]").forEach(initForm);

    /* ---- Formular-Segmente: Immobilie vs. Finanzierung ---- */
    $$("[data-segments]").forEach(function (wrap) {
      var form = wrap.closest("form");
      var leistung = form ? form.querySelector("[name=leistung]") : null;
      $$(".seg", wrap).forEach(function (btn) {
        on(btn, "click", function () {
          $$(".seg", wrap).forEach(function (x) { x.classList.remove("sel"); });
          btn.classList.add("sel");
          var seg = btn.getAttribute("data-segment");
          if (form) $$("[data-seg]", form).forEach(function (fld) {
            fld.style.display = fld.getAttribute("data-seg") === seg ? "" : "none";
          });
          if (leistung) leistung.value = seg === "finanzierung" ? "Baufinanzierung prüfen" : "Immobilie verkaufen";
        });
      });
    });
  });

  /* ====================== Cookie-Consent (DSGVO) ======================
     Kategorien: necessary (immer aktiv), statistics (z. B. Google Analytics),
     marketing (externe Medien: YouTube, Google Maps, Meta Pixel …).
     Kein externer Dienst wird ohne aktive Einwilligung geladen. Die Auswahl
     wird lokal gespeichert und ist über die Cookie-Einstellungen widerrufbar. */
  /* v3 seit 2026-07-28: Bis dahin lud Google Analytics fest im <head> jeder
     Seite — also auch bei abgelehnter Statistik. Die unter v2 eingeholte
     Zustimmung beschrieb damit nicht, was tatsaechlich passierte, und wird
     deshalb nicht uebernommen. Bestehende Besucher werden einmal neu gefragt. */
  var CONSENT_KEY = "hs_consent_v3";
  // Google-Analytics-4-Mess-ID. Wird erst nach Einwilligung in die Kategorie
  // "statistics" geladen (siehe applyConsent/loadAnalytics). Ohne ID kein Tracking.
  var GA_ID = "G-24CQ7EWJZ3";
  var analyticsLoaded = false;

  var Consent = (function () {
    var state = null; // {necessary:true, statistics:bool, marketing:bool} | null
    function read() { try { return JSON.parse(store.get(CONSENT_KEY) || "null"); } catch (e) { return null; } }
    return {
      load: function () { state = read(); return state; },
      current: function () { return state || { necessary: true, statistics: false, marketing: false }; },
      has: function (cat) { return !!(state && state[cat]); },
      set: function (obj) {
        state = { necessary: true, statistics: !!obj.statistics, marketing: !!obj.marketing };
        store.set(CONSENT_KEY, JSON.stringify(state));
        applyConsent();
        try { doc.dispatchEvent(new CustomEvent("hs:consent", { detail: state })); } catch (e) {}
      },
      grant: function (cat) { var c = this.current(); c[cat] = true; this.set(c); }
    };
  })();
  // Öffentliche API für künftige Einbindungen (z. B. YouTube-Video nach Zustimmung)
  window.HSConsent = Consent;

  function applyConsent() {
    var c = Consent.current();
    if (c.statistics) loadAnalytics(); else unloadAnalytics();
    if (c.marketing) { $$(".map-wrap").forEach(loadMap); loadEmbeds(); }
  }

  /* Google-Maps-Einbettung erzeugen (nur nach Einwilligung/Klick) */
  function loadMap(wrap) {
    if (!wrap || wrap.querySelector("iframe")) return;
    var src = wrap.getAttribute("data-map-src");
    if (!src) return;
    var consent = $(".map-consent", wrap);
    if (consent) consent.remove();
    var ifr = doc.createElement("iframe");
    ifr.src = src; ifr.loading = "lazy"; ifr.title = "Standort Highseller Immobilien & Finanzen";
    ifr.setAttribute("referrerpolicy", "no-referrer-when-downgrade");
    ifr.setAttribute("allowfullscreen", "");
    wrap.appendChild(ifr);
  }

  /* Generische externe Medien (Platzhalter mit data-embed-src) nach Einwilligung laden */
  function loadEmbeds() {
    $$("[data-embed-src]").forEach(function (el) {
      if (el.getAttribute("data-loaded")) return;
      el.setAttribute("data-loaded", "1");
      var ifr = doc.createElement("iframe");
      ifr.src = el.getAttribute("data-embed-src");
      ifr.loading = "lazy";
      ifr.title = el.getAttribute("data-embed-title") || "Externer Inhalt";
      ifr.setAttribute("allowfullscreen", "");
      ifr.setAttribute("frameborder", "0");
      el.innerHTML = ""; el.appendChild(ifr);
    });
  }

  /* gtag ist bereits im <head> jeder Seite definiert (Consent Mode v2, alle
     Kategorien auf "denied"). Hier nur absichern, falls das Inline-Skript
     einmal fehlt — niemals neu definieren, sonst ginge die Warteschlange
     der bereits gesetzten Defaults verloren. */
  window.dataLayer = window.dataLayer || [];
  if (typeof window.gtag !== "function") {
    window.gtag = function () { window.dataLayer.push(arguments); };
  }

  function loadAnalytics() {
    if (!GA_ID) return;
    // Einwilligung an Google melden. Muss auch dann laufen, wenn der Tag schon
    // geladen ist (Widerruf und erneute Zustimmung in derselben Sitzung).
    window.gtag("consent", "update", { analytics_storage: "granted" });
    if (analyticsLoaded) return;
    analyticsLoaded = true;
    // Offizielles Google-Tag (gtag.js) — asynchron nachladen
    var s = doc.createElement("script");
    s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    doc.head.appendChild(s);
    window.gtag("js", new Date());
    // Standard-Konfiguration: sendet auf jeder (voll geladenen) Seite einen page_view.
    // Da die Website eine klassische Multi-Page-Site ist, wird jeder Seitenwechsel
    // als vollständiger Seitenaufruf gemessen.
    window.gtag("config", GA_ID, { anonymize_ip: true });
  }

  /* Widerruf: Google die Rücknahme melden und die bereits gesetzten
     Analytics-Cookies entfernen. Ohne das Löschen bliebe die Kennung des
     Besuchers ein Jahr lang im Browser stehen. */
  function unloadAnalytics() {
    window.gtag("consent", "update", { analytics_storage: "denied" });
    var namen = doc.cookie.split(";").map(function (c) { return c.split("=")[0].trim(); })
      .filter(function (n) { return n === "_ga" || n === "_gid" || n.indexOf("_ga_") === 0; });
    var hosts = [location.hostname, "." + location.hostname];
    var basis = location.hostname.replace(/^www\./, "");
    hosts.push(basis, "." + basis);
    namen.forEach(function (n) {
      hosts.forEach(function (h) {
        doc.cookie = n + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=" + h;
      });
      doc.cookie = n + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
    });
  }

  function initCookies() {
    var root = $("#cookie-consent");
    if (!root) return;
    var banner = $(".cc__banner", root);
    var modal  = $(".cc__modal", root);
    var scrim  = $(".cc__scrim", root);
    var boxes  = $$("[data-cc-cat]", root);

    function show()    { root.hidden = false; requestAnimationFrame(function () { root.classList.add("cc--show"); }); }
    function hideAll() { root.classList.remove("cc--show", "cc--modal-open"); root.hidden = true; doc.body.classList.remove("cc-lock"); }

    function openModal() {
      var c = Consent.current();
      boxes.forEach(function (b) { b.checked = !!c[b.getAttribute("data-cc-cat")]; });
      root.hidden = false;
      if (banner) banner.hidden = true;
      if (modal)  modal.hidden  = false;
      if (scrim)  scrim.hidden  = false;
      root.classList.add("cc--show", "cc--modal-open");
      doc.body.classList.add("cc-lock");
      var first = modal && modal.querySelector("button,input");
      if (first) { try { first.focus(); } catch (e) {} }
    }
    function closeModal() {
      doc.body.classList.remove("cc-lock");
      if (!Consent.load()) { // noch keine Entscheidung -> zurück zum Banner
        if (modal) modal.hidden = true;
        if (scrim) scrim.hidden = true;
        if (banner) banner.hidden = false;
        root.classList.remove("cc--modal-open");
      } else { hideAll(); }
    }

    function acceptAll() { Consent.set({ statistics: true, marketing: true }); hideAll(); }
    function rejectAll() { Consent.set({ statistics: false, marketing: false }); hideAll(); }
    function saveSelection() {
      var sel = {};
      boxes.forEach(function (b) { sel[b.getAttribute("data-cc-cat")] = b.checked; });
      Consent.set(sel); hideAll();
    }

    $$("[data-cc-accept]",  root).forEach(function (b) { on(b, "click", acceptAll); });
    $$("[data-cc-reject]",  root).forEach(function (b) { on(b, "click", rejectAll); });
    $$("[data-cc-save]",    root).forEach(function (b) { on(b, "click", saveSelection); });
    $$("[data-cc-dismiss]", root).forEach(function (b) { on(b, "click", closeModal); });
    // „Cookie-Einstellungen“-Trigger auch außerhalb des Banners (z. B. Footer)
    $$("[data-cc-open]").forEach(function (b) { on(b, "click", function (e) { e.preventDefault(); openModal(); }); });
    on(doc, "keydown", function (e) { if (e.key === "Escape" && root.classList.contains("cc--modal-open")) closeModal(); });

    // Erstaufruf: Banner zeigen, wenn keine Entscheidung gespeichert ist
    if (!Consent.load()) { if (banner) banner.hidden = false; setTimeout(show, 700); }
    else { applyConsent(); }
  }

  /* ====================== Kontaktformular ====================== */
  function initForm(form) {
    // Netlify Forms verarbeitet POSTs an "/" (statische Seite). Der frühere
    // PHP-Endpunkt entfällt.
    var endpoint = "/";
    var status = $(".form-status", form);
    var submitBtn = $("button[type=submit]", form);

    // Quelle / Zeitpunkt automatisch füllen
    var qf = form.querySelector("[name=quelle]");   if (qf) qf.value = location.href;
    var zf = form.querySelector("[name=zeitpunkt]"); if (zf) zf.value = new Date().toLocaleString("de-DE");

    // Live: Fehlermarkierung entfernen
    $$("input,select,textarea", form).forEach(function (input) {
      on(input, "input", function () {
        var f = input.closest(".field, .checkbox"); if (f) f.classList.remove("invalid");
      });
    });

    function setStatus(type, msg) {
      if (!status) return;
      status.className = "form-status " + type;
      status.textContent = msg;
    }

    on(form, "submit", function (e) {
      e.preventDefault();

      // Honeypot
      var hp = form.querySelector(".hp input");
      if (hp && hp.value) { setStatus("ok", "Vielen Dank für Ihre Nachricht."); return; }

      // Validierung
      var valid = true;
      $$("[required]", form).forEach(function (input) {
        var ok = input.type === "checkbox" ? input.checked
               : input.type === "email" ? /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim())
               : input.value.trim() !== "";
        var field = input.closest(".field, .checkbox");
        if (field) field.classList.toggle("invalid", !ok);
        if (!ok) valid = false;
      });

      // Mindestens eine Angabe aus einer Gruppe (z. B. Telefon ODER E-Mail)
      var reqOne = form.getAttribute("data-require-one");
      if (reqOne) {
        var names = reqOne.split(/[\s,]+/).filter(Boolean);
        var oneFilled = names.some(function (n) {
          var el = form.querySelector('[name="' + n + '"]');
          return el && el.value.trim() !== "";
        });
        names.forEach(function (n) {
          var el = form.querySelector('[name="' + n + '"]');
          if (!el) return;
          var field = el.closest(".field, .checkbox");
          // Ungültig, wenn keins gefüllt ist – oder eine ausgefüllte E-Mail ungültig ist
          var bad = !oneFilled;
          if (n === "email" && el.value.trim() !== "" &&
              !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value.trim())) bad = true;
          if (field) field.classList.toggle("invalid", bad);
          if (bad) valid = false;
        });
        if (!oneFilled) { setStatus("error", "Bitte geben Sie eine Telefonnummer oder E-Mail-Adresse an."); return; }
      }

      if (!valid) { setStatus("error", "Bitte füllen Sie die markierten Pflichtfelder aus."); return; }

      if (zf) zf.value = new Date().toLocaleString("de-DE");
      var data = new FormData(form);
      if (submitBtn) { submitBtn.disabled = true; submitBtn.dataset.label = submitBtn.textContent; submitBtn.textContent = "Wird gesendet …"; }
      setStatus("", "");

      // Formulare mit Datei-Upload müssen als multipart/form-data gesendet werden
      // (kein Content-Type-Header setzen -> der Browser ergänzt die Boundary).
      // Alle übrigen Formulare weiterhin klassisch als urlencoded.
      var hasFile = !!form.querySelector('input[type="file"]');
      var fetchOpts = hasFile
        ? { method: "POST", headers: { "Accept": "application/json" }, body: data }
        : {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json" },
            body: new URLSearchParams(data).toString()
          };

      fetch(endpoint, fetchOpts)
        .then(function (r) { if (!r.ok) return Promise.reject(r); return true; })
        .then(function () {
          form.innerHTML = '<div class="form-success" role="status">' +
            '<div class="fs-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M20 6L9 17l-5-5"/></svg></div>' +
            '<h3>Vielen Dank für Ihre Anfrage.</h3>' +
            '<p>Wir melden uns zeitnah persönlich bei Ihnen.</p></div>';
          if (typeof gtag === "function") { gtag("event", "generate_lead", { form_name: form.getAttribute("name") || "" }); }
          form.scrollIntoView({ behavior: "smooth", block: "center" });
        })
        .catch(function () {
          /* Fallback: E-Mail-Programm oeffnen. Die Telefonnummer gehoert in
             die Meldung - wer hier strandet, hat kein eingerichtetes
             Mailprogramm oder bricht ab, und beides kostet den Kontakt. */
          setStatus("error", "Der direkte Versand ist momentan nicht möglich. Wir öffnen Ihr E-Mail-Programm, bitte die Nachricht abschicken. Sie erreichen uns auch telefonisch unter +49 162 8811110.");
          mailtoFallback(data);
        })
        .then(function () {
          if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = submitBtn.dataset.label || "Anfrage absenden"; }
        });
    });
  }

  /* Shared: Lead aus den Rechnern (FormData) an Netlify Forms senden.
     formName muss einem im Build erkannten Formular entsprechen
     (siehe __forms.html). */
  window.HS_submitLead = function (formName, formData) {
    var params = new URLSearchParams();
    params.append("form-name", formName);
    formData.forEach(function (v, k) { params.append(k, v); });
    return fetch("/", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json" },
      body: params.toString()
    });
  };

  function mailtoFallback(data) {
    var lines = [];
    var labels = {
      name: "Name", vorname: "Vorname", nachname: "Nachname", telefon: "Telefon", email: "E-Mail",
      leistung: "Leistung", bereich: "Gewünschter Bereich",
      kontaktart: "Kontaktart", objektart: "Immobilienart", objektadresse: "Objektadresse",
      wert: "Geschätzter Wert", nachricht: "Nachricht", finanzierungsdaten: "Finanzierungsdaten",
      wunschort: "Wunschort", budget: "Budget", finanzierung: "Finanzierungsstatus", budgetdaten: "Budget-Berechnung"
    };
    Object.keys(labels).forEach(function (k) {
      var v = data.get(k);
      if (v) lines.push(labels[k] + ": " + v);
    });
    var subject = "Anfrage über high-seller.de";
    var href = "mailto:info@high-seller.de?subject=" + encodeURIComponent(subject) +
               "&body=" + encodeURIComponent(lines.join("\n"));
    window.location.href = href;
  }

  /* Karriere: Klick auf eine Stellenanzeige wählt die Stelle im Formular vor,
     damit die Zuordnung nicht beim Sprung zum Formular verloren geht. */
  $$("[data-stelle]").forEach(function (link) {
    on(link, "click", function () {
      var sel = $("#bereich");
      if (sel) sel.value = link.getAttribute("data-stelle");
    });
  });

  /* Einstiege in den Wertrechner.
     --------------------------------------------------------------------------
     Zwei Wege führen hinein: die Karte im Hero derselben Seite (data-wert-start)
     und die Stadtteilseiten, die per Adressparameter ?art=… herüberschicken.
     Beide wählen am Ende dieselbe Kachel im echten Rechner an — der Zustand
     lebt ausschließlich in wertrechner.js, sonst laufen die Stellen auseinander. */
  /* Rückgabe ist bewusst das ERGEBNIS, nicht nur "Kachel gefunden": main.js wird
     vor wertrechner.js geladen. Ein Klick zu früh verpufft, weil der Zuhörer dort
     noch nicht registriert ist — die Kachel bliebe stumm zurück. */
  function wertrechnerVorwaehlen(art, springen) {
    var kachel = $('.tile[data-type="' + art + '"]');
    if (!kachel) return false;
    kachel.click();
    if (springen) {
      var rechner = $("#wertrechner");
      if (rechner) rechner.scrollIntoView({ behavior: "smooth", block: "start" });
    }
    return kachel.classList.contains("sel");
  }

  $$("[data-wert-start]").forEach(function (btn) {
    on(btn, "click", function () {
      wertrechnerVorwaehlen(btn.getAttribute("data-wert-start"), true);
    });
  });

  /* Ankunft von einer Stadtteilseite: /immobilie-bewerten.html?art=efh
     Nur bekannte Werte zulassen — der Parameter kommt aus der Adresszeile. */
  (function () {
    var treffer = /[?&]art=([a-z]+)/.exec(location.search);
    if (!treffer) return;
    var erlaubt = ["wohnung", "efh", "dhh", "reihenhaus", "mfh", "grundstueck", "gewerbe"];
    if (erlaubt.indexOf(treffer[1]) === -1) return;
    // Der Rechner baut sich erst auf; deshalb kurz warten statt sofort zugreifen.
    var versuche = 0;
    (function probieren() {
      if (wertrechnerVorwaehlen(treffer[1], false)) return;
      if (++versuche < 20) setTimeout(probieren, 100);
    })();
  })();

  /* ==========================================================================
     Sprungleiste (Handy): markiert den Abschnitt, in dem man gerade steht.
     --------------------------------------------------------------------------
     Bewusst kein IntersectionObserver: Die Abschnitte sind teils höher als der
     Bildschirm, teils niedriger, und mehrere sind gleichzeitig sichtbar. Ein
     Observer müsste dann doch entscheiden, welcher davon "der aktuelle" ist.
     Hier gilt schlicht: der letzte Abschnitt, dessen Oberkante die Leiste
     bereits passiert hat.
     ========================================================================== */
  /* Kopfhöhe als CSS-Variable — unabhängig von der Sprungleiste, weil auch
     jede andere Seite sie für den Abstand bei Ankersprüngen braucht. */
  (function () {
    var kopf = $(".header");
    if (!kopf) return;
    function setzen() {
      doc.documentElement.style.setProperty("--header-h", kopf.offsetHeight + "px");
    }
    setzen();
    on(window, "resize", setzen);
    if (window.ResizeObserver) new ResizeObserver(setzen).observe(kopf);
  })();

  (function () {
    var bar = $("#jumpbar");
    if (!bar) return;

    var links = $$("a", bar);
    var ziele = links.map(function (a) { return $(a.getAttribute("href")); });
    var aktiv = -1;
    function markieren() {
      var grenze = bar.getBoundingClientRect().bottom + 8;
      var jetzt = -1;
      for (var i = 0; i < ziele.length; i++) {
        if (ziele[i] && ziele[i].getBoundingClientRect().top <= grenze) jetzt = i;
      }
      if (jetzt === aktiv) return;
      if (aktiv > -1) links[aktiv].classList.remove("is-hier");
      aktiv = jetzt;
      if (aktiv < 0) return;
      var a = links[aktiv];
      a.classList.add("is-hier");
      // aktiven Chip in Sicht holen, ohne die Seite selbst zu verschieben
      var spur = a.parentElement;
      var soll = a.offsetLeft - (spur.clientWidth - a.offsetWidth) / 2;
      spur.scrollTo({ left: Math.max(0, soll), behavior: "smooth" });
    }

    var wartet = false;
    on(window, "scroll", function () {
      if (wartet) return;
      wartet = true;
      requestAnimationFrame(function () { markieren(); wartet = false; });
    });
    markieren();
  })();
  /* ---- Lagekarte der Veedelseiten ----
     Die Karte hat zwei Ansichten: Orientierung mit den Landmarken und die
     amtlichen Bodenrichtwertzonen. Beide Ebenen stecken im selben SVG, der
     Umschalter blendet um — das spart einen zweiten Datensatz und haelt die
     Zuordnung zwischen Zone und Ort erhalten.

     Hinter jedem Punkt und jeder Zone liegt eine Erklaerung. Auf dem Handy
     gibt es kein Hover, deshalb fuehrt der Klick und der Text erscheint in
     einem festen Feld unter der Karte statt in einer Sprechblase. Ohne
     JavaScript bleibt die Karte eine vollstaendige, beschriftete Abbildung;
     es geht nur das Umschalten und die Zusatzerklaerung verloren. */
  (function () {
    var karte = doc.querySelector(".veedelkarte");
    if (!karte) return;
    var feld = karte.querySelector(".veedelkarte__info");
    if (!feld) return;

    var daten = {};
    try { daten = JSON.parse(karte.getAttribute("data-infos") || "{}"); }
    catch (e) { return; }

    var marken = $$(".dz-marke", karte);
    var zonen = $$(".dz-zone", karte);
    var leer = feld.getAttribute("data-leer") || "";
    var offen = null;

    function alleAus() {
      marken.concat(zonen).forEach(function (el) {
        el.classList.remove("dz-marke--aktiv", "dz-zone--aktiv");
        el.setAttribute("aria-pressed", "false");
      });
    }

    function schliessen() {
      alleAus();
      feld.innerHTML = leer;
      feld.classList.remove("veedelkarte__info--gefuellt");
      offen = null;
    }

    function zeigen(art, nr, el) {
      var liste = art === "zone" ? daten.zonen : daten.marken;
      var eintrag = liste && liste[nr];
      if (!eintrag) return;
      alleAus();
      el.classList.add(art === "zone" ? "dz-zone--aktiv" : "dz-marke--aktiv");
      el.setAttribute("aria-pressed", "true");
      feld.innerHTML = "<b>" + eintrag.n + "</b> " + eintrag.t;
      feld.classList.add("veedelkarte__info--gefuellt");
      offen = art + nr;
    }

    function verdrahten(el, art, nr) {
      el.setAttribute("aria-pressed", "false");
      var schluessel = art + nr;
      on(el, "click", function () {
        offen === schluessel ? schliessen() : zeigen(art, nr, el);
      });
      on(el, "keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); zeigen(art, nr, el); }
        if (e.key === "Escape") schliessen();
      });
      on(el, "mouseenter", function () { if (offen === null) zeigen(art, nr, el); });
    }

    marken.forEach(function (el) {
      verdrahten(el, "marke", parseInt(el.getAttribute("data-nr"), 10));
    });

    /* Namensliste unter der Karte (v49). Die Karten tragen seit dem Umbau
       Ziffern statt Namen, damit sie auf dem Telefon mitskalieren koennen.
       Diese Liste traegt die Namen — und ist dort zugleich das bequemere
       Bedienelement, weil ein 44 Pixel hoher Knopf sicherer zu treffen ist
       als ein Kartenpunkt. */
    var listenknoepfe = $$(".dz-liste__knopf", doc);
    listenknoepfe.forEach(function (knopf) {
      var nr = parseInt(knopf.getAttribute("data-nr"), 10);
      on(knopf, "click", function () {
        var ziel = marken.filter(function (m) {
          return parseInt(m.getAttribute("data-nr"), 10) === nr;
        })[0];
        if (!ziel) return;
        zeigen("marke", nr, ziel);
        listenknoepfe.forEach(function (k) { k.removeAttribute("aria-current"); });
        knopf.setAttribute("aria-current", "true");
        /* Die Karte steht ueber der Liste. Ohne diesen Sprung tippt man einen
           Namen an und sieht die zugehoerige Ziffer nicht. */
        if (karte.getBoundingClientRect().top < 0) {
          karte.scrollIntoView({ block: "center", behavior: "smooth" });
        }
      });
    });
    zonen.forEach(function (el) {
      verdrahten(el, "zone", parseInt(el.getAttribute("data-zone"), 10));
    });
    on(karte, "mouseleave", function () { if (offen === null) schliessen(); });

    /* Umschalter zwischen den beiden Ansichten */
    var knoepfe = $$("[data-ansicht]", karte);
    knoepfe.forEach(function (b) {
      on(b, "click", function () {
        var ziel = b.getAttribute("data-ansicht");
        karte.classList.toggle("veedelkarte--zonen", ziel === "zonen");
        knoepfe.forEach(function (o) {
          var an = o === b;
          o.classList.toggle("is-an", an);
          o.setAttribute("aria-pressed", an ? "true" : "false");
        });
        schliessen();
        feld.innerHTML = ziel === "zonen"
          ? (feld.getAttribute("data-leer-zonen") || leer)
          : leer;
      });
    });
  })();

  /* ---- Preisdiagramm ----
     Die Balken wachsen beim Sichtbarwerden von links. Das ist kein Selbstzweck:
     Der Blick folgt der Bewegung und landet am Ende auf der Laenge, also auf
     dem Wert. Wer weniger Bewegung eingestellt hat, sieht sie sofort fertig. */
  (function () {
    var diagramm = doc.querySelector(".preisdiagramm");
    if (!diagramm) return;
    var balken = $$(".pd-balken", diagramm);
    if (!balken.length) return;

    function fertigZeigen() { diagramm.classList.add("preisdiagramm--fertig"); }

    var wenigerBewegung = window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (wenigerBewegung || !("IntersectionObserver" in window)) { fertigZeigen(); return; }

    diagramm.classList.add("preisdiagramm--bereit");
    var io = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        var werte = $$(".pd-wert", diagramm);
        balken.forEach(function (b, i) {
          // Gestaffelt von oben nach unten, gedeckelt, damit der letzte Balken
          // nicht ueber eine Sekunde auf sich warten laesst.
          var ms = Math.min(i * 38, 620);
          b.style.transitionDelay = ms + "ms";
          if (werte[i]) werte[i].style.transitionDelay = (ms + 190) + "ms";
        });
        fertigZeigen();
      });
    }, { threshold: 0.15 });
    io.observe(diagramm);
    setTimeout(fertigZeigen, 3000);
  })();
  /* ---- Lead-Erfassung ----
     Meldet Kontaktereignisse (Anruf-, WhatsApp-, E-Mail-Klick) an
     /.netlify/functions/lead-track, sichtbar im internen Lead-Cockpit.
     Formular-Ereignisse kommen NICHT von hier, sondern serverseitig aus
     submission-created — dort zaehlen nur verifizierte Eingaenge.

     Rechtlich zweistufig:
     - Ohne Einwilligung wird nur das Ereignis selbst gesendet: Art, Seite,
       Zeitpunkt. Kein Zugriff auf den Geraetespeicher, keine Kennung, und
       der Server legt weder IP noch User-Agent ab.
     - Erst mit Statistik-Einwilligung kommt eine zufaellige Sitzungskennung
       aus dem sessionStorage dazu (endet mit dem Schliessen des Browsers).
       Sie verknuepft Ereignisse derselben Sitzung, mehr nicht.

     sendBeacon, weil ein tel:-Klick sofort wegnavigiert — ein normales
     fetch wuerde der Browser dabei haeufig abbrechen. */
  (function () {
    var ENDPUNKT = "/.netlify/functions/lead-track";

    function sitzung() {
      if (!Consent.has("statistics")) return "";
      try {
        var s = window.sessionStorage.getItem("hs_sitzung");
        if (!s) {
          s = Math.random().toString(36).slice(2, 10);
          window.sessionStorage.setItem("hs_sitzung", s);
        }
        return s;
      } catch (e) { return ""; }
    }

    function melden(art, zusatz) {
      try {
        var daten = JSON.stringify({
          art: art,
          seite: location.pathname,
          zusatz: zusatz || "",
          sitzung: sitzung()
        });
        if (navigator.sendBeacon) {
          navigator.sendBeacon(ENDPUNKT, new Blob([daten], { type: "application/json" }));
        } else if (window.fetch) {
          fetch(ENDPUNKT, { method: "POST", body: daten, keepalive: true,
            headers: { "Content-Type": "application/json" } });
        }
      } catch (e) { /* Erfassung darf nie den Klick stoeren */ }
    }

    on(doc, "click", function (e) {
      var a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
      if (!a) return;
      var h = a.getAttribute("href") || "";
      if (h.indexOf("tel:") === 0) melden("anruf");
      else if (h.indexOf("wa.me") !== -1) melden("whatsapp");
      else if (h.indexOf("mailto:") === 0) melden("email");
    });
  })();
  /* ---- Bodenwertrechner (Veedelseiten mit Zonenkarte) ----
     Haengt an der Zonenauswahl: Wer eine Flaeche auf der Karte antippt,
     bekommt den amtlichen Bodenrichtwert auf die eigene Grundstuecksgroesse
     umgerechnet. Der Rechner ist bis zur ersten Auswahl verborgen, damit
     niemand vor einem leeren Formular steht.

     Bewusst nur eine Multiplikation und mit deutlichem Hinweis versehen: Das
     Ergebnis ist der Bodenwert, nicht der Immobilienwert. Alles andere waere
     eine Scheingenauigkeit, die wir nicht halten koennen. */
  (function () {
    var rechner = doc.querySelector(".bodenrechner");
    var karte = doc.querySelector(".veedelkarte");
    if (!rechner || !karte) return;

    var feldZone = doc.getElementById("br-zone");
    var feldFlaeche = doc.getElementById("br-flaeche");
    var feldSumme = doc.getElementById("br-summe");
    if (!feldZone || !feldFlaeche || !feldSumme) return;

    var wert = null;
    var geld = new Intl.NumberFormat("de-DE", {
      style: "currency", currency: "EUR", maximumFractionDigits: 0 });

    function rechnen() {
      if (wert === null) return;
      var qm = parseFloat(feldFlaeche.value);
      if (!(qm > 0)) { feldSumme.textContent = "—"; return; }
      feldSumme.textContent = geld.format(Math.round(wert * qm));
    }

    on(feldFlaeche, "input", rechnen);

    // Auf die Zonenauswahl der Karte hoeren. Der Wert steht im Text der
    // Marke ("2.610 € je m²"), damit hier keine zweite Datenquelle entsteht.
    $$(".dz-zone", karte).forEach(function (el) {
      on(el, "click", function () {
        var label = el.getAttribute("aria-label") || "";
        var tref = label.match(/([\d.]+)\s*Euro je Quadratmeter/);
        if (!tref) return;
        wert = parseFloat(tref[1].replace(/\./g, ""));
        if (!(wert > 0)) return;
        var lage = label.replace(/^Bodenrichtwertzone\s*/, "").split(",")[0];
        feldZone.textContent = geld.format(wert) + " je m²"
          + (lage && !/^\d/.test(lage) ? " · " + lage : "");
        rechner.hidden = false;
        rechnen();
      });
    });
  })();
  /* ---- Zahlenband: Zahlen laufen hoch, wenn sie ins Bild kommen ----
     Nur die Ziffern werden gezaehlt, Zeichen wie Komma, Prozent oder das
     Bindestrich-Paar bei einer Spanne bleiben stehen. Bei reduzierter
     Bewegung oder ohne Observer steht sofort der Endwert. */
  (function () {
    var band = doc.querySelector(".zahlenband");
    if (!band) return;
    var ziele = $$("[data-zahl]", band);
    if (!ziele.length) return;

    function endwert(el) { el.textContent = el.getAttribute("data-zahl"); }

    var wenigerBewegung = window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (wenigerBewegung || !("IntersectionObserver" in window)) {
      ziele.forEach(endwert);
      return;
    }
    ziele.forEach(function (el) { el.textContent = el.getAttribute("data-zahl"); });

    function zaehlen(el) {
      var text = el.getAttribute("data-zahl");
      var zahlen = text.match(/[\d.,]+/g);
      if (!zahlen) { endwert(el); return; }
      var start = null, dauer = 900;
      function schritt(t) {
        if (start === null) start = t;
        var p = Math.min((t - start) / dauer, 1);
        var weich = 1 - Math.pow(1 - p, 3);
        var i = 0;
        el.textContent = text.replace(/[\d.,]+/g, function (treffer) {
          var ziel = parseFloat(treffer.replace(/\./g, "").replace(",", "."));
          if (isNaN(ziel)) return treffer;
          var jetzt = ziel * weich;
          var nachkomma = treffer.indexOf(",") > -1 ? 2 : 0;
          i++;
          return jetzt.toLocaleString("de-DE", {
            minimumFractionDigits: nachkomma, maximumFractionDigits: nachkomma });
        });
        if (p < 1) requestAnimationFrame(schritt); else endwert(el);
      }
      requestAnimationFrame(schritt);
    }

    var io = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        zaehlen(en.target);
      });
    }, { threshold: 0.6 });
    ziele.forEach(function (el) { io.observe(el); });
    setTimeout(function () { ziele.forEach(endwert); }, 4000);
  })();

  /* ---- Scrollytelling: die Karte folgt dem Text ----
     Jeder Textschritt traegt data-zone mit der Nummer der Zone, die er
     bespricht. Waehrend der Schritt in der Bildmitte steht, wird genau diese
     Zone hervorgehoben und alle anderen treten zurueck.

     Faellt JavaScript aus, bleibt die Klasse veedelkarte--erzaehlt weg: Dann
     sind alle Zonen normal eingefaerbt und alle Schritte voll sichtbar. Der
     Abschnitt funktioniert dann als gewoehnliches Nebeneinander. */
  (function () {
    var szene = doc.querySelector(".szene");
    if (!szene) return;
    var schritte = $$(".szene__schritt", szene);
    var karte = szene.querySelector(".veedelkarte");
    if (!schritte.length || !karte) return;

    var zonen = $$(".dz-zone", karte);
    var schmal = window.matchMedia && window.matchMedia("(max-width:900px)").matches;
    var wenigerBewegung = window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (schmal || wenigerBewegung || !("IntersectionObserver" in window)) {
      szene.classList.add("szene--statisch");
      return;
    }
    // Im Erzaehlmodus ist die Zonenansicht die Grundeinstellung — sonst hebt
    // das Scrollytelling Flaechen hervor, die gar nicht eingeblendet sind.
    karte.classList.add("veedelkarte--erzaehlt", "veedelkarte--zonen");
    $$("[data-ansicht]", karte).forEach(function (b) {
      var an = b.getAttribute("data-ansicht") === "zonen";
      b.classList.toggle("is-an", an);
      b.setAttribute("aria-pressed", an ? "true" : "false");
    });
    // Wer von Hand auf Orientierung wechselt, verlaesst das Erzaehlbild.
    $$("[data-ansicht]", karte).forEach(function (b) {
      on(b, "click", function () {
        karte.classList.toggle("veedelkarte--erzaehlt",
          b.getAttribute("data-ansicht") === "zonen");
      });
    });

    /* Die Karte faehrt zur besprochenen Zone. Eine viewBox laesst sich nicht
       per CSS ueberblenden, deshalb wird sie Bild fuer Bild interpoliert.
       getBBox liefert die Ausdehnung der Zone im Koordinatensystem des SVG —
       genau die Einheit, in der auch die viewBox rechnet. */
    var svg = karte.querySelector("svg");
    var ganz = (svg.getAttribute("viewBox") || "").split(/\s+/).map(Number);
    var jetzt = ganz.slice();
    var lauf = null;

    function setzen(v) { svg.setAttribute("viewBox", v.map(function (n) {
      return Math.round(n * 10) / 10; }).join(" ")); }

    function fahren(ziel) {
      if (lauf) cancelAnimationFrame(lauf);
      var von = jetzt.slice(), start = null, dauer = 700;
      function schritt(t) {
        if (start === null) start = t;
        var p = Math.min((t - start) / dauer, 1);
        var weich = p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
        jetzt = von.map(function (a, i) { return a + (ziel[i] - a) * weich; });
        setzen(jetzt);
        if (p < 1) lauf = requestAnimationFrame(schritt); else lauf = null;
      }
      lauf = requestAnimationFrame(schritt);
    }

    function ausschnittFuer(el) {
      var b;
      try { b = el.getBBox(); } catch (e) { return ganz; }
      if (!b || !b.width || !b.height) return ganz;
      /* Fester Ausschnitt, zentriert auf die Zonenmitte — kein Zoom nach
         Zonengroesse. Die zehn Zonen sind extrem verschieden gross; ein
         zonenabhaengiger Faktor ergab Fahrten zwischen 1,0- und 3,3-fach,
         was unruhig wirkt. Eine gleichmaessige Fahrt liest sich besser, und
         der Umriss bleibt im Zusammenhang sichtbar, auch wenn eine grosse
         Zone ueber den Rand hinausragt. */
      var w = ganz[2] * 0.52, h = ganz[3] * 0.52;
      var x = b.x + b.width / 2 - w / 2;
      var y = b.y + b.height / 2 - h / 2;
      x = Math.max(ganz[0], Math.min(x, ganz[0] + ganz[2] - w));
      y = Math.max(ganz[1], Math.min(y, ganz[1] + ganz[3] - h));
      return [x, y, w, h];
    }

    function betonen(nr) {
      var treffer = null;
      zonen.forEach(function (z) {
        var an = z.getAttribute("data-zone") === String(nr);
        z.classList.toggle("dz-zone--betont", an);
        if (an) treffer = z;
      });
      if (treffer && ganz.length === 4) fahren(ausschnittFuer(treffer));
    }

    var io = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (en) {
        if (!en.isIntersecting) return;
        schritte.forEach(function (s) { s.classList.toggle("ist-dran", s === en.target); });
        betonen(en.target.getAttribute("data-zone"));
      });
    }, { rootMargin: "-45% 0px -45% 0px" });
    schritte.forEach(function (s) { io.observe(s); });

    // Anfangszustand: erster Schritt aktiv, damit die Karte nie leer wirkt.
    schritte[0].classList.add("ist-dran");
    betonen(schritte[0].getAttribute("data-zone"));
  })();
  /* ---- Verlaufskurve zeichnet sich beim Sichtbarwerden ----
     Die Pfadlaenge wird zur Laufzeit gemessen und als CSS-Variable gesetzt;
     ein fester Wert im Stylesheet wuerde bei anderer Kurvenform nicht passen. */
  (function () {
    var kurven = $$(".verlauf");
    if (!kurven.length) return;
    var wenigerBewegung = window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (wenigerBewegung || !("IntersectionObserver" in window)) {
      kurven.forEach(function (k) { k.classList.add("verlauf--gezeichnet"); });
      return;
    }
    kurven.forEach(function (k) {
      var linie = k.querySelector(".vl-linie");
      if (linie && linie.getTotalLength) {
        try { k.style.setProperty("--laenge", Math.ceil(linie.getTotalLength()) + "px"); }
        catch (e) {}
      }
    });
    var io = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        en.target.classList.add("verlauf--gezeichnet");
      });
    }, { threshold: 0.35 });
    kurven.forEach(function (k) { io.observe(k); });
    setTimeout(function () {
      kurven.forEach(function (k) { k.classList.add("verlauf--gezeichnet"); });
    }, 4000);
  })();
  /* ---- Preisquellen-Vergleich ----
     Rechnet dieselbe Wohnflaeche gegen mehrere Quellen und zeigt die Spanne.
     Der Kern der Aussage: Portale nennen Angebotspreise, der Gutachter-
     ausschuss notarielle Kaufpreise — deshalb liegen sie auseinander.

     Die Werte stehen als data-Attribute im Markup, damit Zahl und Quelle
     zusammenbleiben und niemand sie im Skript nachpflegen muss. */
  (function () {
    var block = doc.querySelector(".quellen");
    if (!block) return;
    var feld = doc.getElementById("qu-flaeche");
    var zeilen = $$(".quelle", block);
    var fazitWert = block.querySelector(".quellen__fazit b");
    var fazitText = block.querySelector(".quellen__fazit span");
    if (!feld || !zeilen.length) return;

    var geld = new Intl.NumberFormat("de-DE", {
      style: "currency", currency: "EUR", maximumFractionDigits: 0 });
    var art = "wohnung";

    function rechnen() {
      var qm = parseFloat(feld.value);
      if (!(qm > 0)) qm = 0;

      var summen = [];
      zeilen.forEach(function (z) {
        var passt = z.getAttribute("data-art") === art;
        z.hidden = !passt;
        if (!passt) return;
        var preis = parseFloat(z.getAttribute("data-preis"));
        summen.push({ el: z, summe: preis * qm });
      });
      if (!summen.length) return;

      var hoch = Math.max.apply(null, summen.map(function (s) { return s.summe; }));
      var tief = Math.min.apply(null, summen.map(function (s) { return s.summe; }));

      summen.forEach(function (s) {
        s.el.querySelector(".quelle__summe").textContent =
          qm ? geld.format(Math.round(s.summe)) : "—";
        var balken = s.el.querySelector(".quelle__balken i");
        if (balken) balken.style.width = hoch ? (s.summe / hoch * 100) + "%" : "0";
      });

      var spanne = hoch - tief;
      fazitWert.textContent = qm ? geld.format(Math.round(spanne)) : "—";
      fazitText.textContent = qm
        ? "liegen zwischen der niedrigsten und der höchsten Einschätzung für "
          + qm.toLocaleString("de-DE") + " m². Welche davon in Ihrem Kaufvertrag steht, "
          + "entscheidet keine dieser Quellen — sondern Ihr Objekt."
        : "Bitte eine Wohnfläche eingeben.";
    }

    on(feld, "input", rechnen);
    $$(".quellen__art button", block).forEach(function (b) {
      on(b, "click", function () {
        art = b.getAttribute("data-art");
        $$(".quellen__art button", block).forEach(function (o) {
          var an = o === b;
          o.classList.toggle("is-an", an);
          o.setAttribute("aria-pressed", an ? "true" : "false");
        });
        rechnen();
      });
    });
    rechnen();
  })();

  /* Ehrenfelder Lagekarte, Satzungspruefer (v49)
     ---------------------------------------------------------------------
     Drei Ansichten im selben SVG. Anders als bei den frueheren Veedelkarten
     skaliert diese mit der Fensterbreite, statt auf ihrer Entwurfsbreite zu
     stehen und seitlich gewischt zu werden. Moeglich ist das, weil die
     Orientierungspunkte Nummern tragen und die Namen als Liste darunter
     stehen: Eine Ziffer im Kreis bleibt bei 358 Pixeln lesbar, ein
     Strassenname nicht.
     Der Pruefer beantwortet, ob eine Adresse im Gebiet der Sozialen
     Erhaltungssatzung Ehrenfeld-Ost liegt. Die Zuordnung ist im Bauskript
     gegen die amtliche Geometrie aus dem Geoportal der Stadt Koeln geprueft
     und steht als Wahrheitswert in den Daten — hier wird nichts gerechnet
     und nichts geschaetzt. */
  (function () {
    var abschnitt = doc.getElementById("karte");
    var rahmen = doc.getElementById("ehrkarte");
    var feld = doc.getElementById("ehrkarte-info");
    var quelle = doc.getElementById("ehrkarte-daten");
    if (!abschnitt || !rahmen || !feld || !quelle) return;
    var daten = {};
    try { daten = JSON.parse(quelle.textContent || "{}"); } catch (e) { return; }
    var leer = feld.textContent;
    var stufen = abschnitt.querySelector(".ehrkarte__stufen");
    var eintraege = $$(".ehrk-liste__knopf", abschnitt);
    var marken = $$(".ehrk-marke", rahmen);
    var zonen = $$(".ehrk-zone", rahmen);
    var offen = null;
    function zuruecksetzen() {
      eintraege.forEach(function (li) { li.removeAttribute("aria-current"); });
      offen = null;
    }
    function markeZeigen(nr) {
      var m = (daten.marken || []).filter(function (x) { return x.nr === nr; })[0];
      if (!m) return;
      zuruecksetzen();
      feld.innerHTML = "<b>" + m.nr + ". " + m.name + "</b> " + m.text;
      offen = "m" + nr;
      eintraege.forEach(function (li) {
        if (parseInt(li.getAttribute("data-nr"), 10) === nr) li.setAttribute("aria-current", "true");
      });
    }
    function zoneZeigen(el) {
      var brw = el.getAttribute("data-brw");
      var lage = el.getAttribute("data-lage") || "";
      var gfz = el.getAttribute("data-gfz") || "";
      zuruecksetzen();
      /* Die Lagebezeichnungen aus BORIS enden teils selbst auf einem Punkt
         ("Venloer Str./Philippstr."). Ohne diese Pruefung stehen zwei. */
      var lageText = lage.replace(/\.$/, "");
      feld.innerHTML = "<b>" + Number(brw).toLocaleString("de-DE") + " € je m² Grundstück</b> "
        + el.getAttribute("data-nutzung") + (lageText ? ", Lage " + lageText : "")
        + (gfz ? ". Zulässige Geschossflächenzahl " + gfz + "." : ".");
      offen = "z" + brw + lage;
    }
    marken.forEach(function (el) {
      var nr = parseInt(el.getAttribute("data-nr"), 10);
      on(el, "click", function () {
        if (offen === "m" + nr) { feld.innerHTML = leer; zuruecksetzen(); }
        else markeZeigen(nr);
      });
      on(el, "keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); markeZeigen(nr); }
      });
    });
    zonen.forEach(function (el) {
      on(el, "click", function () { zoneZeigen(el); });
      on(el, "keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); zoneZeigen(el); }
      });
    });
    eintraege.forEach(function (li) {
      var nr = parseInt(li.getAttribute("data-nr"), 10);
      function waehlen() {
        markeZeigen(nr);
        /* Die Karte steht oberhalb der Liste. Ohne diesen Sprung tippt man
           auf einen Namen und sieht die zugehoerige Nummer nicht. */
        if (rahmen.getBoundingClientRect().top < 0) {
          rahmen.scrollIntoView({ block: "center", behavior: "smooth" });
        }
      }
      /* Kein eigenes keydown noetig: Ein natives button loest bei Enter
         und Leertaste selbst ein click aus. */
      on(li, "click", waehlen);
    });
    var knoepfe = $$("[data-ansicht]", abschnitt);
    knoepfe.forEach(function (b) {
      on(b, "click", function () {
        var ziel = b.getAttribute("data-ansicht");
        rahmen.classList.toggle("ehrkarte--zonen", ziel === "zonen");
        rahmen.classList.toggle("ehrkarte--satzung", ziel === "satzung");
        if (stufen) stufen.hidden = ziel !== "zonen";
        knoepfe.forEach(function (o) {
          o.setAttribute("aria-pressed", o === b ? "true" : "false");
        });
        feld.innerHTML = ziel === "zonen"
          ? "Tippen oder klicken Sie eine Fläche an: Sie zeigt den amtlichen Bodenrichtwert, die zulässige Nutzung und die Geschossflächenzahl."
          : ziel === "satzung"
            ? "Die rot umrandete Fläche ist das Gebiet der Sozialen Erhaltungssatzung Ehrenfeld-Ost. Innerhalb dieser Grenze sind Rückbau, Änderung und Nutzungsänderung genehmigungspflichtig."
            : leer;
        zuruecksetzen();
      });
    });
    /* Der Pruefer unter der Karte */
    var auswahl = doc.getElementById("satzung-ort");
    var antwort = doc.getElementById("satzung-antwort");
    if (!auswahl || !antwort) return;
    var orte = (daten.marken || []).slice().sort(function (a, b) {
      return a.name.localeCompare(b.name, "de");
    });
    orte.forEach(function (m) {
      var o = doc.createElement("option");
      o.value = String(m.nr);
      o.textContent = m.name;
      auswahl.appendChild(o);
    });
    var DRIN = "<b>Ja — hier gilt die Erhaltungssatzung.</b>"
      + "<p>Für Immobilien in diesem Gebiet brauchen die folgenden Vorhaben eine zusätzliche Genehmigung der Stadt Köln:</p>"
      + "<ul class=\"satzung__folgen\">"
      + "<li>Rückbau baulicher Anlagen, auch teilweise</li>"
      + "<li>Änderung baulicher Anlagen — dazu zählen etwa Grundrissänderungen und das Zusammenlegen von Wohnungen</li>"
      + "<li>Nutzungsänderung, etwa von Wohnraum in Gewerbe oder umgekehrt</li>"
      + "</ul>"
      + "<p>Das gilt auch dann, wenn die Landesbauordnung Nordrhein-Westfalen für dieselbe Maßnahme keine Genehmigung verlangt. Wer mit Entwicklungsabsicht kauft oder verkauft, sollte das vor dem Vermarktungsstart klären.</p>";
    var RAUS = "<b>Nein — hier gilt die Erhaltungssatzung nicht.</b>"
      + "<p>Für diese Lage entfällt der zusätzliche erhaltungsrechtliche Genehmigungsvorbehalt. Es gelten die allgemeinen Regeln: Bauordnung, Bebauungsplan, Denkmalschutz und, bei Eigentumswohnungen, die Teilungserklärung und die Beschlüsse der Eigentümergemeinschaft.</p>"
      + "<p>Für Käufer mit Entwicklungsabsicht kann genau das ein Vorteil sein — ein Konzept, das wenige Straßen weiter am Genehmigungsvorbehalt hängt, ist hier unter den allgemeinen Regeln zu prüfen.</p>";
    on(auswahl, "change", function () {
      var nr = parseInt(auswahl.value, 10);
      if (!nr) {
        antwort.setAttribute("data-lage", "leer");
        antwort.innerHTML = "Wählen Sie einen Punkt aus der Liste. Sie erfahren, ob dort die Erhaltungssatzung gilt und was daraus folgt.";
        return;
      }
      var m = (daten.marken || []).filter(function (x) { return x.nr === nr; })[0];
      if (!m) return;
      var drin = m.satzung === true;
      antwort.setAttribute("data-lage", drin ? "drin" : "raus");
      antwort.innerHTML = "<span style=\"display:block;font-size:.86rem;opacity:.8;margin-bottom:6px\">"
        + m.name + "</span>" + (drin ? DRIN : RAUS);
      /* Die Karte auf die Satzungsansicht stellen: Wer fragt, ob seine Lage
         betroffen ist, will die Grenze auch sehen. */
      var satzungKnopf = knoepfe.filter(function (b) {
        return b.getAttribute("data-ansicht") === "satzung";
      })[0];
      if (satzungKnopf && satzungKnopf.getAttribute("aria-pressed") !== "true") {
        satzungKnopf.click();
      }
      markeZeigen(nr);
    });
  })();

  /* Lindenthaler Lagekarte und Bodenanteil-Rechner (v50)
     ---------------------------------------------------------------------
     Drei Ansichten derselben Karte. Die dritte faerbt die Bodenrichtwert-
     zonen nicht nach ihrem Wert je Quadratmeter Grundstueck, sondern nach
     dem Wert je Quadratmeter Wohnflaeche — also Bodenrichtwert geteilt durch
     zulaessige Geschossflaechenzahl. Dabei verschiebt sich die Rangfolge:
     Die Zone mit dem niedrigsten Bodenrichtwert Lindenthals hat den
     zweithoechsten Anteil, weil dort nur locker gebaut werden darf.

     Der Rechner gibt eine Groessenordnung aus amtlichen Bodenrichtwerten.
     Was das Gebaeude wert ist, kann er nicht wissen — deshalb steht das
     Ergebnis ausdruecklich als Anteil am Vergleichswert da und nicht als
     Immobilienbewertung. */
  (function () {
    var abschnitt = doc.getElementById("karte");
    var rahmen = doc.getElementById("lindkarte");
    var feld = doc.getElementById("lindkarte-info");
    var quelle = doc.getElementById("lindkarte-daten");
    if (!abschnitt || !rahmen || !feld || !quelle) return;

    var daten = {};
    try { daten = JSON.parse(quelle.textContent || "{}"); } catch (e) { return; }

    var leer = feld.textContent;
    var stufenBrw = doc.getElementById("lind-stufen-brw");
    var stufenAnteil = doc.getElementById("lind-stufen-anteil");
    var eintraege = $$(".lind-liste__knopf", abschnitt);
    var marken = $$(".lind-marke", rahmen);
    var offen = null;

    function euro(n) { return Number(n).toLocaleString("de-DE"); }

    function zuruecksetzen() {
      eintraege.forEach(function (k) { k.removeAttribute("aria-current"); });
      offen = null;
    }

    function markeZeigen(nr) {
      var m = (daten.marken || []).filter(function (x) { return x.nr === nr; })[0];
      if (!m) return;
      zuruecksetzen();
      feld.innerHTML = "<b>" + m.nr + ". " + m.name + "</b> " + m.text;
      offen = "m" + nr;
      eintraege.forEach(function (k) {
        if (parseInt(k.getAttribute("data-nr"), 10) === nr) k.setAttribute("aria-current", "true");
      });
    }

    marken.forEach(function (el) {
      var nr = parseInt(el.getAttribute("data-nr"), 10);
      on(el, "click", function () {
        if (offen === "m" + nr) { feld.innerHTML = leer; zuruecksetzen(); }
        else markeZeigen(nr);
      });
      on(el, "keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); markeZeigen(nr); }
      });
    });

    $$(".lind-zone", rahmen).forEach(function (el) {
      function zeigen() {
        var lage = (el.getAttribute("data-lage") || "").replace(/\.$/, "");
        var gfz = el.getAttribute("data-gfz") || "";
        var anzahl = parseInt(el.getAttribute("data-anzahl"), 10) || 1;
        zuruecksetzen();
        if (anzahl > 1) {
          /* Auf dieser Flaeche liegen mehrere Richtwerte. In den BORIS-Daten
             tragen benachbarte Zonen teils dieselbe Umringgeometrie; welcher
             Wert fuer welchen Teil gilt, geht daraus nicht hervor. Beide
             nennen ist ehrlicher, als einen davon zu verschweigen. */
          feld.innerHTML = "<b>" + euro(el.getAttribute("data-tief")) + " bis "
            + euro(el.getAttribute("data-brw")) + " € je m² Grundstück</b> "
            + "Für diese Fläche führt BORIS NRW " + anzahl + " Richtwerte: "
            + (el.getAttribute("data-werte") || "") + ". Die amtlichen Umringe sind hier "
            + "deckungsgleich abgelegt — welcher Wert für ein bestimmtes Flurstück gilt, "
            + "beantwortet der Gutachterausschuss.";
          return;
        }
        feld.innerHTML = "<b>" + euro(el.getAttribute("data-brw")) + " € je m² Grundstück</b> "
          + el.getAttribute("data-nutzung") + (lage ? ", Lage " + lage : "")
          + (gfz ? ". Zulässige Geschossflächenzahl " + gfz + "." : ".");
      }
      on(el, "click", zeigen);
      on(el, "keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); zeigen(); }
      });
    });

    $$(".lind-anteilflaeche", rahmen).forEach(function (el) {
      function zeigen() {
        var lage = (el.getAttribute("data-lage") || "").replace(/\.$/, "");
        zuruecksetzen();
        feld.innerHTML = "<b>" + euro(el.getAttribute("data-jewohn"))
          + " € Bodenwert je m² Wohnfläche</b> " + (lage ? lage + ": " : "")
          + euro(el.getAttribute("data-brw")) + " € je m² Grundstück, geteilt durch die "
          + "zulässige Geschossflächenzahl " + el.getAttribute("data-gfz") + ".";
      }
      on(el, "click", zeigen);
      on(el, "keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); zeigen(); }
      });
    });

    eintraege.forEach(function (knopf) {
      var nr = parseInt(knopf.getAttribute("data-nr"), 10);
      on(knopf, "click", function () {
        markeZeigen(nr);
        if (rahmen.getBoundingClientRect().top < 0) {
          rahmen.scrollIntoView({ block: "center", behavior: "smooth" });
        }
      });
    });

    var knoepfe = $$("[data-lansicht]", abschnitt);
    knoepfe.forEach(function (b) {
      on(b, "click", function () {
        var ziel = b.getAttribute("data-lansicht");
        rahmen.classList.toggle("lindkarte--zonen", ziel === "zonen");
        rahmen.classList.toggle("lindkarte--anteil", ziel === "anteil");
        if (stufenBrw) stufenBrw.hidden = ziel !== "zonen";
        if (stufenAnteil) stufenAnteil.hidden = ziel !== "anteil";
        knoepfe.forEach(function (o) {
          o.setAttribute("aria-pressed", o === b ? "true" : "false");
        });
        feld.innerHTML = ziel === "zonen"
          ? "Tippen oder klicken Sie eine Fläche an: Sie zeigt den amtlichen Bodenrichtwert je Quadratmeter Grundstück, die zulässige Nutzung und die Geschossflächenzahl."
          : ziel === "anteil"
            ? "Dieselben Zonen, umgerechnet auf einen Quadratmeter Wohnfläche. Je dunkler, desto mehr Bodenwert steckt in jedem Quadratmeter Wohnung. Zonen ohne amtliche Geschossflächenzahl bleiben leer."
            : leer;
        zuruecksetzen();
      });
    });

    /* --- Der Rechner ---------------------------------------------------- */
    var wahl = doc.getElementById("ba-zone");
    var grund = doc.getElementById("ba-grund");
    var wohn = doc.getElementById("ba-wohn");
    var summe = doc.getElementById("ba-summe");
    var formel = doc.getElementById("ba-formel");
    var balken = doc.getElementById("ba-balken");
    var anteilText = doc.getElementById("ba-anteil");
    var lesart = doc.getElementById("ba-lesart");
    if (!wahl || !grund || !wohn) return;

    /* Vergleichswert: der amtliche Durchschnitt weiterverkaufter
       Eigentumswohnungen in Lindenthal. Er ist keine Bewertung des einzelnen
       Objekts, aber der einzige belastbare Massstab, den es gibt. */
    var VERGLEICH = 5569;

    var zonen = (daten.zonen || []).slice().sort(function (a, b) { return b.brw - a.brw; });
    zonen.forEach(function (z, i) {
      var o = doc.createElement("option");
      o.value = String(i);
      o.textContent = (z.lage || "Zone") + " — " + euro(z.brw) + " €/m²";
      wahl.appendChild(o);
    });
    /* Mit der teuersten Zone stuende der Balken schon vor der ersten Eingabe
       auf Anschlag. Voreingestellt ist deshalb die mittlere. */
    wahl.value = String(Math.floor(zonen.length / 2));

    function rechnen() {
      var z = zonen[parseInt(wahl.value, 10) || 0];
      if (!z) return;
      var gf = Math.max(0, parseFloat(grund.value) || 0);
      var wf = Math.max(1, parseFloat(wohn.value) || 1);
      var boden = z.brw * gf;
      var gesamt = VERGLEICH * wf;
      var anteil = gesamt > 0 ? boden / gesamt : 0;

      summe.textContent = euro(Math.round(boden)) + " €";
      formel.textContent = euro(z.brw) + " € × " + euro(gf) + " m² Grundstück";

      var prozent = Math.round(anteil * 100);
      /* Der Balken kann nicht ueber die volle Breite hinaus, die Zahl schon —
         und sie soll es auch: Ein gedeckelter Wert wuerde verschweigen, um
         wie viel der Bodenwert den Vergleichswert uebersteigt. */
      balken.style.width = Math.min(100, Math.max(6, prozent)) + "%";
      anteilText.textContent = prozent + " % Boden";

      var vergleichstext = "Gemessen am Lindenthaler Durchschnitt von "
        + euro(VERGLEICH) + " € je m² Wohnfläche entspräche Ihre Immobilie rund "
        + euro(Math.round(gesamt)) + " €. ";

      if (prozent >= 100) {
        lesart.innerHTML = vergleichstext + "<b>Der Bodenwert allein übersteigt diesen Vergleichswert.</b> "
          + "Bei solchen Grundstücken kaufen Interessenten faktisch die Lage — das Gebäude wird "
          + "häufig umgebaut oder ersetzt. Für die Vermarktung heißt das: Grundstück, Zuschnitt und "
          + "Bebauungsmöglichkeiten gehören nach vorn, nicht die Ausstattung.";
      } else if (prozent >= 55) {
        lesart.innerHTML = vergleichstext + "<b>Über die Hälfte davon entfällt auf das Grundstück.</b> "
          + "Modernisierungen heben den Preis hier meist weniger als erhofft. Wichtiger ist, was auf "
          + "dem Grundstück zulässig wäre.";
      } else if (prozent >= 30) {
        lesart.innerHTML = vergleichstext + "Rund ein Drittel bis die Hälfte steckt im Boden — "
          + "ein typisches Verhältnis für Lindenthaler Häuser. Grundstück und Gebäude tragen beide "
          + "erkennbar zum Wert bei, und beide gehören ins Exposé.";
      } else {
        lesart.innerHTML = vergleichstext + "Der Bodenanteil ist gering — typisch für eine "
          + "Eigentumswohnung, bei der sich das Grundstück auf alle Einheiten verteilt. Hier "
          + "entscheiden Zustand, Grundriss, Ausstattung und Hausgeld über den Preis.";
      }
    }

    on(wahl, "change", rechnen);
    on(grund, "input", rechnen);
    on(wohn, "input", rechnen);
    rechnen();
  })();


  /* Klettenberger Lagekarte (v53)
     ---------------------------------------------------------------------
     Zwei Ansichten. Eine dritte nach Bodenwert je Quadratmeter Wohnflaeche
     gibt es hier bewusst nicht: Klettenberg hat nur zwei Zonen, die sich um
     vier Prozent unterscheiden — eine Umrechnung brächte keinen
     Erkenntnisgewinn, nur eine weitere Schaltflaeche. */
  (function () {
    var abschnitt = doc.getElementById("karte");
    var rahmen = doc.getElementById("klettkarte");
    var feld = doc.getElementById("klettkarte-info");
    var quelle = doc.getElementById("klettkarte-daten");
    if (!abschnitt || !rahmen || !feld || !quelle) return;

    var daten = {};
    try { daten = JSON.parse(quelle.textContent || "{}"); } catch (e) { return; }

    var leer = feld.textContent;
    var stufen = doc.getElementById("klett-stufen");
    var eintraege = $$(".klett-liste__knopf", abschnitt);
    var marken = $$(".klett-marke", rahmen);
    var offen = null;

    function euro(n) { return Number(n).toLocaleString("de-DE"); }

    function zuruecksetzen() {
      eintraege.forEach(function (k) { k.removeAttribute("aria-current"); });
      offen = null;
    }

    function markeZeigen(nr) {
      var m = (daten.marken || []).filter(function (x) { return x.nr === nr; })[0];
      if (!m) return;
      zuruecksetzen();
      feld.innerHTML = "<b>" + m.nr + ". " + m.name + "</b> " + m.text;
      offen = "m" + nr;
      eintraege.forEach(function (k) {
        if (parseInt(k.getAttribute("data-nr"), 10) === nr) k.setAttribute("aria-current", "true");
      });
    }

    marken.forEach(function (el) {
      var nr = parseInt(el.getAttribute("data-nr"), 10);
      on(el, "click", function () {
        if (offen === "m" + nr) { feld.innerHTML = leer; zuruecksetzen(); }
        else markeZeigen(nr);
      });
      on(el, "keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); markeZeigen(nr); }
      });
    });

    $$(".klett-zone", rahmen).forEach(function (el) {
      function zeigen() {
        var lage = (el.getAttribute("data-lage") || "").replace(/\.$/, "");
        var gfz = el.getAttribute("data-gfz") || "";
        zuruecksetzen();
        feld.innerHTML = "<b>" + euro(el.getAttribute("data-brw")) + " € je m² Grundstück</b> "
          + el.getAttribute("data-nutzung") + (lage ? ", Lage " + lage : "")
          + (gfz ? ". Zulässige Geschossflächenzahl " + gfz + "." : ".");
      }
      on(el, "click", zeigen);
      on(el, "keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); zeigen(); }
      });
    });

    eintraege.forEach(function (knopf) {
      var nr = parseInt(knopf.getAttribute("data-nr"), 10);
      on(knopf, "click", function () {
        markeZeigen(nr);
        if (rahmen.getBoundingClientRect().top < 0) {
          rahmen.scrollIntoView({ block: "center", behavior: "smooth" });
        }
      });
    });

    var knoepfe = $$("[data-kansicht]", abschnitt);
    knoepfe.forEach(function (b) {
      on(b, "click", function () {
        var ziel = b.getAttribute("data-kansicht");
        rahmen.classList.toggle("klettkarte--zonen", ziel === "zonen");
        if (stufen) stufen.hidden = ziel !== "zonen";
        knoepfe.forEach(function (o) {
          o.setAttribute("aria-pressed", o === b ? "true" : "false");
        });
        feld.innerHTML = ziel === "zonen"
          ? "Zwei Zonen, 1.590 und 1.650 Euro je Quadratmeter Grundstück. Tippen oder klicken Sie eine Fläche an."
          : leer;
        zuruecksetzen();
      });
    });
  })();

  /* Unterlagen-Prüfer (Raderthal) --------------------------------------
     Zeigt je Objektart, welche Unterlagen für Verkauf und Käuferfinanzierung
     gebraucht werden. Die Herkunft steht dabei: Was der Eigentümer selbst
     hat, was eine Behörde ausstellt, was über die Verwaltung kommt. */
  (function () {
    var wurzel = $("[data-rad-pruefer]");
    if (!wurzel) return;

    var GEMEINSAM = [
      ["Aktueller Grundbuchauszug", "Amtsgericht — Beschaffung über unser Notariatsnetzwerk möglich"],
      ["Flurkarte / Liegenschaftskarte", "Stadt Köln, online bestellbar"],
      ["Nachvollziehbare Grundrisse", "Eigentümer oder Bauakte; bei Umbauten aktualisieren"],
      ["Wohn- bzw. Nutzflächenberechnung", "Eigentümer; fehlt sie, über Architekt oder Sachverständigen"],
      ["Gültiger Energieausweis", "gilt zehn Jahre; sonst über Energieberater"]
    ];

    var ARTEN = {
      haus: {
        name: "Einfamilienhaus, Reihenhaus oder Doppelhaushälfte",
        zusatz: [
          ["Bauzeichnungen, Ansichten, Schnitte", "Bauakte der Stadt Köln, falls nicht vorhanden"],
          ["Baugenehmigungen", "besonders wichtig bei An- und Ausbauten"],
          ["Nachweise zu Modernisierungen", "Rechnungen und Handwerkerbelege"],
          ["Baulastenauskunft", "Bauaufsicht; klärt Einschränkungen der Nutzung"],
          ["Angaben zur Heizung und zum energetischen Zustand", "Eigentümer, Wartungsunterlagen"]
        ]
      },
      wohnung: {
        name: "Eigentumswohnung",
        zusatz: [
          ["Teilungserklärung und Gemeinschaftsordnung", "Eigentümer oder Hausverwaltung"],
          ["Aufteilungsplan", "Eigentümer oder Hausverwaltung"],
          ["Aktueller Wirtschaftsplan", "Hausverwaltung"],
          ["Jahresabrechnungen und Hausgeldangaben", "Hausverwaltung"],
          ["Stand der Erhaltungsrücklage", "Hausverwaltung — für Käufer und Bank besonders relevant"],
          ["Protokolle der letzten drei Eigentümerversammlungen", "Hausverwaltung"],
          ["Beschlüsse zu geplanten Maßnahmen", "zeigt bevorstehende Sonderumlagen"]
        ]
      },
      grundstueck: {
        name: "Grundstück",
        zusatz: [
          ["Baulastenauskunft", "Bauaufsicht Stadt Köln"],
          ["Auskunft zu Altlasten und Bodenverunreinigungen", "Altlastenkataster — löst sonst später Prüfbedarf aus"],
          ["Angaben zu Erschließungsbeiträgen", "Stadt Köln; offene Beiträge treffen sonst den Käufer"],
          ["Auskunft zum geltenden Baurecht", "bestimmt, was entstehen darf"],
          ["Eingetragene Dienstbarkeiten", "Grundbuch, Abteilung II — etwa Wege- oder Leitungsrechte"]
        ],
        entfaellt: ["Gültiger Energieausweis", "Wohn- bzw. Nutzflächenberechnung", "Nachvollziehbare Grundrisse"]
      },
      mehrfamilien: {
        name: "Mehrfamilienhaus",
        zusatz: [
          ["Mietvertragsübersicht und Mieterliste", "Eigentümer oder Verwaltung"],
          ["Aufstellung der Ist-Mieten", "Grundlage des Ertragswertverfahrens"],
          ["Betriebskostenabrechnungen", "letzte zwei bis drei Jahre"],
          ["Nachweise zu Instandhaltung und Sanierung", "belegt den Zustand gegenüber Bank und Käufer"],
          ["Angaben zu Leerstand und Mietrückständen", "wird von finanzierenden Banken geprüft"],
          ["Baulastenauskunft", "Bauaufsicht Stadt Köln"]
        ]
      }
    };

    var liste = $("[data-rad-liste]", wurzel);
    var stand = $("[data-rad-stand]", wurzel);
    var knoepfe = $$(".rad-pruefer__knopf", wurzel);

    function zeichnen(schluessel) {
      var art = ARTEN[schluessel];
      if (!art) return;
      var weg = art.entfaellt || [];
      var posten = GEMEINSAM.filter(function (g) {
        return weg.indexOf(g[0]) === -1;
      }).concat(art.zusatz);

      liste.innerHTML = posten.map(function (p) {
        return '<li><b>' + p[0] + '</b><span>' + p[1] + '</span></li>';
      }).join("");
      stand.textContent = art.name + ": " + posten.length + " Unterlagen, die üblicherweise gebraucht werden.";
    }

    knoepfe.forEach(function (b) {
      on(b, "click", function () {
        knoepfe.forEach(function (o) {
          var aktiv = o === b;
          o.classList.toggle("is-aktiv", aktiv);
          o.setAttribute("aria-pressed", aktiv ? "true" : "false");
        });
        zeichnen(b.getAttribute("data-art"));
      });
    });

    zeichnen("haus");
  })();

  /* Mikrolagen-Wähler (Raderberg) --------------------------------------
     Macht den zentralen Gedanken bedienbar: Käufer erleben keine
     Durchschnittslage. Je Straße zeigt die Tafel, welche Eigenschaften dort
     über den Preis entscheiden und welche Käufergruppe zuerst hinschaut. */
  (function () {
    var wurzel = $("[data-rb-lagen]");
    if (!wurzel) return;

    var LAGEN = {
      kreuznacher: {
        name: "Kreuznacher Straße",
        lage: "Am westlichen Rand Raderbergs, nah am Vorgebirgspark.",
        zaehlt: ["Entfernung zum Park in Gehminuten",
                 "Ruhe der Straße zu unterschiedlichen Tageszeiten",
                 "Balkon oder Terrasse zur begrünten Seite",
                 "Stellplatzsituation im Umfeld"],
        kaeufer: "Menschen, denen Grün im Alltag wichtig ist: Familien, Hundehaltende, Ältere mit festen Wegen.",
        hinweis: "Hier ist die Nähe zur Grünfläche ein eigenständiges Verkaufsargument — sie gehört ins Exposé, nicht in den Nebensatz."
      },
      bruehler: {
        name: "Brühler Straße",
        lage: "Verkehrsgeprägte Hauptachse mit direkter Anbindung.",
        zaehlt: ["Lage der Wohnung im Gebäude — vorn oder rückwärtig",
                 "Ausrichtung von Schlafräumen und Balkon",
                 "Schallschutz der Fenster, Baujahr und Nachrüstung",
                 "Garage oder fester Stellplatz"],
        kaeufer: "Pendelnde und Kapitalanlegende, für die Anbindung und Vermietbarkeit zählen.",
        hinweis: "Eine rückwärtig ausgerichtete Wohnung an einer Hauptstraße ist etwas völlig anderes als eine zur Straße hin — dieser Unterschied entscheidet über den Preis und muss aktiv gezeigt werden."
      },
      mannsfelder: {
        name: "Mannsfelder Straße",
        lage: "Wohnstraße im gewachsenen Teil des Stadtteils.",
        zaehlt: ["Etage und Vorhandensein eines Aufzugs",
                 "Grundriss und Schnitt der Räume",
                 "Ausrichtung von Balkon und Wohnräumen",
                 "Zustand des Gemeinschaftseigentums und Erhaltungsrücklage"],
        kaeufer: "Selbstnutzende, die in der Nachbarschaft bleiben oder aus einem größeren Objekt verkleinern wollen.",
        hinweis: "In gewachsenen Wohnlagen entscheidet das Gebäude mit: Wirtschaftsplan, Rücklage und beschlossene Maßnahmen prüfen Käufer genau."
      },
      raderberger: {
        name: "Raderberger Straße",
        lage: "Zentrale Achse Richtung Innenstadt und Grüngürtel.",
        zaehlt: ["Nähe zu Nahversorgung und Haltestellen",
                 "Wie sich die Umgebung durch die Parkstadt Süd verändert",
                 "Zuschnitt und Nutzbarkeit bei Häusern und Grundstücken",
                 "Bestehende Bebauung im direkten Umfeld"],
        kaeufer: "Käufer, die auf die Entwicklung des Stadtteils setzen — und solche, die deshalb zögern.",
        hinweis: "Hier ist die Stadtentwicklung tatsächlich ein Thema im Verkaufsgespräch. Sie sollte belegt angesprochen werden, nicht als Werbeversprechen."
      }
    };

    var tafel = $("[data-rb-tafel]", wurzel);
    var knoepfe = $$(".rb-lagen__knopf", wurzel);

    function zeichnen(schluessel) {
      var l = LAGEN[schluessel];
      if (!l) return;
      tafel.innerHTML =
        '<p class="rb-lagen__ort">' + l.name + '</p>' +
        '<p class="rb-lagen__lage">' + l.lage + '</p>' +
        '<p class="rb-lagen__titel">Was hier über den Preis entscheidet</p>' +
        '<ul class="rb-lagen__liste">' +
          l.zaehlt.map(function (z) { return "<li>" + z + "</li>"; }).join("") +
        '</ul>' +
        '<p class="rb-lagen__titel">Wer zuerst hinschaut</p>' +
        '<p class="rb-lagen__kaeufer">' + l.kaeufer + '</p>' +
        '<p class="rb-lagen__hinweis">' + l.hinweis + '</p>';
    }

    knoepfe.forEach(function (b) {
      on(b, "click", function () {
        knoepfe.forEach(function (o) {
          var aktiv = o === b;
          o.classList.toggle("is-aktiv", aktiv);
          o.setAttribute("aria-pressed", aktiv ? "true" : "false");
        });
        zeichnen(b.getAttribute("data-lage"));
      });
    });

    zeichnen("kreuznacher");
  })();

  /* Bodenwert-Rechner (Marienburg) -------------------------------------
     Rechnet ausschließlich mit dem amtlichen Bodenrichtwert von 2.100 Euro
     je Quadratmeter — keine geschätzten Zu- oder Abschläge. Gezeigt wird,
     was der Boden allein wert ist und wie er sich zum Wohnungspreis
     verhält, denn genau daran scheitert der Quadratmeterpreis bei
     Villengrundstücken. */
  (function () {
    var wurzel = $("[data-mrb-boden]");
    if (!wurzel) return;

    var BRW = 2100;        // BORIS NRW, Stichtag 1.1.2026, eine Zone
    var WOHNUNG = 5684;    // Median Weiterverkauf Eigentumswohnungen 2025

    var regler = $("[data-mrb-flaeche]", wurzel);
    var wohnRegler = $("[data-mrb-wohnflaeche]", wurzel);
    var anzeigeGrund = $("[data-mrb-anzeige-grund]", wurzel);
    var anzeigeWohn = $("[data-mrb-anzeige-wohn]", wurzel);
    var ausgabe = $("[data-mrb-ausgabe]", wurzel);

    function euro(n) {
      return Math.round(n).toLocaleString("de-DE") + " €";
    }

    function rechnen() {
      var grund = parseInt(regler.value, 10);
      var wohn = parseInt(wohnRegler.value, 10);
      var bodenwert = grund * BRW;
      var jeWohnflaeche = bodenwert / wohn;
      var wohnwert = wohn * WOHNUNG;
      var anteil = bodenwert / wohnwert * 100;

      anzeigeGrund.textContent = grund.toLocaleString("de-DE") + " m²";
      anzeigeWohn.textContent = wohn.toLocaleString("de-DE") + " m²";

      var satz;
      if (anteil >= 100) {
        satz = "Der Boden allein ist damit <b>mehr wert</b> als die gesamte Wohnfläche "
             + "zum Kölner Wohnungspreis — ein Quadratmeterpreis für Wohnungen taugt "
             + "hier als Maßstab nicht.";
      } else if (anteil >= 60) {
        satz = "Der Boden macht damit <b>" + Math.round(anteil) + " Prozent</b> dessen aus, "
             + "was dieselbe Fläche als Eigentumswohnung kosten würde. Das Gebäude ist "
             + "der kleinere Teil der Rechnung.";
      } else {
        satz = "Der Boden macht damit <b>" + Math.round(anteil) + " Prozent</b> dessen aus, "
             + "was dieselbe Fläche als Eigentumswohnung kosten würde — hier trägt das "
             + "Gebäude den größeren Teil.";
      }

      ausgabe.innerHTML =
        '<p class="mrb-boden__gross">' + euro(bodenwert) + '</p>' +
        '<p class="mrb-boden__was">reiner Bodenwert bei ' + BRW.toLocaleString("de-DE") +
        ' € je m² Grundstück</p>' +
        '<div class="mrb-boden__zeilen">' +
          '<p><span>Je m² Wohnfläche entfallen auf den Boden</span><b>' +
            euro(jeWohnflaeche) + '</b></p>' +
          '<p><span>' + wohn + ' m² zum Kölner Wohnungspreis (5.684 €/m²)</span><b>' +
            euro(wohnwert) + '</b></p>' +
        '</div>' +
        '<p class="mrb-boden__satz">' + satz + '</p>';
    }

    on(regler, "input", rechnen);
    on(wohnRegler, "input", rechnen);
    rechnen();
  })();

  /* Spannen-Einordner (Hahnwald) ---------------------------------------
     Rechnet die eingegebene Wohnfläche und Preisvorstellung gegen die
     tatsächlich beurkundeten Werte des Grundstücksmarktberichts. Das ist
     bewusst keine Bewertung — es verortet eine Zahl in belegten Zahlen und
     zeigt, was ein Prozentpunkt in diesem Segment bedeutet. */
  (function () {
    var wurzel = $("[data-hw-einordner]");
    if (!wurzel) return;

    var MIN = 4091, MAX = 15758, MITTEL = 7689;   // €/m², Häuser 2025

    var rFlaeche = $("[data-hw-flaeche]", wurzel);
    var rPreis = $("[data-hw-preis]", wurzel);
    var aFlaeche = $("[data-hw-anzeige-flaeche]", wurzel);
    var aPreis = $("[data-hw-anzeige-preis]", wurzel);
    var ausgabe = $("[data-hw-ausgabe]", wurzel);

    function euro(n) { return Math.round(n).toLocaleString("de-DE") + " €"; }
    function mio(n) {
      return (n / 1e6).toLocaleString("de-DE", {minimumFractionDigits: 2,
                                                maximumFractionDigits: 2}) + " Mio €";
    }

    function rechnen() {
      var flaeche = parseInt(rFlaeche.value, 10);
      var preis = parseInt(rPreis.value, 10);
      var jeQm = preis / flaeche;
      var anteil = Math.max(0, Math.min(100, (jeQm - MIN) / (MAX - MIN) * 100));

      aFlaeche.textContent = flaeche.toLocaleString("de-DE") + " m²";
      aPreis.textContent = mio(preis);

      var satz;
      if (jeQm < MIN) {
        satz = "Das liegt <b>unterhalb</b> aller zehn ausgewerteten Verkäufe. Entweder "
             + "bringt die Immobilie Besonderheiten mit, die den Abstand erklären — oder "
             + "die Vorstellung ist zu vorsichtig.";
      } else if (jeQm > MAX) {
        satz = "Das liegt <b>oberhalb</b> aller zehn ausgewerteten Verkäufe. Erreichbar "
             + "ist so etwas, aber es braucht Merkmale, die den Abstand tragen — und "
             + "Käufer, die sie erkennen.";
      } else if (jeQm < MITTEL) {
        satz = "Das liegt in der <b>unteren Hälfte</b> der tatsächlichen Verkäufe, unter "
             + "dem Mittel von 7.689 € je m².";
      } else {
        satz = "Das liegt in der <b>oberen Hälfte</b> der tatsächlichen Verkäufe, über "
             + "dem Mittel von 7.689 € je m².";
      }

      ausgabe.innerHTML =
        '<p class="hw-einordner__gross">' + euro(jeQm) + ' <span>je m² Wohnfläche</span></p>' +
        '<div class="hw-einordner__skala" role="img" aria-label="Einordnung in die Spanne ' +
          'von 4.091 bis 15.758 Euro je Quadratmeter">' +
          '<span class="hw-einordner__marke" style="left:' + anteil.toFixed(1) + '%"></span>' +
        '</div>' +
        '<div class="hw-einordner__enden"><span>4.091 €</span><span>15.758 €</span></div>' +
        '<p class="hw-einordner__satz">' + satz + '</p>' +
        '<p class="hw-einordner__prozent">Ein Prozentpunkt entspricht bei diesem Preis ' +
          '<b>' + euro(preis / 100) + '</b> — fünf Prozent sind ' + euro(preis / 20) + '.</p>';
    }

    on(rFlaeche, "input", rechnen);
    on(rPreis, "input", rechnen);
    rechnen();
  })();

})();

/* ==========================================================================
   Rodenkirchen: Objektart-Vergleicher
   --------------------------------------------------------------------------
   Rechnet eine Wohnfläche gegen den Durchschnitt des gewählten Segments und
   stellt daneben, was dieselbe Fläche in den übrigen fünf Segmenten gekostet
   hätte. Die Zahlen stammen aus dem Grundstücksmarktbericht 2026 der Stadt
   Köln (Berichtsjahr 2025).

   Gerundet wird auf volle hundert Euro. Das ist Absicht: Ein auf den Euro
   genauer Betrag würde eine Genauigkeit vortäuschen, die eine Multiplikation
   mit einem Stadtteildurchschnitt nicht hat.
   ========================================================================== */
(function () {
  "use strict";
  var wurzel = document.getElementById("rdkVergleicher");
  if (!wurzel) return;

  var SEGMENTE = [
    { id: "bestand", kurz: "Wohnung, Bestand",   preis: 4790,
      lang: "Eigentumswohnung, Weiterverkauf, 79 Verkäufe 2025" },
    { id: "neubau",  kurz: "Wohnung, Neubau",    preis: 7699,
      lang: "Neubauwohnung, 18 Verkäufe 2025" },
    { id: "efh",     kurz: "Freistehendes Haus", preis: 6874,
      lang: "freistehendes Ein- oder Zweifamilienhaus, 19 Verkäufe 2025" },
    { id: "dhh",     kurz: "Doppelhaushälfte",   preis: 6283,
      lang: "Doppelhaushälfte oder Reihenendhaus, 15 Verkäufe 2025" },
    { id: "rmh",     kurz: "Reihenmittelhaus",   preis: 5662,
      lang: "Reihenmittelhaus, 7 Verkäufe 2025" },
    { id: "mfh",     kurz: "Mehrfamilienhaus",   preis: 3214,
      lang: "Mehrfamilienhaus, 17 Verkäufe 2025 im gesamten Stadtbezirk" }
  ];

  var knoepfe  = wurzel.querySelectorAll(".rdk-vergleicher__arten button");
  var regler   = document.getElementById("rdkFlaeche");
  var flAus    = document.getElementById("rdkFlaecheAus");
  var ergebnis = document.getElementById("rdkErgebnis");
  var ergText  = document.getElementById("rdkErgebnisText");
  var liste    = document.getElementById("rdkListe");
  if (!regler || !ergebnis || !liste) return;

  var gewaehlt = "bestand";

  function euro(betrag) {
    return Math.round(betrag / 100) * 100;
  }

  function zahl(n) {
    return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  }

  function segment(id) {
    for (var i = 0; i < SEGMENTE.length; i++) {
      if (SEGMENTE[i].id === id) return SEGMENTE[i];
    }
    return SEGMENTE[0];
  }

  function zeichnen() {
    var flaeche = parseInt(regler.value, 10) || 0;
    var eigen = segment(gewaehlt);
    var wert = euro(flaeche * eigen.preis);

    flAus.textContent = flaeche + " m²";
    ergebnis.textContent = zahl(wert) + " €";
    ergText.textContent = flaeche + " m² × " + zahl(eigen.preis) + " €/m² ("
      + eigen.lang + ")";

    liste.innerHTML = "";
    SEGMENTE.forEach(function (seg) {
      if (seg.id === eigen.id) return;
      var w = euro(flaeche * seg.preis);
      var d = wert ? Math.round((w - wert) / wert * 100) : 0;
      var li = document.createElement("li");

      var name = document.createElement("span");
      name.textContent = seg.kurz;

      var rechts = document.createElement("span");
      var b = document.createElement("b");
      b.textContent = zahl(w) + " €";
      rechts.appendChild(b);

      var diff = document.createElement("span");
      diff.className = "rdk-diff";
      diff.textContent = d === 0 ? "gleich" : (d > 0 ? "+" : "−") + Math.abs(d) + " %";
      rechts.appendChild(diff);

      li.appendChild(name);
      li.appendChild(rechts);
      liste.appendChild(li);
    });
  }

  Array.prototype.forEach.call(knoepfe, function (btn) {
    btn.addEventListener("click", function () {
      gewaehlt = btn.getAttribute("data-art");
      Array.prototype.forEach.call(knoepfe, function (b) {
        b.setAttribute("aria-checked", b === btn ? "true" : "false");
      });
      zeichnen();
    });
    // Pfeiltasten innerhalb der Gruppe, wie bei einer Radiogruppe erwartet.
    btn.addEventListener("keydown", function (e) {
      var i = Array.prototype.indexOf.call(knoepfe, btn);
      var ziel = null;
      if (e.key === "ArrowRight" || e.key === "ArrowDown") ziel = knoepfe[(i + 1) % knoepfe.length];
      if (e.key === "ArrowLeft" || e.key === "ArrowUp") ziel = knoepfe[(i - 1 + knoepfe.length) % knoepfe.length];
      if (!ziel) return;
      e.preventDefault();
      ziel.focus();
      ziel.click();
    });
  });

  regler.addEventListener("input", zeichnen);
  zeichnen();
})();

/* ==========================================================================
   Sürth: Baujahr-Einordner
   --------------------------------------------------------------------------
   Rechnet eine Wohnfläche gegen den Durchschnitt der gewählten Baujahresklasse
   und zeigt daneben, wo dieser Wert innerhalb der tatsächlichen Sürther Spanne
   von 1.942 bis 9.233 Euro je Quadratmeter liegt.

   Die Skala ist der eigentliche Punkt: Sie macht sichtbar, dass der
   Baujahresdurchschnitt selbst im teuersten Fall nur im mittleren Drittel der
   Spanne landet — der Rest entscheidet sich über Zustand und Ausstattung.
   ========================================================================== */
(function () {
  "use strict";
  var wurzel = document.getElementById("sueEinordner");
  if (!wurzel) return;

  var KLASSEN = {
    alt:    { preis: 4179, text: "Baujahr 1941 bis 1990" },
    neu:    { preis: 4936, text: "Baujahr ab 1991" },
    neubau: { preis: 6394, text: "Neubau, 5 Verkäufe 2025" }
  };
  var UNTEN = 1942, OBEN = 9233;

  var knoepfe = wurzel.querySelectorAll(".sue-einordner__jahre button");
  var regler  = document.getElementById("sueFlaeche");
  var flAus   = document.getElementById("sueFlaecheAus");
  var erg     = document.getElementById("sueErgebnis");
  var ergText = document.getElementById("sueErgebnisText");
  var uAus    = document.getElementById("sueUnten");
  var oAus    = document.getElementById("sueOben");
  var marke   = document.getElementById("sueMarke");
  if (!regler || !erg) return;

  var gewaehlt = "alt";

  function zahl(n) {
    return String(Math.round(n / 100) * 100).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  }

  function zeichnen() {
    var flaeche = parseInt(regler.value, 10) || 0;
    var k = KLASSEN[gewaehlt] || KLASSEN.alt;

    flAus.textContent = flaeche + " m²";
    erg.textContent = zahl(flaeche * k.preis) + " €";
    ergText.textContent = flaeche + " m² × " + String(k.preis).replace(/\B(?=(\d{3})+(?!\d))/g, ".")
      + " €/m² (" + k.text + ")";
    uAus.textContent = zahl(flaeche * UNTEN) + " €";
    oAus.textContent = zahl(flaeche * OBEN) + " €";

    // Position innerhalb der Spanne — der Preis je Quadratmeter ist von der
    // Fläche unabhängig, die Marke bewegt sich also nur mit der Baujahreswahl.
    var anteil = (k.preis - UNTEN) / (OBEN - UNTEN);
    marke.style.left = "calc(" + (Math.max(0, Math.min(1, anteil)) * 100).toFixed(1) + "% - 2px)";
  }

  Array.prototype.forEach.call(knoepfe, function (btn) {
    btn.addEventListener("click", function () {
      gewaehlt = btn.getAttribute("data-jahr");
      Array.prototype.forEach.call(knoepfe, function (b) {
        b.setAttribute("aria-checked", b === btn ? "true" : "false");
      });
      zeichnen();
    });
    btn.addEventListener("keydown", function (e) {
      var i = Array.prototype.indexOf.call(knoepfe, btn), ziel = null;
      if (e.key === "ArrowRight" || e.key === "ArrowDown") ziel = knoepfe[(i + 1) % knoepfe.length];
      if (e.key === "ArrowLeft" || e.key === "ArrowUp") ziel = knoepfe[(i - 1 + knoepfe.length) % knoepfe.length];
      if (!ziel) return;
      e.preventDefault(); ziel.focus(); ziel.click();
    });
  });

  regler.addEventListener("input", zeichnen);
  zeichnen();
})();

/* ==========================================================================
   Nippes: Budget-Vergleicher Bestand gegen Neubau
   --------------------------------------------------------------------------
   Zeigt, wie viel Wohnfläche ein Käufer für dasselbe Geld im Bestand und im
   Neubau bekommt. Grundlage sind die Durchschnitte des Grundstücksmarkt-
   berichts 2026 für Köln-Nippes: 4.590 Euro je Quadratmeter bei 141
   Weiterverkäufen, 7.532 Euro bei 25 Neubauverkäufen.

   Der Bestandsbalken bleibt immer auf voller Breite, der Neubaubalken zeigt
   den Anteil daran. So bleibt der Vergleich auf einen Blick lesbar, statt sich
   mit dem Budget mitzuskalieren.
   ========================================================================== */
(function () {
  "use strict";
  var wurzel = document.getElementById("nipBudget");
  if (!wurzel) return;

  var BESTAND = 4590, NEUBAU = 7532;
  var regler = document.getElementById("nipBetrag");
  var betrag = document.getElementById("nipBetragAus");
  var aB = document.getElementById("nipBestand");
  var aN = document.getElementById("nipNeubau");
  var bB = document.getElementById("nipBalkenB");
  var bN = document.getElementById("nipBalkenN");
  var diff = document.getElementById("nipDiff");
  if (!regler || !aB) return;

  function punkt(n) {
    return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  }

  function zeichnen() {
    var geld = parseInt(regler.value, 10) || 0;
    var mB = Math.round(geld / BESTAND);
    var mN = Math.round(geld / NEUBAU);

    betrag.textContent = punkt(geld) + " €";
    aB.textContent = mB + " m²";
    aN.textContent = mN + " m²";
    bB.style.width = "100%";
    bN.style.width = (mB ? (mN / mB * 100).toFixed(1) : 0) + "%";
    diff.textContent = (mB - mN) + " m²";
  }

  regler.addEventListener("input", zeichnen);
  zeichnen();
})();

/* Flächen-Rechner Neustadt-Süd -------------------------------------------
   Zeigt für eine eingestellte Wohnfläche die beiden Segmente, die der
   Grundstücksmarktbericht 2026 für den Stadtteil ausweist: den gewöhnlichen
   Weiterverkauf und den Erstverkauf nach Aufteilung. Beide Balken teilen
   sich eine Skala — der obere ist deshalb nie voll, sondern immer im
   Verhältnis zum höheren Wert.

   Die Einordnung vergleicht gegen 65,1 m², die mittlere Wohnungsgröße im
   Stadtteil (Stadt Köln, Bestand zum 31.12.2025). */
(function () {
  var wurzel = document.getElementById("sstRechner");
  if (!wurzel) return;

  var BESTAND = 5766, AUFTEILUNG = 7556, SCHNITT = 65.1;
  var regler = document.getElementById("sstFlaeche");
  var ausFl = document.getElementById("sstFlaecheAus");
  var aB = document.getElementById("sstBestand");
  var aU = document.getElementById("sstUmwandlung");
  var bB = document.getElementById("sstBalkenB");
  var bU = document.getElementById("sstBalkenU");
  var diff = document.getElementById("sstDiff");
  var ein = document.getElementById("sstEinordnung");
  if (!regler || !aB) return;

  function punkt(n) {
    return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  }

  /* Auf volle Tausend runden. Ein Euro-genauer Wert würde eine Genauigkeit
     vortäuschen, die ein Stadtteilmittel nicht hergibt. */
  function aufTausend(n) {
    return Math.round(n / 1000) * 1000;
  }

  function tausend(n) {
    return punkt(aufTausend(n)) + " €";
  }

  function einordnen(qm) {
    var d = qm - SCHNITT;
    if (Math.abs(d) < 2.5) {
      return "Das entspricht ziemlich genau dem Stadtteilschnitt von 65,1 m².";
    }
    var betrag = Math.abs(d).toFixed(0).replace(".", ",");
    if (d < 0) {
      return "Rund " + betrag + " m² unter dem Stadtteilschnitt von 65,1 m² — "
        + "im Kölner Vergleich klein, in Neustadt-Süd der Normalfall.";
    }
    if (d < 25) {
      return "Rund " + betrag + " m² über dem Stadtteilschnitt von 65,1 m². "
        + "Damit sprechen Sie einen kleineren Käuferkreis an als der Durchschnitt.";
    }
    return "Rund " + betrag + " m² über dem Stadtteilschnitt von 65,1 m². "
      + "Wohnungen dieser Größe sind hier selten — das kann ein Vorteil sein, "
      + "verlangt aber eine gezieltere Ansprache.";
  }

  function zeichnen() {
    var qm = parseInt(regler.value, 10) || 0;
    var wB = qm * BESTAND, wU = qm * AUFTEILUNG;

    ausFl.textContent = qm + " m²";
    aB.textContent = tausend(wB);
    aU.textContent = tausend(wU);
    bB.style.width = (wB / wU * 100).toFixed(1) + "%";
    bU.style.width = "100%";
    /* Aus den bereits gerundeten Werten rechnen: sonst zeigt die Zeile
       211.000 an, während 892.000 minus 680.000 daneben steht. */
    diff.textContent = punkt(aufTausend(wU) - aufTausend(wB)) + " €";
    ein.textContent = einordnen(qm);
  }

  regler.addEventListener("input", zeichnen);
  zeichnen();
})();

/* Drei-Segment-Rechner Neustadt-Nord --------------------------------------
   Der Grundstücksmarktbericht 2026 führt für den Stadtteil drei
   Wohnungssegmente mit sehr ungleichen Fallzahlen: 163 Weiterverkäufe, 39
   Neubauten, 6 Aufteilungen. Alle drei Balken teilen sich eine Skala, der
   Neubaubalken ist dabei immer voll.

   Die Einordnung vergleicht gegen 69,4 m², die mittlere Wohnungsgröße im
   Stadtteil (Stadt Köln, Bestand zum 31.12.2025). */
(function () {
  var wurzel = document.getElementById("nndRechner");
  if (!wurzel) return;

  var BESTAND = 5571, AUFTEILUNG = 7387, NEUBAU = 8698, SCHNITT = 69.4;
  var regler = document.getElementById("nndFlaeche");
  var ausFl  = document.getElementById("nndFlaecheAus");
  var aB = document.getElementById("nndBestand");
  var aA = document.getElementById("nndAufteilung");
  var aN = document.getElementById("nndNeubau");
  var bB = document.getElementById("nndBalkenB");
  var bA = document.getElementById("nndBalkenA");
  var bN = document.getElementById("nndBalkenN");
  var diff = document.getElementById("nndDiff");
  var ein  = document.getElementById("nndEinordnung");
  if (!regler || !aB) return;

  function punkt(n) {
    return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  }

  /* Auf volle Tausend runden — ein Stadtteilmittel gibt keine euro-genaue
     Aussage her. Die Differenz weiter unten rechnet aus den gerundeten
     Werten, sonst widerspricht sie den Zahlen darüber. */
  function aufTausend(n) {
    return Math.round(n / 1000) * 1000;
  }

  function tausend(n) {
    return punkt(aufTausend(n)) + " €";
  }

  function einordnen(qm) {
    var d = qm - SCHNITT;
    if (Math.abs(d) < 2.5) {
      return "Das entspricht ziemlich genau dem Stadtteilschnitt von 69,4 m².";
    }
    var betrag = Math.abs(d).toFixed(0);
    if (d < 0) {
      return "Rund " + betrag + " m² unter dem Stadtteilschnitt von 69,4 m². "
        + "In einem Stadtteil, in dem 65 Prozent der Haushalte aus einer Person "
        + "bestehen, ist das der Hauptmarkt.";
    }
    if (d < 30) {
      return "Rund " + betrag + " m² über dem Stadtteilschnitt von 69,4 m². "
        + "Damit sprechen Sie einen kleineren Käuferkreis an als der Durchschnitt.";
    }
    return "Rund " + betrag + " m² über dem Stadtteilschnitt von 69,4 m². "
      + "Wohnungen dieser Größe sind hier selten — das kann ein Vorteil sein, "
      + "verlangt aber eine gezieltere Ansprache.";
  }

  function zeichnen() {
    var qm = parseInt(regler.value, 10) || 0;
    var wB = qm * BESTAND, wA = qm * AUFTEILUNG, wN = qm * NEUBAU;

    ausFl.textContent = qm + " m²";
    aB.textContent = tausend(wB);
    aA.textContent = tausend(wA);
    aN.textContent = tausend(wN);
    bB.style.width = (wB / wN * 100).toFixed(1) + "%";
    bA.style.width = (wA / wN * 100).toFixed(1) + "%";
    bN.style.width = "100%";
    diff.textContent = punkt(aufTausend(wN) - aufTausend(wB)) + " €";
    ein.textContent = einordnen(qm);
  }

  regler.addEventListener("input", zeichnen);
  zeichnen();
})();

/* Aufteilungs-Rechner Weiden ----------------------------------------------
   Zeigt, was der statistische Aufschlag beim Erstverkauf nach Aufteilung für
   ein ganzes Haus bedeutet — und stellt daneben, was derselbe Fall in einem
   Stadtteil mit hohem Aufschlag ergäbe.

   Weiden 2025: 3.436 gegenüber 3.368 Euro je Quadratmeter, also 68 Euro
   Aufschlag aus 12 Verkäufen. Köln-Neustadt-Süd zum Vergleich: 7.556
   gegenüber 5.766 Euro, also 1.790 Euro aus 36 Verkäufen. */
(function () {
  var wurzel = document.getElementById("wdnRechner");
  if (!wurzel) return;

  var AUF_WEIDEN = 68, AUF_SUEDSTADT = 1790;
  var flaeche  = document.getElementById("wdnFlaeche");
  var einheit  = document.getElementById("wdnEinheiten");
  var ausFl    = document.getElementById("wdnFlaecheAus");
  var ausEinh  = document.getElementById("wdnEinheitenAus");
  var aErtrag  = document.getElementById("wdnErtrag");
  var aRef     = document.getElementById("wdnRef");
  var bW       = document.getElementById("wdnBalkenW");
  var bR       = document.getElementById("wdnBalkenR");
  var proW     = document.getElementById("wdnProEinheit");
  var proR     = document.getElementById("wdnRefProEinheit");
  var fazit    = document.getElementById("wdnFazit");
  if (!flaeche || !einheit || !aErtrag) return;

  function punkt(n) {
    return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  }

  /* Auf volle Hundert runden: Der Aufschlag beruht auf zwölf Verkäufen,
     eine feinere Angabe würde eine Genauigkeit vortäuschen. */
  function hundert(n) {
    return punkt(Math.round(n / 100) * 100) + " €";
  }

  function zeichnen() {
    var qm = parseInt(flaeche.value, 10) || 0;
    var n  = parseInt(einheit.value, 10) || 1;
    var eW = qm * AUF_WEIDEN, eR = qm * AUF_SUEDSTADT;

    ausFl.textContent   = punkt(qm) + " m²";
    ausEinh.textContent = n;
    aErtrag.textContent = hundert(eW);
    aRef.textContent    = hundert(eR);
    bW.style.width = (eW / eR * 100).toFixed(1) + "%";
    bR.style.width = "100%";
    proW.textContent = hundert(eW / n) + " je Wohnung";
    proR.textContent = hundert(eR / n) + " je Wohnung";

    /* Das Verhältnis ist konstant (68 zu 1.790, also gut 1 zu 26) und hängt
       nicht von der Fläche ab — der Satz benennt es trotzdem ausdrücklich,
       weil die beiden Beträge sonst nur schwer einzuordnen sind. */
    var faktor = Math.round(AUF_SUEDSTADT / AUF_WEIDEN);
    fazit.textContent = "Dieselbe Aufteilung brächte in der Südstadt rund das "
      + faktor + "-Fache.";
  }

  flaeche.addEventListener("input", zeichnen);
  einheit.addEventListener("input", zeichnen);
  zeichnen();
})();

/* Größen-Einordner Altstadt-Süd -------------------------------------------
   Dieselbe Quadratmeterzahl bedeutet je nach Stadtteil etwas anderes. Der
   Regler setzt einen Zeiger auf eine Skala von 25 bis 150 m², auf der drei
   feste Marken stehen: Altstadt-Süd 60,5 (kleinste Wohnungen Kölns), Köln
   77,3 und Weiden 86,4 (Stand 31.12.2025).

   Der Geldwert nutzt 5.841 Euro je Quadratmeter, den Durchschnitt aus 126
   Weiterverkäufen des Jahres 2025. */
(function () {
  var wurzel = document.getElementById("astRechner");
  if (!wurzel) return;

  var AST = 60.5, KOELN = 77.3, WEIDEN = 86.4, PREIS = 5841;
  var MIN = 25, MAX = 150;
  var regler = document.getElementById("astFlaeche");
  var ausFl  = document.getElementById("astFlaecheAus");
  var zeiger = document.getElementById("astZeiger");
  var wert   = document.getElementById("astWert");
  var ein    = document.getElementById("astEinordnung");
  var vA = document.getElementById("astVglAst");
  var vK = document.getElementById("astVglKoeln");
  var vW = document.getElementById("astVglWeiden");
  if (!regler || !wert) return;

  function punkt(n) {
    return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  }

  /* Auf volle Tausend runden — ein Stadtteilmittel gibt nicht mehr her. */
  function tausend(n) {
    return punkt(Math.round(n / 1000) * 1000) + " €";
  }

  /* Vorzeichen ausschreiben, damit "3 m² mehr" und "3 m² weniger" nicht als
     bloßes Minuszeichen nebeneinanderstehen. */
  function abstand(qm, bezug) {
    var d = qm - bezug;
    if (Math.abs(d) < 0.5) return "genau gleich";
    return Math.abs(d).toFixed(0) + " m² " + (d > 0 ? "mehr" : "weniger");
  }

  function einordnen(qm) {
    var d = qm - AST;
    if (Math.abs(d) < 2.5) {
      return "Das entspricht ziemlich genau dem Schnitt der Altstadt-Süd.";
    }
    if (d < 0) {
      return "Unter dem Stadtteilschnitt von 60,5 m² — und der ist bereits der "
        + "niedrigste in Köln. Für diesen Markt ist das keine Schwäche, "
        + "sondern der Normalfall.";
    }
    if (d < 30) {
      return "Über dem Stadtteilschnitt von 60,5 m². In einem Viertel, in dem "
        + "70 Prozent der Haushalte aus einer Person bestehen, sprechen Sie "
        + "damit einen kleineren, aber zahlungsfähigen Kreis an.";
    }
    return "Deutlich über dem Stadtteilschnitt von 60,5 m². Wohnungen dieser "
      + "Größe sind in der Altstadt-Süd selten — ein Vorteil, der aber gezielt "
      + "beworben werden muss.";
  }

  function zeichnen() {
    var qm = parseInt(regler.value, 10) || 0;
    ausFl.textContent = qm + " m²";
    zeiger.style.left = ((qm - MIN) / (MAX - MIN) * 100).toFixed(1) + "%";
    wert.textContent = tausend(qm * PREIS);
    ein.textContent = einordnen(qm);
    vA.textContent = abstand(qm, AST);
    vK.textContent = abstand(qm, KOELN);
    vW.textContent = abstand(qm, WEIDEN);
  }

  regler.addEventListener("input", zeichnen);
  zeichnen();
})();

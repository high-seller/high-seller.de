import type { Context } from "@netlify/functions";
import { getStore } from "@netlify/blobs";
import { createHash, timingSafeEqual } from "node:crypto";

/**
 * Liefert die Kontaktereignisse für das Lead-Cockpit.
 *
 *   GET /.netlify/functions/lead-feed?key=<Zugangsschlüssel>
 *
 * Zugriffsschutz nach dem Muster von gsc-status, aber eine Stufe strenger:
 * In der Umgebungsvariable LEAD_COCKPIT_TOKEN_HASH liegt nur der SHA-256-Hash
 * des Schlüssels. Der Klartext existiert ausschließlich beim Inhaber; selbst
 * wer die Netlify-Konfiguration einsehen kann, kann sich daraus keinen
 * Zugang bauen. Verglichen wird zeitkonstant.
 *
 * Nebenaufgabe Speicherbegrenzung: Bei jedem Abruf werden bis zu 100
 * Ereignisse gelöscht, die älter als sechs Monate sind. So bleibt der
 * Bestand von selbst klein, ohne dass ein eigener Aufräumjob nötig wäre.
 */

const AUFBEWAHRUNG_MONATE = 6;
const LIMIT = 500;

function monatsListe(anzahl: number): string[] {
  const aus: string[] = [];
  const d = new Date();
  // Auf den Monatsersten stellen, BEVOR zurückgerechnet wird: Am 31. eines
  // Monats liefe setUTCMonth sonst in den Folgemonat über und der Vormonat
  // fiele aus der Liste — genau an Monatsenden fehlten dann Ereignisse.
  d.setUTCDate(1);
  for (let i = 0; i < anzahl; i++) {
    aus.push(d.toISOString().slice(0, 7));
    d.setUTCMonth(d.getUTCMonth() - 1);
  }
  return aus;
}

function schluesselParsen(key: string) {
  // e/<monat>/<iso>~<zufall>~<art>~<seite>~<sitzung>~<zusatz>
  const rest = key.split("/").slice(2).join("/");
  const t = rest.split("~");
  if (t.length < 6) return null;
  try {
    return {
      zeit: t[0],
      art: t[2],
      seite: decodeURIComponent(t[3]),
      sitzung: t[4],
      zusatz: decodeURIComponent(t[5]),
    };
  } catch {
    return null;
  }
}

export default async (req: Request, _context: Context) => {
  const url = new URL(req.url);
  const given = url.searchParams.get("key") || "";
  const erwartet = process.env.LEAD_COCKPIT_TOKEN_HASH || "";

  const gegebenHash = createHash("sha256").update(given).digest("hex");
  const a = Buffer.from(gegebenHash, "utf-8");
  const b = Buffer.from(erwartet, "utf-8");
  const ok = erwartet.length > 0 && a.length === b.length && timingSafeEqual(a, b);
  if (!ok) {
    return new Response(JSON.stringify({ fehler: "kein Zugang" }), {
      status: 401,
      headers: { "Content-Type": "application/json; charset=utf-8" },
    });
  }

  const store = getStore("leads");

  // Aktueller Monat plus Vormonat decken alles ab, was das Cockpit zeigt.
  const eintraege: NonNullable<ReturnType<typeof schluesselParsen>>[] = [];
  for (const monat of monatsListe(2)) {
    const { blobs } = await store.list({ prefix: `e/${monat}/` });
    for (const b of blobs) {
      const e = schluesselParsen(b.key);
      if (e) eintraege.push(e);
    }
  }
  eintraege.sort((x, y) => (x.zeit < y.zeit ? 1 : -1));

  // Aufräumen: der Monat jenseits der Aufbewahrung, häppchenweise.
  let geloescht = 0;
  try {
    const alt = monatsListe(AUFBEWAHRUNG_MONATE + 1)[AUFBEWAHRUNG_MONATE];
    const { blobs } = await store.list({ prefix: `e/${alt}/` });
    for (const b of blobs.slice(0, 100)) {
      await store.delete(b.key);
      geloescht++;
    }
  } catch {
    // Aufräumen darf nie den Abruf verhindern.
  }

  return new Response(
    JSON.stringify({
      stand: new Date().toISOString(),
      anzahl: eintraege.length,
      geloescht,
      eintraege: eintraege.slice(0, LIMIT),
    }),
    {
      status: 200,
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "no-store",
        "X-Robots-Tag": "noindex",
      },
    },
  );
};

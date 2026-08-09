import type { Context } from "@netlify/functions";
import { getStore } from "@netlify/blobs";

/**
 * Nimmt Kontaktereignisse von der Website entgegen und legt sie im
 * Blobs-Store "leads" ab. Gegenstück: lead-feed (Abruf) und die Seite
 * lead-cockpit.html (Anzeige, nur mit Zugangsschlüssel).
 *
 *   POST /.netlify/functions/lead-track
 *   Body: {"art":"anruf","seite":"/immobilienmakler-koeln-deutz.html",
 *          "zusatz":"","sitzung":"ab12cd34"}
 *
 * Datensparsamkeit ist hier die rechtliche Absicherung:
 *  - Es wird KEINE IP-Adresse und KEIN User-Agent gespeichert.
 *  - Ohne Statistik-Einwilligung sendet der Browser keine Sitzungskennung;
 *    das Ereignis ist dann ein anonymer Einzelpunkt ohne Endgeräte-Zugriff
 *    (§ 25 TDDDG greift nicht, DSGVO: berechtigtes Interesse).
 *  - Mit Einwilligung kommt eine zufällige Sitzungskennung aus dem
 *    sessionStorage mit; sie endet mit dem Schließen des Browsers und ist
 *    keiner Person zuordenbar.
 *
 * Formular-Ereignisse laufen NICHT über diesen Endpunkt, sondern werden
 * serverseitig in submission-created.mts erfasst — der Endpunkt hier ist
 * öffentlich, und niemand soll Formulareingänge vortäuschen können.
 *
 * Speicherformat: Alle Angaben stecken im Blob-Schlüssel, der Wert bleibt
 * leer. Dadurch genügt beim Abruf ein einziger list()-Aufruf ohne Einzel-
 * Downloads — wichtig, weil das Cockpit alle zehn Sekunden nachfragt.
 *
 *   e/<JJJJ-MM>/<ISO-Zeit>~<zufall>~<art>~<seite>~<sitzung>~<zusatz>
 *
 * Felder sind URI-codiert, zusätzlich !*'()~ — encodeURIComponent lässt
 * diese Zeichen nämlich stehen, und "~" ist unser Trennzeichen.
 */

const ARTEN = new Set(["anruf", "whatsapp", "email", "test"]);

function enc(s: string): string {
  return encodeURIComponent(s).replace(/[!*'()~]/g,
    (c) => "%" + c.charCodeAt(0).toString(16).toUpperCase());
}

export default async (req: Request, _context: Context) => {
  if (req.method !== "POST") {
    return new Response("Method Not Allowed", { status: 405 });
  }

  let roh = "";
  try {
    roh = await req.text();
  } catch {
    return new Response("Bad Request", { status: 400 });
  }
  if (roh.length > 1200) return new Response("Payload Too Large", { status: 413 });

  let daten: Record<string, unknown>;
  try {
    daten = JSON.parse(roh);
  } catch {
    return new Response("Bad Request", { status: 400 });
  }

  const art = String(daten.art || "");
  if (!ARTEN.has(art)) return new Response("Bad Request", { status: 400 });

  let seite = String(daten.seite || "/");
  if (!seite.startsWith("/")) seite = "/";
  seite = seite.slice(0, 100);

  const sitzung = String(daten.sitzung || "").slice(0, 16);
  if (!/^[a-z0-9]*$/.test(sitzung)) return new Response("Bad Request", { status: 400 });

  const zusatz = String(daten.zusatz || "").slice(0, 60);

  // Zeit serverseitig: Client-Uhren sind unzuverlässig, und die Reihenfolge
  // im Cockpit hängt an diesem Wert.
  const zeit = new Date().toISOString();
  const monat = zeit.slice(0, 7);
  const zufall = Math.random().toString(36).slice(2, 6);

  const schluessel =
    `e/${monat}/${zeit}~${zufall}~${art}~${enc(seite)}~${sitzung}~${enc(zusatz)}`;

  try {
    const store = getStore("leads");
    await store.set(schluessel, "1");
  } catch {
    // Blobs nicht erreichbar: lieber das Ereignis verlieren als dem
    // Besucher einen Fehler zeigen — der Aufruf kommt per sendBeacon
    // und niemand wartet auf die Antwort.
  }

  return new Response(null, { status: 204 });
};

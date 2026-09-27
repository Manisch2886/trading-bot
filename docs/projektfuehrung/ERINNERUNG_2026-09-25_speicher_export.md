# Erinnerung an: Manuel — Export des bisherigen Projektspeichers

**Projekt:** Trading Bots
**Erstellt:** 25.09.2026 (geplante Erinnerung, Cloud-Lauf ohne Mac-Zugriff)
**Frist:** **29.09.2026 (Dienstag)** — heute sind es noch **4 Tage**

## In einfacher Sprache

Der alte Projektspeicher lässt sich nur noch bis Dienstag herunterladen.
Danach ist die Sicherungsdatei weg. Der Export ist ein Klick in der App —
niemand ausser dir kann ihn auslösen. Die inhaltliche Gegenprüfung, ob im
neuen Speicher etwas Wichtiges fehlt, ist bereits gemacht; das Ergebnis
steht in `PRUEFUNG_2026-09-25_drei_festlegungen_im_speicher.md`.

---

## Schritt 1 — Export auslösen  [ortsunabhängig]

**Was:** Im Projekt „Trading Bots" auf den Hinweis
*„den bisherigen Speicher dieses Projekts exportieren"* tippen.
**Wo:** Claude-App oder Web, Projektansicht „Trading Bots" (der Hinweis steht
im Projektkopf, nicht in einem einzelnen Chat).
**Woran du merkst, dass es geklappt hat:** Es entsteht eine Sicherungsdatei
des alten Wissensstands und der Download startet.

## Schritt 2 — Datei ablegen  [Mac-pflichtig]

**Was:** Die heruntergeladene Datei aus dem Download-Ordner nach
`~/trading-bot/docs/archiv/` verschieben (Ordner ggf. anlegen).
**Wo:** MacBook. Einzeiler fürs Terminal oder die Mac-Sitzung:

    mkdir -p ~/trading-bot/docs/archiv && mv ~/Downloads/<DATEINAME> ~/trading-bot/docs/archiv/

**Woran du merkst, dass es geklappt hat:** `ls ~/trading-bot/docs/archiv/`
nennt die Datei.

⚠️ **Nicht ungeprüft committen.** Der Ordner liegt im Repo, ein Commit
schiebt die Datei nach GitHub. Entweder erst hineinsehen, ob personen- oder
zugangsbezogene Inhalte darin stehen, oder den Pfad in `.gitignore`
aufnehmen. Das entscheidet der nächste Mac-Auftrag mit, nicht dieser Lauf.

## Schritt 3 — Gegenprüfung  [erledigt, nichts zu tun]

Die drei genannten Festlegungen wurden gegen den **neuen** Projektspeicher
geprüft. **Alle drei sind vorhanden.** Eine Zeile ist inhaltlich überholt,
drei Ergänzungen fehlen — Einzelheiten und Wortlaut in
`PRUEFUNG_2026-09-25_drei_festlegungen_im_speicher.md`.

---

## Was dieser Lauf NICHT konnte

- **Den Export selbst auslösen.** Er ist eine Schaltfläche in der App; ein
  geplanter Cloud-Lauf hat keinen Zugriff auf die Oberfläche.
- **Prüfen, ob du ihn längst gemacht hast.** Es gibt dafür kein Signal, das
  von hier aus lesbar wäre. Ist die Datei schon in `docs/archiv/`, sind
  Schritt 1 und 2 hinfällig.
- **Auf den Mac zugreifen.** Dieser geplante Auftrag läuft in der Cloud;
  das Gerät ist für ihn nicht verbunden.

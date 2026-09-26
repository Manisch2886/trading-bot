# AUFGABEN für den Betreiber — nach der Rückkehr am 26.09.2026

**Angelegt:** 25.09.2026, 22:55, vom steuernden Chat. **Stand:** Es läuft keine Mac-Sitzung; TB-105, TB-106 und TB-107 sind abgegeben und geschlossen, HEAD `f61bd97`. Alles unten wartet auf dich, sonst auf nichts.

⚠️ Die Befehle stehen je in **einer Zeile** (Termius). Keiner gibt einen Schlüssel oder ein Log aus.

---

## 1. Zuerst — Fable (in dieser Reihenfolge)

| | Was | Datei (Projektablage) | Hinweis |
|---|---|---|---|
| 1a | **Anfrage 25d** an Fable geben, falls noch nicht geschehen | `projektfuehrung/FABLE_ANFRAGE_2026-09-25d_tb106_abgegeben_vier_fragen.md` | Antwort bitte als `…_2026-09-25d_<stichwort>.md` ablegen lassen |
| 1b | **Anfrage 25e** an Fable geben | `projektfuehrung/FABLE_ANFRAGE_2026-09-25e_tb107_abgegeben_drei_fragen.md` | Antwort als `…_2026-09-25e_<stichwort>.md` |
| 1c | **Anfrage 25f, die Gesamtanalyse**, an Fable geben | `projektfuehrung/FABLE_ANFRAGE_2026-09-25f_gesamtanalyse_und_ideen.md` | ⚠️ Vorher im Fable-Chat die **Websuche einschalten**. Die Freigabe steht im Text, technisch schaltet sie nur die App frei. **Danach wieder ausschalten.** Antwort als `…_2026-09-25f_gesamtanalyse_und_ideen.md` |
| 1d | Mir danach **„Fable ist fertig“** schreiben | — | Ich lese die Antworten selbst aus der Projektablage |

*Warum diese Reihenfolge:* 25d und 25e entscheiden über zwei kleine Stellen im Code (eine davon, Commit `f5fdb53`, ist schon gebaut und lässt sich zurücknehmen). 25f ist unabhängig davon und darf länger dauern.

## 2. Eine Nachlieferung von gestern (einmal im Terminal)

Die Mac-Sitzungen durften `crontab -l` nicht ausführen. Beide Zeilen geben nur eine Zahl aus:

```
crontab -l | grep -c equity_simulation
```

```
crontab -l | grep -c multi_symbol_optimise
```

Die beiden Zahlen einfach hier in den Chat schreiben.

## 3. Termin: Speicher-Export bis **29.09.2026**

Nur du kannst das: `projektfuehrung/ERINNERUNG_2026-09-25_speicher_export.md`.

## 4. Entscheidungen, die ich dir als Auswahlkarten vorlege, sobald Fable geantwortet hat

| | Entscheidung | vorbereitet in |
|---|---|---|
| 4a | **Registerauftrag (TB-108):** gut sechzig Einträge aus Fable 24b bis 25e ins Register, Gliederung 41/42 | `projektfuehrung/STOFFSAMMLUNG_REGISTER_41_42.md` |
| 4b | **Auftrag zu Register 19:** Sauberkeitsprüfung über den ganzen Laufbereich (Tag-Vorbedingung; ändert die Startprüfung jedes Laufs, `shared/paths.py`) | Fable 25b 3 (2), 25c 2 (d) |
| 4c | Je nach 25d: `herkunft.py` ein zweites Mal öffnen (Prüfansicht, `TB30A_BASE_DIR`)? `Abbruch` in `auswertung.py` auf rc 2? | Anfrage 25d |
| 4d | Je nach 25e: zwei weitere Zwischenablagen, zehn `trades.empty`-Stellen, altes Werkzeug `pfadvergleich.py` | Anfrage 25e |
| 4e | Die drei nächtlichen Cron-Wächter mit Ersatzmodul (Live-Code): weiter nur Notiz, oder jetzt anfassen? | Betreiber 25.09., 18:09: „Jetzt nicht“ |
| 4f | Die vier Nachträge in den Projektspeicher: ja/nein | `projektfuehrung/PRUEFUNG_2026-09-25_drei_festlegungen_im_speicher.md` |

## 5. Beim nächsten Mac-Auftrag

- Nach dem Auslöser erscheint ein **Terminalfenster** mit dem Satz. **Einmal Enter drücken und das Fenster offen lassen.** Gestern Abend wurde es zweimal vor dem Abschicken geschlossen.
- Oder in der Claude-App: **„Neu“** ⇒ Sitzung auf dem Laptop im Ordner `trading-bot` ⇒ Einfügesatz einfügen und senden.

## 6. Freiwillig: alte Zwischenordner aufräumen

In deinem temporären Ordner liegen etwa **4765** Ordner `tb40_lauf_*` aus Läufen **vor** TB-107. Neue kommen nicht mehr dazu. Sie stören nicht, belegen aber Platz. Zählen:

```
find "$TMPDIR" -maxdepth 1 -type d -name 'tb40_*' | wc -l
```

Löschen, nur wenn du willst und **keine** Mac-Sitzung läuft (löscht nur Ordner, die älter als einen Tag sind):

```
find "$TMPDIR" -maxdepth 1 -type d -name 'tb40_*' -mtime +1 -exec rm -rf {} +
```

---

## In einfacher Sprache

Während du weg warst, habe ich:
- den Auftrag TB-107 geprüft und die Sitzung geschlossen;
- die Anfragen an Fable geschrieben: die zum letzten Auftrag und die grosse Gesamtanalyse;
- die Übergabe fortgeschrieben;
- alles gesammelt, was als Nächstes ins Regelwerk muss.

Für dich bleibt:
1. Die drei Anfragen an Fable geben, bei der Gesamtanalyse vorher die Websuche einschalten und danach wieder aus.
2. Zwei Zahlen aus der Crontab nachliefern.
3. Bis Dienstag, 29.09., den Speicher-Export machen.

Alles Weitere lege ich dir als Auswahlkarten vor, sobald Fable geantwortet hat.

---

## Nachtrag 23:30 — was sich seit 22:55 geändert hat

- **Punkt 1a und 1b sind erledigt:** Fable hat 25d und 25e beantwortet. **Offen bleibt 1c**, die Gesamtanalyse 25f (vorher im Fable-Chat die Websuche einschalten, danach wieder aus).
- **Über Nacht laufen zwei Sitzungen:**
  - **A**, Hauptordner: TB-109, danach TB-110.
  - **B**, eigener Ordner `~/trading-bot-tb111`: TB-111.
- **Was du dafür tun musst, nur einmal:**
  1. Im Terminalfenster des Wächters **Enter** drücken. Damit startet A.
  2. **Warten, bis A den Ordner `~/trading-bot-tb111` angelegt hat.** Das ist etwa zwei bis fünf Minuten nach dem Start der Fall; ich melde es im Chat.
  3. In der Claude-App **„Neu“** ⇒ Sitzung auf dem Laptop im Ordner **`trading-bot-tb111`** öffnen ⇒ den Einfügesatz für **TB-111** senden.
- **Morgen:** Sitzung B schliesst sich nicht von selbst, also das Fenster schliessen, wenn ihr Ergebnis da ist. Danach folgt die Zusammenführung (TB-112) per Auswahlkarte.

---

## Nachtrag 26.09.2026, 20:50 — was für dich offen ist

1. **Morgen, 27.09.: Fable-Tagesanfrage 27a schicken.** Die Datei liegt in der Projektablage: `projektfuehrung/FABLE_ANFRAGE_2026-09-27a_tagesanfrage_tb114_tb115.md`, dazu die beiden Ergebnisse TB-114 und TB-115. Danach „Fable ist fertig“ schreiben.
2. **Termin: Speicher-Export bis 29.09.2026** (unverändert, Abschnitt 3).
3. **Zwei Zählungen im Terminal**, je eine Zeile, zeigen nur eine Zahl:
   - `crontab -l | grep -c equity_simulation`
   - `crontab -l | grep -c multi_symbol_optimise`
4. **Nichts sonst.** Es läuft keine Sitzung. Die db-Sicherung prüfe ich morgen nach 05:20 selbst.

Erledigt seit dem letzten Nachtrag: TB-109 bis TB-115; Fable 25f und 26a; db-Sicherung eingerichtet; Wächter mit Aufwand „hoch“.

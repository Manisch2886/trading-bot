# Messung 01.10.2026 — warum die Umzugsampel fast nach jeder Eingabe umziehen will

*Steuernder Chat, 01.10.2026, ca. 21:30. Anlass: Rückfrage des Betreibers 21:25 („wie kann es sein, dass man mittlerweile nach fast jeder Eingabe umziehen soll?“). Gemessen aus dem eigenen Sitzungsprotokoll mit `docs/werkzeuge/ampel.py` (md5 `0c42ee78…`). Die Gewichte sind die aus dem Nachtrag 20:15: Eingabe ×1, Cache-Lesen ×0,1, Cache-Schreiben ×2, Ausgabe ×5.*

## Befund 1 — Einheitenfehler in S2 (Fehler Nr. 13)

- UMZUG 3, Auslöser 6 (29.09.) zählt **den Verlauf**: „was im Chat gelesen und geschrieben wurde (Bytes der Werkzeugausgaben ÷ ~3,3)“. Die Schwellen 200 000/300 000 waren als „das Zwei- bis Dreifache der Einlesekosten“ gemeint.
- S2 (01.10., 20:10) misst die **Gesamtgrösse** `input + cache_read + cache_creation`. Darin steckt die Grundlast aus festen Anweisungen und Werkzeugen. Die Schwellen sind unverändert übernommen.
- Die Grundlast ist gemessen: Dieser Chat begann bei **120 452**, der vorige bei 122 866. Ein frischer Chat steht also schon bei 60 % der grünen Schwelle, bevor er eine Zeile liest. Nach der Kernlektüre stand dieser Chat bei 143 859, nach dem ersten Arbeitsschritt bei 166 517, nach einer Fable-Übergabe bei 🟡.
- ⇒ Die Ampel springt nach einer Auftragsrunde auf Gelb. Das ist der Mechanismus hinter „fast nach jeder Eingabe“. Der Fehler liegt in der Regel. Der Vorgängerchat hat sie geschrieben, ich habe sie ungeprüft angewandt.

## Befund 2 — Ein Umzug ist nicht umsonst

- Die Grundlast kommt fast ganz aus einem schon warmen Cache. Im ersten Schritt dieses Chats wurden nur 19 567 Token neu geschrieben, rund 100 900 waren schon gecacht (einmal gemessen).
- **Teuer ist das Einlesen:** Dieser Chat brauchte 19 Schritte und rund **477 000 effektive Token**, um von 120 452 auf 166 517 zu kommen. Darin stecken Zugriffsprüfung, Kernlektüre und das Schreiben der ersten Fable-Bitte.
- **Was ein Umzug spart:** Je Schritt rund 0,1 × (alte Grösse − neue Grösse). Von 248 600 auf rund 166 000 sind das etwa 8 000 je Schritt.
- ⇒ **Gewinnschwelle:** rund 50–60 Schritte. Dieser Chat hat für die ganze bisherige Arbeit 44 Schritte gebraucht. Ein Umzug bei 248 600 hätte also mehr gekostet als gespart.

## Befund 3 — Was wirklich teuer ist

| Posten | gemessen | Wirkung |
|---|---|---|
| Pause über eine Stunde (Cache verfällt) | erster Schritt danach schreibt den ganzen Kontext neu: 2 × Grösse, bei 248 600 also ~500 000 | entspricht ungefähr einem Neustart; erst bei grossen Chats lohnt der Umzug vor der Pause klar (504 000 ⇒ ~1 Mio.) |
| grosse Werkzeugausgaben im Chat | `project_read` der Fable-Übergabe (30 KB): +25 253 Grösse, bleibt in jedem Folgeschritt; Fehler Nr. 12: +87 700 | jede solche Ausgabe kostet in allen späteren Schritten ×0,1 mit |
| Helfer | Start je rund 83 000–120 000 (Grundlast), 37–52 Schritte (Nachtrag 20:15) | ein Helfer kostet so viel wie ein halber Chat |
| lange eigene Ausgaben | Ausgabe ×5; hier 17 % der Kosten | Kopierblöcke und Dokumente nur einmal schreiben (S6) |

## Vorschlag (Betreiberentscheid, Karte)

- **Ampel misst den Verlauf** = Grösse − Grundlast (Grundlast = erster Schritt des Chats; `ampel.py` gibt beides aus).
- **Schwellen unverändert im Sinn von 29.09.:** 🟢 Verlauf unter 200 000 · 🟡 200 000–300 000 · 🔴 darüber. In Gesamtgrösse sind das rund 320 000 / 420 000.
- **Pausenregel aus S1 enger:** Umzug vor einer Pause über einer Stunde nur ab 🟡. Darunter kostet das Neu-Cachen ungefähr so viel wie das Einlesen in einem neuen Chat.
- **S1 bleibt dem Sinn nach** (ein Chat je Auftragsrunde). Umgezogen wird am sauberen Stand nach der Ampel, nicht nach jeder Runde.
- **Die Hebel, die wirklich sparen:** keine grossen Dateien inline (auch kein `project_read` über ~10 KB, wenn eine Datei nur geprüft werden soll), Helfer nur für Urteil (S3/S5), keine Pausen über eine Stunde mitten in einem grossen Chat.

**Stand dieses Chats nach dem Vorschlag:** Grösse 248 600, Grundlast 120 452, Verlauf 128 148 ⇒ 🟢.

## In einfacher Sprache

Die Ampel hat seit heute Abend falsch gezählt. Sie rechnet den festen Grundtext mit, den jeder Chat von Anfang an mitschleppt (gut 120 000), aber die Grenzwerte stammen aus der Zeit, als nur der eigentliche Gesprächsverlauf gezählt wurde. Deshalb stand jeder neue Chat schon nach einer Runde auf Gelb. Ausserdem ist ein Umzug nicht gratis: Das Einlesen kostet ungefähr so viel wie 50 Arbeitsschritte im alten Chat an Mehrkosten. Richtig gezählt ist dieser Chat grün und kann TB-127 selbst schreiben.

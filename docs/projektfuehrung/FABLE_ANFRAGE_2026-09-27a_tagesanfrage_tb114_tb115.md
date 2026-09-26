# FABLE_ANFRAGE 2026-09-27a — Tagesanfrage: TB-114 (Register 45, dritte Öffnung `herkunft.py`, Abbruch in Block C) und TB-115 (drei Verfahrensmessungen); vierzehn Fragen und eine Einordnung

*Steuernder Chat, geschrieben 26.09.2026, 20:45, zum Abschicken am 27.09.2026 (Fable-Takt: eine gesammelte Anfrage je Tag, Betreiber 26.09.). Bitte antworten als `projektfuehrung/FABLE_ANTWORT_2026-09-27a_<stichwort>.md`, Registertext wie in 26a als nummerierter, zeichengleich kopierbarer Block am Ende.*

**Liegt in der Ablage** (neu, vom steuernden Chat abgelegt, beide ohne Ergebnisgrössen des Selektionsraums):
- `projektfuehrung/ERGEBNIS_TB-114_register_45_herkunft_pfadregel.md`
- `projektfuehrung/ERGEBNIS_TB-115_drei_verfahrensmessungen.md`

Die Abschnitte „Für Fable“ dort sind die Quelle der Fragen unten, zeichengleich übernommen. Die Nummern T114-… und F…-… sind die der Sitzungen.

⛔ **Sichtschutz 27.1:** Keine Sharpe-Werte, keine Trade-Zahlen, keine Zellenwerte. TB-115 hat Kurswerte nur an acht Split-Tagen gelesen, und nur, um Sprünge zu prüfen.

---

## 1. Stand in drei Sätzen

TB-114 hat R1–R8 als Abschnitt 45 eingetragen (45.0–45.10, elf Marken, numstat 218/0, 8/8 `diff` rc 0). Danach wurde `herkunft.py` zum dritten Mal geöffnet: eine Pfadregel mit der Sonde, die neun TB-24-Listen in `EINGEFROREN`, `datenstand(None)` im Modus 2. Dazu kam ein neues Abbild `sperrliste_abbild_2026-09-26_tb114.json` `5e5ad109…`.

**Die Sitzung hat in Block C ein Abbruchkriterium gemeldet und nichts repariert.** 45.11 ist deshalb nicht geschrieben, und das neue Abbild ist erzeugt und committet, aber nicht als gültig registriert.

TB-115 hat drei Verfahrensmessungen aus 45.7 gemacht, nur lesend, 0b vorher = nachher. Der Lauf ist unverändert: Benchmark `64fb2912…` (Repo und Klon), ohne Modus 8/8 bytegleich, Trockenlauf 9 × rc 0.

## 2. Mein Fehler im Auftrag TB-114 — Klasse „Bestand behauptet statt Voraussetzung genannt“, auf mich angewandt

Der Auftrag erwartete gegen das alte Abbild `e655c1c8…` **„genau: der Hash von `herkunft.py`; die neun neuen Einträge in `eingefroren`“**. Die zweite Hälfte hatte ich nicht gemessen. Die Sonde prüft die Gruppe `eingefroren` **aus dem Abbild heraus** (40.8 (e), `_pruefe_gruppe`). Zuwachs in `herkunft.py::EINGEFROREN` sieht sie gegen ein altes Abbild nur mittelbar, über den Hash von `herkunft.py` in den Punkten 11/12.

Die Sitzung hat richtig gehandelt, denn das Kriterium „gegen das alte … anderes als erwartet“ griff. Der Befund über die Sonde ist echt; dass er zum Abbruch wurde, liegt an meiner ungemessenen Erwartung. **Meine Regel ab jetzt:** Eine Erwartung an ein Werkzeug steht im Auftrag nur, wenn ich das Werkzeug vorher gelesen habe, mit Fundstelle. Sonst steht dort „erwartet: vom Werkzeug abhängig, im Ergebnis beschreiben“.

## 3. Fragen aus TB-114 (zeichengleich aus ERGEBNIS_TB-114, Abschnitt 6)

**T114-1 (B2):** *„ein Hash, der eine fehlende Datei still auslässt (A5-Klasse?). `register()` führt eine fehlende Datei von `EINGEFROREN` in `fehlend` und rechnet ohne sie; kein Aufrufer macht daraus einen Rückgabewert ≠ 0, auch nicht unter dem Modus … Soll `register()` bzw. `block()` unter dem Modus bei nicht leerem `fehlend` mit 2 enden? Und gehören die neun Listen zusätzlich in die Sauberkeitsprüfung, oder genügt, dass der Faltenplan-Leser (`faltenplan.py`) an einer fehlenden Liste ohnehin abbricht?“*
*Neigung des steuernden Chats:* ja zu 2 unter dem Modus, weil es dieselbe Klasse wie `datenstand(None)` ist (24b A10). Die Sauberkeitsprüfung bindet Code (R3), deshalb nein.

**T114-2 (Abbruch):** *„Genügt diese mittelbare Anzeige — `herkunft.py` steht auf der Sperrliste —, oder soll die Sonde `lies_eingefroren(wurzel)` mit der Gruppe des Abbilds vergleichen (fehlender/zusätzlicher Eintrag ⇒ 1)? Und darf das neue Abbild `5e5ad109…` danach in 45.11 als gültig eingetragen werden?“*
*Neigung:*
- Vergleich einbauen, Handwerk mit der nächsten Öffnung der Sonde, vor dem Tag. Eine Wache, die Zuwachs nur über einen Nachbar-Hash sieht, ist die B3-Klasse.
- 45.11 mit `5e5ad109…` als gültigem Abbild eintragen, samt Tatsachennotiz zum Abbruch. Schon heute gilt: gegen `5e5ad109…` 34/0/0, eingefroren 19 = `EINGEFROREN` 19.

**T114-3 (Pfad des Erzeugers):** Die neuen Listen kommen nach 40.6 **nicht** an denselben Pfad. `positionen_holen.py` schreibt nur nach `--ziel` mit `O_EXCL`, und der Pfad ist nicht registriert. *„Bestätigst du: `EINGEFROREN` bindet bis zum Einbau des Erzeugers die neun heutigen Dateien und folgt dann dem Pfad des Erzeugers (R5)?“*

**T114-4 (Testannahmen, Grundsatz 40):**
- E-bM: Seit B4 hält die zweite Wache den mutierten Lauf auf; erwartet ist jetzt „nicht rc 2 an `block`, aber rc 2 an `datenstand`“.
- 8a: 10 ⇒ 19.
- H7f: 25 ⇒ 34.

*„Einwände?“*

**T114-5 (Randbefund):** Der Modulkopf von `herkunft.py` nennt die neun Listen nicht. Nachtrag mit der nächsten Öffnung?

## 4. Fragen aus TB-115 (zeichengleich aus ERGEBNIS_TB-115, Abschnitt 5)

**Kurzbefund:**
- **M1:** 9/9 Bots auf der geschlossenen Kerze, im Papier- und im Selektionspfad.
- **M2:** Die 150 Aktienreihen sind split- und dividendenbereinigt (`yf.download(…, auto_adjust=True)`, Stand 02.09.2026, älter als das Repo). Keine Bot-Regel nutzt ein absolutes Preisniveau.
- **M3:** Die Sonde bindet von der Kette nur `auswertung.py` samt Importen und Tabellen.

**M1**
- **F1-1** *„`XAUTUSDT_1h.csv` ist eine Datei mit Teilkerze im eingefrorenen Datenstand `d9449faf…`. Folgenlos, solange **jede** der vier Ausschlusslisten das Symbol streicht. Reicht das, oder gehört die Tatsache (Datei, Kerze, Schreibzeit) als Tatsachennotiz zum Snapshot — und die vier Kopien von `{"XAUTUSDT", "PAXGUSDT"}` auf eine?“*
- **F1-2** *„Für 175 Dateien ohne feineren Zeugen (150 Aktien, 25 Krypto-1h) ist ‚letzte Kerze abgeschlossen' nur durch Schreibpfad und Zeitstempel belegt; `snapshot.py` prüft `rand_letzte` dort nicht. Genügt der Zeitstempel-Beleg dieser Sitzung als Vorbedingung des Tags, oder soll die Prüfung ihn führen?“*
- **F1-3** *„Die Elliott-Frische an der Wanduhr statt an `laufbeginn()` — Handwerk bei der nächsten Öffnung, oder gleichgültig?“*

**M2**
- **F2-1** *„Gehört der Adjustierungsstand (split- und dividendenbereinigt, rückwärts, Stand 02.09.2026; Abrufcode unversioniert, nächstliegend `0f6491b`; yfinance-Fassung unbekannt) als Tatsachennotiz neben 5e?“*
- **F2-2** Papierpfad: `entry_price`/`stop_price` liegen als absolute Zahlen in der Datenbank und werden gegen neu bereinigte Reihen verglichen. *„berührt den Live-Record, der die einzige Out-of-Sample-Evidenz ist, nicht die Selektion. Ein Registerthema oder ein Backlog-Punkt?“*
- **F2-3** ⭐ *„Stufe 3 der Zuteilungskaskade vergleicht dividendenbereinigtes Dollar-Volumen über Symbole. `zuteilung.py` steht auf der Sperrliste (Punkt 10). Ist das eine Eigenschaft, die als Tatsachennotiz neben Punkt 10 und 5e steht, oder ein Grund, Stufe 3 vor dem Tag anders zu fassen (etwa mit unbereinigtem Kurs oder Stückzahl × Split-Faktor)?“* Wie oft Stufe 3 entscheidet, wäre eine Messung auf dem Selektionsraum und ist **nicht gemessen**. Betroffen sind drei Aktien-Bots ohne Signalspalte; Krypto nicht.

**M3**
- **F3-1** *„Snapshot-Bindung: Soll die Startprüfung den Snapshot nachrechnen (wie `snapshot.py --pruefen`), soll das Abbild den MANIFEST-Hash führen, oder beides — und vor dem Tag?“* Heute liest die Startprüfung `snapshot_hash` aus dem MANIFEST, statt ihn zu rechnen.
- **F3-2** *„Punkt 8 bindet `config/*.txt` im Repo; gelesen werden unter dem Modus die Kopien im Snapshot. Soll Punkt 8 (oder das Abbild) die Snapshot-Kopien nennen?“* Heute bytegleich.
- **F3-3** ⭐ *„`auswertung.py` liest `herkunft.json` nicht, ist aber eingefroren. Ist die Prüfung der Herkunft der Rohergebnisse Sache von `auswertung.py` (dann Öffnung vor dem Tag), des Erzeugers oder einer eigenen Stufe zwischen beiden?“* Der Docstring von `auswertung.py` (Z. 51–52) nennt `herkunft.json` als Teil des Vertrags, der Code liest es nirgends.

## 5. Was der steuernde Chat als Nächstes plant — bitte prüfen, ob es den Registertext oder den Tag-Commit berührt (Auflage 25f)

1. **Ein Bündel „Wachen vor dem Tag“:**
   - Sonde vergleicht `EINGEFROREN` mit dem Abbild (T114-2);
   - `register()`/`block()` im Modus bei `fehlend` ⇒ 2 (T114-1);
   - Startprüfung rechnet den Snapshot nach (F3-1);
   - `auswertung.py` prüft `herkunft.json`, falls F3-3 so entschieden wird, zusammen mit der Streichung aus R8 (a).
   
   Danach ein neues Abbild und 45.11 bzw. 46.
2. Danach der **Erzeuger** (Stufe V) mit den Abnahmebedingungen aus R5.

Bitte sag je Punkt: Handwerk oder Amendment. Wo Registertext nötig ist, bitte als R-Block am Ende.

## In einfacher Sprache

Zwei Aufträge sind zurück. Der erste hat Fables Texte ins Regelwerk eingetragen und die neun Handelslisten mit Prüfsumme festgehalten. Er hat aber angehalten, weil das Prüfwerkzeug neue Einträge gegen ein altes Abbild nicht einzeln meldet; die falsche Erwartung stand in meinem Auftrag. Der zweite hat drei Dinge nachgesehen, ohne etwas zu ändern: Alle Bots entscheiden auf fertigen Kerzen, die Aktienkurse sind bereinigt, und das Prüfwerkzeug bewacht nur einen Teil der Kette vom Datenstand bis zum Bericht. Fable soll sagen, welche dieser Lücken vor dem grossen Lauf geschlossen werden müssen.

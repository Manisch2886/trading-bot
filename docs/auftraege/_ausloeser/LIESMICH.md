# Auslöserordner des Sitzungswächters

⚠️ **Hier gehört nichts von Hand hinein.**

Taucht in diesem Ordner eine Datei namens `starte_TB-<Nummer>` auf, startet der
Sitzungswächter auf dem MacBook eine Claude-Code-Sitzung für genau diesen
Auftrag. Der **Inhalt** der Datei wird nie gelesen und nie ausgeführt — nur der
Name, und aus dem nur die Nummer.

Der Wächter kennt hier zwei weitere Auslöser
(`docs/werkzeuge/sitzungswaechter/LIESMICH.md`, Abschnitt „Gilt seit TB-144
(Wächter-Reparatur)“): Nach `schliesse_<HEAD>` (beide Wachen unverändert:
HEAD-Gleichheit, 600 s) schliesst der Wächter genau das gemerkte Fenster; die
Bedingungen dafür stehen dort. Eine Datei `probe_<PID>` öffnet ein Fenster
wie ein echter Start, prüft die Eingabezeile, beendet genau die dabei
entstandene Sitzung mit `TERM` und räumt das Fenster auf — kein Auftrag, kein
Satz; gelesen wird nur der Dateiname.

**Eingerichtet:** `docs/werkzeuge/sitzungswaechter/`
**Protokoll:** `logs/sitzungswaechter/waechter.log`

Erledigte und abgewiesene Auslöser wandern nach `_erledigt/` — sie werden
verschoben, nie gelöscht.

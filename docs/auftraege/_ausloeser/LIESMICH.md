# Auslöserordner des Sitzungswächters

⚠️ **Hier gehört nichts von Hand hinein.**

Taucht in diesem Ordner eine Datei namens `starte_TB-<Nummer>` auf, startet der
Sitzungswächter auf dem MacBook eine Claude-Code-Sitzung für genau diesen
Auftrag. Der **Inhalt** der Datei wird nie gelesen und nie ausgeführt — nur der
Name, und aus dem nur die Nummer.

**Eingerichtet:** `docs/werkzeuge/sitzungswaechter/`
**Protokoll:** `logs/sitzungswaechter/waechter.log`

Erledigte und abgewiesene Auslöser wandern nach `_erledigt/` — sie werden
verschoben, nie gelöscht.

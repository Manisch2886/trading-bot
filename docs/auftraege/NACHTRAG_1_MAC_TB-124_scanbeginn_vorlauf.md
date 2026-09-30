# NACHTRAG 1 zu TB-124 — Scanbeginn nie vor dem Vorlauf der Zelle (Fable 30a, R53); ersetzt B1, ergänzt C2; 0c nachholen

**Empfänger:** die laufende Mac-Sitzung TB-124 · **Von:** steuernder Chat, 30.09.2026, ca. 20:15 · **Gilt ab:** vor Schritt B. Ist B schon committet: B nach diesem Nachtrag nachziehen, C1–C6 danach.
**Anlass:** Fables Antwort 30a ist eingegangen, jetzt im Repo als `docs/projektfuehrung/FABLE_ANTWORT_2026-09-30a_vorgepruefte_fragen_e2.md` (Abschrift aus einem Chat-Anhang, 12 925 B, md5 `f9cdbbef…`). Z. 10: *„Zu TB-122 F1 … Behebung Handwerk mit Freigabe, mit einer Bedingung aus dieser Antwort — der Scanbeginn einer Zelle ist nie früher als ihr Vorlauf …“*; R53 (Z. 25): *„Der Scanbeginn einer Zelle liegt nie vor ihrem Vorlauf (TB-122 F1, Handwerk).“* R53 ist noch nicht im Register (E-2); die Bedingung gilt für TB-124 als Handwerksvorgabe des steuernden Chats. Freigabe und Dateiumfang von TB-124 bleiben unverändert.

## Was am Auftrag falsch war

B1 im Auftrag setzt den Scanbeginn auf `max(BB_PERIOD, L, VOLUME_AVG_PERIOD) + 1`, also L + 1. Das liegt **vor** dem Vorlauf der Zelle: Der Squeeze-Status, den der Einstieg bei i am Vortag braucht, ist erst ab einem späteren Balken definiert. B1 wird deshalb ersetzt.

**Gemessen vom steuernden Chat (30.09.2026, ca. 20:05, nur lesend), von der Sitzung nachzumessen:**
- `strategies/volatility_breakout/indicators.py`: `bollinger_bands` rechnet `close.rolling(window=period)` (mean, std); `squeeze_threshold` rechnet `width.rolling(window=lookback_days).quantile(percentile / 100)`. `min_periods` ist nicht gesetzt. Der Krypto-Zwilling ist gleich gebaut.
- `strategies/volatility_breakout/backtest_breakout.py` Z. 155–166: Scan ab `start_i`, Einstieg bei i nur mit `is_squeeze[i − 1]` und `close[i] > upper[i]`. Vor dem ersten Einstieg führt die Schleife keinen Zustand mit.

**Erschlossen daraus** (0-basierter Index):
- `bb_width` ist ab 19 definiert, `squeeze_thresh` ab 19 + (L − 1) = L + 18.
- Ein Einstieg ist frühestens bei **i = L + 19 = BB_PERIOD + L − 1** möglich.
- Bei der Voreinstellung 126 ist das 145. Der heutige Scanbeginn 127 hat also nie etwas abgeschnitten, und ein Scanbeginn 145 sollte mit den Voreinstellungen bytegleich bleiben.

## B1 (ersetzt)

- **Scanbeginn:** Er ist der erste Index, an dem die Einstiegsbedingung der Zelle definiert ist. Die Sitzung leitet ihn aus den Indikatordefinitionen im Code her; nach obiger Messung ist er `BB_PERIOD + L − 1`. Die Formel steht mit ihrer Herleitung als Kommentar im Code.
- `entry_cutoff`: Die Zeile `max(start_i, …)` bleibt unverändert.
- `WARMUP_PERIOD` bleibt als Modulkonstante mit unverändertem Wert stehen (B3).
- **Nicht** `max(BB_PERIOD, L, VOLUME_AVG_PERIOD) + 1`.
- Bauart wie B2 im Auftrag: Der Lookback reist mit dem Frame.
- Weicht die Herleitung der Sitzung von `BB_PERIOD + L − 1` ab (etwa weil ein Indikator anders gebaut ist als gemessen), gilt die Herleitung der Sitzung. Die Abweichung steht im Ergebnis.

## C2 (ergänzt)

Zusätzlich zu C2 im Auftrag, in den zwei `test_posten3_durchreichung.py`:
- **(i) Knapp am Vorlauf:** Für **jede** Stufe von `bb_lookback` aus `registerdaten.raster()` (beide Bots, also auch die Stufen über 126) gilt:
  - Der Scanbeginn ist gleich dem hergeleiteten Wert.
  - Am Index davor ist die Einstiegsbedingung nicht definiert (NaN im Squeeze-Status des Vortags).
  - Ab dem Scanbeginn ist sie definiert.
  Das ist die Probe auf „nie vor dem Vorlauf“ und zugleich auf „nicht später als nötig“.
- **(ii) Einstiegsfall:** Die Bereiche im Auftrag (39–126 bei Stufe 20, 116–126 bei Stufe 97) passen zu dieser Herleitung. Das Einstiegssignal liegt am ersten zulässigen Index und wird gefunden.
- **(iii) Gegenprobe (40.7)** wie im Auftrag.

C1 bleibt der Massstab: Mit Voreinstellungen ist die Ausgabe **bytegleich** (Scanbeginn 145 statt 127). Weicht C1 ab, gilt das Abbruchkriterium des Auftrags.

## Für das Ergebnis

- Ein Absatz „Nachtrag 1 (Fable 30a, R53)“: Wortlaut dieses Nachtrags, hergeleiteter Scanbeginn je Stufe (Tabelle Stufe ⇒ Index), Belegdatei.
- **Befund für E-2, nur benennen:** R53 beschreibt den Vorlauf als „die oberste registrierte Stufe … zuzüglich der festen Fenster des Bots (etwa Bollinger-Fenster …)“. Wörtlich addiert wären das L + 20 Balken; die zwei hintereinanderliegenden rollenden Fenster teilen sich aber einen Balken. Die Sitzung nennt die hergeleitete Zahl neben der wörtlich addierten. Die Einordnung macht der steuernde Chat in E-2.
- In „Entwurf der Tatsachennotiz“ (E2 des Auftrags): „Stand 11.3“ nach TB-124 samt dem Satz, dass der Scanbeginn der Zelle an ihrem Vorlauf liegt (Fable 30a, R53).

## 0c nachholen (Dialog-Index)

Die Antwort 30a lag beim Start noch nicht im Repo, deshalb ist 0c entfallen. Jetzt nachholen:
- `trading-env/bin/python3 docs/werkzeuge/dialog_index.py --handfelder docs/belege/TB-124/0c_handfelder.json` (Datei vom steuernden Chat beigelegt);
- danach `--pruefen` ⇒ rc 0. Weicht es ab: Befund, kein Abbruch.

## Dateien, die der steuernde Chat während des Laufs ablegt

Mit dem **nächsten Commit** der Sitzung committen und im Ergebnis nennen:
- dieser Nachtrag `docs/auftraege/NACHTRAG_1_MAC_TB-124_scanbeginn_vorlauf.md`;
- `docs/projektfuehrung/FABLE_ANTWORT_2026-09-30a_vorgepruefte_fragen_e2.md`;
- `docs/belege/TB-124/0c_handfelder.json`;
- der Nachtrag am Ende von `docs/projektfuehrung/UEBERGABE.md` (nur angehängt).

Diese Einträge sind **kein** Abbruchgrund nach 0a; 0a ist vorbei. Kommt später weiteres vom steuernden Chat unter `docs/` dazu, gilt dasselbe.

## BACKLOG-Nachtrag (5b), wörtlich

In `docs/projektfuehrung/BACKLOG.md` als neuen Block am Ende von Abschnitt „## 5 — Nach TB-30b“ einfügen, direkt vor der Zeile „## 6 — Geparkt, null Arbeit …“. Nur `docs/`, `numstat` belegen, nichts umformulieren:

```
### Aus Fable 30a (30.09.2026) — Folgen von R53–R55, vor bzw. mit E-2

- **R53 (a):** `research/faltenplan_neun/faltenplan_neun.py` führt den Vorlauf je Bot als feste Zahl; künftig aus `registerdaten.py` gerechnet (oberste Stufe je Rückblick-Achse zuzüglich fester Fenster), kein Literal; der Faltenplan trägt ihn je Bot als Feld. Erste Falte danach neu ableiten (Verfahrensmessung nach 27.2). Voraussetzung zu messen: Sind oberste Stufe und feste Fenster maschinell aus `registerdaten.py` lesbar? Sonst Literal mit Test nach 32.5 (c).
- **R53 (b):** Tatsachennotiz zu den Nachmessungen 25.2, 15.5, 21.4 (vor TB-30b Posten 3).
- **R53, Zählweise:** wörtlich addiertes „zuzüglich der festen Fenster“ gegen den aus dem Code hergeleiteten Vorlauf (TB-124 Nachtrag 1) — in E-2 einordnen.
- **R54:** Messbitte — liest irgendein Code `netto_rendite_pct` aus dem Vertrag von `auswertung.py` und rechnet damit?
- **R55:** Probe „leere Menge ⇒ (d) nicht erfüllt“ mit Gegenprobe (40.7), Handwerk; heute prüft sie kein Test. Zu konstruieren: alle zulässigen Zellen sind Spitzen.
```

Im Journalblock **DV** einen Satz dazu: „Fable 30a eingegangen (R53–R55); Nachtrag 1 zu TB-124 (Scanbeginn nie vor dem Vorlauf) umgesetzt; BACKLOG-Block ‚Aus Fable 30a‘ eingefügt.“

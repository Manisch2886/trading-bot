# REGISTER-KOPIE Abschnitt 18 (von 0–52) — Register-Z. 3023–3087 — Commit ad351d5f0351d8a25479547edb96a32dd6cf3bd5 — 2026-10-02 — Original sha256 a749678043f32e5c6bf7034205bc7176550ec4ea35d08171b43d40401aec7ece — KOPIE, nicht das Register

## 18. Tatsachennotiz zu Registertext 5 / 5a — der gezogene Snapshot (TB-55, 19.09.2026)

**Datiert angehängt. Nichts entfernt. Kein Registertext wird geändert — hier
wird eine Messung festgehalten**, in der Form der Tatsachennotiz zu 4d
(Abschnitt 15.6). Das ist der Nachtrag, den `docs/ERGEBNIS_TB-55_snapshot.md`
angekündigt hat: TB-55 hat den Snapshot gezogen und ausdrücklich keinen
Registertext angefasst.

**Der gezogene Snapshot** (Tatsachennotiz zu 5 / 5a; jede Zahl aus
`snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/MANIFEST.json` gelesen, nicht abgeschrieben):

| | |
|---|---|
| Gezogen (`zeitpunkt_utc`) | **2026-09-19T06:49:32+00:00** |
| Name (`snapshot_hash`) | **`63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2`** |
| Ort | `snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/` |
| Versioniert | Commit **`1075dec`** auf `main` (`git log --oneline -- snapshots/ \| tail -1`; liegt auf `origin/main`) |
| Dateien gesamt (`dateien_gesamt`) | **225** — 223 Kursdateien sowie `config/sp500_top150.txt` und `config/top25_symbols.txt` |
| Bytes gesamt (`bytes_gesamt`) | **211 040 678** |
| Datenstand (`datenstand_hash`) | **`d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`** bei **223** Kursdateien — dreimal gemessen (vor dem Ziehen, danach, am Ende), dreimal gleich |
| Zugelassene Befunde der Zeitabdeckungsprüfung (`zugelassene_befunde_anzahl`) | **36**, sämtlich der Art `rand_erste`, nach der Ausnahme in **Abschnitt 17.3** (`zugelassene_befunde_herkunft.fundstelle` = `docs/VORREGISTRIERUNG_neuselektion.md, Abschnitt 17.3`) |
| Übergangene Befunde (`teilkerzen.nicht_zugelassen`) | **leer** — kein Befund wurde übergangen |
| Nachprüfung (`shared/snapshot.py --pruefen`) | **`UNVERAENDERT`**, Rückgabewert 0 |

⭐ **Der Datenstand `d9449faf…` ist derselbe wie in der Tatsachennotiz vom
15.09.2026 (Abschnitt 10) und im Nachtrag 17.9** — der Snapshot enthält den
Bestand, den das Register seit dem 15.09. verankert. Der Name `63e4b6c8…`
läuft über die 225 Dateien des Laufs (Kursdateien plus die zwei
Symbollisten); der Wert `4fee547d…` aus 17.9 lief nur über die 223 Kursdateien
und bezeichnet **nicht** diesen Snapshot. Beide Werte bleiben richtig; sie
beantworten verschiedene Fragen.

Vier Punkte, die diese Tabelle tragen:

1. **Jede der 225 Dateien wurde beim Kopieren byteweise gegen die Quelle
   geprüft**; die anschliessende Nachprüfung meldet `UNVERAENDERT`. Beim
   Einchecken legte git **keinen neuen Blob für eine der 225 Dateien** an —
   ein Blob (das Manifest), vier Trees, ein Commit. Die Inhalte sind identisch
   mit `data/`; Nachweis in `docs/ERGEBNIS_TB-55_snapshot.md`.
2. **Der Name wurde viermal unabhängig gerechnet**: TB-49 in der Cloud
   (Python 3.11, echter Zug in ein Wegwerfverzeichnis), TB-49 auf dem MacBook
   (Python 3.9.6, Trockenlauf), TB-55 in der Cloud (3.11.15, Trockenlauf) und
   TB-55 auf dem MacBook (3.9.6, dieser Zug) — viermal derselbe. Er hängt weder
   an der Maschine noch am Python-Zweig.
3. **Die 36 Befunde sind keine Lücke im Register, sondern seine Anwendung.**
   Die Ausnahme in 17.3 verlangt drei Bedingungen; das Manifest führt jeden
   Befund je Datei mit Art und erster Kerze auf (17.3 (c)). `nicht_zugelassen`
   ist leer, das Werkzeug hätte sonst nicht gezogen (Registertext 5a, Zusatz).
4. ⚠️ **Dieser Snapshot ist der Eingabezustand des Selektionslaufs. Ein
   zweiter Snapshot ist ein neuer Lauf** (Registertext 5 in 16.3, 5a in 17.1;
   Backlog F1a). `snapshots/` wird von hier an nur gelesen.

**Was diese Notiz nicht tut:** kein Selektionslauf, kein signierter Tag, kein
Zeitanker, kein Amendment — nichts an Registertext 5, 5a oder 5c ist
umformuliert. Der signierte Tag bleibt der nächste Schritt und gehört dem
Betreiber (Abschnitt 13).

*Nachgetragen in TB-55b, 19.09.2026. Tatsachennotiz: eine Messung, keine
Festlegung.*

> ⭐ **Abschnitt 18 ERGÄNZT durch R28 (47.11)** (Fable 27c R28, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

---


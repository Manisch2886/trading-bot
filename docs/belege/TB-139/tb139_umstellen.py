#!/usr/bin/env python3
"""TB-139: stellt die uebernommenen Skripte der Sitzung um (Schritt 0, nach dem Commit S0).
Je Skript: Vorlage lesen (docs/belege/TB-136/ oder docs/belege/TB-140/), sha256 der Vorlage pruefen, die Ersetzungen
der Liste anwenden - jeder alte Text muss genau so oft vorkommen wie angegeben -, sha256 des Ergebnisses pruefen und
nach docs/belege/TB-139/<name> schreiben. Weicht etwas ab, wird fuer dieses Skript nichts geschrieben (rc 1).
Gebaut und an Kopien geprueft vom Erbauer des Auftrags; die Liste steht unten als Daten, nichts ist abgetippt.

Aufruf aus der Repo-Wurzel (Python 3.9, nur Standardbibliothek):
  trading-env/bin/python3 <dieses Skript>              schreibt die 20 Skripte, druckt je Skript Name und sha256
  trading-env/bin/python3 <dieses Skript> --pruefen    schreibt nichts; vergleicht die vorhandenen Dateien mit dem Soll
  weitere: --wurzel <ordner> (Standard "."), --ziel <ordner> (Standard docs/belege/TB-139)
rc 0 = alle wie das Soll, rc 1 = Abweichung.
"""
import hashlib
import os
import sys

argv = sys.argv[1:]
PRUEFEN = "--pruefen" in argv
def wert(name, standard):
    return argv[argv.index(name) + 1] if name in argv else standard
WURZEL = wert("--wurzel", ".").rstrip("/") + "/"
ZIEL = wert("--ziel", WURZEL + "docs/belege/TB-139").rstrip("/") + "/"
def sha(t): return hashlib.sha256(t.encode("utf-8")).hexdigest()

# (Vorlage, sha256 der Vorlage, Zielname, sha256 des Ergebnisses, [(alter Text, neuer Text, Zahl der Vorkommen), ...])
SPEC = [('docs/belege/TB-136/0b_ausgang.sh',
  'f341486639bea9c7cb34ee30960c282281745c2522d459a70f5bbccc088e82f3',
  '0b_ausgang.sh',
  'af9a7e4fee688d959c42f5167683009ded7bb199e51de7f7a406288db23a8f62',
  [('# TB-136 0b/A5 - Ausgangs- bzw. Nachher-Werte (Vorlage docs/belege/TB-132/0b_ausgang.sh, dort Bauart TB-117):',
    '# TB-139 0b/A5 - Ausgangs- bzw. Nachher-Werte (Vorlage docs/belege/TB-136/0b_ausgang.sh, dort nach TB-132 und Bauart TB-117):',
    1),
   ('md5 und Bytes der Quelle 04a am Commit S0, Abschnitt 10', 'md5 und Bytes der Quelle 07a am Commit S0, Abschnitt 10', 1),
   ('#   bash docs/belege/TB-136/0b_ausgang.sh', '#   bash docs/belege/TB-139/0b_ausgang.sh', 1),
   ('BL=docs/belege/TB-136', 'BL=docs/belege/TB-139', 1),
   ('echo "# TB-136 0b ($M)', 'echo "# TB-139 0b ($M)', 1),
   ('(Soll vorher: 11471 Zeilen, sha256 9a2cefb7..., md5 1ce393ae...)', '(Soll vorher: 11581 Zeilen, sha256 8d505a38..., md5 757cda8c...)', 1),
   ('(Soll vorher 66480962..., fehlend [], 23 Teile)', '(Soll vorher cfff54ca..., fehlend [], 23 Teile)', 1),
   ('md5 und Bytes der Quelle 04a am Commit $S0 und im Arbeitsbaum (Soll 856b2c15..., 29195 B)',
    'md5 und Bytes der Quelle 07a am Commit $S0 und im Arbeitsbaum (Soll 388187e2..., 57165 B)',
    1),
   ('Q=FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md', 'Q=FABLE_ANTWORT_2026-10-07a_schnitt_im_erzeuger_wache_ein_eintrag.md', 1)]),
 ('docs/belege/TB-136/a4_probelauf.sh',
  '07b037a73590e790df11d6305120cde7423daa8ea883baa7b4134a772cd1a992',
  'a4_probelauf.sh',
  '176bcee31518973e1355f6600880c9dcac373ff03ce68a66ce744a1e4ae8691d',
  [('# TB-136 A4 - Probelauf', '# TB-139 A4 - Probelauf', 1),
   ('# Vorlage docs/belege/TB-132/a4_probelauf.sh;', '# Vorlage docs/belege/TB-136/a4_probelauf.sh;', 1),
   ('bash docs/belege/TB-136/a4_probelauf.sh', 'bash docs/belege/TB-139/a4_probelauf.sh', 1),
   ('BL=docs/belege/TB-136', 'BL=docs/belege/TB-139', 1),
   ('echo "# TB-136 A4 Probelauf', 'echo "# TB-139 A4 Probelauf', 1),
   ('echo "## git diff --quiet $S0 -- Auftrag Quelle"; git diff --quiet $S0 -- docs/auftraege/MAC_TB-136_register_fable_04a.md '
    'docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md;',
    'echo "## git diff --quiet $S0 -- Auftrag Quelle Anfrage Eroeffnungstext"; git diff --quiet $S0 -- docs/auftraege/MAC_TB-139_register_fable_07a.md '
    'docs/projektfuehrung/FABLE_ANTWORT_2026-10-07a_schnitt_im_erzeuger_wache_ein_eintrag.md '
    'docs/projektfuehrung/FABLE_ANFRAGE_2026-10-07a_go_live_schnitt_voraussetzungen.md docs/projektfuehrung/FABLE_UEBERGABE_2026-10-07_eroeffnung.md;',
    1)]),
 ('docs/belege/TB-136/a5_r_diff.py',
  '3b41200aaa4cd3f2e0cc02e9788bc7d7259f89b4a0ba4734fd7ef73543592a04',
  'a5_r_diff.py',
  'e594b64b989ce40b74fff1ce176263045bf85dea5e9547123e5f6504bef3aca4',
  [('"""TB-136 A5: jeder der 4 R-Bloecke (R74-R77) im Register gegen die Quelle 04a, mit `diff`.',
    '"""TB-139 A5: jeder der 6 R-Bloecke (R78-R83) im Register gegen die Quelle 07a, mit `diff`.',
    1),
   ('nur in Z. 156-166).', 'nur in Z. 227-243).', 1),
   ("Im Register: Ueberschrift '### 54.<n> R<nn> — ',", "Im Register: Ueberschrift '### 55.<n> R<nn> — ',", 1),
   ('docs/belege/TB-136/a5_r_diff.py <S0> [<register>]', 'docs/belege/TB-139/a5_r_diff.py <S0> [<register>]', 1),
   ('rc 0 = 4/4 diff rc 0; rc 1 = Abweichung.', 'rc 0 = 6/6 diff rc 0; rc 1 = Abweichung.', 1),
   ('Q = ("docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md", 156, 166)',
    'Q = ("docs/projektfuehrung/FABLE_ANTWORT_2026-10-07a_schnitt_im_erzeuger_wache_ein_eintrag.md", 227, 243)',
    1),
   ('re.match(r"^### 54\\.(\\d+) R(\\d+) — ", s)', 're.match(r"^### 55\\.(\\d+) R(\\d+) — ", s)', 1),
   ('print("# TB-136 A5 R-Diff:', 'print("# TB-139 A5 R-Diff:', 1),
   ('    for r in range(74, 78):', '    for r in range(78, 84):', 1),
   ('print("Ergebnis: %d/4 rc 0" % gut)', 'print("Ergebnis: %d/6 rc 0" % gut)', 1),
   ('sys.exit(0 if gut == 4 and sorted(quelle) == list(range(74, 78)) else 1)',
    'sys.exit(0 if gut == 6 and sorted(quelle) == list(range(78, 84)) else 1)',
    1)]),
 ('docs/belege/TB-136/a5_zitate.py',
  '365887ab05821aa602612d4b8cb9ead2501d75846bab59dbbc726d3f3a72adc7',
  'a5_zitate.py',
  '59d81de92647abeab802c3ab5259e07b08a0bbb07500fecb2bf36f0f4c74ade4',
  [('"""TB-136 A5: Kopf', '"""TB-139 A5: Kopf', 1),
   ('54.5-54.6', '55.7-55.8', 2),
   ('54.5', '55.7', 4),
   ('54.1', '55.1', 2),
   ('54.0', '55.0', 2),
   ('## 54. ', '## 55. ', 4),
   ('docs/belege/TB-136/a5_zitate.py', 'docs/belege/TB-139/a5_zitate.py', 1),
   ('MAC_TB-136_register_fable_04a.md', 'MAC_TB-139_register_fable_07a.md', 1),
   ('print("# TB-136 A5 Zitate', 'print("# TB-139 A5 Zitate', 1)]),
 ('docs/belege/TB-136/a5_mutation.py',
  '8e7dca48e883062398ad9d32f7dc1ed1ce3b9ff839629468115f420d9041b59c',
  'a5_mutation.py',
  'e1b759c16f89ceca76b5c0387107e8a23bcc3248457dda3c39b1b56ee2b1e80a',
  [('"""TB-136 A5 Mutationsprobe', '"""TB-139 A5 Mutationsprobe', 1),
   ('(Block R74 unter 54.1, erstes Vorkommen', '(Block R78 unter 55.1, erstes Vorkommen', 1),
   ('docs/belege/TB-136/a5_mutation.py', 'docs/belege/TB-139/a5_mutation.py', 1),
   ('s.startswith("### 54.1 R74 — ")', 's.startswith("### 55.1 R78 — ")', 1),
   ("(R74), ' die ' -> ' der '", "(R78), ' die ' -> ' der '", 1),
   ('"docs/belege/TB-136/a5_r_diff.py"', '"docs/belege/TB-139/a5_r_diff.py"', 1),
   ('s.startswith("R74")', 's.startswith("R78")', 1)]),
 ('docs/belege/TB-136/a5_marken.py',
  '622022a380d863ef124637a060d53ca5c02ccdbad4b098847400dd8ec8931325',
  'a5_marken.py',
  'a143f80f4d8ef76ca6318bebe6db1ce174d29e5a096fa79860420665bc4cd72a',
  [('TB-136', 'TB-139', 9),
   ('04a', '07a', 1),
   ('re.match(r"^\\| 54\\.\\d \\|", s)', 're.match(r"^\\| 55\\.\\d \\|", s)', 1),
   ('if len(ueber) != 4:', 'if len(ueber) != 6:', 1),
   ('gezaehlt: Soll 15;', 'gezaehlt: Soll 20;', 1),
   ('Marken gesetzt: %d/15;', 'Marken gesetzt: %d/20;', 1),
   ('im Register: %d (Soll 15)', 'im Register: %d (Soll 20)', 1),
   ('if alle != 15 or gesetzt != 15:', 'if alle != 20 or gesetzt != 20:', 1)]),
 ('docs/belege/TB-136/a5_nachweis.sh',
  '2ca6a4fd6a4b07a99dabca1c3505111bc129073ef3e0b5d751c821aee973f0da',
  'a5_nachweis.sh',
  '23016a19b6af567cb3a11d82a8acb3590255c50cfaf51591839af411a92ca026',
  [('# TB-136 A5 - Nachweis', '# TB-139 A5 - Nachweis', 1),
   ('Vorlage docs/belege/TB-132/a5_nachweis.sh', 'Vorlage docs/belege/TB-136/a5_nachweis.sh', 1),
   ('bash docs/belege/TB-136/a5_nachweis.sh', 'bash docs/belege/TB-139/a5_nachweis.sh', 1),
   ('BL=docs/belege/TB-136', 'BL=docs/belege/TB-139', 1)]),
 ('docs/belege/TB-136/test_vorregistrierung.sh',
  '038128b64ee71f31a5e2419dbd73e6c2e1626ef2b270589ff6494fab60ff55c2',
  'test_vorregistrierung.sh',
  'a14e25af1bbba00d849d118377a3d35daa99e6c6f1aacc808550d3a94d1a14de',
  [('# TB-136 A5 - test_vorregistrierung', '# TB-139 A5 - test_vorregistrierung', 1),
   ('(Vorlage docs/belege/TB-132/test_vorregistrierung.sh)', '(Vorlage docs/belege/TB-136/test_vorregistrierung.sh)', 1),
   ('bash docs/belege/TB-136/test_vorregistrierung.sh', 'bash docs/belege/TB-139/test_vorregistrierung.sh', 1),
   ('echo "# TB-136 test_vorregistrierung', 'echo "# TB-139 test_vorregistrierung', 1)]),
 ('docs/belege/TB-140/einfuegen.py',
  'c755023e811ecd21ca6b25bf8f01f6ebab201833c16b7ecbd0f121c917e50268',
  'b_einfuegen.py',
  '25d5ee586a9feb6ce0a5c2242f3607890aecfc825f8375ba4d45f06c74621b6e',
  [('"""TB-140 Schritt N: Einfügung E1 (BACKLOG) aus dem Auftragsdokument ausführen.',
    '"""TB-139 Schritt B: Einfügungen E1 und E2 (BACKLOG) aus dem Auftragsdokument ausführen.',
    1),
   ('erste Zeile des Texts nachher zählen (Soll 1). Ergebnis nach einfuegungen.txt.',
    'erste Zeile des Texts nachher zählen (Soll 1). Ergebnis nach b_einfuegung.txt.',
    1),
   ('docs/belege/TB-140/einfuegen.py', 'docs/belege/TB-139/b_einfuegen.py', 2),
   ('Vorlage: docs/belege/TB-133/einfuegen.py (dort aus TB-131).', 'Vorlage: docs/belege/TB-140/einfuegen.py (dort aus TB-133 und TB-131).', 1),
   ('docs/auftraege/MAC_TB-140_verfahrensmessung_voraussetzungen.md', 'docs/auftraege/MAC_TB-139_register_fable_07a.md', 1),
   ('AUSGABE = Path("docs/belege/TB-140/einfuegungen.txt")', 'AUSGABE = Path("docs/belege/TB-139/b_einfuegung.txt")', 1),
   ('BLOECKE = {"E1"}', 'BLOECKE = {"E1", "E2"}', 1),
   ('if nummern != ["E1"]:', 'if nummern != ["E1", "E2"]:', 1),
   ('"# TB-140 Schritt N — Einfügung E1 (erzeugt von einfuegen.py)\\n"', '"# TB-139 Schritt B — Einfügungen E1 und E2 (erzeugt von b_einfuegen.py)\\n"', 1)]),
 ('docs/belege/TB-140/c3_vergleich.py',
  '0dc710c796f491bd3870b753966780359177c3d0ce110e496bed822fe1d5db86',
  'b_vergleich.py',
  'cf6b78d7d26cd15eea1276ef873c16f92552bf4c2d9c1cc929fd97084e7ed2f6',
  [('"""TB-140 Schritt N: Zeichengleichheit der Einfügung E1.', '"""TB-139 Schritt B: Zeichengleichheit der Einfügungen E1 und E2.', 1),
   ('an Zeilengrenzen vorkommt. Ausgabe nach c3_vergleich.txt.', 'an Zeilengrenzen vorkommt. Ausgabe nach b_vergleich.txt.', 1),
   ('Vorlage: docs/belege/TB-133/c3_vergleich.py (dort aus TB-131).', 'Vorlage: docs/belege/TB-140/c3_vergleich.py (dort aus TB-133 und TB-131).', 1),
   ('trading-env/bin/python3 -B docs/belege/TB-140/c3_vergleich.py', 'trading-env/bin/python3 -B docs/belege/TB-139/b_vergleich.py', 1),
   ('docs/auftraege/MAC_TB-140_verfahrensmessung_voraussetzungen.md', 'docs/auftraege/MAC_TB-139_register_fable_07a.md', 1),
   ('AUSGABE = Path("docs/belege/TB-140/c3_vergleich.txt")', 'AUSGABE = Path("docs/belege/TB-139/b_vergleich.txt")', 1),
   ("if alle_gut and anzahl == 1 else 'ABWEICHUNG'", "if alle_gut and anzahl == 2 else 'ABWEICHUNG'", 1),
   ('"# TB-140 N — Zeichengleichheit (c3_vergleich.py)\\n"', '"# TB-139 B — Zeichengleichheit (b_vergleich.py)\\n"', 1)]),
 ('docs/belege/TB-136/c1_registerkopie.sh',
  'f04ce4bdd2614ee39fb2765ba8c8794ab0c81aa8f71f2ecc61fd1957adfc259b',
  'c1_registerkopie.sh',
  '1db8e97ceb87c53625168e900a0c1ca5b0d02444fd26b966c77adffa37aaabf9',
  [('# TB-136 C1 - Registerkopie (wie TB-132 C1, dort nach TB-130 C1 und TB-129 C1):',
    '# TB-139 C1 - Registerkopie (wie TB-136 C1, dort nach TB-132, TB-130 und TB-129):',
    1),
   ('# je Ausgabe und rc nach docs/belege/TB-136/c1_*.txt.', '# je Ausgabe und rc nach docs/belege/TB-139/c1_*.txt.', 1),
   ('bash docs/belege/TB-136/c1_registerkopie.sh', 'bash docs/belege/TB-139/c1_registerkopie.sh', 1),
   ('BL=docs/belege/TB-136', 'BL=docs/belege/TB-139', 1),
   ('{ echo "# TB-136 C1: registerkopie.py', '{ echo "# TB-139 C1: registerkopie.py', 1)]),
 ('docs/belege/TB-136/c2_index_zeilen.py',
  '85a2aa2c4dc6a95045512be57167de5cba21ec44ea86ef008fb7794d3f763cbe',
  'c2_index_zeilen.py',
  'ef5d1ca129477c986dcc7d3630f389fb26a02a23384ea3f615a74cd830fc52ed',
  [('"""TB-136 C2 (mechanischer Teil)', '"""TB-139 C2 (mechanischer Teil)', 1),
   ('Vorlage docs/belege/TB-132/c2_index_zeilen.py, dort nach TB-130 und Bauart TB-129 (jede Zahl;',
    'Vorlage docs/belege/TB-136/c2_index_zeilen.py, dort nach TB-132, TB-130 und Bauart TB-129 (jede Zahl;',
    1),
   ('docs/belege/TB-136/c2_index_zeilen.py <S0> <commit_A>', 'docs/belege/TB-139/c2_index_zeilen.py <S0> <commit_A>', 1)]),
 ('docs/belege/TB-136/c2_index_04a.py',
  'b30791894ce63d7c87f94290ef2b810f1841c9f1f93d60d89d4baed46b2db043',
  'c2_index_07a.py',
  '61473d1565a982867c43140761b7abaf48ace6668562147dbba7eb9761aed968',
  [('"""TB-136 C2: die Tabelle der 15 Marken aus Fable 04a fuer REGISTER_INDEX.md erzeugen (Abschnitt 9 des Index),',
    '"""TB-139 C2: die Tabelle der 20 Marken aus Fable 07a fuer REGISTER_INDEX.md erzeugen (Abschnitt 10 des Index),',
    1),
   ('(Vorlage docs/belege/TB-132/c2_index_02c.py)', '(Vorlage docs/belege/TB-136/c2_index_04a.py)', 1),
   ('docs/belege/TB-136/c2_index_04a.py <S0> <datum>', 'docs/belege/TB-139/c2_index_07a.py <S0> <datum>', 1),
   ('MAC_TB-136_register_fable_04a.md', 'MAC_TB-139_register_fable_07a.md', 1),
   ('open("docs/belege/TB-136/c1_marken.txt"', 'open("docs/belege/TB-139/c1_marken.txt"', 1),
   ('"TB-136, " + DATUM in s', '"TB-139, " + DATUM in s', 1),
   ('assert len(zeilen) == 15 and len(km) == 15, (len(zeilen), len(km))', 'assert len(zeilen) == 20 and len(km) == 20, (len(zeilen), len(km))', 1)]),
 ('docs/belege/TB-136/c2_index_eintraege.py',
  '2acbe9fb76d814d1b03ee94e0eba6a8a70637b0b80aaacfde3e483c53e21b645',
  'c2_index_eintraege.py',
  '5e4064927fc977127640f1557d2f35def954b69a6806c48a46988c39e935a939',
  [('"""TB-136 C2: REGISTER_INDEX.md nach Fable 04a nachziehen (nach c2_index_zeilen.py).',
    '"""TB-139 C2: REGISTER_INDEX.md nach Fable 07a nachziehen (nach c2_index_zeilen.py).',
    1),
   ('Vorlage docs/belege/TB-132/c2_index_eintraege.py (dort nach TB-130 und Bauart TB-129): jede Ersetzung hat einen',
    'Vorlage docs/belege/TB-136/c2_index_eintraege.py (dort nach TB-132, TB-130 und Bauart TB-129): jede Ersetzung hat einen',
    1),
   ('Verweis auf die Abschnittsdateien bis _54.md, Zahl der Teile)', 'Verweis auf die Abschnittsdateien bis _55.md, Zahl der Teile)', 1),
   ('der Liste Nr. 1 bis 9 aus C2 des Auftrags (Tabelle 3: 2d, 5f; Tabelle 4: 48, 51, 52, 53, neue Zeile 54; neuer\n'
    'Abschnitt 9 mit der Tabelle aus c2_index_04a_tabelle.md; Pflegeblock). Die Indexzeilen aus Fable 04a setzt',
    'der Liste Nr. 1 bis 9 aus C2 des Auftrags (Tabelle 2: neue Zeile 5.2; Tabelle 4: 42, 46, 48, 53, 54, neue Zeile 55; neuer\n'
    'Abschnitt 10 mit der Tabelle aus c2_index_07a_tabelle.md; Pflegeblock). Die Indexzeilen aus Fable 07a setzt',
    1),
   ('Anders als die Vorlage: die neuen Texte der Liste Nr. 1 bis 7 und der Vorspann von Abschnitt 9 werden aus dem\n'
    'Auftrag am Commit S0 gelesen (Codespannen der Listenpunkte bzw. der Codeblock nach "Vorspann von Abschnitt 9"),',
    'Wie die Vorlage: die neuen Texte der Liste Nr. 1 bis 7 und der Vorspann von Abschnitt 10 werden aus dem\n'
    'Auftrag am Commit S0 gelesen (Codespannen der Listenpunkte bzw. der Codeblock nach "Vorspann von Abschnitt 10"),',
    1),
   ('von Abschnitt 54 aus c1_registerkopie.txt; in Nr. 7 die Nummer ohne "T", wie in den Zeilen darueber). Der\n'
    'Vorspann wird wie in Abschnitt 8 umbrochen (Breite 118, nur an Leerzeichen).',
    'von Abschnitt 55 aus c1_registerkopie.txt; in Nr. 7 die Nummer ohne "T", wie in den Zeilen darueber; in Nr. 1 kommt die neue Zeile\n'
    'vor die Zeile 5.3). Der Vorspann wird wie in Abschnitt 9 umbrochen (Breite 118, nur an Leerzeichen).',
    1),
   ('docs/belege/TB-136/c2_index_eintraege.py <S0> <commit_A> <datum>', 'docs/belege/TB-139/c2_index_eintraege.py <S0> <commit_A> <datum>', 1),
   ('BL = "docs/belege/TB-136/"', 'BL = "docs/belege/TB-139/"', 1),
   ('T9 = open(BL + "c2_index_04a_tabelle.md"', 'T9 = open(BL + "c2_index_07a_tabelle.md"', 1),
   ('assert sorted(Z) == list(range(1, 16))', 'assert sorted(Z) == list(range(1, 21))', 1),
   ('assert sorted(ab) == list(range(55)), sorted(ab)', 'assert sorted(ab) == list(range(56)), sorted(ab)', 1),
   ('zeilen_reg = ab[54][1]', 'zeilen_reg = ab[55][1]', 1),
   ('t54 = next(n for n, a, b in teile if a <= 54 <= b)', 't54 = next(n for n, a, b in teile if a <= 55 <= b)', 1),
   ('MAC_TB-136_register_fable_04a.md', 'MAC_TB-139_register_fable_07a.md', 1),
   ('c2.split("Vorspann von Abschnitt 9 des Index", 1)', 'c2.split("Vorspann von Abschnitt 10 des Index", 1)', 1),
   ('vorspann.startswith("Alle 15 Marken, die TB-136 gesetzt hat")', 'vorspann.startswith("Alle 20 Marken, die TB-139 gesetzt hat")', 1),
   ('    for n in range(15, 0, -1):', '    for n in range(20, 0, -1):', 1),
   ('p1_alt, p1_neu = punkte[1][0], setze(punkte[1][1])\n'
    'p2_alt, p2_neu = punkte[2][0], setze(punkte[2][1])\n'
    'assert punkte[3][0] == "| 48 aus 29b |" and punkte[4][0] == "| 51 aus 01a |" and punkte[5][0] == "| 52 aus 02a |"\n'
    'assert punkte[6][0] == "| 53 aus 02c |" and punkte[6][1] == "| – |" and punkte[6][2] == "–"\n'
    'neue_zeile = setze(punkte[7][0], ohne_t=True)\n'
    'assert neue_zeile.startswith("| 54 aus 04a | %d |" % t54), neue_zeile\n'
    'assert punkte[9][:2] == ["Zuletzt nachgezogen in TB-132 (04.10.2026):", "In TB-132 (04.10.2026):"], punkte[9][:2]',
    'p1_alt = punkte[1][0]\n'
    'p1_neu = setze(punkte[1][1]) + "\\n" + p1_alt\n'
    'assert p1_alt == "| 5.3 „Krypto: Platzhalter mit Regel“ |" and punkte[1][1].startswith("| 5.2 „Der Go-Live-Schnitt“ | "), punkte[1]\n'
    'assert [punkte[k][0] for k in (2, 3, 4, 5)] == ["| 42 aus 25a/25b/25c |", "| 46 aus 27a |", "| 48 aus 29b |", "| 53 aus 02c |"]\n'
    'assert all(punkte[k][1] == " |" for k in (2, 3, 4, 5))\n'
    'assert punkte[6][0] == "| 54 aus 04a |" and punkte[6][1] == "| – |" and punkte[6][2] == "–"\n'
    'neue_zeile = setze(punkte[7][0], ohne_t=True)\n'
    'assert neue_zeile.startswith("| 55 aus 07a | %d |" % t54), neue_zeile\n'
    'assert punkte[9][:2] == ["Zuletzt nachgezogen in TB-136 (05.10.2026):", "In TB-136 (05.10.2026):"], punkte[9][:2]',
    1),
   ('assert alt_tab == [str(n) for n in range(54)], alt_tab', 'assert alt_tab == [str(n) for n in range(55)], alt_tab', 1),
   ('E = [\n'
    '# Kopf (Index Z. 3-5)\n'
    '("""am Commit `ee43f5f` (04.10.2026), Abschnitte 0–53,\n'
    '11 471 Zeilen, sha256 `9a2cefb7…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4), nachgezogen in TB-126 (E-2), TB-129 (Fable 01a), TB-130 (Fable 02a) und '
    'TB-132 (Fable 02c). **Das ist ein Wegweiser, nicht das\n'
    'Register.** Der Wortlaut steht nur im Register bzw. in der Kopie je Abschnitt `register_kopie/REGISTER_KOPIE_ABSCHNITT_00.md` … `_53.md` (Tabelle unten; '
    'dazu die Teile `REGISTER_KOPIE_teil1–4.md`).""",\n'
    ' """am Commit `%s` (%s), Abschnitte 0–54,\n'
    '%s Zeilen, sha256 `%s…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4), nachgezogen in TB-126 (E-2), TB-129 (Fable 01a), TB-130 (Fable 02a), TB-132 (Fable '
    '02c) und TB-136 (Fable 04a). **Das ist ein Wegweiser, nicht das\n'
    'Register.** Der Wortlaut steht nur im Register bzw. in der Kopie je Abschnitt `register_kopie/REGISTER_KOPIE_ABSCHNITT_00.md` … `_54.md` (Tabelle unten; '
    'dazu die Teile `REGISTER_KOPIE_teil1–%d.md`)."""\n'
    ' % (commit[:7], DATUM, "{:,}".format(zeilen_reg).replace(",", " "), sha[:8], len(teile))),\n'
    '# Wie gemessen\n'
    '("(das Suchmuster des Auftrags, Art `MARKE`, 84 Zeilen)", "(das Suchmuster des Auftrags, Art `MARKE`, %d Zeilen)" % art["MARKE"]),\n'
    '("(Art `MARKE+`, 121 Zeilen)", "(Art `MARKE+`, %d Zeilen)" % art["MARKE+"]),\n'
    '("Art `UEBERSCHRIFT`, 88 Zeilen). Die\\nAusgabe liegt in `docs/belege/TB-132/c1_marken.txt` (zuvor `docs/belege/TB-130/c1_marken.txt`, '
    '`docs/belege/TB-129/c1_marken.txt`, `docs/belege/TB-126/c1_marken.txt`, `docs/belege/TB-118/a4_marken.txt`).",\n'
    ' "Art `UEBERSCHRIFT`, %d Zeilen). Die\\nAusgabe liegt in `docs/belege/TB-136/c1_marken.txt` (zuvor `docs/belege/TB-132/c1_marken.txt`, '
    '`docs/belege/TB-130/c1_marken.txt`, `docs/belege/TB-129/c1_marken.txt`, `docs/belege/TB-126/c1_marken.txt`, `docs/belege/TB-118/a4_marken.txt`)."\n'
    ' % art["UEBERSCHRIFT"]),\n'
    '# Liste Nr. 1 und 2: Tabelle 3, Zeilen 2d und 5f\n'
    '(p1_alt, p1_neu),\n'
    '(p2_alt, p2_neu),\n'
    '# Liste Nr. 8: Abschnitt 9, vor dem Pflegeblock\n'
    '("\\n\\n---\\n\\n**Pflege:**",\n'
    ' "\\n\\n## 9. Die Marken aus Fable 04a (TB-136)\\n\\n" + vorspann + "\\n\\n" + T9 + "\\n\\n---\\n\\n**Pflege:**"),\n'
    '# Liste Nr. 9: Pflegeblock\n'
    '(punkte[9][0], punkte[9][1]),\n'
    '("21 Marken und den drei Indexzeilen nach R70 (b) (`c3_indexzeilen.py`).",\n'
    ' "21 Marken und den drei Indexzeilen nach R70 (b) (`c3_indexzeilen.py`).\\n"\n'
    ' "Zuletzt nachgezogen in TB-136 (%s): Zeilenangaben mit `docs/belege/TB-136/c2_index_zeilen.py` vom Stand\\n"\n'
    ' "`ee43f5f` auf `%s` umgeschrieben (jede Zahl in Listen und Bereichen); 54 kommt zu %s; Abschnittstabelle aus den\\n"\n'
    ' "Köpfen der Abschnittsdateien; Einträge mit `docs/belege/TB-136/c2_index_eintraege.py`; neuer Abschnitt 9 mit den\\n"\n'
    ' "15 Marken und zwei Indexzeilen nach R77 (b) und (c) (`c3_indexzeilen.py`)."\n'
    ' % (DATUM, commit[:7], T)),\n'
    ']',
    'E = [\n'
    '# Kopf (Index Z. 3-5)\n'
    '("""am Commit `9b7b060` (05.10.2026), Abschnitte 0–54,\n'
    '11 581 Zeilen, sha256 `8d505a38…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4), nachgezogen in TB-126 (E-2), TB-129 (Fable 01a), TB-130 (Fable 02a), '
    'TB-132 (Fable 02c) und TB-136 (Fable 04a). **Das ist ein Wegweiser, nicht das\n'
    'Register.** Der Wortlaut steht nur im Register bzw. in der Kopie je Abschnitt `register_kopie/REGISTER_KOPIE_ABSCHNITT_00.md` … `_54.md` (Tabelle unten; '
    'dazu die Teile `REGISTER_KOPIE_teil1–5.md`).""",\n'
    ' """am Commit `%s` (%s), Abschnitte 0–55,\n'
    '%s Zeilen, sha256 `%s…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4), nachgezogen in TB-126 (E-2), TB-129 (Fable 01a), TB-130 (Fable 02a), TB-132 (Fable '
    '02c), TB-136 (Fable 04a) und TB-139 (Fable 07a). **Das ist ein Wegweiser, nicht das\n'
    'Register.** Der Wortlaut steht nur im Register bzw. in der Kopie je Abschnitt `register_kopie/REGISTER_KOPIE_ABSCHNITT_00.md` … `_55.md` (Tabelle unten; '
    'dazu die Teile `REGISTER_KOPIE_teil1–%d.md`)."""\n'
    ' % (commit[:7], DATUM, "{:,}".format(zeilen_reg).replace(",", " "), sha[:8], len(teile))),\n'
    '# Wie gemessen\n'
    '("(das Suchmuster des Auftrags, Art `MARKE`, 95 Zeilen)", "(das Suchmuster des Auftrags, Art `MARKE`, %d Zeilen)" % art["MARKE"]),\n'
    '("(Art `MARKE+`, 128 Zeilen)", "(Art `MARKE+`, %d Zeilen)" % art["MARKE+"]),\n'
    '("Art `UEBERSCHRIFT`, 91 Zeilen). Die\\nAusgabe liegt in `docs/belege/TB-136/c1_marken.txt` (zuvor `docs/belege/TB-132/c1_marken.txt`, '
    '`docs/belege/TB-130/c1_marken.txt`, `docs/belege/TB-129/c1_marken.txt`, `docs/belege/TB-126/c1_marken.txt`, `docs/belege/TB-118/a4_marken.txt`).",\n'
    ' "Art `UEBERSCHRIFT`, %d Zeilen). Die\\nAusgabe liegt in `docs/belege/TB-139/c1_marken.txt` (zuvor `docs/belege/TB-136/c1_marken.txt`, '
    '`docs/belege/TB-132/c1_marken.txt`, `docs/belege/TB-130/c1_marken.txt`, `docs/belege/TB-129/c1_marken.txt`, `docs/belege/TB-126/c1_marken.txt`, '
    '`docs/belege/TB-118/a4_marken.txt`)."\n'
    ' % art["UEBERSCHRIFT"]),\n'
    '# Liste Nr. 1: Tabelle 2, neue Zeile 5.2 vor der Zeile 5.3\n'
    '(p1_alt, p1_neu),\n'
    '# Liste Nr. 8: Abschnitt 10, vor dem Pflegeblock\n'
    '("\\n\\n---\\n\\n**Pflege:**",\n'
    ' "\\n\\n## 10. Die Marken aus Fable 07a (TB-139)\\n\\n" + vorspann + "\\n\\n" + T9 + "\\n\\n---\\n\\n**Pflege:**"),\n'
    '# Liste Nr. 9: Pflegeblock\n'
    '(punkte[9][0], punkte[9][1]),\n'
    '("15 Marken und zwei Indexzeilen nach R77 (b) und (c) (`c3_indexzeilen.py`).",\n'
    ' "15 Marken und zwei Indexzeilen nach R77 (b) und (c) (`c3_indexzeilen.py`).\\n"\n'
    ' "Zuletzt nachgezogen in TB-139 (%s): Zeilenangaben mit `docs/belege/TB-139/c2_index_zeilen.py` vom Stand\\n"\n'
    ' "`9b7b060` auf `%s` umgeschrieben (jede Zahl in Listen und Bereichen); 55 kommt zu %s; Abschnittstabelle aus den\\n"\n'
    ' "Köpfen der Abschnittsdateien; Einträge mit `docs/belege/TB-139/c2_index_eintraege.py`; neuer Abschnitt 10 mit den\\n"\n'
    ' "20 Marken und drei Indexzeilen nach R80 (b) (`c3_indexzeilen.py`)."\n'
    ' % (DATUM, commit[:7], T)),\n'
    ']',
    1),
   ("# Liste Nr. 3 bis 7: Tabelle 4, Zeilen an ihrem Anfang finden (genau eine), Zusatz vor dem Schluss ' |' bzw. statt '– |'\n"
    'ANH = [\n'
    '("| 48 aus 29b |", "anhaengen", setze(punkte[3][2])),\n'
    '("| 51 aus 01a |", "anhaengen", setze(punkte[4][1])),\n'
    '("| 52 aus 02a |", "anhaengen", setze(punkte[5][1])),\n'
    '("| 53 aus 02c |", "ersetzen", setze(punkte[6][3])),\n'
    ']',
    "# Liste Nr. 2 bis 7: Tabelle 4, Zeilen an ihrem Anfang finden (genau eine), Zusatz vor dem Schluss ' |' bzw. statt '– |'\n"
    'ANH = [\n'
    '("| 42 aus 25a/25b/25c |", "anhaengen", setze(punkte[2][2])),\n'
    '("| 46 aus 27a |", "anhaengen", setze(punkte[3][2])),\n'
    '("| 48 aus 29b |", "anhaengen", setze(punkte[4][2])),\n'
    '("| 53 aus 02c |", "anhaengen", setze(punkte[5][2])),\n'
    '("| 54 aus 04a |", "ersetzen", setze(punkte[6][3])),\n'
    ']',
    1),
   ('    if prefix == "| 53 aus 02c |":', '    if prefix == "| 54 aus 04a |":', 1),
   ('# Abschnittstabelle neu (alle Zeilen aus den Koepfen) und Zeile 54; Teilgrenzen',
    '# Abschnittstabelle neu (alle Zeilen aus den Koepfen) und Zeile 55; Teilgrenzen',
    1),
   ('        if m.group(1) == "53":\n            zz[k] += "\\n" + tabzeile(54)',
    '        if m.group(1) == "54":\n            zz[k] += "\\n" + tabzeile(55)',
    1),
   ('und neue Zeile 54, je Anker genau 1; Abschnittstabelle 0-54 aus den Koepfen;',
    'und neue Zeile 55, je Anker genau 1; Abschnittstabelle 0-55 aus den Koepfen;',
    1)]),
 ('docs/belege/TB-136/c2_index_pruefen.py',
  '202efa0e810d5f59fb8e16a78730a28cd0d6645a2c0e0975fcd88da2abca14c5',
  'c2_index_pruefen.py',
  '96bf9ee88dd7eacddf6f0767984b2c2418e1a0a3d707f7ab53427eafe67a7a1f',
  [('"""TB-136 C2/C3 Gegenprobe (Vorlage docs/belege/TB-132/c2_index_pruefen.py, dort nach TB-130 und Bauart TB-129): jede Angabe',
    '"""TB-139 C2/C3 Gegenprobe (Vorlage docs/belege/TB-136/c2_index_pruefen.py, dort nach TB-132, TB-130 und Bauart TB-129): jede Angabe',
    1),
   ("die 21 Marken aus 02c in Abschnitt 8, die 15 Marken aus 04a in Abschnitt 9; der Block '### Indexzeilen aus Fable 04a'\n"
    'traegt genau die zwei Zeilen aus C3 des Auftrags (am Commit S0);',
    'die 21 Marken aus 02c in Abschnitt 8, die 15 Marken aus 04a in Abschnitt 9, die 20 Marken aus 07a in Abschnitt 10; der Block\n'
    "'### Indexzeilen aus Fable 07a' traegt genau die drei Zeilen aus C3 des Auftrags (am Commit S0);",
    1),
   ('die Abschnittstabelle nennt 0-54 mit den Zeilen', 'die Abschnittstabelle nennt 0-55 mit den Zeilen', 1),
   ('docs/belege/TB-136/c2_index_pruefen.py <S0> <datum>', 'docs/belege/TB-139/c2_index_pruefen.py <S0> <datum>', 1),
   ('                              ("TB-136", "## 9. Die Marken aus Fable 04a (TB-136)", DATUM, 15)):',
    '                              ("TB-136", "## 9. Die Marken aus Fable 04a (TB-136)", "05.10.2026", 15),\n'
    '                              ("TB-139", "## 10. Die Marken aus Fable 07a (TB-139)", DATUM, 20)):',
    1),
   ('# C3: zwei Zeilen aus dem Auftrag, zeichengleich, im Block unter Abschnitt 9',
    '# C3: drei Zeilen aus dem Auftrag, zeichengleich, im Block unter Abschnitt 10',
    1),
   ('MAC_TB-136_register_fable_04a.md', 'MAC_TB-139_register_fable_07a.md', 1),
   ('auf.split("**C3. Indexzeilen aus Fable 04a (R77 (b) und (c)).**", 1)', 'auf.split("**C3. Indexzeilen aus Fable 07a (R80 (b)).**", 1)', 1),
   ('a8 = abschnitt("## 9. Die Marken aus Fable 04a (TB-136)") if "## 9. Die Marken aus Fable 04a (TB-136)" in I else ""',
    'a8 = abschnitt("## 10. Die Marken aus Fable 07a (TB-139)") if "## 10. Die Marken aus Fable 07a (TB-139)" in I else ""',
    1),
   ('kb = "### Indexzeilen aus Fable 04a\\n\\n"', 'kb = "### Indexzeilen aus Fable 07a\\n\\n"', 1),
   ('ok3 = blk == c3 and I.count("### Indexzeilen aus Fable 04a") == 1', 'ok3 = blk == c3 and I.count("### Indexzeilen aus Fable 07a") == 1', 1),
   ('im Block \'### Indexzeilen aus Fable 04a\' (Abschnitt 9) zeichengleich: %s"',
    'im Block \'### Indexzeilen aus Fable 07a\' (Abschnitt 10) zeichengleich: %s"',
    1),
   ('if gut != len(dateien) or len(dateien) != 55:', 'if gut != len(dateien) or len(dateien) != 56:', 1)]),
 ('docs/belege/TB-136/c3_indexzeilen.py',
  '7efffe11ab868c71d70ea9912fb1de473470efbed4db2888301bcd95676f506d',
  'c3_indexzeilen.py',
  'b913190aa8c922307b92353bfab83c7670ab33229c0b2d6c41da42449c49fb15',
  [('TB-136', 'TB-139', 5),
   ('04a', '07a', 12),
   ('(R77 (b) und (c))', '(R80 (b))', 2),
   ('im neuen Abschnitt 9 von REGISTER_INDEX.md', 'im neuen Abschnitt 10 von REGISTER_INDEX.md', 1),
   ('mit genau den zwei\nZeilen aus C3', 'mit genau den drei\nZeilen aus C3', 1),
   ('nach der Markentabelle von Abschnitt 9,', 'nach der Markentabelle von Abschnitt 10,', 1),
   ('assert len(zeilen) == 2 and', 'assert len(zeilen) == 3 and', 1),
   ('KOPF8 = "## 9. Die Marken', 'KOPF8 = "## 10. Die Marken', 1),
   ('(Soll 0); Abschnitt 9 %dx (Soll 1)', '(Soll 0); Abschnitt 10 %dx (Soll 1)', 1),
   ('Zeilen zeichengleich im Index: %d/2"', 'Zeilen zeichengleich im Index: %d/3"', 1)]),
 ('docs/belege/TB-136/c4_dialog_index.sh',
  '22575b8b884d75da8cf6b744a2b3aff5e10426cf96ce45b2bb0ce45919de6019',
  'c4_dialog_index.sh',
  '472044172c295c3374b4a09a00d1368a62211ccb2322e8d0872a40d1577a3b0d',
  [('# TB-136 C4 - Dialog-Index (Bauart TB-132 C4, dort nach TB-130): Handfelder',
    '# TB-139 C4 - Dialog-Index (Bauart TB-136 C4, dort nach TB-132 und TB-130): Handfelder',
    1),
   ('# dann --pruefen; Zeilen 02c, 04a, Schlusszeile', '# dann --pruefen; Zeilen 04a, 06a, 07a, Schlusszeile', 1),
   ('bash docs/belege/TB-136/c4_dialog_index.sh', 'bash docs/belege/TB-139/c4_dialog_index.sh', 1),
   ('BL=docs/belege/TB-136', 'BL=docs/belege/TB-139', 1),
   ('echo "# TB-136 C4', 'echo "# TB-139 C4', 1),
   ('MAC_TB-136_register_fable_04a.md', 'MAC_TB-139_register_fable_07a.md', 1),
   ('for b in 02c 04a; do', 'for b in 04a 06a 07a; do', 1)]),
 ('docs/belege/TB-136/d2_journal.py',
  'a1eab10656fe3dc09049b11ace12ced36985c33c847684b5d718e035ec4c17e5',
  'd2_journal.py',
  'f0f288bd8b8f9bfc5d5530558d1e9366a19d4e5a66f783f644031a4a16b4f546',
  [('"""TB-136 D2: Journalblock EE vor', '"""TB-139 D2: Journalblock EI vor', 1),
   ("Kennung 'EE' vorher 0,\nletzter Buchstabenblock ED).", "Kennung 'EI' vorher 0,\nletzter Buchstabenblock EH).", 1),
   ('docs/belege/TB-136/d2_journal.py', 'docs/belege/TB-139/d2_journal.py', 1),
   ('open("docs/belege/TB-136/d2_journal_block.md"', 'open("docs/belege/TB-139/d2_journal_block.md"', 1),
   ('"| \'## EE \' vorher:", t.count("\\n## EE "))', '"| \'## EI \' vorher:", t.count("\\n## EI "))', 1),
   ('kennungen[-1] == "ED" and t.count("\\n## EE ") == 0', 'kennungen[-1] == "EH" and t.count("\\n## EI ") == 0', 1)]),
 ('docs/belege/TB-140/j1_einsetzen.py',
  '35c35a3de72a61a7325f4fb8b6c3185ae47cf762f6ecf678c16ffe51c3a604cb',
  'j1_einsetzen.py',
  'e4e80582cf848c2740c832e977ec1c0e8849d2f53c9cedb1320c5b9fcd5cdf4f',
  [('docs/auftraege/MAC_TB-140_verfahrensmessung_voraussetzungen.md', 'docs/auftraege/MAC_TB-139_register_fable_07a.md', 1),
   ('TB-140', 'TB-139', 8),
   ('EH', 'EI', 3)]),
 ('docs/belege/TB-140/j1_vergleich.py',
  'bb2ca6c7822ee87365764dd6e147a524eb0f178b4031a1bebfc35e742c39e641',
  'j1_vergleich.py',
  '51fa7f735fd4f3b3f3ba01501c9b2c4bd5619b6ce3a2114ceb7a7d5fa88fb137',
  [('docs/auftraege/MAC_TB-140_verfahrensmessung_voraussetzungen.md', 'docs/auftraege/MAC_TB-139_register_fable_07a.md', 1),
   ('TB-140', 'TB-139', 5),
   ('--kennung EH', '--kennung EI', 1)])]

fehler = 0
if not PRUEFEN:
    os.makedirs(ZIEL, exist_ok=True)
for vorlage, sha_alt, name, sha_neu, liste in SPEC:
    try:
        if PRUEFEN:
            ist = sha(open(ZIEL + name, encoding="utf-8", newline="").read())
            gut = ist == sha_neu
            print("%s %s %s" % ("ok  " if gut else "FEHL", name, ist))
            fehler += not gut
            continue
        t = open(WURZEL + vorlage, encoding="utf-8", newline="").read()
        assert sha(t) == sha_alt, "sha256 der Vorlage %s weicht ab" % vorlage
        for k, (alt, neu, zahl) in enumerate(liste, 1):
            assert t.count(alt) == zahl, "Ersetzung %d: alter Text %d-mal statt %d-mal" % (k, t.count(alt), zahl)
            t = t.replace(alt, neu)
        assert sha(t) == sha_neu, "sha256 des Ergebnisses weicht ab: %s" % sha(t)
        open(ZIEL + name, "w", encoding="utf-8", newline="").write(t)
        print("ok   %s %s (%d Ersetzungen, Vorlage %s)" % (name, sha_neu, len(liste), vorlage))
    except (AssertionError, OSError) as e:
        print("FEHL %s: %s" % (name, e))
        fehler += 1
print("Skripte: %d, Abweichungen: %d" % (len(SPEC), fehler))
sys.exit(1 if fehler else 0)

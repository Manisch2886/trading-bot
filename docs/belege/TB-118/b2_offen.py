#!/usr/bin/env python3
# TB-118 B2 - Messung fuer das Feld "offen": je Antwort (1) Zahl der Frage-/Messbitte-Muster im Text,
# (2) spaetere Anfragen, die ihren Buchstaben nennen - einmal nach Buchstabenfolge, einmal nach dem Commit,
# mit dem die Datei ins Repo kam (die Buchstaben von Anfragen und Antworten sind getrennte Folgen; beides zusammen
# ist die Messung, die Einordnung ist gelesen). Aufruf aus der Repo-Wurzel, rein lesend.
import glob, re, subprocess
D = 'docs/projektfuehrung/'
def tok(f):
    m = re.search(r'_2026-09-(\d\d)([a-z]?)_', f); return m.group(1) + m.group(2)
def t_add(f):
    o = subprocess.run(['git', 'log', '--diff-filter=A', '--format=%ct', '--', f], capture_output=True, text=True).stdout.split()
    return int(o[-1]) if o else 0
anf = [(tok(q), t_add(q), open(q, encoding='utf-8').read()) for q in glob.glob(D + 'FABLE_ANFRAGE_*.md')]
for a in sorted(glob.glob(D + 'FABLE_ANTWORT_*.md'), key=lambda f: (tok(f)[:2], tok(f)[2:])):
    k, ta, txt = tok(a), t_add(a), open(a, encoding='utf-8').read()
    fr = len(re.findall(r'Messbitte|Messung vorher|Frage zurück|Rückfrage|Frage an (den|dich|euch)|messen\b|Eine Messung', txt))
    pat = (r'FABLE_ANTWORT_2026-09-20_' if k == '20' else r'(?<![0-9A-Za-z.])' + re.escape(k) + r'(?![0-9a-z])')
    nach_bst = sorted(q for q, tq, t in anf if (q[:2], q[2:]) > (k[:2], k[2:]) and re.search(pat, t))
    nach_zeit = sorted(q for q, tq, t in anf if tq > ta and re.search(pat, t))
    print('%-4s Muster %2d | spaetere Anfragen (Buchstabe): %-30s | (Commit-Zeit): %s'
          % (k, fr, ' '.join(nach_bst) or '-', ' '.join(nach_zeit) or '-'))

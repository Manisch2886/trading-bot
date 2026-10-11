import hashlib, os, shutil, sys
P, Z = sys.argv[1], sys.argv[2]
MD5_ALT = "46c6a18024784b86561ec2486cadc863"
NAME = "EROEFFNUNG_STEUERNDER_CHAT.md"
ANKER = '         "PROJEKTSTAND_einfache_sprache.md", "FABLE_DIALOG_INDEX.md", "KANDIDATEN_DURCHGANG_2.md"]  # 27b B2\n'
NEU = ['         "PROJEKTSTAND_einfache_sprache.md", "FABLE_DIALOG_INDEX.md", "KANDIDATEN_DURCHGANG_2.md",\n',
       '         "EROEFFNUNG_STEUERNDER_CHAT.md"]  # 27b B2\n',
       '# EROEFFNUNG_STEUERNDER_CHAT.md: Eroeffnung des steuernden Chats, fester Name, bei jedem Umzug ersetzt (TB-151)\n']
roh = open(P, "rb").read()
assert hashlib.md5(roh).hexdigest() == MD5_ALT, "md5 der Vorfassung %s" % hashlib.md5(roh).hexdigest()
z = roh.decode("ascii").splitlines(True)
assert len(z) == 290, "Zeilen %d" % len(z)
assert z.count(ANKER) == 1, "Anker kommt %d-mal vor" % z.count(ANKER)
assert z.index(ANKER) + 1 == 56, "Anker steht in Z. %d" % (z.index(ANKER) + 1)
assert sum(NAME in x for x in z) == 0, "Name steht schon im Skript"
z[55:56] = NEU
text = "".join(z)
text.encode("ascii")
probe = {"__name__": "tb151_probe"}
exec(compile(text, Z, "exec"), probe)
assert len(probe["STAND"]) == 9 and probe["STAND"][-1] == NAME and probe["STAND"].count(NAME) == 1, "STAND"
tmp = Z + ".tb151.neu"
with open(tmp, "w", encoding="ascii", newline="") as f:
    f.write(text)
shutil.copymode(P, tmp)
os.replace(tmp, Z)
n = open(Z, "rb").read()
print("ablage_soll.py | %d -> %d Zeilen | Anker Z. 56 einmal | 1 Zeile ersetzt durch 3 | STAND %d Namen, letzter %s"
      % (290, len(n.decode("ascii").splitlines()), len(probe["STAND"]), probe["STAND"][-1]))
print("md5 vorher %s | md5 nachher %s | Bytes %d" % (MD5_ALT, hashlib.md5(n).hexdigest(), len(n)))

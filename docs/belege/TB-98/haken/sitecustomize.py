"""TB-98 A1: prozessuebergreifender Lesehaken mit Aufrufstapel (Bauart TB-92
A1b). Ueber PYTHONPATH geladen, gilt damit auch fuer Kindprozesse. Jeder
Prozess oeffnet BEIM START <TB98_PROTOKOLL>/<pid>.tsv (O_EXCL) und schreibt
jede geoeffnete Datei sofort per os.write auf den offenen Deskriptor.

Zeilenformat: modus <TAB> pfad <TAB> stapel
stapel = die innersten Rahmen AUSSERHALB von Standardbibliothek und
site-packages, innen zuerst, als datei:zeile, mit " < " getrennt."""
import os, sys
_ziel = os.environ.get("TB98_PROTOKOLL")
if _ziel:
    _fd = os.open(os.path.join(_ziel, "%d.tsv" % os.getpid()),
                  os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    os.write(_fd, ("#argv\t%s\n" % " ".join(sys.argv)).encode("utf-8"))
    _frame = sys._getframe

    def _stapel(tiefe=6):
        teile = []
        try:
            f = _frame(2)
        except ValueError:          # Aufruf aus dem Interpreter selbst, kein Python-Rahmen
            return ""

        while f is not None and len(teile) < tiefe:
            datei = f.f_code.co_filename
            if ("/lib/python" not in datei and "site-packages" not in datei
                    and not datei.startswith("<") and "sitecustomize" not in datei):
                teile.append("%s:%d" % (datei, f.f_lineno))
            f = f.f_back
        return " < ".join(teile)

    def _haken(ereignis, args, _fd=_fd, _w=os.write):
        if ereignis == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
            m = str(args[1]) if len(args) > 1 else ""
            _w(_fd, ("%s\t%s\t%s\n" % (m, os.fsdecode(args[0]), _stapel()))
               .encode("utf-8", "replace"))
    sys.addaudithook(_haken)

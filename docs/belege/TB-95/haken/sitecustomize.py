"""TB-95 D1: Lesehaken aus TB-92 (docs/belege/TB-92/haken/sitecustomize.py),
ergaenzt um den Aufrufstapel. Ueber PYTHONPATH geladen, gilt damit auch fuer
Kindprozesse. Jeder Prozess oeffnet BEIM START <TB92_PROTOKOLL>/<pid>.tsv und
schreibt jede geoeffnete Datei sofort per os.write auf den offenen Deskriptor
(die Schreibsperre von loaderlauf.py bewacht open/os.open, nicht os.write).
Neu: Fuer Pfade, die TB95_STAPEL_MUSTER enthalten (Standard '_alle_trades'),
folgt jeder Zeile der Aufrufstapel (traceback.extract_stack) als
'#stapel'-Zeilen - Datei:Zeile Funktion, aeusserster Rahmen zuerst."""
import os, sys
_ziel = os.environ.get("TB92_PROTOKOLL")
if _ziel:
    import traceback
    _muster = os.environ.get("TB95_STAPEL_MUSTER", "_alle_trades")
    _fd = os.open(os.path.join(_ziel, "%d.tsv" % os.getpid()),
                  os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    os.write(_fd, ("#argv\t%s\n" % " ".join(sys.argv)).encode("utf-8"))
    def _haken(ereignis, args, _fd=_fd, _w=os.write, _tb=traceback):
        if ereignis == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
            m = str(args[1]) if len(args) > 1 else ""
            p = os.fsdecode(args[0])
            zeilen = ["%s\t%s\n" % (m, p)]
            if _muster in p:
                for r in _tb.extract_stack()[:-1]:
                    zeilen.append("#stapel\t%s:%d\t%s\n" % (r.filename, r.lineno, r.name))
            _w(_fd, "".join(zeilen).encode("utf-8", "replace"))
    sys.addaudithook(_haken)

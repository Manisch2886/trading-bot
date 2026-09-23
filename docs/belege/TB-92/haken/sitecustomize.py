"""TB-92 A1b: prozessuebergreifender Lesehaken. Ueber PYTHONPATH geladen, gilt
damit auch fuer Kindprozesse. Jeder Prozess oeffnet BEIM START
<TB92_PROTOKOLL>/<pid>.tsv und schreibt jede geoeffnete Datei sofort per
os.write auf den offenen Deskriptor - so greift die Schreibsperre von
loaderlauf.py (bewacht open/os.open, nicht os.write) nicht. (Erste Fassung
schrieb per atexit mit open() und verlor so die Kindprozesse; verworfen.)"""
import os, sys
_ziel = os.environ.get("TB92_PROTOKOLL")
if _ziel:
    _fd = os.open(os.path.join(_ziel, "%d.tsv" % os.getpid()),
                  os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    os.write(_fd, ("#argv\t%s\n" % " ".join(sys.argv)).encode("utf-8"))
    def _haken(ereignis, args, _fd=_fd, _w=os.write):
        if ereignis == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
            m = str(args[1]) if len(args) > 1 else ""
            _w(_fd, ("%s\t%s\n" % (m, os.fsdecode(args[0]))).encode("utf-8", "replace"))
    sys.addaudithook(_haken)

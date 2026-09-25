"""TB-104 C5/D1: prozessuebergreifender Haken (Bauart TB-98 haken/sitecustomize.py,
dort unveraendert). Ueber PYTHONPATH geladen, gilt damit auch fuer Kindprozesse.
Jeder Prozess oeffnet BEIM START <TB104_PROTOKOLL>/<pid>.tsv (O_EXCL) und schreibt
sofort per os.write:

  open  <TAB> modus <TAB> pfad <TAB> stapel      jede geoeffnete Datei (Audit "open")
  mkdir <TAB> -     <TAB> pfad <TAB> stapel      jede Verzeichnisanlage (Audit "os.mkdir")

stapel = die innersten Rahmen AUSSERHALB von Standardbibliothek und site-packages,
innen zuerst, als datei:zeile, mit " < " getrennt.

Beim Prozessende (atexit) zusaetzlich <pid>.module.tsv: je geladenes Modul
Name <TAB> Quelldatei. Bytecode aus dem Cache wird auf die Quelldatei
zurueckgefuehrt (importlib.util.source_from_cache); Module ohne Datei
(eingebaut, eingefroren) stehen mit "-". Ein Prozess, der mit os._exit endet,
schreibt diese Liste nicht - das steht dann im Beleg."""
import os, sys
_ziel = os.environ.get("TB104_PROTOKOLL")
if _ziel:
    _pid = os.getpid()
    _fd = os.open(os.path.join(_ziel, "%d.tsv" % _pid),
                  os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    os.write(_fd, ("#argv\t%s\n" % " ".join(sys.argv)).encode("utf-8"))
    _frame = sys._getframe

    def _stapel(tiefe=6):
        teile = []
        try:
            f = _frame(2)
        except ValueError:
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
            _w(_fd, ("open\t%s\t%s\t%s\n" % (m, os.fsdecode(args[0]), _stapel()))
               .encode("utf-8", "replace"))
        elif ereignis == "os.mkdir" and args:
            _w(_fd, ("mkdir\t-\t%s\t%s\n" % (os.fsdecode(args[0]), _stapel()))
               .encode("utf-8", "replace"))
    sys.addaudithook(_haken)

    def _module(_ziel=_ziel, _pid=_pid):
        import importlib.util
        zeilen = []
        for name, modul in sorted(list(sys.modules.items())):
            datei = getattr(modul, "__file__", None)
            if datei and datei.endswith(".pyc"):
                try:
                    datei = importlib.util.source_from_cache(datei)
                except ValueError:
                    pass
            zeilen.append("%s\t%s\n" % (name, datei or "-"))
        with open(os.path.join(_ziel, "%d.module.tsv" % _pid), "w",
                  encoding="utf-8") as f:
            f.writelines(zeilen)
    import atexit
    atexit.register(_module)

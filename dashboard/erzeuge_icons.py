"""
Erzeugt die beiden PWA-Icons (static/icon-192.png, static/icon-512.png)
=========================================================================
    python3 dashboard/erzeuge_icons.py

Die Icons sind mit Absicht KEIN eingecheckter Binaerblob unbekannter
Herkunft, sondern werden hier aus wenigen Zeilen Code erzeugt: ein
dunkles, abgerundetes Quadrat mit einer steigenden Linie und drei
Balken - erkennbar klein auf dem Home-Bildschirm, ohne fremdes
Bildmaterial und ohne zusaetzliche Abhaengigkeit (Pillow ist in diesem
Projekt nicht installiert; die PNG-Kodierung unten ist reine
Standardbibliothek: zlib + struct).

Die erzeugten PNG-Dateien liegen im Repo, damit das Dashboard direkt
lauffaehig ist - dieses Skript dient dazu, sie jederzeit
nachvollziehbar neu erzeugen zu koennen.
"""

import os
import struct
import zlib

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

HINTERGRUND = (20, 23, 28)     # --hintergrund aus style.css
KARTE = (29, 34, 42)           # --karte
GRUEN = (70, 184, 119)         # --gruen
BLAU = (106, 169, 224)         # --akzent


def _png(pixel, breite: int, hoehe: int) -> bytes:
    """Kodiert eine Liste von (r,g,b)-Zeilen als PNG (Filter 0 je Zeile)."""
    roh = b"".join(
        b"\x00" + b"".join(struct.pack("3B", *pixel[y][x]) for x in range(breite))
        for y in range(hoehe)
    )

    def block(typ: bytes, daten: bytes) -> bytes:
        return (struct.pack(">I", len(daten)) + typ + daten
                + struct.pack(">I", zlib.crc32(typ + daten) & 0xFFFFFFFF))

    kopf = struct.pack(">2I5B", breite, hoehe, 8, 2, 0, 0, 0)  # 8 Bit, Truecolor
    return (b"\x89PNG\r\n\x1a\n" + block(b"IHDR", kopf)
            + block(b"IDAT", zlib.compress(roh, 9)) + block(b"IEND", b""))


def _im_kreis(x, y, mx, my, r) -> bool:
    return (x - mx) ** 2 + (y - my) ** 2 <= r * r


def zeichne(groesse: int) -> list:
    e = groesse / 512.0          # Einheit, damit beide Groessen gleich aussehen
    radius = 96 * e              # Eckenrundung
    bild = [[HINTERGRUND for _ in range(groesse)] for _ in range(groesse)]

    # Abgerundetes Quadrat als Kachel-Hintergrund
    for y in range(groesse):
        for x in range(groesse):
            innen = True
            for mx, my in ((radius, radius), (groesse - radius, radius),
                            (radius, groesse - radius), (groesse - radius, groesse - radius)):
                if ((x < radius and y < radius and (mx, my) == (radius, radius)) or
                        (x > groesse - radius and y < radius and (mx, my) == (groesse - radius, radius)) or
                        (x < radius and y > groesse - radius and (mx, my) == (radius, groesse - radius)) or
                        (x > groesse - radius and y > groesse - radius
                         and (mx, my) == (groesse - radius, groesse - radius))):
                    innen = _im_kreis(x, y, mx, my, radius)
            if innen:
                bild[y][x] = KARTE

    # Drei Balken (Volumen), unten
    for i, (links, hoehe) in enumerate(((150, 90), (240, 150), (330, 210))):
        x0, x1 = int(links * e), int((links + 55) * e)
        y0, y1 = int((390 - hoehe) * e), int(390 * e)
        for y in range(y0, y1):
            for x in range(x0, x1):
                if 0 <= x < groesse and 0 <= y < groesse:
                    bild[y][x] = BLAU if i < 2 else GRUEN

    # Steigende Linie darueber
    punkte = [(130, 330), (220, 260), (300, 290), (390, 150)]
    dicke = max(1, int(18 * e))
    for (ax, ay), (bx, by) in zip(punkte, punkte[1:]):
        schritte = int(max(abs(bx - ax), abs(by - ay)) * e) + 1
        for s in range(schritte + 1):
            t = s / schritte
            x = int((ax + (bx - ax) * t) * e)
            y = int((ay + (by - ay) * t) * e)
            for dy in range(-dicke // 2, dicke // 2 + 1):
                for dx in range(-dicke // 2, dicke // 2 + 1):
                    px, py = x + dx, y + dy
                    if 0 <= px < groesse and 0 <= py < groesse:
                        bild[py][px] = GRUEN
    return bild


def main():
    os.makedirs(STATIC_DIR, exist_ok=True)
    for groesse in (192, 512):
        pfad = os.path.join(STATIC_DIR, f"icon-{groesse}.png")
        with open(pfad, "wb") as datei:
            datei.write(_png(zeichne(groesse), groesse, groesse))
        print(f"geschrieben: {pfad} ({os.path.getsize(pfad)} Bytes)")


if __name__ == "__main__":
    main()

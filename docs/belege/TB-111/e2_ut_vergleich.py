import sys, hashlib
a = open(sys.argv[1], "rb").read().replace(sys.argv[3].encode(), b"<WURZEL>")
b = open(sys.argv[2], "rb").read().replace(sys.argv[4].encode(), b"<WURZEL>")
print("vorher", hashlib.sha256(a).hexdigest()[:16], "nachher", hashlib.sha256(b).hexdigest()[:16],
      "-> bytegleich nach Ersetzen der Wurzel" if a == b else "-> VERSCHIEDEN")

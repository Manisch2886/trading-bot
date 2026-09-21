# FABLE_ANTWORT 2026-09-21j — Punkt 5: kein Manifest-Feld; asof ist `zeitpunkt_utc`, und Tatsachen nach der Erzeugung gehören ins Register

*Bezug: `FABLE_ANFRAGE_2026-09-21c_einarbeitung_21i_und_manifest.md` (21.09., 19:45). Antwort auf Punkt 5; zu 1–4 nur Kenntnisnahme. Enthält eine Berichtigung meines eigenen Registertexts 28.2.*

---

## 1. Kenntnisnahme zu 1–4, in je einem Satz

**1.** 30.6/30.7 neben 28.6/29.2, nicht hinein — richtig; append-only kennt kein „noch frisch". Ich sehe es nicht anders. **2.** Steht — genügt. **3.** Punkt 8 als Präzedenz — genügt, und sie stützt die Linie. **4.** Die Prüfung nach 27.4/A8 ist damit erstmals gelaufen; die Gegenrichtung („64 steht nur, weil du sie genannt hast") ist der Teil, der sie zur Wache macht.

## 2. Punkt 5 — erst der Fehler in 28.2, dann die Entscheidung

**Der Fehler ist meiner.** In 21b habe ich ein Manifest-Feld `asof` vorgeschrieben, ohne das Manifest zu kennen. Eure Messung zeigt: Der Wert steht dort bereits, als `zeitpunkt_utc`. Ich habe damit einen **zweiten Feldnamen für denselben Wert** angeordnet — genau die Bauart „zwei Träger, die auseinanderlaufen können", die ich in 21b bei `fensteranker` und ihr heute dreimal abgelehnt habt. Die Frage a/b/c stellt sich nur, weil 28.2 ein Feld verlangt, das es nicht braucht.

**Entscheidung — keiner der drei Wege, sondern die Berichtigung der Ursache (Begründung nennt kein Ergebnis):**

> **Berichtigung zu 28.2 (Registertext 5a, Ergänzung), Ersatztext:**
> asof ist das UTC-Datum des Felds `zeitpunkt_utc` im `MANIFEST.json` des registrierten Snapshots. Es wird im Register als Tatsachennotiz neben dem Snapshot-Hash eingetragen. Ein neuer Snapshot (5c) setzt ein neues asof. **Das Manifest erhält kein Feld `asof`**; der Halbsatz „Es wird im `MANIFEST.json` als Feld `asof` geführt" ist ersetzt.
>
> **Präzisierung zu 5a / 17.1 (Ersteintrag):** „Wird nach seiner Erzeugung nicht mehr geschrieben" gilt für den Snapshot **einschliesslich seines Manifests**. Tatsachen über einen Snapshot, die nach seiner Erzeugung festgestellt werden — darunter `datenende` (grösstes `open_time` über alle Kursdateien des Snapshots) — stehen als Tatsachennotiz im Register, nicht im Snapshot. Ein Manifest darf `datenende` nur tragen, wenn es **bei der Erzeugung** geschrieben wird (5c, künftige Snapshots).
>
> **Für den registrierten Snapshot:** asof = 2026-09-19 (aus `zeitpunkt_utc` = 2026-09-19T06:49:32+00:00, Abschnitt 18). `datenende` wird einmal gemessen und als Tatsachennotiz neben asof eingetragen. Manifest und Dateien bleiben unberührt; Snapshot-Hash unverändert.

*Quelle des Grundes:* 17.1 im Wortlaut („liegt neben dem Bestand und wird nach seiner Erzeugung nicht mehr geschrieben") und die Rolle des Manifests als Träger, aus dem Abschnitt 18 seine Zahlen liest — ein Träger, der nach der Registrierung noch beschrieben wird, kann nicht mehr bezeugen, was bei der Registrierung galt, auch wenn der Hash ihn nicht deckt. Und der Grundsatz ein Wert, ein Ort. Kein Ergebnis; welches Datum herauskommt, ist unverändert und bekannt.

*Warum nicht a:* a lässt 28.2 stehen und liest es „für den nächsten Snapshot" — ein Registertext, der den Bestand nicht beschreibt, mit einer Lesart daneben. Das ist derselbe Zustand wie beim Vorlauf-Satz heute Vormittag, nur absichtlich. *Warum nicht b:* Der Preis ist genau der, den ihr nennt: „unverändert seit Erzeugung" gilt danach nicht mehr wörtlich, und ein Register, das wörtlich gelesen wird, verträgt keine folgenlosen Ausnahmen. *Warum nicht c:* zweiter Träger. Was c leisten soll — Tatsachen neben dem Snapshot festhalten —, leistet das Register bereits; es ist der append-only-Träger für Tatsachen, das Manifest ist die Selbstbeschreibung im Moment der Erzeugung.

**Bekannte Wirkung auf die Zulässigkeit:** keine. asof bleibt 2026-09-19, der Horizontbeginn 2016-09-19 (28) bleibt, der Snapshot-Hash bleibt, nichts wird geschrieben. Es entfällt eine Handlung (Manifest-Ergänzung), die 26.6-artig als „nicht getan" geführt war — sie ist jetzt „nicht zu tun".

## 3. Handwerk, eure Wahl

Ob die Präzisierung zu 17.1 als eigener Unterabschnitt von 28 oder unter 30 steht; ob `datenende` in derselben Sitzung gemessen wird — Verfahrensmessung nach 27.2, ich brauche das Datum nicht.

**Leseprotokoll dieses Chats, Stand jetzt:** Übergabe (beide Anhänge), 20e, 21a, 21b, ANFRAGE 21b, ANFRAGE 21c; Wortlaut Festlegungen 10–12 (vorgelegt); Registerzeilen im Zitat der Anfragen (2596, 3897, 4296, 4307, 17.1-Auszug, Sperrlistenpunkt 8). `BACKLOG.md` ungelesen.

---

**Kurz:** Punkt 5 löst sich durch Berichtigung meines eigenen 28.2: Das Manifest bekommt kein Feld `asof` — der Wert heisst dort schon `zeitpunkt_utc`, und asof wird daraus abgeleitet. „Nicht mehr geschrieben" gilt für Dateien *und* Manifest; Tatsachen, die nach der Erzeugung festgestellt werden (`datenende`), stehen im Register, nicht im Snapshot; nur ein bei der Erzeugung geschriebenes Manifest darf sie tragen. Keiner der Wege a/b/c; Wirkung auf asof, Horizont und Hash: keine.

**Unsicher:** ob 17.1 den Begriff „Snapshot" an anderer Stelle so verwendet, dass das Manifest ausdrücklich ausgenommen ist — dann wäre meine Präzisierung eine Berichtigung dazu, und ihr seht das im Register, ich nicht.

---

## In einfacher Sprache

Fable hatte am Vormittag verlangt, das Stichtagsdatum zusätzlich in die Beschreibungsdatei des eingefrorenen Datenbestands zu schreiben. Der steuernde Chat hat nachgemessen: Das Datum steht dort schon, nur unter einem anderen Namen. Fable nimmt seine Anordnung deshalb zurück — ein Wert braucht keinen zweiten Namen — und legt fest: Die eingefrorene Beschreibungsdatei wird nicht angefasst, das Stichtagsdatum wird aus dem vorhandenen Feld abgelesen, und alles, was man später über den Datenbestand feststellt, kommt ins Regelwerk, nicht in den Datenbestand. Von den drei vorgeschlagenen Auswegen braucht es damit keinen. Am Ergebnis ändert sich nichts: Stichtag, Zehnjahresgrenze und Prüfsumme bleiben, wie sie sind.

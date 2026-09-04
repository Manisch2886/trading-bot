"""
Aktuell live genutzte Parameter - Turtle Soup (False-Breakout-Reversal, Aktien)
================================================================================================
Siehe elliott_wave/live_params.py fuer die Erklaerung des Zwecks dieser Datei.

Historie:
- 2026-09-04: Erste Live-Uebernahme nach vollstaendiger Validierung
  (Backtest -> Walk-Forward -> Equity-Simulation -> Buy-and-Hold ->
  Abgrenzung zu Volatility Breakout -> Kapitalmanagement-Tuning,
  siehe PROTOTYPE_FINDINGS.md Abschnitt 8). Donchian-Lookback 10, KEIN
  Stop-Loss (musterspezifischer "structural"-Stop empirisch klar die
  SCHLECHTESTE Variante bei Aktien, Abschnitt 2 - "kein Stop" verlaesst
  sich allein auf den Zeit-Exit), 10-Tage-Zeit-Exit als validierte
  Basiskonfiguration uebernommen. 2% Allokation / Limit unbegrenzt aus der
  Kapitalmanagement-Nachpruefung uebernommen (Abschnitt 8c) statt des
  urspruenglichen Start-Limits 8/10% - dominiert die Basiskonfiguration auf
  fast jeder Dimension: hoehere Gesamtzeitraum-Rendite bei GLEICHZEITIG
  niedrigerem Max Drawdown, UND eine deutlich verbesserte 2022-
  Baerenmarkt-Performance.

  WICHTIG - MAX_CONCURRENT_POSITIONS = None (unbegrenzt), Begruendung
  (siehe PROTOTYPE_FINDINGS.md Abschnitt 8b/8c): bei 2% Allokation pro
  Trade saettigt die Kapitalbindung rechnerisch bei ca. 50 gleichzeitig
  offenen Positionen (50 x 2% = 100% des Kapitals) - ein explizites
  Positionslimit ist bei dieser kleinen Positionsgroesse kein zusaetzlicher
  Risikohebel mehr, sondern wuerde nur unnoetig Signale blockieren (wie bei
  10% Allokation empirisch belegt, wo Limit 15/20/unbegrenzt bereits
  IDENTISCHE Ergebnisse lieferten). forward_test.py und die Kapitalpruefung
  sind defensiv gegen None abgesichert (Praezedenzfall: TypeError-Bug beim
  Elliott-Wave-Aktien-Bot) - hier ist das kein reiner Vorsichtsfall wie bei
  anderen Bots, sondern der tatsaechliche Live-Wert, siehe
  experiment_max_concurrent_none_sandbox_test.py fuer den gezielten Test
  dieses Pfads mit vielen gleichzeitigen synthetischen Signalen.

  WICHTIG - bekannte 2020-Schwaeche (siehe PROTOTYPE_FINDINGS.md Abschnitt
  6c/8c): Turtle Soup erleidet in einem echten, schnellen Crash (COVID
  2020) seinen Allzeit-schlechtesten Drawdown (-32,22% Basis, -29,91% neue
  Konfiguration - durch das Kapitalmanagement-Tuning NUR marginal
  gemildert, strukturell unveraendert), waehrend Volatility Breakout davon
  kaum betroffen ist. Grund: in einem echten Crash ist ein Kursrueckgang
  unter ein N-Tage-Tief meist KEIN Fehlausbruch, sondern der Beginn einer
  echten Abwaertsbewegung - Turtle Soups "kaufe die Rueckkehr ueber das
  gebrochene Tief"-Logik kauft hier systematisch in ein fallendes Messer.
  Falls eine kuenftige Ueberpruefung in einer aehnlichen Marktphase eine
  ungewoehnlich schwache Performance feststellt, ist das KEINE neue,
  unerwartete Verschlechterung, sondern das bereits bekannte, dokumentierte
  Risiko dieser Strategie - nicht ohne erneute Pruefung als Bug
  missverstehen.
"""

DONCHIAN_PERIOD = 10
STOP_MODE = None  # "kein Stop" - beste validierte Kombination (siehe Historie oben)
MAX_HOLD_DAYS = 10
ALLOCATION_PCT = 2           # in Prozent - NUR zur Dokumentation, siehe
                              # rsi2_mean_reversion/live_params.py fuer die
                              # Begruendung (forward_test.py trackt kein Kapital)
MAX_CONCURRENT_POSITIONS = None  # unbegrenzt - siehe Historie oben, TATSAECHLICHER Live-Wert

LAST_UPDATED = "2026-09-04"

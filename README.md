# Produktdaten und Protokollauswertung

Zwei kleine, lokal ausführbare Lernprojekte für Anwendungsentwicklung. Beide verarbeiten ausschließlich mitgelieferte, frei erfundene Beispieldaten und benötigen nur die jeweilige Standardbibliothek.

| Projekt | Fragestellung | Technik |
| --- | --- | --- |
| [Produktdaten vor dem Import prüfen](produktdaten/) | Welche Artikel brauchen eine Korrektur, bevor sie in den Shop übernommen werden? | Python 3, CSV, JSON, unittest |
| [Anmeldeereignisse zusammenfassen](auditbericht/) | Wie viele Anmeldungen waren je Dienst und UTC-Tag erfolgreich oder fehlerhaft? | Java 17+, TSV, Zeitstempel, automatisierte Prüffälle |

## Ausprobieren

Im Hauptverzeichnis des entpackten Projekts eine Konsole öffnen. Unter Windows kann für Python auch `py` verwendet werden.

```text
python produktdaten/katalogcheck.py produktdaten/beispiel.csv
java auditbericht/AuditReport.java auditbericht/beispiel.tsv
```

Der erste Aufruf meldet zwei fehlerhafte Datensätze unter vier Artikeln und setzt dafür absichtlich Exitcode 1. Beim zweiten ergibt sich für das Portal am 1. November ein Erfolg und ein Fehlversuch. Ein Zeitstempel im Beispiel enthält einen Zeitzonenversatz. Der Bericht zählt ihn zum UTC-Tag.

## Woran sich die Ergebnisse prüfen lassen

Sieben Python-Tests und sieben Java-Prüffälle decken unter anderem doppelte Artikelnummern, ungültige Preise und den UTC-Tageswechsel ab. Nach jeder Änderung auf `main` führt GitHub Actions beide Testsuiten aus. Die einzelnen Prüfschritte und ihr Ergebnis stehen im [Testprotokoll](https://github.com/canerconnect/produktdaten-und-auditberichte/actions/workflows/tests.yml).

## Entstehung und Lernstand

Die erste Version dieser Lernvorlagen wurde mit KI-Unterstützung erstellt. Sie bildet den Ausgangspunkt für eigene Änderungen. Die mitgelieferten Tests zeigen, wie das beschriebene Verhalten überprüft werden kann. Eigene Erweiterungen lassen sich als einzelne Commits mit neuen Tests dokumentieren.

# Tagesbericht aus Anmeldeereignissen

Ein lokaler Beispiel-Log enthält Zeitstempel, Dienstkennung und Ergebnis. Der Tagesbericht zählt Erfolge und Fehlversuche getrennt. Er enthält weder Benutzernamen noch IP-Adressen. Die Anzahl der Fehlversuche allein lässt keine Aussage über deren Ursache zu.

## Start und Tests mit JDK 17 oder neuer

Im Hauptverzeichnis des Repositorys ausführen.

```text
java auditbericht/AuditReport.java auditbericht/beispiel.tsv
javac -encoding UTF-8 -d build auditbericht/AuditReport.java auditbericht/AuditReportTest.java
java -cp build AuditReportTest
```

Die Eingabe ist eine UTF-8-Datei mit Tabulatoren. Die Kopfzeile muss die drei Felder `zeitpunkt`, `dienst` und `ergebnis` in dieser Reihenfolge enthalten. Die Dienstkennung besteht aus Buchstaben des englischen Alphabets, Ziffern, Unterstrichen oder Bindestrichen. Gültige Ereignisse heißen `OK` und `FEHLER`. Der Zeitstempel enthält UTC oder einen expliziten UTC-Versatz. Eine ungültige Zeile bricht die Auswertung mit Exitcode 2 ab. Eine reine Kopfzeile ergibt einen leeren Bericht mit Kopfzeile.

## Erwartetes Ergebnis

| UTC-Tag | Dienst | Erfolge | Fehlversuche |
| --- | --- | ---: | ---: |
| 2026-11-01 | portal | 1 | 1 |
| 2026-11-02 | katalog | 1 | 1 |
| 2026-11-02 | portal | 1 | 0 |

Das Ereignis um `2026-11-02T01:05:00+02:00` fällt auf den vorherigen UTC-Tag. Das Programm sortiert nach Datum und Dienst, unabhängig von der Reihenfolge der Eingabe. Es verbindet sich mit keinem Netzwerk.

**Zum Weiterentwickeln.** Ergänze eine Spalte mit der gesamten Ereigniszahl je Dienst und Tag. Lege den erwarteten Wert zuerst in einem Test fest. Erkläre danach, was bei einem leeren Bericht passiert.

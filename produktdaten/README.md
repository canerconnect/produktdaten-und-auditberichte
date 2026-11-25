# Produktkatalog vor dem Import prüfen

Eine CSV-Datei enthält Artikelnummer, Name, Preis und Lagerbestand. Das Programm nennt im JSON-Bericht die Nummer jedes fehlerhaften Datensatzes und die betroffenen Regeln. Der erste Artikel nach der Kopfzeile ist Datensatz 1. Die Datei wird ausschließlich gelesen.

## Start und Test

Im Hauptverzeichnis des Repositorys ausführen.

```text
python produktdaten/katalogcheck.py produktdaten/beispiel.csv
python produktdaten/katalogcheck.py produktdaten/gueltig.csv
python -m unittest discover -s produktdaten -p "test_*.py" -v
```

Die Eingabe verwendet UTF-8, optional mit BOM, und ein Semikolon als Trennzeichen. Überschriften müssen genau einmal vorkommen. Ihre Reihenfolge darf wechseln. Ein in Anführungszeichen gesetztes Feld darf ein Semikolon enthalten.

| Feld | Regel |
| --- | --- |
| artikelnummer | Pflichtwert. Nach Entfernen äußerer Leerzeichen und unabhängig von Groß- und Kleinschreibung eindeutig. Weitere Vorkommen gelten als Duplikat. |
| name | Pflichtwert nach Entfernen äußerer Leerzeichen. |
| preis_eur | Nichtnegativer Betrag mit Dezimalkomma und genau zwei Nachkommastellen, z. B. 6,90. |
| bestand | Nichtnegative ganze Zahl aus Ziffern. |

Die Beispieldatei enthält ein Duplikat im dritten Datensatz. Der vierte enthält einen leeren Namen, einen Dezimalpunkt und einen negativen Bestand. Erwartet werden insgesamt vier Artikel, davon zwei mit Fehlern. Die Datei `gueltig.csv` zeigt eine korrigierte Fassung.

Exitcode 0 steht für einen gültigen Katalog, 1 für fehlerhafte Datensätze und 2 für eine unlesbare oder strukturell unbrauchbare Datei. Eine unpassende Spaltenzahl in einer einzelnen Zeile wird als Datenfehler gemeldet.

**Zum Weiterentwickeln.** Ergänze eine Spalte `waehrung`. Definiere zulässige Werte, schreibe zuerst einen Test und ergänze anschließend die Prüfung. Beschreibe im Commit die fachliche Entscheidung.

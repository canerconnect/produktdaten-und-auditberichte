"""Prüft einen Produktkatalog vor dem Import. Benötigt nur die Python-Standardbibliothek."""

import argparse
import csv
import json
import re
import sys
from pathlib import Path


SPALTEN = ("artikelnummer", "name", "preis_eur", "bestand")
PREIS = re.compile(r"[0-9]+,[0-9]{2}")
BESTAND = re.compile(r"[0-9]+")


def pruefe_katalog(datei):
    zeilen = csv.reader(datei, delimiter=";", strict=True)
    kopf = next(zeilen, None)
    if kopf is None or sorted(kopf) != sorted(SPALTEN):
        raise ValueError("Erwartete Spalten (je einmal): " + ", ".join(SPALTEN))

    gesehen = set()
    hinweise = []
    anzahl = 0
    for werte in zeilen:
        anzahl += 1
        if len(werte) != len(kopf):
            hinweise.append({"datensatz": anzahl, "regeln": ["spaltenzahl"]})
            continue
        artikel = dict(zip(kopf, (wert.strip() for wert in werte)))
        nummer = artikel["artikelnummer"].casefold()
        regeln = []
        if not nummer:
            regeln.append("artikelnummer_fehlt")
        elif nummer in gesehen:
            regeln.append("artikelnummer_doppelt")
        if nummer:
            gesehen.add(nummer)
        if not artikel["name"]:
            regeln.append("name_fehlt")
        if not PREIS.fullmatch(artikel["preis_eur"]):
            regeln.append("preisformat")
        if not BESTAND.fullmatch(artikel["bestand"]):
            regeln.append("bestand_ungueltig")
        if regeln:
            hinweise.append({"datensatz": anzahl, "regeln": regeln})
    if not anzahl:
        raise ValueError("Die Datei enthält nur eine Kopfzeile.")
    return {"datensaetze": anzahl, "fehlerhafte_datensaetze": len(hinweise), "hinweise": hinweise}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("datei", type=Path, help="CSV-Datei, UTF-8, Trennzeichen Semikolon")
    args = parser.parse_args(argv)
    try:
        with args.datei.open(encoding="utf-8-sig", newline="") as datei:
            bericht = pruefe_katalog(datei)
    except (OSError, UnicodeError, ValueError, csv.Error) as fehler:
        print(f"Datei kann nicht geprüft werden: {fehler}", file=sys.stderr)
        return 2
    print(json.dumps(bericht, ensure_ascii=False, indent=2))
    return 1 if bericht["hinweise"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

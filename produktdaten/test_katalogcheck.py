import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

from katalogcheck import main, pruefe_katalog


KOPF = "artikelnummer;name;preis_eur;bestand\n"


class KatalogTest(unittest.TestCase):
    def pruefe(self, daten):
        return pruefe_katalog(io.StringIO(KOPF + daten))

    def test_gueltig_und_zitiertes_semikolon(self):
        bericht = self.pruefe('A1;"Heft; liniert";0,00;0\n')
        self.assertEqual(bericht, {"datensaetze": 1, "fehlerhafte_datensaetze": 0, "hinweise": []})

    def test_doppelte_nummer_wird_normalisiert(self):
        bericht = self.pruefe("a1;Stift;1,50;3\n A1 ;Mappe;2,00;5\n")
        self.assertEqual(bericht["hinweise"], [{"datensatz": 2, "regeln": ["artikelnummer_doppelt"]}])

    def test_mehrere_fehler_in_einer_zeile(self):
        bericht = self.pruefe("; ;NaN;-3\n")
        self.assertEqual(bericht["fehlerhafte_datensaetze"], 1)
        self.assertEqual(bericht["hinweise"][0]["regeln"],
                         ["artikelnummer_fehlt", "name_fehlt", "preisformat", "bestand_ungueltig"])

    def test_zeile_mit_falscher_breite(self):
        self.assertEqual(self.pruefe("A1;Zwei Werte\n")["hinweise"][0]["regeln"], ["spaltenzahl"])

    def test_kopf_muss_jede_spalte_einmal_enthalten(self):
        for text in ["", KOPF, "name;name;preis_eur;bestand\n"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                pruefe_katalog(io.StringIO(text))

    def test_spaltenreihenfolge_ist_flexibel(self):
        bericht = pruefe_katalog(io.StringIO("name;bestand;artikelnummer;preis_eur\nMaus;4;Z;8,25\n"))
        self.assertEqual(bericht["fehlerhafte_datensaetze"], 0)

    def test_statistik_zaehlt_jede_betroffene_regel(self):
        with TemporaryDirectory() as temp:
            pfad = Path(temp, "artikel.csv")
            pfad.write_text(KOPF + "A;;2.00;1\nA;;3,00;0\n", encoding="utf-8")
            with redirect_stdout(io.StringIO()) as ausgabe:
                self.assertEqual(main([str(pfad), "--statistik"]), 1)
            bericht = json.loads(ausgabe.getvalue())
            self.assertEqual(bericht["fehlerhafte_datensaetze"], 2)
            self.assertEqual(bericht["fehler_pro_regel"], {
                "artikelnummer_doppelt": 1, "name_fehlt": 2, "preisformat": 1
            })

    def test_statistik_ist_optional_und_gueltige_daten_ergeben_leere_zaehlung(self):
        with TemporaryDirectory() as temp:
            pfad = Path(temp, "artikel.csv")
            pfad.write_text(KOPF + "A;Mappe;2,00;1\n", encoding="utf-8")
            with redirect_stdout(io.StringIO()) as ausgabe:
                self.assertEqual(main([str(pfad)]), 0)
            self.assertNotIn("fehler_pro_regel", json.loads(ausgabe.getvalue()))
            with redirect_stdout(io.StringIO()) as ausgabe:
                self.assertEqual(main(["--statistik", str(pfad)]), 0)
            self.assertEqual(json.loads(ausgabe.getvalue())["fehler_pro_regel"], {})

    def test_dateiaufruf_bom_und_exitcodes(self):
        with TemporaryDirectory() as temp, redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            pfad = Path(temp, "katalog.csv")
            self.assertEqual(main([str(pfad)]), 2)
            pfad.write_text(KOPF + "A1;Mappe;1,50;3\n", encoding="utf-8-sig")
            self.assertEqual(main([str(pfad)]), 0)
            pfad.write_text(KOPF + "A1;Mappe;1.50;3\n", encoding="utf-8")
            self.assertEqual(main([str(pfad)]), 1)


if __name__ == "__main__":
    unittest.main()

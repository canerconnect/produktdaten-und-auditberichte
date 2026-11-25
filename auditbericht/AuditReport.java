import java.io.BufferedReader;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneOffset;
import java.time.format.DateTimeParseException;
import java.util.Map;
import java.util.TreeMap;

/** Fasst eine lokale TSV-Datei nach UTC-Tag und Dienst zusammen. Java 17+. */
public class AuditReport {
    private static final String HEADER = "zeitpunkt\tdienst\tergebnis";

    record Tageswert(LocalDate tag, String dienst) implements Comparable<Tageswert> {
        public int compareTo(Tageswert anderer) {
            int vergleich = tag.compareTo(anderer.tag);
            return vergleich != 0 ? vergleich : dienst.compareTo(anderer.dienst);
        }
    }

    static class Zaehler {
        int erfolge;
        int fehler;
    }

    static Map<Tageswert, Zaehler> zusammenfassen(BufferedReader reader) throws IOException {
        String kopf = reader.readLine();
        if (kopf == null || !HEADER.equals(kopf.replaceFirst("^\uFEFF", ""))) {
            throw new IllegalArgumentException("Erwarteter TSV-Kopf: zeitpunkt, dienst, ergebnis.");
        }
        Map<Tageswert, Zaehler> werte = new TreeMap<>();
        int zeilennummer = 1;
        String zeile;
        while ((zeile = reader.readLine()) != null) {
            zeilennummer++;
            String[] felder = zeile.split("\t", -1);
            if (felder.length != 3 || !felder[1].matches("[A-Za-z0-9_-]+")) {
                throw new IllegalArgumentException("Ungültige Spalten oder Dienstkennung in Zeile " + zeilennummer);
            }
            Instant zeit;
            try {
                zeit = Instant.parse(felder[0]);
            } catch (DateTimeParseException fehler) {
                throw new IllegalArgumentException("Ungültiger Zeitstempel in Zeile " + zeilennummer);
            }
            Tageswert gruppe = new Tageswert(zeit.atZone(ZoneOffset.UTC).toLocalDate(), felder[1]);
            Zaehler zaehler = werte.computeIfAbsent(gruppe, key -> new Zaehler());
            switch (felder[2]) {
                case "OK" -> zaehler.erfolge++;
                case "FEHLER" -> zaehler.fehler++;
                default -> throw new IllegalArgumentException("Unbekanntes Ergebnis in Zeile " + zeilennummer);
            }
        }
        return werte;
    }

    static void ausgeben(Map<Tageswert, Zaehler> werte, PrintStream ziel) {
        ziel.println("utc_tag\tdienst\terfolge\tfehlversuche");
        werte.forEach((gruppe, anzahl) ->
                ziel.printf("%s\t%s\t%d\t%d%n", gruppe.tag(), gruppe.dienst(), anzahl.erfolge, anzahl.fehler));
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("Aufruf: java AuditReport.java <ereignisse.tsv>");
            System.exit(2);
        }
        try (var reader = Files.newBufferedReader(Path.of(args[0]), StandardCharsets.UTF_8)) {
            ausgeben(zusammenfassen(reader), System.out);
        } catch (IOException | IllegalArgumentException fehler) {
            System.err.println(fehler.getMessage());
            System.exit(2);
        }
    }
}

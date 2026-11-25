import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.io.StringReader;
import java.nio.charset.StandardCharsets;

public class AuditReportTest {
    private static final String KOPF = "zeitpunkt\tdienst\tergebnis\n";

    private static String auswertung(String tsv) throws Exception {
        var daten = AuditReport.zusammenfassen(new BufferedReader(new StringReader(tsv)));
        var puffer = new ByteArrayOutputStream();
        try (var out = new PrintStream(puffer, true, StandardCharsets.UTF_8)) {
            AuditReport.ausgeben(daten, out);
        }
        return puffer.toString(StandardCharsets.UTF_8).replace("\r\n", "\n");
    }

    private static void erwarte(String soll, String ist) {
        if (!soll.equals(ist)) throw new AssertionError("Erwartet: " + soll + " Erhalten: " + ist);
    }

    private static void ungueltig(String tsv) throws Exception {
        try {
            auswertung(tsv);
            throw new AssertionError("Fehler erwartet");
        } catch (IllegalArgumentException erwartet) {
            // Fehlermeldung wird vom Aufrufer behandelt.
        }
    }

    public static void main(String[] args) throws Exception {
        String ausgabekopf = "utc_tag\tdienst\terfolge\tfehlversuche\n";
        erwarte(ausgabekopf, auswertung(KOPF));
        String tsv = "\uFEFF" + KOPF
                + "2026-01-02T00:05:00Z\tshop\tOK\n"
                + "2026-01-02T01:00:00+02:00\tshop\tFEHLER\n"
                + "2026-01-01T23:00:00Z\tshop\tOK\n"
                + "2026-01-01T21:00:00Z\tarchiv\tFEHLER\n";
        erwarte(ausgabekopf + "2026-01-01\tarchiv\t0\t1\n2026-01-01\tshop\t1\t1\n"
                + "2026-01-02\tshop\t1\t0\n", auswertung(tsv));
        ungueltig("falscher Kopf\n");
        ungueltig(KOPF + "gestern\tshop\tOK\n");
        ungueltig(KOPF + "2026-01-02T00:05:00Z\tshop\tUNBEKANNT\n");
        ungueltig(KOPF + "2026-01-02T00:05:00Z\t\tOK\n");
        ungueltig(KOPF + "2026-01-02T00:05:00Z\tshop\tOK\textra\n");
        System.out.println("Alle 7 Java-Prüffälle erfolgreich.");
    }
}

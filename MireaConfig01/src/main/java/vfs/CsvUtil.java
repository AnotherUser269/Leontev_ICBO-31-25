package vfs;

import java.util.ArrayList;
import java.util.List;

/** RFC 4180 reader/writer. */
final class CsvUtil {
    private CsvUtil() {}

    static List<List<String>> parse(String text) {
        List<List<String>> rows = new ArrayList<>();
        List<String> row = new ArrayList<>();
        StringBuilder f = new StringBuilder();
        boolean inQuotes = false;
        int i = 0, n = text.length();

        while (i < n) {
            char ch = text.charAt(i);
            if (inQuotes) {
                if (ch == '"') {
                    if (i + 1 < n && text.charAt(i + 1) == '"') { f.append('"'); i += 2; }
                    else { inQuotes = false; i++; }
                } else { f.append(ch); i++; }
            } else {
                if (ch == '"' && f.isEmpty()) { inQuotes = true; i++; }
                else if (ch == ',') { row.add(f.toString()); f.setLength(0); i++; }
                else if (ch == '\n' || ch == '\r') {
                    row.add(f.toString()); f.setLength(0);
                    rows.add(row); row = new ArrayList<>(); i++;
                    if(ch == '\r' && i < n && text.charAt(i) == '\n') i++;
                } else { f.append(ch); i++; }
            }
        }
        if (!f.isEmpty() || !row.isEmpty()) {
            row.add(f.toString());
            rows.add(row);
        }
        return rows;
    }

    static String format(List<List<String>> rows) {
        StringBuilder sb = new StringBuilder();
        for (List<String> row : rows) {
            for (int i = 0; i < row.size(); i++) {
                if (i > 0) sb.append(',');
                sb.append(escape(row.get(i)));
            }
            sb.append('\n');
        }
        return sb.toString();
    }

    private static String escape(String v) {
        if (v.indexOf(',') >= 0 || v.indexOf('"') >= 0
                || v.indexOf('\n') >= 0 || v.indexOf('\r') >= 0) {
            return "\"" + v.replace("\"", "\"\"") + "\"";
        }
        return v;
    }
}
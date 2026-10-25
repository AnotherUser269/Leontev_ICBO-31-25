package vfs;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;

public class VFS {
    private final String name;
    private final Path sourcePath;
    private final LinkedHashMap<String, VfsNode> nodes = new LinkedHashMap<>();

    public VFS(String name, Path sourcePath) {
        this.name = Objects.requireNonNull(name);
        this.sourcePath = Objects.requireNonNull(sourcePath);
    }

    public String getName() { return name; }
    public int size() { return nodes.size(); }

    public void load() throws IOException {
        String text = Files.readString(sourcePath, StandardCharsets.UTF_8);
        List<List<String>> rows = CsvUtil.parse(text);
        if (rows.isEmpty()) throw new IOException("empty CSV");

        List<String> header = rows.get(0);
        if (header.size() < 3
                || !"path".equalsIgnoreCase(header.get(0).trim())
                || !"type".equalsIgnoreCase(header.get(1).trim())) {
            throw new IOException("bad header, expected: path,type,content_base64");
        }

        LinkedHashMap<String, VfsNode> loaded = new LinkedHashMap<>();

        for (int i = 1; i < rows.size(); i++) {
            List<String> r = rows.get(i);
            if (r.isEmpty() || (r.size() == 1 && r.get(0).isBlank())) continue;
            if (r.size() < 3) throw new IOException("row " + (i + 1) + ": expected 3 columns");

            String path = normalize(r.get(0));
            VfsNode.Type type = parseType(r.get(1), i + 1);

            byte[] content = null;
            if (type == VfsNode.Type.FILE) {
                String b64 = r.get(2).trim();
                try {
                    content = b64.isEmpty() ? new byte[0] : Base64.getDecoder().decode(b64);
                } catch (IllegalArgumentException e) {
                    throw new IOException("row " + (i + 1) + ": bad base64");
                }
            }

            if (loaded.containsKey(path))
                throw new IOException("row " + (i + 1) + ": duplicate path " + path);

            loaded.put(path, new VfsNode(path, type, content));
        }

        System.out.println("[DEBUG] Contents of vfs: " + loaded.keySet());
        validate(loaded);

        this.nodes.clear();
        this.nodes.putAll(loaded);
    }

    private static void validate(Map<String, VfsNode> m) throws IOException {
        if (!m.containsKey("/")) throw new IOException("missing root '/'");
        for (VfsNode n : m.values()) {
            if ("/".equals(n.path())) continue;
            String parent = parentOf(n.path());
            VfsNode p = m.get(parent);
            if (p == null) throw new IOException("missing parent '" + parent + "' for " + n.path());
            if (p.isFile()) throw new IOException("parent '" + parent + "' is a FILE");
        }
    }

    public void saveState(Path dest) throws IOException {
        List<List<String>> rows = new ArrayList<>();
        rows.add(List.of("path", "type", "content_base64"));

        for (VfsNode n : nodes.values()) {
            String content = n.isFile()
                    ? Base64.getEncoder().encodeToString(n.content())
                    : "";
            String type = n.isDirectory() ? "dir" : "file";
            rows.add(List.of(n.path(), type, content));
        }

        Files.writeString(dest, CsvUtil.format(rows), StandardCharsets.UTF_8);
    }

    private static String normalize(String p) {
        if (p == null || p.isBlank()) return "/";
        String s = p.trim();
        if (!s.startsWith("/")) s = "/" + s;
        while (s.length() > 1 && s.endsWith("/")) s = s.substring(0, s.length() - 1);
        return s;
    }

    private static String parentOf(String path) {
        if ("/".equals(path)) return null;
        int i = path.lastIndexOf('/');
        return i <= 0 ? "/" : path.substring(0, i);
    }

    private static VfsNode.Type parseType(String s, int row) throws IOException {
        return switch (s.trim().toLowerCase()) {
            case "dir", "directory", "d" -> VfsNode.Type.DIRECTORY;
            case "file", "f"             -> VfsNode.Type.FILE;
            default -> throw new IOException("row " + row + ": unknown type '" + s + "'");
        };
    }
}
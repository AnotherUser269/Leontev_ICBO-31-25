package vfs;

public record VfsNode(String path, vfs.VfsNode.Type type, byte[] content) {
    public enum Type {DIRECTORY, FILE}

    public boolean isDirectory() {
        return type == Type.DIRECTORY;
    }

    public boolean isFile() {
        return type == Type.FILE;
    }
}
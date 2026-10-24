package org.example;

public class VFS {
    private final String name;
    private final String vfsFilePath;

    public VFS(String name, String vfsFilePath) {
        this.name = name;
        this.vfsFilePath = vfsFilePath;
    }

    public String getName() {
        return name;
    }

    public String getVfsFilePath() {
        return vfsFilePath;
    }
}

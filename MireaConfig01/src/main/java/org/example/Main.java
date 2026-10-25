package org.example;

import org.example.parser.CommandExecutor;
import org.example.parser.CommandParser;
import vfs.VFS;

import java.io.IOException;
import java.nio.file.Path;

public class Main {
    public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("Usage: java Main <VSF_PATH> <SCRIPT_PATH>");
            System.exit(1);
        }

        System.out.println("[DEBUG] vfs="+args[0]);
        System.out.println("[DEBUG] start_script="+args[1]);

        // Loading vfs
        VFS vfs = new VFS("unix", Path.of(args[0]));
        try {
            vfs.load();
            System.out.println("[INFO] VFS loaded. Nodes: " + vfs.size());
        } catch (IOException e) {
            System.err.println("[FATAL] Can't load vfs: " + e.getMessage());
            System.exit(1);
        }

        REPL repl = new REPL(
                new CommandParser(),
                new CommandExecutor(vfs),
                vfs.getName(),
                args[1]
        );

        repl.start();
    }
}
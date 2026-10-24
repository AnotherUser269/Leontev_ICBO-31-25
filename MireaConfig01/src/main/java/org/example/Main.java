package org.example;

import org.example.parser.CommandExecutor;
import org.example.parser.CommandParser;

public class Main {
    public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("Usage: java Main <VSF_PATH> <SCRIPT_PATH>");
            System.exit(1);
        }

        System.out.println("[DEBUG] vfs="+args[0]);
        System.out.println("[DEBUG] start_script="+args[1]);

        VFS vfs = new VFS("unix", args[0]);

        CommandParser commandParser = new CommandParser();
        CommandExecutor commandExecutor = new CommandExecutor();

        REPL repl = new REPL(
                commandParser,
                commandExecutor,

                vfs.getName(),
                vfs.getVfsFilePath(),
                args[1]
        );

        repl.start();
    }
}
package org.example;

import org.example.parser.CommandExecutor;
import org.example.parser.CommandParser;

public class Main {
    public static void main(String[] args) {
        VFS vfs = new VFS(
                "unix",
                "C:\\Users\\Michail\\vfs.csv"
        );

        CommandParser commandParser = new CommandParser();
        CommandExecutor commandExecutor = new CommandExecutor();

        String startScriptPath = "C:\\Users\\Michail\\script";

        REPL repl = new REPL(
                commandParser,
                commandExecutor,

                vfs.getName(),
                vfs.getVfsFilePath(),
                startScriptPath
        );

        repl.start();
    }
}
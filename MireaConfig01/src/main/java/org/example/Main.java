package org.example;

import org.example.parser.CommandExecutor;
import org.example.parser.CommandParser;

public class Main {
    public static void main(String[] args) {
        VFS vfs = new VFS("unix");
        CommandParser commandParser = new CommandParser();
        CommandExecutor commandExecutor = new CommandExecutor();

        REPL repl = new REPL(commandParser, commandExecutor, vfs.getName());

        repl.start();
    }
}
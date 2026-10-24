package org.example;

import org.example.enums.CommandExecutionStatus;
import org.example.enums.REPLStatus;
import org.example.parser.CommandExecutor;
import org.example.parser.CommandParser;

import java.util.List;
import java.util.Scanner;

public class REPL {
    private REPLStatus replStatus;
    private final CommandParser commandParser;
    private final CommandExecutor commandExecutor;

    private final String vfsName;

    public REPL(CommandParser commandParser, CommandExecutor commandExecutor, String vfsName) {
        this.commandParser = commandParser;
        this.commandExecutor = commandExecutor;
        this.vfsName = vfsName;

        this.replStatus = REPLStatus.READY;
    }

    public void start() {
        System.out.println("(i) REPL is ready.");
        this.replStatus = REPLStatus.RUNNING;

        try (Scanner sc = new Scanner(System.in)) {
            while (replStatus != REPLStatus.NOT_WORKING) {
                System.out.print(vfsName + "$ ");

                String rawInput = sc.nextLine();

                // Empty input should not be a forbidden command
                if (rawInput.isBlank()) {
                    continue;
                }

                List<String> commandTokens = commandParser.parseInput(rawInput);
                CommandExecutionStatus commandStatus = commandExecutor.execute(commandTokens);

                // If command returned a terminate emulator status, we exit
                if (commandStatus == CommandExecutionStatus.TERMINATE_EMULATOR) {
                    replStatus = REPLStatus.NOT_WORKING;
                }

                // If command status is not OK, then we have an error. Print the message
                // and ask again
                else if (commandStatus != CommandExecutionStatus.OK) {
                    System.out.println(commandStatus.getMessage());
                }
            }
        }

        System.out.println("(i) REPL isn't working.");
    }
}

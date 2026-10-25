package org.example;

import org.example.enums.CommandExecutionStatus;
import org.example.enums.REPLStatus;
import org.example.parser.CommandExecutor;
import org.example.parser.CommandParser;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;
import java.util.Objects;
import java.util.Scanner;

public class REPL {
    private REPLStatus replStatus;
    private final CommandParser commandParser;
    private final CommandExecutor commandExecutor;

    private final String vfsName;
    private final String startScriptPath;

    public REPL(CommandParser commandParser,
                CommandExecutor commandExecutor,
                String vfsName,
                String startScriptPath
    ) {
        this.commandParser = commandParser;
        this.commandExecutor = commandExecutor;
        this.vfsName = Objects.requireNonNull(vfsName);
        this.startScriptPath = Objects.requireNonNull(startScriptPath);

        this.replStatus = REPLStatus.READY;
    }

    private CommandExecutionStatus executeLine(String rawInput) {
        if (rawInput.isBlank()) {
            return CommandExecutionStatus.OK;
        }

        List<String> tokens = commandParser.parseInput(rawInput);
        CommandExecutionStatus status = commandExecutor.execute(tokens);
        if (status != CommandExecutionStatus.OK &&
            status != CommandExecutionStatus.TERMINATE_EMULATOR &&
            status != CommandExecutionStatus.EXECUTION_ERROR
        ) {
            System.out.println(status.getMessage());
        }

        return status;
    }

    private void executeScript(String scriptPath) throws FileNotFoundException {
        try (Scanner scanner = new Scanner(new File(scriptPath))) {
            while (scanner.hasNextLine() && replStatus != REPLStatus.NOT_WORKING) {
                String line = scanner.nextLine();
                System.out.println(vfsName + "$ " + line);

                CommandExecutionStatus status = executeLine(line);

                if (status == CommandExecutionStatus.TERMINATE_EMULATOR) {
                    replStatus = REPLStatus.NOT_WORKING;
                }
            }
        }
    }

    public void start() {
        System.out.println("[INFO] REPL is ready.");
        this.replStatus = REPLStatus.RUNNING;

        // Start script execution
        try {
            System.out.println("[INFO] Starting script on " + startScriptPath);
            this.executeScript(startScriptPath);
            System.out.println("[INFO] Start script was executed.");
        } catch (FileNotFoundException e) {
            System.out.println("[ERROR] Can't find a start script path.");
        }

        System.out.println();

        try (Scanner sc = new Scanner(System.in)) {
            while (replStatus != REPLStatus.NOT_WORKING) {
                System.out.print(vfsName + "$ ");

                String rawInput = sc.nextLine();
                CommandExecutionStatus status = executeLine(rawInput);

                if (status == CommandExecutionStatus.TERMINATE_EMULATOR) {
                    replStatus = REPLStatus.NOT_WORKING;
                }
            }
        }

        System.out.println("[INFO] REPL isn't working.");
    }
}

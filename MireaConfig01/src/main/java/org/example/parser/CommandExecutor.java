package org.example.parser;

import org.example.enums.Command;
import org.example.enums.CommandExecutionStatus;

import java.util.Arrays;
import java.util.List;

public class CommandExecutor {
    public CommandExecutionStatus execute(List<String> tokens) {
        if (tokens == null || tokens.isEmpty()) {
            return CommandExecutionStatus.COMMAND_NOT_FOUND;
        }

        // Trying to find a valid command enum
        Command command = Arrays.stream(Command.values())
                                .filter(c -> c.getName().equalsIgnoreCase(tokens.getFirst()))
                                .findFirst()
                                .orElse(null);

        if (command == null) return CommandExecutionStatus.COMMAND_NOT_FOUND;

        // Return exit status of a command
        return switch (command) {
            case EXIT -> {
                if (tokens.size() != 1) {
                    yield CommandExecutionStatus.WRONG_ARGUMENT;
                }

                yield CommandExecutionStatus.TERMINATE_EMULATOR;
            }

            case LS -> {
                if (tokens.size() > 2) yield CommandExecutionStatus.WRONG_ARGUMENT;

                System.out.println(command.getHelpMessage());
                yield CommandExecutionStatus.OK;
            }

            case CD -> {
                if (tokens.size() != 2) {
                    yield CommandExecutionStatus.WRONG_ARGUMENT;
                }

                System.out.println(command.getHelpMessage());
                yield CommandExecutionStatus.OK;
            }
        };
    }
}

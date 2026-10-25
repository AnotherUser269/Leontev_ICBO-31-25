package org.example.parser;

import org.example.enums.Command;
import org.example.enums.CommandExecutionStatus;
import vfs.VFS;

import java.io.IOException;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;

public class CommandExecutor {
    private final VFS vfs;

    public CommandExecutor(VFS vfs) {
        this.vfs = vfs;
    }

    public CommandExecutionStatus execute(List<String> tokens) {
        if (tokens == null || tokens.isEmpty()) {
            return CommandExecutionStatus.COMMAND_NOT_FOUND;
        }

        // Trying to find a valid command enum
        Command command = Arrays.stream(Command.values())
                                .filter(c -> c.getName().equalsIgnoreCase(tokens.get(0)))
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

            case VFS_SAVE -> {
                if (tokens.size() != 2) {
                    yield CommandExecutionStatus.WRONG_ARGUMENT;
                }

                try {
                    vfs.saveState(Path.of(tokens.get(1)));
                    System.out.println("[OK] VFS saved to " + tokens.get(1));
                    yield CommandExecutionStatus.OK;
                } catch (IOException e) {
                    System.out.println("[ERROR] vfs-saved failed: " + e.getMessage());
                    yield CommandExecutionStatus.EXECUTION_ERROR;
                }
            }
        };
    }
}

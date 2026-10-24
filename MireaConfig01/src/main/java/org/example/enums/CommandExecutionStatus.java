package org.example.enums;

public enum CommandExecutionStatus {
    OK("Successfully executed"),
    COMMAND_NOT_FOUND("Got an unknown command."),
    WRONG_ARGUMENT("Wrong arguments provided."),
    TERMINATE_EMULATOR("Got a call to terminate emulator. Exiting...");

    private final String MESSAGE;

    CommandExecutionStatus(String message) {
        this.MESSAGE = message;
    }

    public String getMessage() {
        return this.MESSAGE;
    }
}

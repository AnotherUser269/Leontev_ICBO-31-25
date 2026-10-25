package org.example.enums;

public enum Command {
    EXIT("exit", "Usage: exit\nTerminates the emulator."),
    LS("ls", "Usage: ls [path]\nShows the contents of the current directory or the specified directory."),
    CD("cd", "Usage: cd <path>\nChanges the current directory."),
    VFS_SAVE("vfs-save", "Usage: vfs-save <path>\nSave current VFS to CSV.");

    private final String NAME;
    private final String HELP_MESSAGE;

    Command(String name, String helpMessage) {
        HELP_MESSAGE = helpMessage;
        NAME = name;
    }

    public String getName() {
        return NAME;
    }

    public String getHelpMessage() {
        return HELP_MESSAGE;
    }
}

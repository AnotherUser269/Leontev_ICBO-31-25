package org.example.parser;

import java.util.List;

public class CommandParser {
    public List<String> parseInput(String input) {
        return List.of(input.trim().split("\\s+"));
    }
}

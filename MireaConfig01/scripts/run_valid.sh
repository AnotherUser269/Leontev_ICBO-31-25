#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CLASSPATH="$PROJECT_ROOT/target/classes"

echo "=== Запуск 1: basic.csv + startup_a.txt ==="
echo exit | java -cp "$CLASSPATH" org.example.Main "$PROJECT_ROOT/vfs/vfs1.csv" "$PROJECT_ROOT/scripts/start_up_A.txt"

echo ""
echo "=== Запуск 2: nested.csv + startup_b.txt ==="
echo exit | java -cp "$CLASSPATH" org.example.Main "$PROJECT_ROOT/vfs/vfs2.csv" "$PROJECT_ROOT/scripts/start_up_B.txt"

read -p "Нажмите любую клавишу для выхода..."
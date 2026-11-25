#!/bin/bash

if [ -z "$1" ]; then
    echo "Ошибка: укажите путь к выходному файлу"
    echo "Использование: ./run.sh <output.xml>"
    exit 1
fi

python3 -m src.main "$1"

#!/bin/bash

directories=(
    "./src/clash"
    "./src/lab"
    "./src/bot_programming"
    "./src/codegolf/easy"
    "./src/codegolf/medium"
    "./src/codegolf/hard"
    "./src/codegolf/expert"
    "./src/optimization"
    "./src/puzzles/easy"
    "./src/puzzles/medium"
    "./src/puzzles/hard"
    "./src/puzzles/expert"
)

for dir in "${directories[@]}"; do
    mkdir -p "$dir"
    echo "Created directory: $dir"
done

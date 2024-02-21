#!/bin/bash

option="${1:-$(echo "Choose what to delete (Clash, Lab, Solutions, Everything): " && read -r choice && echo $choice)}"

delete_files() {
    path=$1
    echo "Deleting all files in $path"
    find "$path" -type f -exec rm -f {} +
}

echo "Are you sure you want to delete files under $option? (yes/no)"
read -r confirmation

if [ "$confirmation" = "yes" ]; then
    case $option in
        Clash)
            delete_files "./src/clash"
            ;;
        Lab)
            delete_files "./src/lab"
            ;;
        Solutions)
            delete_files "./src/bot_programming"
            delete_files "./src/codegolf"
            delete_files "./src/optimization"
            delete_files "./src/puzzles"
            ;;
        Everything)
            delete_files "./src/clash"
            delete_files "./src/lab"
            delete_files "./src/bot_programming"
            delete_files "./src/codegolf"
            delete_files "./src/optimization"
            delete_files "./src/puzzles"
            ;;
        *)
            echo "Invalid option selected."
            ;;
    esac
else
    echo "Operation cancelled."
fi

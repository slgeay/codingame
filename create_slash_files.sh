#!/bin/bash

directoryPath="./src/clash/"
extensions=(
    # "sh"
    "c"
    # "cs"
    "cpp"
    # "clj"
    # "d"
    # "dart"
    # "fs"
    # "go"
    # "groovy"
    # "hs"
    # "java"
    # "js"
    # "kt"
    # "lua"
    # "m"
    # "ml"
    # "pas"
    # "pl" # dss
    "php"
    "py"
    # "rb"
    "rs"
    # "scala"
    # "swift"
    # "ts"
    # "vb"
)

if [ ! -d "$directoryPath" ]; then
    mkdir -p "$directoryPath"
fi

for extension in "${extensions[@]}"; do
    fileName="$directoryPath/clash.$extension"
    if [ ! -f "$fileName" ]; then
        echo "Creating $fileName"
        touch "$fileName"
    else
        echo "$fileName already exists"
    fi
done

echo "Operation completed."

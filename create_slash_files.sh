#!/bin/bash

directoryPath="./src/clash/"
iniPath="languages.ini"

declare -a extensions
declare -a languages
currentLanguage=""
extension=""
enabled=""

while IFS='=' read -r key value; do
    if [[ $key =~ ^\[.*\]$ ]]; then
        currentLanguage=${key:1:-1}
    elif [[ $key == "extension" ]]; then
        currentExtension=$value
    elif [[ $key == "enabled" && $value -eq 1 ]]; then
        extensions+=("$currentExtension")
        languages+=("$currentLanguage ($currentExtension)")
    fi
done < "$iniPath"

if [ ! -d "$directoryPath" ]; then
    mkdir -p "$directoryPath"
fi

for extension in "${extensions[@]}"; do
    fileName="$directoryPath/clash$extension"
    if [ ! -f "$fileName" ]; then
        echo "Creating $fileName"
        touch "$fileName"
    else
        echo "$fileName already exists"
    fi
done

echo "Operation completed."

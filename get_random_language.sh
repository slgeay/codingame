#!/bin/bash

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

rand=$[$RANDOM % ${#languages[@]}]
echo "Random Language: ${languages[$rand]}"

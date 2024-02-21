#!/bin/bash

apiUrl="https://api.github.com/repos/jmerle/cg-local-app/releases/latest"
downloadDir="./.cg_local_app"

mkdir -p "$downloadDir"

jarUrl=$(curl -s "$apiUrl" | jq -r '.assets[] | select(.name | test("cg-local-app.*\\.jar$")) | .browser_download_url')

if [ -z "$jarUrl" ]; then
    echo "JAR URL not found."
    exit 1
fi

fileName=$(basename "$jarUrl")
filePath="$downloadDir/$fileName"

if [ ! -f "$filePath" ]; then
    echo "Downloading cg-local-app JAR..."
    curl -L "$jarUrl" -o "$filePath"
fi

java -jar "$filePath"

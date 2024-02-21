#!/bin/bash

languages=(
    "Bash (.sh)"
    "C (.c)"
    "C# (.cs)"
    "C++ (.cpp)"
    "Clojure (.clj)"
    "D (.d)"
    "Dart (.dart)"
    "F# (.fs)"
    "Go (.go)"
    "Groovy (.groovy)"
    "Haskell (.hs)"
    "Java (.java)"
    "JavaScript (.js)"
    "Kotlin (.kt)"
    "Lua (.lua)"
    "Objective-C (.m)"
    "OCaml (.ml)"
    "Pascal (.pas)"
    "Perl (.pl)"
    "PHP (.php)"
    "Python 3 (.py)"
    "Ruby (.rb)"
    "Rust (.rs)"
    "Scala (.scala)"
    "Swift (.swift)"
    "TypeScript (.ts)"
    "VB.NET (.vb)"
)

rand=$[$RANDOM % ${#languages[@]}]
echo "Random Language: ${languages[$rand]}"

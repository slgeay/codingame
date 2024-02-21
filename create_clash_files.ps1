$directoryPath = ".\src\clash\"
$extensions = @(
    # "sh" # Bash
    "c" # C
    # "cs" # C#
    "cpp" # C++
    # "clj" # Clojure
    # "d" # D
    # "dart" # Dart
    # "fs" # F#
    # "go" # Go
    # "groovy" # Groovy
    # "hs" # Haskell
    # "java" # Java
    # "js" # JavaScript
    # "kt" # Kotlin
    # "lua" # Lua
    # "m" # Objective-C
    # "ml" # OCaml
    # "pas" # Pascal
    # "pl" # Perl
    "php" # PHP
    "py" # Python
    # "rb" # Ruby
    "rs" # Rust
    # "scala" # Scala
    # "swift" # Swift
    # "ts" # TypeScript
    # "vb" # VB.NET
) -join ', ' -split ', ' | Where-Object { $_ -ne '' }




foreach ($extension in $extensions) {
    $fileName = $directoryPath + "clash.$extension"
    if (-not (Test-Path -Path $fileName)) {
        Write-Host "Creating $fileName"
        New-Item -ItemType File -Path $fileName -Force
    }
    else {
        Write-Host "$fileName already exists"
    }
}

Write-Host "Operation completed"

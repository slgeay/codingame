$directories = @(
    ".\src\clash",
    ".\src\lab",
    ".\src\bot_programming",
    ".\src\codegolf\easy",
    ".\src\codegolf\medium",
    ".\src\codegolf\hard",
    ".\src\codegolf\expert",
    ".\src\optimization",
    ".\src\puzzles\easy",
    ".\src\puzzles\medium",
    ".\src\puzzles\hard",
    ".\src\puzzles\expert"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir
        Write-Host "Created directory: $dir"
    }
}

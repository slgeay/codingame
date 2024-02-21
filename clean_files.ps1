param (
    [string]$Option = $(Read-Host "Choose what to clean (Clash, Lab, Solutions, Everything)")
)

function Remove-ItemFiles {
    param (
        [string]$Path,
        [bool]$IsRecursive = $false
    )
    Get-ChildItem -Path $Path -File -Recurse | Remove-Item -Force
    Write-Host "Deleted all files in $Path"
}

$confirmation = Read-Host "Are you sure you want to clean $($Option)? (yes/no)"
if ($confirmation -eq 'yes') {
    switch ($Option) {
        "Clash" {
            Remove-ItemFiles -Path "./src/clash"
        }
        "Lab" {
            Get-ChildItem -Path "./src/lab" | Remove-Item -Force -Recurse
            Write-Host "Deleted everything in ./src/lab"
        }
        "Solutions" {
            Remove-ItemFiles -Path "./src/bot_programming"
            Remove-ItemFiles -Path "./src/codegolf"
            Remove-ItemFiles -Path "./src/optimization"
            Remove-ItemFiles -Path "./src/puzzles"
        }
        "Everything" {
            Remove-ItemFiles -Path "./src/clash"
            Get-ChildItem -Path "./src/lab" | Remove-Item -Force -Recurse
            Write-Host "Deleted everything in ./src/lab"
            Remove-ItemFiles -Path "./src/bot_programming"
            Remove-ItemFiles -Path "./src/codegolf"
            Remove-ItemFiles -Path "./src/optimization"
            Remove-ItemFiles -Path "./src/puzzles"
        }
        default {
            Write-Host "Invalid option selected."
        }
    }
} else {
    Write-Host "Operation cancelled."
}

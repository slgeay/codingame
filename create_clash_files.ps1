$directoryPath = ".\src\clash\"
$iniPath = "languages.ini"

$extensions = @()
$languages = @()
Get-Content $iniPath | ForEach-Object {
    if ($_ -match "^\[(.+)\]") {
        $currentLanguage = $matches[1]
        $currentExtension = ""
    } elseif ($_ -match "^extension=(.+)$") {
        $currentExtension = $matches[1]
    } elseif ($_ -match "^enabled=(\d)") {
        if ($matches[1] -eq "1") {
            $extensions += $currentExtension
            $languages += "$currentLanguage ($currentExtension)"
        }
    }
}

foreach ($extension in $extensions) {
    $fileName = $directoryPath + "clash$extension"
    if (-not (Test-Path -Path $fileName)) {
        Write-Host "Creating $fileName"
        New-Item -ItemType File -Path $fileName -Force
    }
    else {
        Write-Host "$fileName already exists"
    }
}

Write-Host "Operation completed"

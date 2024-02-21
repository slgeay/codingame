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

$randomLanguage = Get-Random -InputObject $languages
Write-Host "Random Language: $randomLanguage"

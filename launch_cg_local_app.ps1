$apiUrl = "https://api.github.com/repos/jmerle/cg-local-app/releases/latest"
$downloadDir = ".\.cg_local_app\"

try {
    $latestRelease = Invoke-RestMethod -Uri $apiUrl
    $jarUrl = $latestRelease.assets | Where-Object { $_.name -match "cg-local-app.*\.jar$" } | Select-Object -ExpandProperty browser_download_url

    if (-not $jarUrl) {
        Write-Error "JAR URL not found."
        exit
    }

    $filePath = Join-Path -Path $downloadDir -ChildPath ($jarUrl -split "/" | Select-Object -Last 1)

    if (-Not (Test-Path -Path $filePath)) {
        if (-Not (Test-Path -Path $downloadDir)) {
            New-Item -ItemType Directory -Force -Path $downloadDir
        }
        Write-Host "Downloading cg-local-app JAR..."
        Invoke-WebRequest -Uri $jarUrl -OutFile $filePath
    }

    java -jar $filePath
} catch {
    Write-Error "An error occurred: $_"
}

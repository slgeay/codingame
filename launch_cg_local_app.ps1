$s = curl -s https://api.github.com/repos/jmerle/cg-local-app/releases/latest | findstr /r /c:"cg-local-app.*jar"
$r = [regex]::matches($s,'"([^"]*jar)"')
$d = ".cg_local_app\"
$f = $d+$r[0].Groups[1].Value
if (-Not (Test-Path $f)) {
    if (-Not (Test-Path $d)) {
        New-Item -ItemType Directory -Force -Path $d
    }
    Invoke-WebRequest -Uri $r[1].Groups[1].Value -OutFile $f
}
java -jar $f
param(
    [ValidateRange(1024, 65500)][int]$Port = 8787,
    [string]$NodePath,
    [string]$CloudflaredPath
)
$ErrorActionPreference = 'Stop'
$siteRoot = $PSScriptRoot
$runtimeRoot = Join-Path $siteRoot '.runtime'
$statePath = Join-Path $runtimeRoot 'runtime.json'
$serverPath = Join-Path $siteRoot 'server.mjs'
if (-not (Test-Path -LiteralPath (Join-Path $siteRoot 'dist/index.html') -PathType Leaf)) { throw 'Build dist/index.html before starting the site.' }
if (-not $NodePath) { $NodePath = (Get-Command node.exe -ErrorAction Stop).Source }
if (-not $CloudflaredPath) { $CloudflaredPath = (Get-Command cloudflared.exe -ErrorAction Stop).Source }
$NodePath = (Resolve-Path -LiteralPath $NodePath).Path
$CloudflaredPath = (Resolve-Path -LiteralPath $CloudflaredPath).Path
New-Item -ItemType Directory -Force -Path $runtimeRoot | Out-Null

function Get-OwnedProcess($record) {
    if (-not $record) { return $null }
    $candidate = Get-Process -Id ([int]$record.id) -ErrorAction SilentlyContinue
    if (-not $candidate) { return $null }
    try {
        if ($candidate.StartTime.ToUniversalTime().Ticks.ToString() -ne [string]$record.startedUtcTicks) { return $null }
        if ($candidate.Path -ne [string]$record.executable) { return $null }
        return $candidate
    } catch { return $null }
}
function Process-Record($process, $executable) {
    $process.Refresh()
    return @{ id = $process.Id; startedUtcTicks = $process.StartTime.ToUniversalTime().Ticks.ToString(); executable = $executable }
}
function Save-State($state) {
    $state | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $statePath -Encoding UTF8
}
function Read-PublicUrl {
    foreach ($name in @('tunnel.err.log', 'tunnel.out.log')) {
        $logPath = Join-Path $runtimeRoot $name
        if (Test-Path -LiteralPath $logPath) {
            $text = Get-Content -LiteralPath $logPath -Raw -ErrorAction SilentlyContinue
            if ([string]::IsNullOrEmpty($text)) { continue }
            $match = [regex]::Match([string]$text, 'https://[a-z0-9-]+\.trycloudflare\.com')
            if ($match.Success) { return $match.Value }
        }
    }
    return $null
}

$state = $null
if (Test-Path -LiteralPath $statePath) { $state = Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json }
$ownedServer = if ($state) { Get-OwnedProcess $state.server } else { $null }
$ownedTunnel = if ($state) { Get-OwnedProcess $state.tunnel } else { $null }

if ($ownedServer) {
    $origin = [string]$state.origin
    try { $health = Invoke-RestMethod -Uri "$origin/healthz" -TimeoutSec 3 }
    catch { throw 'The recorded site process is running but its health check failed. Run stop.ps1, then start.ps1.' }
    if ($health.instance -ne $state.instance -or $health.service -ne 'simworld-static') { throw 'Recorded server identity did not match. No process was stopped.' }
} else {
    if ($ownedTunnel) { Stop-Process -Id $ownedTunnel.Id; $ownedTunnel.WaitForExit(5000) | Out-Null; $ownedTunnel = $null }
    $selectedPort = $null
    foreach ($portCandidate in $Port..($Port + 20)) {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $portCandidate)
        try { $listener.Start(); $selectedPort = $portCandidate; break }
        catch { }
        finally { $listener.Stop() }
    }
    if (-not $selectedPort) { throw 'No available loopback port was found.' }
    $origin = "http://127.0.0.1:$selectedPort"
    $instance = [guid]::NewGuid().ToString()
    $serverArguments = '"{0}" --port {1} --instance {2}' -f $serverPath, $selectedPort, $instance
    $server = Start-Process -FilePath $NodePath -ArgumentList $serverArguments -WorkingDirectory $siteRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $runtimeRoot 'server.out.log') -RedirectStandardError (Join-Path $runtimeRoot 'server.err.log')
    $state = @{ origin = $origin; instance = $instance; server = (Process-Record $server $NodePath); tunnel = $null; publicUrl = $null }
    Save-State $state
    $healthy = $false
    for ($attempt = 0; $attempt -lt 40; $attempt++) {
        Start-Sleep -Milliseconds 250
        if ($server.HasExited) { throw 'The site server exited. See website/.runtime/server.err.log.' }
        try {
            $health = Invoke-RestMethod -Uri "$origin/healthz" -TimeoutSec 1
            if ($health.instance -eq $instance -and $health.service -eq 'simworld-static') { $healthy = $true; break }
        } catch { }
    }
    if (-not $healthy) { throw 'The site server did not become ready. See website/.runtime/server.err.log.' }
}

if (-not $ownedTunnel) {
    $tunnelArguments = "tunnel --no-autoupdate --url $origin --metrics 127.0.0.1:0 --loglevel info"
    $tunnel = Start-Process -FilePath $CloudflaredPath -ArgumentList $tunnelArguments -WorkingDirectory $runtimeRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $runtimeRoot 'tunnel.out.log') -RedirectStandardError (Join-Path $runtimeRoot 'tunnel.err.log')
    $state.tunnel = Process-Record $tunnel $CloudflaredPath
    $state.publicUrl = $null
    Save-State $state
    $ownedTunnel = $tunnel
}

$publicUrl = $null
for ($attempt = 0; $attempt -lt 55; $attempt++) {
    $ownedTunnel.Refresh()
    if ($ownedTunnel.HasExited) { throw 'Cloudflare Tunnel exited. See website/.runtime/tunnel.err.log.' }
    $publicUrl = Read-PublicUrl
    if ($publicUrl) { break }
    Start-Sleep -Seconds 1
}
if ($publicUrl) {
    $state.publicUrl = $publicUrl
    Save-State $state
    [pscustomobject]@{ local = $origin; public = $publicUrl; serverPid = $state.server.id; tunnelPid = $state.tunnel.id; status = 'Tunnel URL issued; verify public availability' } | ConvertTo-Json
} else {
    [pscustomobject]@{ local = $origin; status = 'Server running; tunnel still connecting'; logs = $runtimeRoot } | ConvertTo-Json
}

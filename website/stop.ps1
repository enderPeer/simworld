$ErrorActionPreference = 'Stop'
$statePath = Join-Path $PSScriptRoot '.runtime/runtime.json'
if (-not (Test-Path -LiteralPath $statePath)) { Write-Output 'No recorded SimWorld website processes.'; exit 0 }
$state = Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json
$stopped = @()
$unowned = @()
foreach ($name in @('tunnel', 'server')) {
    $record = $state.$name
    if (-not $record) { continue }
    $candidate = Get-Process -Id ([int]$record.id) -ErrorAction SilentlyContinue
    if (-not $candidate) { continue }
    $matches = $false
    try { $matches = ($candidate.StartTime.ToUniversalTime().Ticks.ToString() -eq [string]$record.startedUtcTicks -and $candidate.Path -eq [string]$record.executable) }
    catch { }
    if ($matches) {
        Stop-Process -Id $candidate.Id
        $candidate.WaitForExit(5000) | Out-Null
        $stopped += $name
    } else { $unowned += $name }
}
if ($unowned.Count) { Write-Output ('Skipped processes whose recorded identity no longer matched: ' + ($unowned -join ', ')) }
Write-Output ('Stopped owned website processes: ' + $(if ($stopped.Count) { $stopped -join ', ' } else { 'none were running' }))
# Keep state and logs for troubleshooting; the next start safely checks process identities.

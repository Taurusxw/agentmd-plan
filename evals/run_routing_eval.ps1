[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$OutputRoot,

    [Parameter(Mandatory = $true)]
    [string]$FixturePath,

    [string]$ScenarioFile = (Join-Path $PSScriptRoot 'v30-routing-scenarios.json'),
    [string]$Model = 'gpt-5.6-sol',
    [int[]]$ScenarioIds = @()
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $ScenarioFile -PathType Leaf)) {
    throw "Scenario file not found: $ScenarioFile"
}
if (-not (Test-Path -LiteralPath $FixturePath -PathType Container)) {
    throw "Fixture repository not found: $FixturePath"
}

New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
$scenarios = @(Get-Content -Raw -LiteralPath $ScenarioFile | ConvertFrom-Json)
if ($ScenarioIds.Count -gt 0) {
    $selected = @($scenarios | Where-Object { [int]$_.id -in $ScenarioIds })
    if ($selected.Count -ne $ScenarioIds.Count) {
        throw 'One or more requested scenario IDs do not exist.'
    }
    $scenarios = $selected
}

$rows = @()
foreach ($scenario in $scenarios | Sort-Object id) {
    $stem = '{0:D2}-{1}' -f [int]$scenario.id, $scenario.name
    $jsonlPath = Join-Path $OutputRoot ($stem + '.jsonl')
    $lastMessagePath = Join-Path $OutputRoot ($stem + '.txt')

    & codex exec --ephemeral --sandbox read-only --json `
        -m $Model -C $FixturePath -o $lastMessagePath $scenario.prompt 2>&1 |
        Out-File -LiteralPath $jsonlPath -Encoding utf8
    $exitCode = $LASTEXITCODE

    $events = @(
        Get-Content -LiteralPath $jsonlPath |
            Where-Object { $_ -like '{*' } |
            ForEach-Object {
                try { $_ | ConvertFrom-Json } catch { }
            }
    )
    $items = @(
        $events |
            Where-Object { $_.type -eq 'item.completed' } |
            ForEach-Object { $_.item }
    )
    $commands = @(
        $items |
            Where-Object { $_.type -eq 'command_execution' } |
            ForEach-Object { $_.command }
    )
    $usage = $events | Where-Object { $_.type -eq 'turn.completed' } | Select-Object -Last 1
    if (-not $usage) {
        throw "Scenario $($scenario.id) did not emit turn.completed. See $jsonlPath"
    }

    $skills = @()
    foreach ($command in $commands) {
        foreach ($match in [regex]::Matches(
            [string]$command,
            'skills\\\\([^\\]+)\\\\SKILL\.md'
        )) {
            $skills += $match.Groups[1].Value
        }
    }

    $serializedItems = $items | ConvertTo-Json -Depth 12 -Compress
    $rows += [pscustomobject]@{
        id                  = [int]$scenario.id
        name                = [string]$scenario.name
        exit_code           = [int]$exitCode
        input_tokens        = [int64]$usage.usage.input_tokens
        cached_input_tokens = [int64]$usage.usage.cached_input_tokens
        output_tokens       = [int64]$usage.usage.output_tokens
        governance_loaded   = [bool]($commands -match 'seer-codex-rules')
        skills_loaded       = @(($skills | Sort-Object -Unique))
        subagent_dispatched = [bool]($serializedItems -match 'spawn_agent|create_thread')
        hash_command        = [bool]($commands -match 'Get-FileHash|sha256sum|certutil|hashlib|checksum')
        jsonl               = $jsonlPath
        last_message        = $lastMessagePath
    }

    Write-Output (
        'DONE {0} exit={1} governance={2} subagent={3} hashCommand={4} input={5} output={6}' -f
        $stem,
        $exitCode,
        $rows[-1].governance_loaded,
        $rows[-1].subagent_dispatched,
        $rows[-1].hash_command,
        $rows[-1].input_tokens,
        $rows[-1].output_tokens
    )
}

$summaryPath = Join-Path $OutputRoot 'summary.json'
$rows | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $summaryPath -Encoding utf8

$inputs = @($rows | ForEach-Object { $_.input_tokens } | Sort-Object)
if ($inputs.Count % 2 -eq 1) {
    $medianInput = $inputs[[int](($inputs.Count - 1) / 2)]
} else {
    $medianInput = ($inputs[$inputs.Count / 2 - 1] + $inputs[$inputs.Count / 2]) / 2
}

[pscustomobject]@{
    scenario_count       = $rows.Count
    input_tokens_total   = ($rows | Measure-Object input_tokens -Sum).Sum
    input_tokens_median  = $medianInput
    governance_loads     = @($rows | Where-Object governance_loaded).Count
    subagent_dispatches  = @($rows | Where-Object subagent_dispatched).Count
    hash_commands        = @($rows | Where-Object hash_command).Count
    summary_path         = $summaryPath
}

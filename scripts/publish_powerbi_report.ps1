param(
    [Parameter(Mandatory = $true)][string]$TenantId,
    [Parameter(Mandatory = $true)][string]$ClientId,
    [Parameter(Mandatory = $true)][string]$ClientSecret,
    [Parameter(Mandatory = $true)][string]$WorkspaceId,
    [Parameter(Mandatory = $true)][string]$PbixPath,
    [string]$ShareEmail = ""
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $PbixPath)) {
    throw "PBIX file not found: $PbixPath. Export the report from Power BI Desktop to this path before running deploy.yml."
}

$tokenResponse = Invoke-RestMethod `
    -Method Post `
    -Uri "https://login.microsoftonline.com/$TenantId/oauth2/v2.0/token" `
    -Body @{
        client_id     = $ClientId
        client_secret = $ClientSecret
        scope         = "https://analysis.windows.net/powerbi/api/.default"
        grant_type    = "client_credentials"
    }

$headers = @{ Authorization = "Bearer $($tokenResponse.access_token)" }
$displayName = [System.IO.Path]::GetFileNameWithoutExtension($PbixPath)
$importUri = "https://api.powerbi.com/v1.0/myorg/groups/$WorkspaceId/imports?datasetDisplayName=$([uri]::EscapeDataString($displayName))&nameConflict=CreateOrOverwrite"

$import = Invoke-RestMethod `
    -Method Post `
    -Uri $importUri `
    -Headers $headers `
    -Form @{ file = Get-Item -LiteralPath $PbixPath }

$importId = $import.id
$state = $import.importState
for ($i = 0; $i -lt 60 -and $state -notin @("Succeeded", "Failed"); $i++) {
    Start-Sleep -Seconds 5
    $current = Invoke-RestMethod `
        -Method Get `
        -Uri "https://api.powerbi.com/v1.0/myorg/groups/$WorkspaceId/imports/$importId" `
        -Headers $headers
    $state = $current.importState
}

if ($state -ne "Succeeded") {
    throw "Power BI import did not succeed. Final state: $state"
}

$reports = Invoke-RestMethod `
    -Method Get `
    -Uri "https://api.powerbi.com/v1.0/myorg/groups/$WorkspaceId/reports" `
    -Headers $headers

$report = $reports.value | Where-Object { $_.name -eq $displayName } | Select-Object -First 1
if (-not $report) {
    throw "Published report was not found in workspace after import."
}

if ($ShareEmail) {
    $shareBody = @{
        identifier           = $ShareEmail
        principalType        = "User"
        groupUserAccessRight = "Viewer"
    } | ConvertTo-Json

    Invoke-RestMethod `
        -Method Post `
        -Uri "https://api.powerbi.com/v1.0/myorg/groups/$WorkspaceId/users" `
        -Headers ($headers + @{ "Content-Type" = "application/json" }) `
        -Body $shareBody | Out-Null
}

"report_url=$($report.webUrl)" >> $env:GITHUB_OUTPUT
Write-Host "Published report: $($report.webUrl)"

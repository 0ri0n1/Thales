###############################################################################
# run_recon.ps1 - Windows Launcher for Pineapple Wireless Reconnaissance
#
# This script:
#   1. Enumerates home devices from the Windows ARP table
#   2. Copies the device list into the Kali Docker container
#   3. Launches pineapple_recon.sh inside the container
#   4. Retrieves the generated report to E:\Thon\reports\
#
# Usage:
#   powershell -File E:\Thon\scripts\run_recon.ps1
#   powershell -File E:\Thon\scripts\run_recon.ps1 -ScanDuration 120
#   powershell -File E:\Thon\scripts\run_recon.ps1 -SkipDenylist
#
# Prerequisites:
#   - Docker Desktop running with kali-mcp-pentest container
#   - WiFi Pineapple connected via USB (172.16.42.0/24)
#   - Windows connected to home WiFi
###############################################################################

param(
    [int]$ScanDuration = 90,
    [int]$ChannelDwell = 30,
    [string]$PineIP = "172.16.42.1",
    [string]$PinePass = "Mousepad7",
    [string]$Band = "bg",
    [string]$HomeSubnet = "192.168.1",
    [string]$HomeSSIDs = "TELUS5434,TELUS5434_RPT",
    [string]$WiFiAdapter = "Wi-Fi",
    [switch]$SkipDenylist,
    [switch]$SkipScan,
    [switch]$VerboseOutput
)

$ErrorActionPreference = "Stop"

# ------- Configuration -------
$ContainerName = "kali-mcp-pentest"
$ContainerWorkDir = "/tmp/recon_output"
$ScriptName = "pineapple_recon.sh"
$LocalScriptPath = Join-Path $PSScriptRoot $ScriptName
$LocalReportDir = "E:\Thon\reports"
$Timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"

# ------- Helper Functions -------
function Write-Status {
    param([string]$Message)
    $ts = Get-Date -Format "HH:mm:ss"
    Write-Host "[$ts] $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    $ts = Get-Date -Format "HH:mm:ss"
    Write-Host "[$ts] [+] $Message" -ForegroundColor Green
}

function Write-Warn {
    param([string]$Message)
    $ts = Get-Date -Format "HH:mm:ss"
    Write-Host "[$ts] [!] $Message" -ForegroundColor Yellow
}

function Write-Fatal {
    param([string]$Message)
    $ts = Get-Date -Format "HH:mm:ss"
    Write-Host "[$ts] [x] $Message" -ForegroundColor Red
    exit 1
}

# ------- Banner -------
Write-Host ""
Write-Host "+==============================================================+" -ForegroundColor Magenta
Write-Host "|     PINEAPPLE WIRELESS RECON - WINDOWS LAUNCHER              |" -ForegroundColor Magenta
Write-Host "|     Classification: RECON ONLY                               |" -ForegroundColor Magenta
Write-Host "+==============================================================+" -ForegroundColor Magenta
Write-Host ""

# ------- Preflight -------
Write-Status "Running preflight checks..."

# Check Docker is running
try {
    $dockerInfo = docker info 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Docker not running" }
    Write-Success "Docker is running"
}
catch {
    Write-Fatal "Docker Desktop is not running. Start Docker and try again."
}

# Check container is running
$containerState = docker inspect --format "{{.State.Running}}" $ContainerName 2>&1
if ($containerState -ne "true") {
    Write-Status "Starting $ContainerName container..."
    docker start $ContainerName 2>&1 | Out-Null
    Start-Sleep -Seconds 3
    $containerState = docker inspect --format "{{.State.Running}}" $ContainerName 2>&1
    if ($containerState -ne "true") {
        Write-Fatal "Cannot start container $ContainerName"
    }
}
Write-Success "Container $ContainerName is running"

# Check WiFi adapter exists
try {
    $adapter = Get-NetAdapter -Name $WiFiAdapter -ErrorAction Stop
    Write-Success "WiFi adapter found (MAC: $($adapter.MacAddress))"
}
catch {
    Write-Warn "WiFi adapter not found - home enumeration may be incomplete"
}

# Check Pineapple connectivity
$pingResult = Test-Connection -ComputerName $PineIP -Count 1 -TimeoutSeconds 3 -ErrorAction SilentlyContinue
if ($pingResult) {
    Write-Success "Pineapple at $PineIP is reachable"
}
else {
    Write-Warn "Cannot ping Pineapple at $PineIP - USB connection may be down"
}

# ------- Phase 1: Home Device Enumeration (Windows side) -------
Write-Host ""
Write-Status "=== PHASE 1: HOME DEVICE ENUMERATION ==="

# Get ARP table for home subnet
Write-Status "Querying Windows ARP table for ${HomeSubnet}.*..."
$arpEntries = Get-NetNeighbor -AddressFamily IPv4 |
    Where-Object { $_.IPAddress -like "${HomeSubnet}.*" -and $_.State -ne "Unreachable" } |
    Select-Object IPAddress, LinkLayerAddress, State |
    Sort-Object { [int]($_.IPAddress -split '\.')[-1] }

# Get own WiFi MAC
$ownMac = ""
try {
    $ownMac = (Get-NetAdapter -Name $WiFiAdapter -ErrorAction Stop).MacAddress -replace '-', ':'
    Write-Status "Operator WiFi MAC: $ownMac"
}
catch {
    Write-Warn "Could not get WiFi adapter MAC"
}

# Build CSV for the container
$arpCsvPath = Join-Path $env:TEMP "home_arp_input.csv"
$arpEntries | ForEach-Object {
    $mac = $_.LinkLayerAddress -replace '-', ':'
    "$($_.IPAddress),$mac,$($_.State)"
} | Out-File -FilePath $arpCsvPath -Encoding UTF8

# Add own MAC if found
if ($ownMac) {
    "SELF,$ownMac,Self" | Out-File -FilePath $arpCsvPath -Append -Encoding UTF8
}

$deviceCount = ($arpEntries | Measure-Object).Count
Write-Success "Found $deviceCount home devices in ARP table"

# Display device table
Write-Host ""
Write-Host "  Home Device Inventory:" -ForegroundColor White
Write-Host "  -----------------------------------------------" -ForegroundColor DarkGray
$arpEntries | ForEach-Object {
    $mac = $_.LinkLayerAddress -replace '-', ':'
    Write-Host "  $($_.IPAddress.PadRight(18)) $mac  $($_.State)" -ForegroundColor Gray
}
if ($ownMac) {
    Write-Host "  SELF               $ownMac  Operator" -ForegroundColor Gray
}
Write-Host ""

# ------- Copy files into container -------
Write-Status "Preparing container workspace..."

# Create working directory in container
docker exec $ContainerName mkdir -p $ContainerWorkDir 2>&1 | Out-Null

# Copy ARP input
docker cp $arpCsvPath "${ContainerName}:${ContainerWorkDir}/home_arp_input.csv" 2>&1 | Out-Null
Write-Success "Home device list copied to container"

# Copy recon script
if (Test-Path $LocalScriptPath) {
    docker cp $LocalScriptPath "${ContainerName}:/tmp/${ScriptName}" 2>&1 | Out-Null
    docker exec $ContainerName chmod +x "/tmp/${ScriptName}" 2>&1 | Out-Null
    # Fix line endings (Windows to Unix)
    docker exec $ContainerName bash -c "sed -i 's/\r$//' /tmp/${ScriptName}" 2>&1 | Out-Null
    Write-Success "Recon script deployed to container"
}
else {
    Write-Fatal "Recon script not found at: $LocalScriptPath"
}

# ------- Launch Recon Script -------
Write-Host ""
Write-Status "=== LAUNCHING RECON SCRIPT IN CONTAINER ==="
Write-Host ""

# Build arguments
$scriptArgs = @(
    "--pine-ip", $PineIP,
    "--pine-pass", $PinePass,
    "--scan-duration", $ScanDuration,
    "--channel-dwell", $ChannelDwell,
    "--band", $Band,
    "--home-subnet", $HomeSubnet,
    "--home-ssids", $HomeSSIDs,
    "--report-dir", $ContainerWorkDir
)

if ($SkipDenylist) { $scriptArgs += "--skip-denylist" }
if ($SkipScan) { $scriptArgs += "--skip-scan" }
if ($VerboseOutput) { $scriptArgs += "--verbose" }

$argsString = $scriptArgs -join " "

Write-Status "Executing: /tmp/${ScriptName} $argsString"
Write-Host "-------------------------------------------------------------" -ForegroundColor DarkGray

# Execute with streaming output
docker exec $ContainerName bash -c "/tmp/${ScriptName} $argsString" 2>&1 | ForEach-Object {
    if ($_ -match "FATAL") {
        Write-Host $_ -ForegroundColor Red
    }
    elseif ($_ -match "WARNING") {
        Write-Host $_ -ForegroundColor Yellow
    }
    elseif ($_ -match "COMPLETE") {
        Write-Host $_ -ForegroundColor Green
    }
    else {
        Write-Host $_ -ForegroundColor Gray
    }
}

$exitCode = $LASTEXITCODE

Write-Host "-------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host ""

if ($exitCode -ne 0) {
    Write-Warn "Recon script exited with code $exitCode"
}

# ------- Retrieve Report -------
Write-Status "=== RETRIEVING RESULTS ==="

# Create reports directory if needed
if (-not (Test-Path $LocalReportDir)) {
    New-Item -ItemType Directory -Path $LocalReportDir -Force | Out-Null
}

# Find and copy report files
$reportFiles = docker exec $ContainerName bash -c "ls ${ContainerWorkDir}/*.md 2>/dev/null" 2>&1
if ($reportFiles -and ($reportFiles -notmatch "No such file")) {
    foreach ($remoteFile in ($reportFiles -split "`n")) {
        $remoteFile = $remoteFile.Trim()
        if ($remoteFile) {
            $localFile = Join-Path $LocalReportDir (Split-Path $remoteFile -Leaf)
            docker cp "${ContainerName}:${remoteFile}" $localFile 2>&1 | Out-Null
            Write-Success "Report saved: $localFile"
        }
    }
}
else {
    Write-Warn "No report files found in container"
}

# Copy raw data archive
$rawDirs = docker exec $ContainerName bash -c "ls -d ${ContainerWorkDir}/raw_* 2>/dev/null" 2>&1
if ($rawDirs -and ($rawDirs -notmatch "No such file")) {
    $rawArchive = Join-Path $LocalReportDir "raw_data_${Timestamp}.tar.gz"
    docker exec $ContainerName bash -c "cd ${ContainerWorkDir} && tar czf /tmp/raw_data.tar.gz raw_*/" 2>&1 | Out-Null
    docker cp "${ContainerName}:/tmp/raw_data.tar.gz" $rawArchive 2>&1 | Out-Null
    Write-Success "Raw data archive: $rawArchive"
}

# ------- Summary -------
Write-Host ""
Write-Host "+==============================================================+" -ForegroundColor Green
Write-Host "|  RECON PIPELINE COMPLETE                                      |" -ForegroundColor Green
Write-Host "+==============================================================+" -ForegroundColor Green
Write-Host ""
Write-Status "Reports directory: $LocalReportDir"
Write-Status "Container workspace: $ContainerWorkDir"
Write-Host ""

# Cleanup temp files
Remove-Item $arpCsvPath -Force -ErrorAction SilentlyContinue

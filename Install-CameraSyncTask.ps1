<#
.SYNOPSIS
    Installe ou desinstalle la tache planifiee Windows pour la sync photos.
.PARAMETER Uninstall
    Supprime la tache planifiee.
#>

param(
    [switch]$Uninstall
)

$TaskName = "SyncCameraPhotos"
$TaskDescription = "Sync automatique des photos appareil vers Google Drive"
$ScriptPath = Join-Path $PSScriptRoot "Sync-CameraPhotos.ps1"

if ($Uninstall) {
    Write-Host "Suppression de la tache '$TaskName'..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Tache supprimee." -ForegroundColor Green
    exit 0
}

if (-not (Test-Path $ScriptPath)) {
    Write-Host "ERREUR : Sync-CameraPhotos.ps1 introuvable dans : $PSScriptRoot" -ForegroundColor Red
    exit 1
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Installation - Sync Photos Appareil" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Activer le journal DriverFrameworks-UserMode pour detection future
try {
    $log = Get-WinEvent -ListLog "Microsoft-Windows-DriverFrameworks-UserMode/Operational" -ErrorAction Stop
    if (-not $log.IsEnabled) {
        $log.IsEnabled = $true
        $log.SaveChanges()
        Write-Host "Journal DriverFrameworks active." -ForegroundColor Green
    }
} catch {
    Write-Host "Note: Impossible d'activer DriverFrameworks (pas admin?)." -ForegroundColor Yellow
}

# Supprimer ancienne tache si elle existe
$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Tache existante trouvee - mise a jour..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Construire le XML complet de la tache planifiee
# Triggers multiples pour maximiser la detection:
#   1. Partition/Diagnostic EventID 1006 (toujours actif, se declenche quand un disque USB est connecte)
#   2. Kernel-PnP EventID 400 (periph PnP)
#   3. Au login utilisateur (pour les cas ou l'appareil est branche au demarrage)
$taskXml = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>$TaskDescription</Description>
  </RegistrationInfo>
  <Triggers>
    <EventTrigger>
      <Enabled>true</Enabled>
      <Subscription>&lt;QueryList&gt;&lt;Query Id="0" Path="Microsoft-Windows-Partition/Diagnostic"&gt;&lt;Select Path="Microsoft-Windows-Partition/Diagnostic"&gt;*[System[EventID=1006]]&lt;/Select&gt;&lt;/Query&gt;&lt;/QueryList&gt;</Subscription>
      <Delay>PT8S</Delay>
    </EventTrigger>
    <EventTrigger>
      <Enabled>true</Enabled>
      <Subscription>&lt;QueryList&gt;&lt;Query Id="0" Path="Microsoft-Windows-DriverFrameworks-UserMode/Operational"&gt;&lt;Select Path="Microsoft-Windows-DriverFrameworks-UserMode/Operational"&gt;*[System[EventID=2101]]&lt;/Select&gt;&lt;/Query&gt;&lt;/QueryList&gt;</Subscription>
      <Delay>PT8S</Delay>
    </EventTrigger>
    <LogonTrigger>
      <Enabled>true</Enabled>
      <UserId>$($env:USERDOMAIN)\$($env:USERNAME)</UserId>
      <Delay>PT30S</Delay>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>$($env:USERDOMAIN)\$($env:USERNAME)</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <ExecutionTimeLimit>PT30M</ExecutionTimeLimit>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>powershell.exe</Command>
      <Arguments>-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "$ScriptPath"</Arguments>
      <WorkingDirectory>$PSScriptRoot</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"@

try {
    Register-ScheduledTask -TaskName $TaskName -Xml $taskXml -Force | Out-Null
    Write-Host ""
    Write-Host "Tache planifiee installee avec succes !" -ForegroundColor Green
    Write-Host ""
    Write-Host "Configuration :" -ForegroundColor Cyan
    Write-Host "  Nom       : $TaskName"
    Write-Host "  Script    : $ScriptPath"
    Write-Host "  Triggers  : "
    Write-Host "    1. Partition/Diagnostic (EventID 1006) - detection disque USB"
    Write-Host "    2. DriverFrameworks (EventID 2101) - detection appareil USB"
    Write-Host "    3. Au demarrage de session Windows (apres 30s)"
    Write-Host ""
    Write-Host "Pour desinstaller : .\Install-CameraSyncTask.ps1 -Uninstall" -ForegroundColor DarkGray
    Write-Host "Pour tester       : .\Sync-CameraPhotos.ps1" -ForegroundColor DarkGray
} catch {
    Write-Host "ERREUR lors de l'installation : $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

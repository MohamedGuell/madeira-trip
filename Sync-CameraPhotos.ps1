<#
.SYNOPSIS
    Synchronise automatiquement les photos/vidéos d'un appareil photo vers Google Drive.
    Ne remplace JAMAIS les fichiers existants — n'ajoute que les nouveaux.

.DESCRIPTION
    Ce script :
    1. Détecte les disques amovibles contenant un dossier DCIM (appareil photo)
    2. Copie les nouvelles photos/vidéos vers G:\My Drive\photos
    3. Conserve la structure des sous-dossiers (100KWPZ2, etc.)
    4. Ne touche pas aux fichiers déjà présents sur le Drive
    5. Affiche un résumé de ce qui a été copié
    6. Écrit un log dans le même dossier que le script

.NOTES
    Auteur : Antigravity
    Date   : 2026-09-13
#>

# ============================================================
# CONFIGURATION — Modifiez ces valeurs si nécessaire
# ============================================================

# Dossier de destination sur Google Drive (via Drive for Desktop)
$DestinationRoot = "G:\My Drive\photos"

# Extensions de fichiers à synchroniser (photos + vidéos)
$Extensions = @("*.JPG", "*.JPEG", "*.PNG", "*.RAW", "*.ARW", "*.CR2", "*.CR3",
                "*.NEF", "*.DNG", "*.HEIF", "*.HEIC", "*.TIFF", "*.TIF",
                "*.MOV", "*.MP4", "*.AVI", "*.MTS")

# Fichier de log
$LogFile = Join-Path $PSScriptRoot "camera-sync.log"

# ============================================================
# FONCTIONS
# ============================================================

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $entry = "[$timestamp] $Message"
    Write-Host $entry
    Add-Content -Path $LogFile -Value $entry -Encoding UTF8
}

function Find-CameraDrives {
    <#
    .SYNOPSIS
        Trouve tous les disques amovibles qui contiennent un dossier DCIM.
    #>
    $cameraRoots = @()

    # Méthode 1 : Disques amovibles classiques (clé USB, lecteur de carte SD)
    $removableDrives = Get-WmiObject Win32_LogicalDisk | Where-Object {
        $_.DriveType -eq 2  # Removable
    }

    foreach ($drive in $removableDrives) {
        $dcimPath = Join-Path $drive.DeviceID "DCIM"
        if (Test-Path $dcimPath) {
            $cameraRoots += $dcimPath
            Write-Log "Appareil photo détecté sur $($drive.DeviceID) (disque amovible)"
        }
    }

    # Méthode 2 : Appareils PTP/MTP (certains appareils se montent différemment)
    # Vérifier aussi les lecteurs fixes qui ne sont pas C: ou G: (lecteur de carte intégré)
    $otherDrives = Get-WmiObject Win32_LogicalDisk | Where-Object {
        $_.DriveType -eq 3 -and  # Fixed
        $_.DeviceID -notin @("C:", "G:") -and
        $_.DeviceID -ne $null
    }

    foreach ($drive in $otherDrives) {
        $dcimPath = Join-Path $drive.DeviceID "DCIM"
        if (Test-Path $dcimPath) {
            $cameraRoots += $dcimPath
            Write-Log "Dossier DCIM trouvé sur $($drive.DeviceID) (disque fixe/lecteur carte)"
        }
    }

    return $cameraRoots
}

function Sync-Photos {
    param(
        [string]$SourceDCIM,
        [string]$Destination
    )

    $copiedCount = 0
    $skippedCount = 0
    $errorCount = 0
    $totalSize = 0

    # Parcourir tous les sous-dossiers DCIM (100KWPZ2, 101KWPZ2, etc.)
    $subfolders = Get-ChildItem -Path $SourceDCIM -Directory -ErrorAction SilentlyContinue

    if (-not $subfolders) {
        # Pas de sous-dossiers — chercher directement dans DCIM
        $subfolders = @([PSCustomObject]@{ FullName = $SourceDCIM; Name = "" })
    }

    foreach ($folder in $subfolders) {
        # Créer le sous-dossier de destination s'il n'existe pas
        if ($folder.Name) {
            $destSubfolder = Join-Path $Destination $folder.Name
        } else {
            $destSubfolder = $Destination
        }

        if (-not (Test-Path $destSubfolder)) {
            New-Item -ItemType Directory -Path $destSubfolder -Force | Out-Null
            Write-Log "Nouveau dossier créé : $destSubfolder"
        }

        # Trouver tous les fichiers photos/vidéos dans ce sous-dossier
        $files = @()
        foreach ($ext in $Extensions) {
            $files += Get-ChildItem -Path $folder.FullName -Filter $ext -File -ErrorAction SilentlyContinue
        }

        foreach ($file in $files) {
            $destFile = Join-Path $destSubfolder $file.Name

            if (Test-Path $destFile) {
                # Le fichier existe déjà — NE PAS remplacer
                $skippedCount++
            } else {
                # Nouveau fichier — copier
                try {
                    Copy-Item -Path $file.FullName -Destination $destFile -ErrorAction Stop
                    $copiedCount++
                    $totalSize += $file.Length
                    Write-Log "  + Copié : $($file.Name) ($([math]::Round($file.Length / 1MB, 1)) Mo)"
                } catch {
                    $errorCount++
                    Write-Log "  ! ERREUR pour $($file.Name) : $($_.Exception.Message)"
                }
            }
        }
    }

    return @{
        Copied  = $copiedCount
        Skipped = $skippedCount
        Errors  = $errorCount
        Size    = $totalSize
    }
}

# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

Write-Log "=========================================="
Write-Log "Démarrage de la synchronisation photos"
Write-Log "=========================================="

# Vérifier que le dossier de destination existe
if (-not (Test-Path $DestinationRoot)) {
    Write-Log "ERREUR : Le dossier de destination n'existe pas : $DestinationRoot"
    Write-Log "Vérifiez que Google Drive for Desktop est actif."
    exit 1
}

# Attendre quelques secondes pour que le disque soit bien monté
Start-Sleep -Seconds 3

# Chercher les appareils photos connectés
$cameraDrives = Find-CameraDrives

if ($cameraDrives.Count -eq 0) {
    Write-Log "Aucun appareil photo détecté (pas de dossier DCIM trouvé)."
    Write-Log "Branchez votre appareil photo ou insérez la carte SD, puis relancez."
    exit 0
}

# Synchroniser chaque appareil trouvé
$grandTotal = @{ Copied = 0; Skipped = 0; Errors = 0; Size = 0 }

foreach ($dcim in $cameraDrives) {
    Write-Log "Synchronisation depuis : $dcim"
    Write-Log "Destination : $DestinationRoot"
    Write-Log "------------------------------------------"

    $result = Sync-Photos -SourceDCIM $dcim -Destination $DestinationRoot

    $grandTotal.Copied  += $result.Copied
    $grandTotal.Skipped += $result.Skipped
    $grandTotal.Errors  += $result.Errors
    $grandTotal.Size    += $result.Size
}

# Résumé
Write-Log "=========================================="
Write-Log "RÉSUMÉ"
Write-Log "=========================================="
Write-Log "  Nouvelles photos copiées : $($grandTotal.Copied)"
Write-Log "  Photos déjà présentes   : $($grandTotal.Skipped) (non touchées)"
Write-Log "  Erreurs                 : $($grandTotal.Errors)"

if ($grandTotal.Size -gt 0) {
    $sizeMB = [math]::Round($grandTotal.Size / 1MB, 1)
    Write-Log "  Taille totale copiée    : $sizeMB Mo"
}

if ($grandTotal.Copied -gt 0) {
    Write-Log "Google Drive va synchroniser automatiquement les nouveaux fichiers."
}

Write-Log "=========================================="
Write-Log "Terminé !"
Write-Log "=========================================="

# Notification Windows (toast)
if ($grandTotal.Copied -gt 0) {
    $msg = "$($grandTotal.Copied) nouvelle(s) photo(s) copiée(s) vers Google Drive !"
} else {
    $msg = "Aucune nouvelle photo à copier. Tout est à jour !"
}

# Afficher une notification via BurntToast si disponible, sinon une popup simple
try {
    [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms") | Out-Null
    [System.Windows.Forms.MessageBox]::Show($msg, "Sync Photos Appareil", "OK", "Information") | Out-Null
} catch {
    Write-Host "`n$msg`n"
}

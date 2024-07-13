Echo 'Backup is under progress...'

$ConfirmPreference = "None"

$projectPath = "C:\Projects\Pharmacy"
$backupPath = "C:\Projects\Pharmacy\pharmacy_backend\app\backups"
$destinationPaths = @("C:\Projects\Pharmacy\backups\1", "C:\Projects\Pharmacy\backups\2", "C:\Projects\Pharmacy\backups\3")

& $projectPath\env\Scripts\activate.ps1

Set-Location $projectPath\Pharmacy_backend

Echo '1. Backup database...'
python manage.py dbbackup --clean

# Verify the directory to be zipped
$mediaPath = "$projectPath\Pharmacy_backend\frontend\public\dist"
if (Test-Path $mediaPath) {
    $mediaFiles = Get-ChildItem -Path $mediaPath
    if ($mediaFiles.Count -gt 0) {
        Echo '2. Backup and Compressing Media ...'
        Compress-Archive -Path $mediaPath\* -DestinationPath "$backupPath\media_backup.zip" -Force
    } else {
        Echo "Warning: Media directory is empty. No files to zip."
    }
} else {
    Echo "Error: Media directory does not exist. Path: $mediaPath"
    exit 1
}

# Verify the zip file creation
$zipPath = "$backupPath\media_backup.zip"
if (Test-Path $zipPath) {
    Echo '3. Copy Files to Directories ...'
    foreach ($destination in $destinationPaths) {
        # Clean the destination directory
        if (Test-Path $destination) {
            Get-ChildItem -Path $destination -Recurse | Remove-Item -Force -Recurse -Confirm:$false
        } else {
            New-Item -Path $destination -ItemType Directory
        }

        # Copy the backup directory to the destination
        Copy-Item -Path $backupPath -Destination $destination -Recurse -Force -Container
    }
    Echo 'Backup Progress was successful!'
} else {
    Echo "Error: Zip file was not created. Path: $zipPath"
    exit 1
}
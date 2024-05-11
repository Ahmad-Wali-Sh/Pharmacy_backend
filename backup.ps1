Echo 'Backup is under progress...'

$ConfirmPreference = "None"

$projectPath = "C:\Projects\Pharmacy"
$backupPath = "C:\Projects\Pharmacy\pharmacy_backend\app\backups"
$destinationPaths = @("C:\Projects\Pharmacy\backups\1", "C:\Projects\Pharmacy\backups\2", "C:\Projects\Pharmacy\backups\3")

& $projectPath\env\Scripts\activate.ps1


Set-Location $projectPath\pharmacy_backend

Echo '1. Backup database...'
Echo '2. Backup and Compressing Media ...'

python manage.py dbbackup --clean

# Zip media files
Echo '2. Backup and Compressing Media ...'
Compress-Archive -Path "$projectPath\pharmacy_backend\frontend\public" -DestinationPath "$backupPath\media_backup.zip" -Force

# Copy the backup directory to the destinations
Echo '3. Copy Files to Directories ...'
foreach ($destination in $destinationPaths) {
    Get-ChildItem -Path $destination -Recurse | Remove-Item -Force -Recurse -Confirm:$false

    Copy-Item -Path $backupPath -Destination $destination -Recurse -Force -Container
}


Echo 'Backup Progress was successful!'



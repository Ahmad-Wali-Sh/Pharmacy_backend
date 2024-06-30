Echo 'Backup is under progress...'

$ConfirmPreference = "None"

$projectPath = "D:\Sharif_Pharmacy_Platform"
$backupPath = "D:\Sharif_Pharmacy_Platform\Pharmacy_backend\app\backups"
$destinationPaths = @("D:\Sharif_Pharmacy_Platform\Backups\1", "F:\USB Backup", "D:\Sharif_Pharmacy_Platform\Backups\3")

& $projectPath\env\Scripts\activate.ps1


Set-Location $projectPath\Pharmacy_backend

Echo '1. Backup database...'
Echo '2. Backup and Compressing Media ...'

python manage.py dbbackup --clean

# Zip media files
Echo '2. Backup and Compressing Media ...'
Compress-Archive -Path "$projectPath\Pharmacy_backend\frontend\public\dist" -DestinationPath "$backupPath\media_backup.zip" 

# Copy the backup directory to the destinations
Echo '3. Copy Files to Directories ...'
foreach ($destination in $destinationPaths) {
    Get-ChildItem -Path $destination -Recurse | Remove-Item -Force -Recurse -Confirm:$false

    Copy-Item -Path $backupPath -Destination $destination -Recurse -Force -Container
}


Echo 'Backup Progress was successful!'



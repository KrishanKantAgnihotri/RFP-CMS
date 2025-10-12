# PowerShell script to download and install MongoDB Community Edition on Windows

# Configuration
$mongoVersion = "7.0.5"
$downloadUrl = "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-$mongoVersion-signed.msi"
$downloadPath = "$env:TEMP\mongodb-$mongoVersion.msi"
$installPath = "C:\Program Files\MongoDB\Server\$mongoVersion"
$dataPath = "C:\data\db"
$logPath = "C:\data\log"

# Create necessary directories
Write-Host "Creating data and log directories..."
New-Item -ItemType Directory -Force -Path $dataPath | Out-Null
New-Item -ItemType Directory -Force -Path $logPath | Out-Null

# Download MongoDB installer
Write-Host "Downloading MongoDB installer..."
Invoke-WebRequest -Uri $downloadUrl -OutFile $downloadPath

# Install MongoDB
Write-Host "Installing MongoDB..."
Start-Process msiexec.exe -ArgumentList "/i `"$downloadPath`" /quiet INSTALLLOCATION=`"$installPath`"" -Wait

# Create MongoDB configuration file
$configContent = @"
storage:
  dbPath: $dataPath
systemLog:
  destination: file
  path: $logPath\mongod.log
  logAppend: true
net:
  bindIp: 127.0.0.1
  port: 27017
"@

$configPath = "$env:ProgramData\MongoDB\mongod.cfg"
Write-Host "Creating MongoDB configuration file at $configPath..."
New-Item -ItemType File -Force -Path $configPath | Out-Null
Set-Content -Path $configPath -Value $configContent

# Install MongoDB as a service
Write-Host "Installing MongoDB as a service..."
& "$installPath\bin\mongod.exe" --config "$configPath" --install

# Start MongoDB service
Write-Host "Starting MongoDB service..."
Start-Service MongoDB

# Verify installation
Write-Host "Verifying MongoDB installation..."
$mongoService = Get-Service -Name MongoDB -ErrorAction SilentlyContinue
if ($mongoService -and $mongoService.Status -eq "Running") {
    Write-Host "MongoDB has been successfully installed and is running."
} else {
    Write-Host "MongoDB installation may have failed. Please check the logs."
}

# Clean up
Write-Host "Cleaning up..."
Remove-Item -Path $downloadPath -Force

Write-Host "MongoDB installation completed!"

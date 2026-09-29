$ErrorActionPreference = "SilentlyContinue"
Unregister-ScheduledTask -TaskName "Lucid Screenshot Organizer" -Confirm:$false
Write-Host "Removed startup task. Repository, screenshots, config, and logs were not deleted."
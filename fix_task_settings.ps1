$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 10)
Set-ScheduledTask -TaskName 'Q3SiteDailyNews' -Settings $settings | Out-Null
(Get-ScheduledTask -TaskName 'Q3SiteDailyNews').Settings | Select-Object StartWhenAvailable, AllowStartIfOnBatteries, DontStopIfGoingOnBatteries, ExecutionTimeLimit | Format-List

param(
    [string]$PrinterName = "ACARS Virtual Printer",
    [string]$PortName = "IP_127.0.0.1_ACARS_VP"
)

$ErrorActionPreference = "Stop"

$existingPrinter = Get-Printer -Name $PrinterName -ErrorAction SilentlyContinue
if ($existingPrinter) {
    Remove-Printer -Name $PrinterName
    Write-Host "Removed printer '$PrinterName'."
}
else {
    Write-Host "Printer '$PrinterName' was not found."
}

$existingPort = Get-PrinterPort -Name $PortName -ErrorAction SilentlyContinue
if ($existingPort) {
    Remove-PrinterPort -Name $PortName
    Write-Host "Removed printer port '$PortName'."
}
else {
    Write-Host "Printer port '$PortName' was not found."
}

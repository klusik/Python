param(
    [string]$PrinterName = "ACARS Virtual Printer",
    [string]$DriverName = "Generic / Text Only",
    [string]$PortName = "IP_127.0.0.1_ACARS_VP",
    [string]$PrinterHostAddress = "127.0.0.1",
    [int]$PortNumber = 9100
)

$ErrorActionPreference = "Stop"

Write-Host "Installing Windows printer '$PrinterName'..."
Write-Host "This may require administrator rights."

$existingPort = Get-PrinterPort -Name $PortName -ErrorAction SilentlyContinue
if (-not $existingPort) {
    Add-PrinterPort -Name $PortName -PrinterHostAddress $PrinterHostAddress -PortNumber $PortNumber
    Write-Host "Created printer port '$PortName'."
}
else {
    Write-Host "Printer port '$PortName' already exists."
}

$existingDriver = Get-PrinterDriver -Name $DriverName -ErrorAction SilentlyContinue
if (-not $existingDriver) {
    throw "Printer driver '$DriverName' is not installed. Add the built-in Generic / Text Only driver first through Windows print management if needed."
}

$existingPrinter = Get-Printer -Name $PrinterName -ErrorAction SilentlyContinue
if (-not $existingPrinter) {
    Add-Printer -Name $PrinterName -DriverName $DriverName -PortName $PortName
    Write-Host "Created printer '$PrinterName'."
}
else {
    Write-Host "Printer '$PrinterName' already exists."
}

Write-Host "Done. You should now see '$PrinterName' in Windows printers."

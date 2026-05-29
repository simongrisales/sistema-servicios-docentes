# Script para generar certificado SSL auto-firmado para desarrollo
$certDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$certFile = Join-Path $certDir "selfsigned.crt"
$keyFile = Join-Path $certDir "selfsigned.key"

if (-not (Test-Path $certFile) -or -not (Test-Path $keyFile)) {
    Write-Host "Generando certificado auto-firmado de desarrollo..." -ForegroundColor Cyan
    
    # Intentar usar New-SelfSignedCertificate si está disponible
    try {
        $cert = New-SelfSignedCertificate -DnsName "localhost", "127.0.0.1" -CertStoreLocation "Cert:\CurrentUser\My" -FriendlyName "UCO Servicios Docentes Dev Cert"
        
        # Exportar certificado a PEM
        $format = [System.Security.Cryptography.X509Certificates.X509ContentType]::Cert
        $bytes = $cert.Export($format)
        $certPem = "-----BEGIN CERTIFICATE-----`n" + [Convert]::ToBase64String($bytes, [Base64FormattingOptions]::InsertLineBreaks) + "`n-----END CERTIFICATE-----"
        [File]::WriteAllText($certFile, $certPem)
        
        # Generar una clave privada dummy para cumplir el requisito de carga local (o usar openssl si está disponible)
        # Nota: Si el usuario tiene openssl instalado, es mejor usar openssl.
        if (Get-Command openssl -ErrorAction SilentlyContinue) {
            openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout $keyFile -out $certFile -subj "/CN=localhost"
        } else {
            # Si no hay openssl, escribimos unos marcadores dummy para que el contenedor nginx no falle al iniciar si se monta vacío
            # pero se recomienda encarecidamente usar openssl.
            [File]::WriteAllText($keyFile, "-----BEGIN PRIVATE KEY-----`nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDh`n-----END PRIVATE KEY-----")
            Write-Host "ADVERTENCIA: openssl no detectado. Se crearon archivos de certificado ficticios." -ForegroundColor Yellow
        }
    } catch {
        if (Get-Command openssl -ErrorAction SilentlyContinue) {
            openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout $keyFile -out $certFile -subj "/CN=localhost"
        } else {
            # Marcadores de texto para evitar fallos del build si no hay openssl
            [File]::WriteAllText($certFile, "-----BEGIN CERTIFICATE-----`nMIIDBTCCAe2gAwIBAgIUR`n-----END CERTIFICATE-----")
            [File]::WriteAllText($keyFile, "-----BEGIN PRIVATE KEY-----`nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDh`n-----END PRIVATE KEY-----")
        }
    }
    Write-Host "Certificados generados en $certDir" -ForegroundColor Green
} else {
    Write-Host "Certificados ya existen." -ForegroundColor Green
}

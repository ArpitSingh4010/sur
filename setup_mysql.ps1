# 🏥 ClaimEase MySQL Setup PowerShell Script

Write-Host "🏥 ClaimEase MySQL Schema Setup" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Check if MySQL is installed
Write-Host "`n📋 Checking MySQL installation..." -ForegroundColor Yellow

$mysqlPath = Get-Command mysql -ErrorAction SilentlyContinue
if ($mysqlPath) {
    Write-Host "✅ MySQL found at: $($mysqlPath.Source)" -ForegroundColor Green
} else {
    Write-Host "❌ MySQL not found in PATH" -ForegroundColor Red
    Write-Host "Please install MySQL or XAMPP first:" -ForegroundColor Yellow
    Write-Host "  - MySQL: https://dev.mysql.com/downloads/mysql/" -ForegroundColor Cyan
    Write-Host "  - XAMPP: https://www.apachefriends.org/" -ForegroundColor Cyan
    exit 1
}

# Get MySQL credentials
Write-Host "`n🔐 MySQL Connection Setup" -ForegroundColor Yellow
$username = Read-Host "Enter MySQL username (default: root)"
if ([string]::IsNullOrEmpty($username)) {
    $username = "root"
}

$password = Read-Host "Enter MySQL password" -AsSecureString
$plainPassword = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))

# Test MySQL connection
Write-Host "`n🔗 Testing MySQL connection..." -ForegroundColor Yellow
$testCommand = "mysql -u $username -p$plainPassword -e 'SELECT VERSION();'"
try {
    $result = Invoke-Expression $testCommand 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ MySQL connection successful!" -ForegroundColor Green
    } else {
        Write-Host "❌ MySQL connection failed!" -ForegroundColor Red
        Write-Host $result -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Error connecting to MySQL: $_" -ForegroundColor Red
    exit 1
}

# Create the database schema
Write-Host "`n🏗️ Creating ClaimEase database schema..." -ForegroundColor Yellow
$schemaFile = "create_schema_simple.sql"

if (Test-Path $schemaFile) {
    $createCommand = "mysql -u $username -p$plainPassword < $schemaFile"
    try {
        Invoke-Expression $createCommand
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Database schema created successfully!" -ForegroundColor Green
        } else {
            Write-Host "❌ Error creating schema!" -ForegroundColor Red
            exit 1
        }
    } catch {
        Write-Host "❌ Error executing schema file: $_" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "❌ Schema file '$schemaFile' not found!" -ForegroundColor Red
    Write-Host "Please ensure the file exists in the current directory." -ForegroundColor Yellow
    exit 1
}

# Verify schema creation
Write-Host "`n✅ Verifying schema creation..." -ForegroundColor Yellow
$verifyCommand = "mysql -u $username -p$plainPassword claimease -e 'SHOW TABLES;'"
try {
    $tables = Invoke-Expression $verifyCommand
    Write-Host "📋 Tables created:" -ForegroundColor Green
    Write-Host $tables -ForegroundColor Cyan
} catch {
    Write-Host "❌ Error verifying schema: $_" -ForegroundColor Red
}

# Show hospital data sample
Write-Host "`n📊 Sample hospital data:" -ForegroundColor Yellow
$dataCommand = "mysql -u $username -p$plainPassword claimease -e 'SELECT state_name, public_hospitals_count, private_hospitals_count FROM Hospital_States LIMIT 5;'"
try {
    $data = Invoke-Expression $dataCommand
    Write-Host $data -ForegroundColor Cyan
} catch {
    Write-Host "❌ Error retrieving data: $_" -ForegroundColor Red
}

Write-Host "`n🎉 ClaimEase MySQL schema setup complete!" -ForegroundColor Green
Write-Host "You can now:" -ForegroundColor Yellow
Write-Host "  1. Run: python flask_api.py" -ForegroundColor Cyan
Write-Host "  2. Open: index.html in your browser" -ForegroundColor Cyan
Write-Host "  3. Access API at: http://localhost:5000/api" -ForegroundColor Cyan

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
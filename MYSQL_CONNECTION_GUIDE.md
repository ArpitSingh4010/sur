# 🔗 MySQL Server Connection Guide

## Method 1: Install MySQL Server (Official)

### Download and Install:
1. Go to: https://dev.mysql.com/downloads/mysql/
2. Download "MySQL Installer for Windows"
3. Run installer and choose "Server only" or "Full"
4. Set root password during installation (REMEMBER THIS!)
5. Complete installation

### Start MySQL Service:
```powershell
# Check if MySQL service is running
Get-Service -Name "MySQL*"

# Start MySQL service if stopped
Start-Service -Name "MySQL80"  # or MySQL57, MySQL81 depending on version
```

## Method 2: Install XAMPP (Easier for Development)

### Download and Install:
1. Go to: https://www.apachefriends.org/
2. Download XAMPP for Windows
3. Install XAMPP
4. Open XAMPP Control Panel
5. Click "Start" next to MySQL

### XAMPP MySQL Details:
- **Host**: localhost
- **Port**: 3306
- **Username**: root
- **Password**: (empty by default)

## Step 2: Connect to MySQL

### Option A: Command Line
```bash
# Open PowerShell or Command Prompt
mysql -u root -p
# Enter password when prompted
```

### Option B: MySQL Workbench (GUI)
1. Download from: https://dev.mysql.com/downloads/workbench/
2. Install MySQL Workbench
3. Open Workbench
4. Click "+" to create new connection
5. Enter connection details:
   - Connection Name: Local MySQL
   - Hostname: localhost
   - Port: 3306
   - Username: root
   - Password: [your password]

### Option C: phpMyAdmin (if using XAMPP)
1. Start XAMPP
2. Start MySQL service
3. Open browser: http://localhost/phpmyadmin
4. Login (usually no password required for XAMPP)

## Step 3: Test Connection

### In Command Line:
```sql
-- Test connection
mysql> SELECT VERSION();
mysql> SHOW DATABASES;
mysql> EXIT;
```

### Common Connection Issues:

#### Issue 1: "mysql command not found"
```powershell
# Add MySQL to PATH
# 1. Find MySQL installation (usually C:\Program Files\MySQL\MySQL Server 8.0\bin)
# 2. Add to Windows PATH environment variable
# 3. Restart PowerShell

# Or use full path:
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

#### Issue 2: "Access denied for user 'root'"
- Check if you're using the correct password
- Try connecting without password first
- Reset root password if forgotten

#### Issue 3: "Can't connect to MySQL server"
```powershell
# Check if MySQL service is running
Get-Service -Name "MySQL*"

# Start the service
Start-Service -Name "MySQL80"

# Check if port 3306 is open
netstat -an | findstr "3306"
```

## Step 4: Create ClaimEase Database

Once connected, run:
```sql
-- Create database
CREATE DATABASE claimease;

-- Use database
USE claimease;

-- Run schema file
SOURCE create_schema_simple.sql;

-- Verify
SHOW TABLES;
```
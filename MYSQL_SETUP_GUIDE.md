# 🗄️ MySQL Schema Creation Guide for ClaimEase

## Step 1: Install MySQL

### For Windows:
1. Download MySQL from: https://dev.mysql.com/downloads/mysql/
2. Download MySQL Installer for Windows
3. Run the installer and choose "Full" installation
4. Set up root password during installation
5. Install MySQL Workbench (GUI tool)

### Alternative - Using XAMPP (Easier):
1. Download XAMPP from: https://www.apachefriends.org/
2. Install XAMPP (includes MySQL)
3. Start MySQL from XAMPP Control Panel

## Step 2: Access MySQL

### Using Command Line:
```bash
# Open Command Prompt or PowerShell as Administrator
mysql -u root -p
# Enter your MySQL password when prompted
```

### Using MySQL Workbench:
1. Open MySQL Workbench
2. Click on your local MySQL connection
3. Enter password

## Step 3: Create the Database

```sql
-- Create the database
CREATE DATABASE IF NOT EXISTS claimease;

-- Use the database
USE claimease;

-- Verify database creation
SHOW DATABASES;
```

## Step 4: Create Tables (Schema)

### Method A: Run the SQL file directly
```bash
# From command line (outside MySQL)
mysql -u root -p claimease < claimease_schema.sql
```

### Method B: Copy-paste in MySQL Workbench
1. Open claimease_schema.sql in a text editor
2. Copy all content
3. Paste in MySQL Workbench Query tab
4. Click Execute

### Method C: Step by step in MySQL command line
```sql
-- 1. Create Insurance Companies table
CREATE TABLE Insurance_Companies (
    company_id INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(100) NOT NULL,
    helpline VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(100),
    registration_number VARCHAR(50),
    established_date DATE,
    headquarters VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Create Policies table
CREATE TABLE Policies (
    policy_id INT PRIMARY KEY AUTO_INCREMENT,
    policy_name VARCHAR(150) NOT NULL,
    policy_number VARCHAR(50) UNIQUE,
    company_id INT,
    coverage_amount DECIMAL(15,2),
    premium DECIMAL(10,2),
    deductible DECIMAL(10,2),
    policy_type VARCHAR(50),
    description TEXT,
    terms_conditions TEXT,
    validity_period INT,
    waiting_period INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES Insurance_Companies(company_id)
);

-- Continue with all other tables...
```

## Step 5: Verify Schema Creation

```sql
-- Check all tables in the database
SHOW TABLES;

-- Check table structure
DESCRIBE Insurance_Companies;
DESCRIBE Policies;
DESCRIBE Users;
DESCRIBE Claims;

-- Check if foreign keys are created
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'claimease'
AND REFERENCED_TABLE_NAME IS NOT NULL;
```

## Step 6: Insert Sample Data

```sql
-- Insert sample insurance companies
INSERT INTO Insurance_Companies (company_name, helpline, email, website) VALUES
('HDFC ERGO Health Insurance', '1800-266-0625', 'info@hdfcergo.com', 'www.hdfcergo.com'),
('ICICI Lombard General Insurance', '1800-266-7766', 'care@icicilombard.com', 'www.icicilombard.com'),
('Star Health Insurance', '1800-425-2255', 'info@starhealth.in', 'www.starhealth.in'),
('New India Assurance', '1800-209-1415', 'info@newindia.co.in', 'www.newindia.co.in');

-- Verify data insertion
SELECT * FROM Insurance_Companies;
```

## Quick Commands Summary:

```bash
# 1. Start MySQL
mysql -u root -p

# 2. Create and use database
CREATE DATABASE claimease;
USE claimease;

# 3. Run schema file
SOURCE claimease_schema.sql;

# 4. Check tables
SHOW TABLES;

# 5. Exit MySQL
EXIT;
```

## Common Issues & Solutions:

### Issue 1: "Access Denied"
```bash
# Solution: Check MySQL is running
# In XAMPP: Start MySQL service
# In Windows Services: Start MySQL80 service
```

### Issue 2: "Database exists"
```sql
-- Solution: Drop and recreate
DROP DATABASE IF EXISTS claimease;
CREATE DATABASE claimease;
```

### Issue 3: "Foreign key constraint fails"
```sql
-- Solution: Create tables in correct order
-- 1. Insurance_Companies first
-- 2. Policies (references Insurance_Companies)
-- 3. Users, Hospitals
-- 4. Claims (references Users, Hospitals, Policies)
-- 5. Other dependent tables
```

## Visual Schema Check:

```sql
-- Get table relationships
SELECT 
    CONCAT(table_name, '.', column_name) as 'Foreign Key',
    CONCAT(referenced_table_name, '.', referenced_column_name) as 'References'
FROM information_schema.key_column_usage
WHERE referenced_table_name IS NOT NULL
    AND table_schema = 'claimease';
```
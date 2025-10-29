# 🏥 ClaimEase MySQL Schema Setup Guide

## Step 1: Install MySQL
1. Download MySQL from https://dev.mysql.com/downloads/mysql/
2. Install MySQL Server and MySQL Workbench
3. Set up root password during installation

## Step 2: Create the Database Schema
```sql
-- Method 1: Using MySQL Command Line
mysql -u root -p
mysql> SOURCE claimease_schema.sql;
mysql> exit;

-- Method 2: Using MySQL Workbench
-- Open MySQL Workbench → File → Run SQL Script → Select claimease_schema.sql
```

## Step 3: Import Your Hospital Data
```bash
# Run the Python setup script
python setup_database.py
```

## Step 4: Verify Schema Creation
```sql
-- Check if database exists
SHOW DATABASES;

-- Use the database
USE claimease;

-- Check all tables
SHOW TABLES;

-- Check table structure
DESCRIBE Users;
DESCRIBE Claims;
DESCRIBE Hospital_States;

-- Check your imported data
SELECT * FROM Hospital_States LIMIT 5;
```

## Schema Structure Visualization:

```
claimease (DATABASE)
├── Insurance_Companies
├── Policies ──────┐
├── Users ─────────┼─── Claims ─── Documents
├── Hospitals ─────┘       │
├── Hospital_States        │
├── Admins ────────────────┘
├── Hospital_Insurance_Empanelment
├── Claim_Status_History
└── Pre_Authorization
```

## Your Data in the Schema:
- **Hospital_States table** contains your 32 states/UTs data
- **Public hospitals:** 3,147,691 total
- **Private hospitals:** 866,622 total
- **Financial data:** Amounts in crores by state

## Benefits of This Schema:
✅ **Normalized Design** - No data redundancy
✅ **Scalable** - Can handle millions of records
✅ **Secure** - Proper constraints and relationships
✅ **Flexible** - Easy to add new features
✅ **Your Data Integrated** - Hospital statistics built-in

## Next Steps:
1. Run `mysql -u root -p < claimease_schema.sql`
2. Run `python setup_database.py`
3. Start using the ClaimEase system!
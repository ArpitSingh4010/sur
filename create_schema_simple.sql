-- 🏥 ClaimEase MySQL Schema Creation Script
-- Run this script step by step in MySQL

-- ======================================
-- STEP 1: CREATE DATABASE
-- ======================================
CREATE DATABASE IF NOT EXISTS claimease;
USE claimease;

-- ======================================
-- STEP 2: CREATE CORE TABLES
-- ======================================

-- Insurance Companies (Must be created first)
CREATE TABLE Insurance_Companies (
    company_id INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(100) NOT NULL,
    helpline VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Policies (References Insurance_Companies)
CREATE TABLE Policies (
    policy_id INT PRIMARY KEY AUTO_INCREMENT,
    policy_name VARCHAR(150) NOT NULL,
    policy_number VARCHAR(50) UNIQUE,
    company_id INT,
    coverage_amount DECIMAL(15,2),
    premium DECIMAL(10,2),
    policy_type VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES Insurance_Companies(company_id)
);

-- Users/Policyholders
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    date_of_birth DATE,
    policy_id INT,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (policy_id) REFERENCES Policies(policy_id)
);

-- Hospitals
CREATE TABLE Hospitals (
    hospital_id INT PRIMARY KEY AUTO_INCREMENT,
    hospital_name VARCHAR(150) NOT NULL,
    hospital_type ENUM('Public', 'Private') NOT NULL,
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    contact_number VARCHAR(15),
    email VARCHAR(100),
    bed_capacity INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Claims (References Users, Hospitals, Policies)
CREATE TABLE Claims (
    claim_id INT PRIMARY KEY AUTO_INCREMENT,
    claim_number VARCHAR(50) UNIQUE,
    user_id INT,
    hospital_id INT,
    policy_id INT,
    claim_type ENUM('Cashless', 'Reimbursement') NOT NULL,
    claim_date DATE DEFAULT (CURRENT_DATE),
    claim_status ENUM('Pending', 'Under Review', 'Approved', 'Rejected') DEFAULT 'Pending',
    claim_amount DECIMAL(15,2),
    approved_amount DECIMAL(15,2),
    diagnosis TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (hospital_id) REFERENCES Hospitals(hospital_id),
    FOREIGN KEY (policy_id) REFERENCES Policies(policy_id)
);

-- Hospital State Statistics (Your CSV data)
CREATE TABLE Hospital_States (
    state_id INT PRIMARY KEY AUTO_INCREMENT,
    state_name VARCHAR(100) NOT NULL,
    public_hospitals_count INT,
    public_hospitals_amount DECIMAL(10,2),
    private_hospitals_count INT,
    private_hospitals_amount DECIMAL(10,2)
);

-- ======================================
-- STEP 3: INSERT SAMPLE DATA
-- ======================================

-- Insert Insurance Companies
INSERT INTO Insurance_Companies (company_name, helpline, email, website) VALUES
('HDFC ERGO Health Insurance', '1800-266-0625', 'info@hdfcergo.com', 'www.hdfcergo.com'),
('ICICI Lombard General Insurance', '1800-266-7766', 'care@icicilombard.com', 'www.icicilombard.com'),
('Star Health Insurance', '1800-425-2255', 'info@starhealth.in', 'www.starhealth.in'),
('New India Assurance', '1800-209-1415', 'info@newindia.co.in', 'www.newindia.co.in');

-- Insert Sample Policies
INSERT INTO Policies (policy_name, policy_number, company_id, coverage_amount, premium, policy_type) VALUES
('HDFC Health Suraksha', 'HDFC-HS-001', 1, 500000.00, 15000.00, 'Individual'),
('ICICI Complete Health Guard', 'ICICI-CHG-001', 2, 1000000.00, 25000.00, 'Family'),
('Star Comprehensive Policy', 'STAR-CIP-001', 3, 300000.00, 12000.00, 'Individual'),
('New India Mediclaim', 'NIA-MCP-001', 4, 200000.00, 8000.00, 'Individual');

-- Insert Sample Hospitals
INSERT INTO Hospitals (hospital_name, hospital_type, city, state, contact_number, bed_capacity) VALUES
('Apollo Hospital Delhi', 'Private', 'New Delhi', 'Delhi', '011-26925858', 500),
('AIIMS New Delhi', 'Public', 'New Delhi', 'Delhi', '011-26588500', 2500),
('Fortis Hospital Mumbai', 'Private', 'Mumbai', 'Maharashtra', '022-61769999', 400),
('KEM Hospital Mumbai', 'Public', 'Mumbai', 'Maharashtra', '022-24136051', 1800),
('Manipal Hospital Bangalore', 'Private', 'Bangalore', 'Karnataka', '080-25023030', 650);

-- Insert Hospital State Data (Your CSV data)
INSERT INTO Hospital_States (state_name, public_hospitals_count, public_hospitals_amount, private_hospitals_count, private_hospitals_amount) VALUES
('Andaman and Nicobar Islands', 8, 0.01, 2, 0.00),
('Andhra Pradesh', 660094, 693.57, 305840, 404.17),
('Arunachal Pradesh', 957, 1.30, 9, 0.01),
('Assam', 82154, 97.84, 5866, 7.30),
('Bihar', 33699, 34.92, 1268, 0.99),
('Chandigarh', 105, 0.11, 13, 0.02),
('Chhattisgarh', 214498, 281.48, 92219, 142.70),
('Gujarat', 36898, 40.04, 72465, 83.71),
('Haryana', 41722, 34.39, 2308, 3.10),
('Karnataka', 903417, 337.77, 22361, 20.49),
('Kerala', 85627, 78.37, 78834, 83.53),
('Maharashtra', 4366, 5.39, 7594, 11.22),
('Tamil Nadu', 35389, 58.22, 6436, 12.61),
('Uttar Pradesh', 60742, 67.62, 11987, 13.13);

-- ======================================
-- STEP 4: VERIFY CREATION
-- ======================================

-- Show all tables
SHOW TABLES;

-- Check table data
SELECT COUNT(*) as 'Insurance Companies' FROM Insurance_Companies;
SELECT COUNT(*) as 'Policies' FROM Policies;
SELECT COUNT(*) as 'Hospitals' FROM Hospitals;
SELECT COUNT(*) as 'States' FROM Hospital_States;

-- Show your hospital data
SELECT 
    state_name,
    public_hospitals_count,
    private_hospitals_count,
    (public_hospitals_count + private_hospitals_count) as total_hospitals
FROM Hospital_States 
ORDER BY total_hospitals DESC 
LIMIT 5;

-- ======================================
-- SUCCESS MESSAGE
-- ======================================
SELECT 'ClaimEase Schema Created Successfully!' as Status;
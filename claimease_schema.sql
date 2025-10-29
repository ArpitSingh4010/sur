-- ClaimEase Database Schema
-- Health Insurance Claims Management System

-- Create database
CREATE DATABASE IF NOT EXISTS claimease;
USE claimease;

-- 1. Insurance Companies Table
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

-- 2. Policies Table
CREATE TABLE Policies (
    policy_id INT PRIMARY KEY AUTO_INCREMENT,
    policy_name VARCHAR(150) NOT NULL,
    policy_number VARCHAR(50) UNIQUE,
    company_id INT,
    coverage_amount DECIMAL(15,2),
    premium DECIMAL(10,2),
    deductible DECIMAL(10,2),
    policy_type VARCHAR(50), -- Individual, Family, Group, Senior Citizen
    description TEXT,
    terms_conditions TEXT,
    validity_period INT, -- in years
    waiting_period INT, -- in days
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES Insurance_Companies(company_id)
);

-- 3. Users/Policyholders Table
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(10),
    date_of_birth DATE,
    gender ENUM('Male', 'Female', 'Other'),
    aadhar_number VARCHAR(12),
    pan_number VARCHAR(10),
    policy_id INT,
    policy_start_date DATE,
    policy_end_date DATE,
    nominee_name VARCHAR(100),
    nominee_relation VARCHAR(50),
    password_hash VARCHAR(255),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (policy_id) REFERENCES Policies(policy_id)
);

-- 4. Hospital States Data (from your CSV)
CREATE TABLE Hospital_States (
    state_id INT PRIMARY KEY AUTO_INCREMENT,
    state_name VARCHAR(100) NOT NULL,
    public_hospitals_count INT,
    public_hospitals_amount DECIMAL(10,2),
    private_hospitals_count INT,
    private_hospitals_amount DECIMAL(10,2)
);

-- 5. Hospitals Table
CREATE TABLE Hospitals (
    hospital_id INT PRIMARY KEY AUTO_INCREMENT,
    hospital_name VARCHAR(150) NOT NULL,
    hospital_type ENUM('Public', 'Private') NOT NULL,
    registration_number VARCHAR(50),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(10),
    contact_number VARCHAR(15),
    email VARCHAR(100),
    website VARCHAR(100),
    specializations TEXT, -- JSON array of specializations
    bed_capacity INT,
    accreditation VARCHAR(100), -- NABH, JCI, etc.
    empaneled_insurers TEXT, -- JSON array of insurance company IDs
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 6. Hospital Insurance Empanelment (Many-to-Many relationship)
CREATE TABLE Hospital_Insurance_Empanelment (
    empanelment_id INT PRIMARY KEY AUTO_INCREMENT,
    hospital_id INT,
    company_id INT,
    empanelment_date DATE,
    cashless_available BOOLEAN DEFAULT TRUE,
    reimbursement_available BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hospital_id) REFERENCES Hospitals(hospital_id),
    FOREIGN KEY (company_id) REFERENCES Insurance_Companies(company_id),
    UNIQUE KEY unique_empanelment (hospital_id, company_id)
);

-- 7. Claims Table
CREATE TABLE Claims (
    claim_id INT PRIMARY KEY AUTO_INCREMENT,
    claim_number VARCHAR(50) UNIQUE,
    user_id INT,
    hospital_id INT,
    policy_id INT,
    claim_type ENUM('Cashless', 'Reimbursement') NOT NULL,
    treatment_type VARCHAR(100),
    admission_date DATE,
    discharge_date DATE,
    claim_date DATE DEFAULT (CURRENT_DATE),
    claim_status ENUM('Pending', 'Under Review', 'Approved', 'Rejected', 'Settled') DEFAULT 'Pending',
    claim_amount DECIMAL(15,2),
    approved_amount DECIMAL(15,2),
    rejected_reason TEXT,
    settlement_date DATE,
    diagnosis TEXT,
    treatment_details TEXT,
    doctor_name VARCHAR(100),
    room_type VARCHAR(50),
    is_emergency BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (hospital_id) REFERENCES Hospitals(hospital_id),
    FOREIGN KEY (policy_id) REFERENCES Policies(policy_id)
);

-- 8. Documents Table
CREATE TABLE Documents (
    document_id INT PRIMARY KEY AUTO_INCREMENT,
    claim_id INT,
    document_name VARCHAR(255) NOT NULL,
    document_type ENUM('Medical Report', 'Bills', 'Discharge Summary', 'Lab Reports', 'Prescription', 'ID Proof', 'Other') NOT NULL,
    file_path VARCHAR(500),
    file_size INT, -- in bytes
    mime_type VARCHAR(100),
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    uploaded_by INT, -- user_id or admin_id
    is_verified BOOLEAN DEFAULT FALSE,
    verification_date TIMESTAMP NULL,
    verified_by INT, -- admin_id
    FOREIGN KEY (claim_id) REFERENCES Claims(claim_id),
    FOREIGN KEY (uploaded_by) REFERENCES Users(user_id)
);

-- 9. Admins Table
CREATE TABLE Admins (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    role ENUM('Super Admin', 'Claims Officer', 'Medical Officer', 'Customer Support') NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 10. Claim Status History (Audit Trail)
CREATE TABLE Claim_Status_History (
    history_id INT PRIMARY KEY AUTO_INCREMENT,
    claim_id INT,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    changed_by INT, -- admin_id
    change_reason TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (claim_id) REFERENCES Claims(claim_id),
    FOREIGN KEY (changed_by) REFERENCES Admins(admin_id)
);

-- 11. Pre-authorization Requests (for cashless claims)
CREATE TABLE Pre_Authorization (
    preauth_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    hospital_id INT,
    policy_id INT,
    estimated_amount DECIMAL(15,2),
    treatment_details TEXT,
    doctor_recommendation TEXT,
    requested_date DATE DEFAULT (CURRENT_DATE),
    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    approved_amount DECIMAL(15,2),
    validity_date DATE,
    approval_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (hospital_id) REFERENCES Hospitals(hospital_id),
    FOREIGN KEY (policy_id) REFERENCES Policies(policy_id)
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON Users(email);
CREATE INDEX idx_users_phone ON Users(phone);
CREATE INDEX idx_claims_user ON Claims(user_id);
CREATE INDEX idx_claims_status ON Claims(claim_status);
CREATE INDEX idx_claims_date ON Claims(claim_date);
CREATE INDEX idx_hospitals_city ON Hospitals(city);
CREATE INDEX idx_hospitals_state ON Hospitals(state);
CREATE INDEX idx_documents_claim ON Documents(claim_id);

-- Insert sample data for testing
INSERT INTO Insurance_Companies (company_name, helpline, email, website) VALUES
('HDFC ERGO Health Insurance', '1800-266-0625', 'info@hdfcergo.com', 'www.hdfcergo.com'),
('ICICI Lombard General Insurance', '1800-266-7766', 'care@icicilombard.com', 'www.icicilombard.com'),
('Star Health Insurance', '1800-425-2255', 'info@starhealth.in', 'www.starhealth.in'),
('New India Assurance', '1800-209-1415', 'info@newindia.co.in', 'www.newindia.co.in');

INSERT INTO Policies (policy_name, policy_number, company_id, coverage_amount, premium, policy_type) VALUES
('HDFC ERGO Health Suraksha', 'HDFC-HS-001', 1, 500000.00, 15000.00, 'Individual'),
('ICICI Lombard Complete Health Guard', 'ICICI-CHG-001', 2, 1000000.00, 25000.00, 'Family'),
('Star Comprehensive Insurance Policy', 'STAR-CIP-001', 3, 300000.00, 12000.00, 'Individual'),
('New India Mediclaim Policy', 'NIA-MCP-001', 4, 200000.00, 8000.00, 'Individual');
"""
ClaimEase Database Entity-Relationship Diagram
This file contains a textual representation of the ER diagram for the ClaimEase database.
You can use tools like draw.io, Lucidchart, or MySQL Workbench to create a visual diagram.
"""

# ClaimEase Database ER Diagram Structure

## Primary Entities

### 1. Users (Policyholders)
- **Primary Key**: user_id
- **Attributes**: 
  - Personal Info: first_name, last_name, email, phone, address, city, state, pincode
  - Identity: date_of_birth, gender, aadhar_number, pan_number
  - Policy: policy_id (FK), policy_start_date, policy_end_date
  - Nominee: nominee_name, nominee_relation
  - Security: password_hash, is_verified
  - Timestamps: created_at, updated_at

### 2. Insurance_Companies
- **Primary Key**: company_id
- **Attributes**: 
  - Basic Info: company_name, helpline, email, website
  - Business: registration_number, established_date, headquarters
  - Timestamps: created_at, updated_at

### 3. Policies
- **Primary Key**: policy_id
- **Foreign Key**: company_id → Insurance_Companies(company_id)
- **Attributes**:
  - Identity: policy_name, policy_number (UNIQUE)
  - Financial: coverage_amount, premium, deductible
  - Terms: policy_type, validity_period, waiting_period
  - Details: description, terms_conditions
  - Status: is_active
  - Timestamps: created_at, updated_at

### 4. Hospitals
- **Primary Key**: hospital_id
- **Attributes**:
  - Basic Info: hospital_name, hospital_type, registration_number
  - Location: address, city, state, pincode, latitude, longitude
  - Contact: contact_number, email, website
  - Medical: specializations (JSON), bed_capacity, accreditation
  - Business: empaneled_insurers (JSON)
  - Status: is_active
  - Timestamps: created_at, updated_at

### 5. Claims
- **Primary Key**: claim_id
- **Foreign Keys**: 
  - user_id → Users(user_id)
  - hospital_id → Hospitals(hospital_id)
  - policy_id → Policies(policy_id)
- **Attributes**:
  - Identity: claim_number (UNIQUE)
  - Medical: treatment_type, diagnosis, treatment_details, doctor_name
  - Dates: admission_date, discharge_date, claim_date, settlement_date
  - Financial: claim_amount, approved_amount
  - Process: claim_type, claim_status, rejected_reason
  - Details: room_type, is_emergency
  - Timestamps: created_at, updated_at

### 6. Documents
- **Primary Key**: document_id
- **Foreign Keys**: 
  - claim_id → Claims(claim_id)
  - uploaded_by → Users(user_id)
  - verified_by → Admins(admin_id)
- **Attributes**:
  - File Info: document_name, document_type, file_path, file_size, mime_type
  - Process: is_verified, verification_date
  - Timestamps: upload_date

### 7. Admins
- **Primary Key**: admin_id
- **Attributes**:
  - Personal: first_name, last_name, email, phone
  - Access: role, password_hash, last_login, is_active
  - Timestamps: created_at, updated_at

## Supporting Entities

### 8. Hospital_States (Statistical Data)
- **Primary Key**: state_id
- **Attributes**:
  - Location: state_name
  - Public Stats: public_hospitals_count, public_hospitals_amount
  - Private Stats: private_hospitals_count, private_hospitals_amount

### 9. Hospital_Insurance_Empanelment (Many-to-Many Relationship)
- **Primary Key**: empanelment_id
- **Foreign Keys**:
  - hospital_id → Hospitals(hospital_id)
  - company_id → Insurance_Companies(company_id)
- **Attributes**:
  - Business: empanelment_date, cashless_available, reimbursement_available
  - Status: is_active
  - Timestamp: created_at
- **Unique Constraint**: (hospital_id, company_id)

### 10. Claim_Status_History (Audit Trail)
- **Primary Key**: history_id
- **Foreign Keys**:
  - claim_id → Claims(claim_id)
  - changed_by → Admins(admin_id)
- **Attributes**:
  - Status: old_status, new_status, change_reason
  - Timestamp: changed_at

### 11. Pre_Authorization (Cashless Claims)
- **Primary Key**: preauth_id
- **Foreign Keys**:
  - user_id → Users(user_id)
  - hospital_id → Hospitals(hospital_id)
  - policy_id → Policies(policy_id)
- **Attributes**:
  - Financial: estimated_amount, approved_amount
  - Medical: treatment_details, doctor_recommendation
  - Process: status, approval_number, validity_date
  - Dates: requested_date
  - Timestamp: created_at

## Key Relationships

### One-to-Many Relationships
1. **Insurance_Companies** → **Policies**
   - One insurance company can have multiple policies
   
2. **Policies** → **Users**
   - One policy can cover multiple users (family policies)
   
3. **Users** → **Claims**
   - One user can submit multiple claims
   
4. **Hospitals** → **Claims**
   - One hospital can process multiple claims
   
5. **Policies** → **Claims**
   - One policy can have multiple claims
   
6. **Claims** → **Documents**
   - One claim can have multiple supporting documents
   
7. **Claims** → **Claim_Status_History**
   - One claim can have multiple status changes
   
8. **Users** → **Pre_Authorization**
   - One user can have multiple pre-authorization requests

### Many-to-Many Relationships
1. **Hospitals** ↔ **Insurance_Companies** (via Hospital_Insurance_Empanelment)
   - One hospital can be empaneled with multiple insurance companies
   - One insurance company can empanel multiple hospitals

## Indexes for Performance
- Users: email, phone
- Claims: user_id, claim_status, claim_date
- Hospitals: city, state
- Documents: claim_id

## Data Flow
1. **User Registration**: User → Users table
2. **Policy Assignment**: Admin assigns policy to user
3. **Hospital Network**: Hospitals empaneled with insurance companies
4. **Claim Submission**: User submits claim → Claims table
5. **Document Upload**: User uploads documents → Documents table
6. **Claim Processing**: Admin reviews and updates claim status
7. **Status Tracking**: All status changes logged in Claim_Status_History

## Visual Representation Notes
When creating the visual ER diagram:
- Use rectangles for entities
- Use diamonds for relationships
- Use ovals for attributes
- Use lines to connect entities with their relationships
- Mark primary keys with underlines
- Mark foreign keys with dashed underlines
- Show cardinalities (1:1, 1:M, M:M) on relationship lines

## Tools for Creating Visual ER Diagram
1. **MySQL Workbench**: Can reverse engineer from existing database
2. **draw.io**: Free online diagramming tool
3. **Lucidchart**: Professional diagramming software
4. **ERD Plus**: Free web-based ER diagram tool
5. **dbdiagram.io**: Database diagram tool with code-based input
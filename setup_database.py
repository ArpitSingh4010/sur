"""
ClaimEase Database Setup and Data Import Script
This script sets up the ClaimEase database and imports hospital data from CSV
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime
import hashlib

class ClaimEaseDB:
    def __init__(self, host='localhost', user='root', password='', database='claimease'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print(f"✅ Successfully connected to {self.database} database")
                return True
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            return False
    
    def execute_sql_file(self, sql_file_path):
        """Execute SQL file to create schema"""
        try:
            cursor = self.connection.cursor()
            with open(sql_file_path, 'r', encoding='utf-8') as file:
                sql_script = file.read()
                
            # Split and execute statements
            statements = sql_script.split(';')
            for statement in statements:
                if statement.strip():
                    cursor.execute(statement)
            
            self.connection.commit()
            print("✅ Database schema created successfully")
            cursor.close()
            return True
        except Error as e:
            print(f"❌ Error executing SQL file: {e}")
            return False
    
    def import_hospital_state_data(self, csv_data):
        """Import hospital state data from CSV"""
        try:
            cursor = self.connection.cursor()
            
            # Clear existing data
            cursor.execute("DELETE FROM Hospital_States")
            
            insert_query = """
            INSERT INTO Hospital_States (state_name, public_hospitals_count, 
                                       public_hospitals_amount, private_hospitals_count, 
                                       private_hospitals_amount) 
            VALUES (%s, %s, %s, %s, %s)
            """
            
            data_to_insert = []
            for _, row in csv_data.iterrows():
                # Clean the data
                state_name = row['State/UT'].strip()
                pub_count = int(row['Public Hospitals - Count']) if pd.notna(row['Public Hospitals - Count']) else 0
                pub_amount = float(row['Public Hospitals - Amount (In Crores)']) if pd.notna(row['Public Hospitals - Amount (In Crores)']) else 0.0
                priv_count = int(row['Private Hospitals - Count']) if pd.notna(row['Private Hospitals - Count']) and str(row['Private Hospitals - Count']).upper() != 'NA' else 0
                priv_amount = float(row['Private Hospitals - Amount (In Crores)']) if pd.notna(row['Private Hospitals - Amount (In Crores)']) and str(row['Private Hospitals - Amount (In Crores)']).upper() != 'NA' else 0.0
                
                data_to_insert.append((state_name, pub_count, pub_amount, priv_count, priv_amount))
            
            cursor.executemany(insert_query, data_to_insert)
            self.connection.commit()
            print(f"✅ Imported {len(data_to_insert)} state/UT hospital records")
            cursor.close()
            return True
            
        except Error as e:
            print(f"❌ Error importing hospital state data: {e}")
            return False
    
    def add_sample_hospitals(self):
        """Add sample hospital data"""
        try:
            cursor = self.connection.cursor()
            
            sample_hospitals = [
                ('Apollo Hospital Delhi', 'Private', 'APL001', '123 Nehru Place, New Delhi', 'New Delhi', 'Delhi', '110019', '011-26925858', 'delhi@apollohospitals.com', 'www.apollohospitals.com', '["Cardiology", "Oncology", "Neurology"]', 500, 'NABH', '[1, 2, 3]'),
                ('AIIMS New Delhi', 'Public', 'AIIMS001', 'Ansari Nagar, New Delhi', 'New Delhi', 'Delhi', '110029', '011-26588500', 'info@aiims.edu', 'www.aiims.edu', '["General Medicine", "Surgery", "Pediatrics"]', 2500, 'NABH', '[1, 2, 3, 4]'),
                ('Fortis Hospital Mumbai', 'Private', 'FOR001', 'Mulund Goregaon Link Road, Mumbai', 'Mumbai', 'Maharashtra', '400078', '022-61769999', 'mumbai@fortishealthcare.com', 'www.fortishealthcare.com', '["Cardiology", "Orthopedics", "Gastroenterology"]', 400, 'JCI', '[1, 2, 3]'),
                ('KEM Hospital Mumbai', 'Public', 'KEM001', 'Acharya Donde Marg, Parel, Mumbai', 'Mumbai', 'Maharashtra', '400012', '022-24136051', 'info@kem.edu', 'www.kem.edu', '["Emergency Medicine", "Internal Medicine", "Surgery"]', 1800, 'NABH', '[1, 2, 4]'),
                ('Manipal Hospital Bangalore', 'Private', 'MAN001', 'Old Airport Road, Bangalore', 'Bangalore', 'Karnataka', '560017', '080-25023030', 'bangalore@manipalhospitals.com', 'www.manipalhospitals.com', '["Neurosurgery", "Cardiac Surgery", "Oncology"]', 650, 'NABH', '[1, 2, 3]')
            ]
            
            insert_query = """
            INSERT INTO Hospitals (hospital_name, hospital_type, registration_number, address, 
                                 city, state, pincode, contact_number, email, website, 
                                 specializations, bed_capacity, accreditation, empaneled_insurers) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.executemany(insert_query, sample_hospitals)
            self.connection.commit()
            print(f"✅ Added {len(sample_hospitals)} sample hospitals")
            cursor.close()
            return True
            
        except Error as e:
            print(f"❌ Error adding sample hospitals: {e}")
            return False
    
    def add_sample_users(self):
        """Add sample user data"""
        try:
            cursor = self.connection.cursor()
            
            # Hash password for demo
            password_hash = hashlib.sha256("password123".encode()).hexdigest()
            
            sample_users = [
                ('Rahul', 'Sharma', 'rahul.sharma@email.com', '9876543210', '123 MG Road, Bangalore', 'Bangalore', 'Karnataka', '560001', '1990-05-15', 'Male', '123456789012', 'ABCDE1234F', 1, '2024-01-01', '2025-01-01', 'Priya Sharma', 'Spouse', password_hash, True),
                ('Priya', 'Patel', 'priya.patel@email.com', '9876543211', '456 FC Road, Pune', 'Pune', 'Maharashtra', '411001', '1985-03-20', 'Female', '123456789013', 'BCDEF2345G', 2, '2024-02-01', '2025-02-01', 'Amit Patel', 'Spouse', password_hash, True),
                ('Amit', 'Kumar', 'amit.kumar@email.com', '9876543212', '789 Connaught Place, Delhi', 'New Delhi', 'Delhi', '110001', '1988-07-10', 'Male', '123456789014', 'CDEFG3456H', 3, '2024-03-01', '2025-03-01', 'Sunita Kumar', 'Spouse', password_hash, True)
            ]
            
            insert_query = """
            INSERT INTO Users (first_name, last_name, email, phone, address, city, state, pincode, 
                             date_of_birth, gender, aadhar_number, pan_number, policy_id, 
                             policy_start_date, policy_end_date, nominee_name, nominee_relation, 
                             password_hash, is_verified) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.executemany(insert_query, sample_users)
            self.connection.commit()
            print(f"✅ Added {len(sample_users)} sample users")
            cursor.close()
            return True
            
        except Error as e:
            print(f"❌ Error adding sample users: {e}")
            return False
    
    def create_sample_claims(self):
        """Create sample claims data"""
        try:
            cursor = self.connection.cursor()
            
            sample_claims = [
                ('CLM001', 1, 1, 1, 'Cashless', 'Cardiac Surgery', '2024-10-15', '2024-10-20', '2024-10-16', 'Under Review', 250000.00, None, None, None, 'Coronary Artery Disease', 'Bypass Surgery', 'Dr. Rajesh Kumar', 'Private AC', True),
                ('CLM002', 2, 3, 2, 'Reimbursement', 'Maternity', '2024-10-10', '2024-10-12', '2024-10-13', 'Approved', 50000.00, 45000.00, None, '2024-10-25', 'Normal Delivery', 'Caesarean Section', 'Dr. Sunita Verma', 'General Ward', False),
                ('CLM003', 3, 2, 3, 'Cashless', 'Orthopedic Surgery', '2024-10-20', '2024-10-22', '2024-10-21', 'Pending', 80000.00, None, None, None, 'Fracture Tibia', 'Internal Fixation', 'Dr. Anil Joshi', 'Semi Private', False)
            ]
            
            insert_query = """
            INSERT INTO Claims (claim_number, user_id, hospital_id, policy_id, claim_type, 
                              treatment_type, admission_date, discharge_date, claim_date, 
                              claim_status, claim_amount, approved_amount, rejected_reason, 
                              settlement_date, diagnosis, treatment_details, doctor_name, 
                              room_type, is_emergency) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.executemany(insert_query, sample_claims)
            self.connection.commit()
            print(f"✅ Added {len(sample_claims)} sample claims")
            cursor.close()
            return True
            
        except Error as e:
            print(f"❌ Error creating sample claims: {e}")
            return False
    
    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔒 Database connection closed")

def main():
    """Main function to set up ClaimEase database"""
    print("🏥 ClaimEase Database Setup Starting...")
    
    # Initialize database
    db = ClaimEaseDB()
    
    if not db.connect():
        return
    
    # Execute schema
    print("\n📋 Creating database schema...")
    if not db.execute_sql_file('claimease_schema.sql'):
        return
    
    # Import hospital state data from CSV
    print("\n📊 Importing hospital state data...")
    try:
        # CSV data from the attachment
        csv_data = [
            ['Andaman and Nicobar Islands', 8, 0.01, 2, 0.00],
            ['Andhra Pradesh', 660094, 693.57, 305840, 404.17],
            ['Arunachal Pradesh', 957, 1.30, 9, 0.01],
            ['Assam', 82154, 97.84, 5866, 7.30],
            ['Bihar', 33699, 34.92, 1268, 0.99],
            ['Chandigarh', 105, 0.11, 13, 0.02],
            ['Chhattisgarh', 214498, 281.48, 92219, 142.70],
            ['Dadra and Nagar Haveli and Daman and Diu', 3035, 3.04, 22, 0.02],
            ['Gujarat', 36898, 40.04, 72465, 83.71],
            ['Haryana', 41722, 34.39, 2308, 3.10],
            ['Himachal Pradesh', 428, 0.43, 488, 0.46],
            ['Jammu and Kashmir', 44494, 50.94, 325, 0.33],
            ['Jharkhand', 150277, 94.06, 1546, 1.14],
            ['Karnataka', 903417, 337.77, 22361, 20.49],
            ['Kerala', 85627, 78.37, 78834, 83.53],
            ['Ladakh', 1337, 1.40, 0, 0.00],  # NA converted to 0
            ['Lakshadweep', 49, 0.05, 1, 0.00],
            ['Madhya Pradesh', 299232, 301.53, 11755, 13.23],
            ['Maharashtra', 4366, 5.39, 7594, 11.22],
            ['Manipur', 3365, 4.98, 5440, 8.08],
            ['Meghalaya', 9377, 6.11, 6507, 5.42],
            ['Mizoram', 4810, 4.64, 35, 0.02],
            ['Nagaland', 2200, 4.12, 2564, 4.94],
            ['Puducherry', 3940, 4.50, 33, 0.04],
            ['Punjab', 60260, 66.34, 1491, 1.81],
            ['Rajasthan', 538364, 471.55, 28401, 33.17],
            ['Sikkim', 193, 0.23, 56, 0.06],
            ['Tamil Nadu', 35389, 58.22, 6436, 12.61],
            ['Telangana', 62669, 93.60, 6990, 16.77],
            ['Tripura', 9568, 11.41, 45, 0.05],
            ['Uttar Pradesh', 60742, 67.62, 11987, 13.13],
            ['Uttarakhand', 6319, 7.40, 10101, 14.63]
        ]
        
        # Convert to DataFrame
        columns = ['State/UT', 'Public Hospitals - Count', 'Public Hospitals - Amount (In Crores)', 
                  'Private Hospitals - Count', 'Private Hospitals - Amount (In Crores)']
        df = pd.DataFrame(csv_data, columns=columns)
        
        if db.import_hospital_state_data(df):
            print("✅ Hospital state data imported successfully")
    except Exception as e:
        print(f"❌ Error processing CSV data: {e}")
    
    # Add sample data
    print("\n🏥 Adding sample hospitals...")
    db.add_sample_hospitals()
    
    print("\n👥 Adding sample users...")
    db.add_sample_users()
    
    print("\n📋 Creating sample claims...")
    db.create_sample_claims()
    
    # Close connection
    db.close_connection()
    
    print("\n🎉 ClaimEase database setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Install required Python packages: pip install mysql-connector-python pandas flask")
    print("2. Update database credentials in the script")
    print("3. Run the Flask API (create_flask_api.py)")
    print("4. Build the frontend (React/HTML)")

if __name__ == "__main__":
    main()
"""
ClaimEase Flask API Backend
RESTful API for Health Insurance Claims Management System
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import hashlib
import jwt
import datetime
from functools import wraps
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
app.config['UPLOAD_FOLDER'] = 'uploads/documents'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

CORS(app)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mahalakshmi',  # Update with your actual MySQL password
    'database': 'claimease'
}

# Allowed file extensions for document upload
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

def get_db_connection():
    """Get database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def token_required(f):
    """Decorator for routes that require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user_id, *args, **kwargs)
    return decorated

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Authentication Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'date_of_birth']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Hash password
        password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT user_id FROM Users WHERE email = %s", (data['email'],))
        if cursor.fetchone():
            return jsonify({'error': 'User already exists'}), 409
        
        # Insert new user
        insert_query = """
        INSERT INTO Users (first_name, last_name, email, phone, address, city, state, 
                          pincode, date_of_birth, gender, password_hash) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        user_data = (
            data['first_name'], data['last_name'], data['email'], data['phone'],
            data.get('address', ''), data.get('city', ''), data.get('state', ''),
            data.get('pincode', ''), data['date_of_birth'], data.get('gender', ''),
            password_hash
        )
        
        cursor.execute(insert_query, user_data)
        connection.commit()
        
        return jsonify({'message': 'User registered successfully'}), 201
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT user_id, first_name, last_name, email, policy_id 
            FROM Users 
            WHERE email = %s AND password_hash = %s
        """, (email, password_hash))
        
        user = cursor.fetchone()
        
        if user:
            # Generate JWT token
            token = jwt.encode({
                'user_id': user['user_id'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, app.config['SECRET_KEY'])
            
            return jsonify({
                'token': token,
                'user': user
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# User Routes
@app.route('/api/user/profile', methods=['GET'])
@token_required
def get_user_profile(current_user_id):
    """Get user profile"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT u.*, p.policy_name, p.coverage_amount, ic.company_name
            FROM Users u
            LEFT JOIN Policies p ON u.policy_id = p.policy_id
            LEFT JOIN Insurance_Companies ic ON p.company_id = ic.company_id
            WHERE u.user_id = %s
        """, (current_user_id,))
        
        user = cursor.fetchone()
        
        if user:
            # Remove sensitive data
            user.pop('password_hash', None)
            return jsonify(user), 200
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Hospital Routes
@app.route('/api/hospitals', methods=['GET'])
def get_hospitals():
    """Get list of hospitals"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Get query parameters
        city = request.args.get('city')
        state = request.args.get('state')
        hospital_type = request.args.get('type')
        
        query = "SELECT * FROM Hospitals WHERE is_active = TRUE"
        params = []
        
        if city:
            query += " AND city LIKE %s"
            params.append(f"%{city}%")
        
        if state:
            query += " AND state LIKE %s"
            params.append(f"%{state}%")
        
        if hospital_type:
            query += " AND hospital_type = %s"
            params.append(hospital_type)
        
        query += " ORDER BY hospital_name"
        
        cursor.execute(query, params)
        hospitals = cursor.fetchall()
        
        return jsonify(hospitals), 200
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/hospitals/<int:hospital_id>', methods=['GET'])
def get_hospital_details(hospital_id):
    """Get hospital details"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM Hospitals WHERE hospital_id = %s", (hospital_id,))
        hospital = cursor.fetchone()
        
        if hospital:
            return jsonify(hospital), 200
        else:
            return jsonify({'error': 'Hospital not found'}), 404
            
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Claims Routes
@app.route('/api/claims', methods=['GET'])
@token_required
def get_user_claims(current_user_id):
    """Get user's claims"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT c.*, h.hospital_name, p.policy_name, ic.company_name
            FROM Claims c
            JOIN Hospitals h ON c.hospital_id = h.hospital_id
            JOIN Policies p ON c.policy_id = p.policy_id
            JOIN Insurance_Companies ic ON p.company_id = ic.company_id
            WHERE c.user_id = %s
            ORDER BY c.claim_date DESC
        """, (current_user_id,))
        
        claims = cursor.fetchall()
        return jsonify(claims), 200
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/claims', methods=['POST'])
@token_required
def create_claim(current_user_id):
    """Create new claim"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['hospital_id', 'claim_type', 'treatment_type', 'claim_amount', 'diagnosis']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Get user's policy
        cursor.execute("SELECT policy_id FROM Users WHERE user_id = %s", (current_user_id,))
        user_policy = cursor.fetchone()
        
        if not user_policy or not user_policy[0]:
            return jsonify({'error': 'User does not have an active policy'}), 400
        
        # Generate claim number
        claim_number = f"CLM{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Insert claim
        insert_query = """
        INSERT INTO Claims (claim_number, user_id, hospital_id, policy_id, claim_type, 
                          treatment_type, admission_date, discharge_date, claim_amount, 
                          diagnosis, treatment_details, doctor_name, room_type, is_emergency) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        claim_data = (
            claim_number, current_user_id, data['hospital_id'], user_policy[0],
            data['claim_type'], data['treatment_type'], data.get('admission_date'),
            data.get('discharge_date'), data['claim_amount'], data['diagnosis'],
            data.get('treatment_details', ''), data.get('doctor_name', ''),
            data.get('room_type', ''), data.get('is_emergency', False)
        )
        
        cursor.execute(insert_query, claim_data)
        connection.commit()
        
        return jsonify({'message': 'Claim created successfully', 'claim_number': claim_number}), 201
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/claims/<int:claim_id>', methods=['GET'])
@token_required
def get_claim_details(current_user_id, claim_id):
    """Get claim details"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT c.*, h.hospital_name, h.contact_number as hospital_phone,
                   p.policy_name, p.coverage_amount, ic.company_name, ic.helpline
            FROM Claims c
            JOIN Hospitals h ON c.hospital_id = h.hospital_id
            JOIN Policies p ON c.policy_id = p.policy_id
            JOIN Insurance_Companies ic ON p.company_id = ic.company_id
            WHERE c.claim_id = %s AND c.user_id = %s
        """, (claim_id, current_user_id))
        
        claim = cursor.fetchone()
        
        if claim:
            # Get claim documents
            cursor.execute("""
                SELECT document_id, document_name, document_type, upload_date, is_verified
                FROM Documents 
                WHERE claim_id = %s
            """, (claim_id,))
            
            documents = cursor.fetchall()
            claim['documents'] = documents
            
            return jsonify(claim), 200
        else:
            return jsonify({'error': 'Claim not found'}), 404
            
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Insurance Routes
@app.route('/api/insurance-companies', methods=['GET'])
def get_insurance_companies():
    """Get list of insurance companies"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM Insurance_Companies ORDER BY company_name")
        companies = cursor.fetchall()
        
        return jsonify(companies), 200
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/policies', methods=['GET'])
def get_policies():
    """Get list of policies"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        company_id = request.args.get('company_id')
        
        query = """
            SELECT p.*, ic.company_name 
            FROM Policies p
            JOIN Insurance_Companies ic ON p.company_id = ic.company_id
            WHERE p.is_active = TRUE
        """
        params = []
        
        if company_id:
            query += " AND p.company_id = %s"
            params.append(company_id)
        
        query += " ORDER BY p.policy_name"
        
        cursor.execute(query, params)
        policies = cursor.fetchall()
        
        return jsonify(policies), 200
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Statistics Routes
@app.route('/api/stats/dashboard', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        stats = {}
        
        # Total hospitals
        cursor.execute("SELECT COUNT(*) as total FROM Hospitals WHERE is_active = TRUE")
        stats['total_hospitals'] = cursor.fetchone()['total']
        
        # Total insurance companies
        cursor.execute("SELECT COUNT(*) as total FROM Insurance_Companies")
        stats['total_insurance_companies'] = cursor.fetchone()['total']
        
        # Total policies
        cursor.execute("SELECT COUNT(*) as total FROM Policies WHERE is_active = TRUE")
        stats['total_policies'] = cursor.fetchone()['total']
        
        # Total users
        cursor.execute("SELECT COUNT(*) as total FROM Users WHERE is_verified = TRUE")
        stats['total_users'] = cursor.fetchone()['total']
        
        # Claims by status
        cursor.execute("""
            SELECT claim_status, COUNT(*) as count 
            FROM Claims 
            GROUP BY claim_status
        """)
        stats['claims_by_status'] = cursor.fetchall()
        
        # Hospital statistics by state
        cursor.execute("""
            SELECT state_name, public_hospitals_count, private_hospitals_count,
                   (public_hospitals_count + private_hospitals_count) as total_hospitals
            FROM Hospital_States 
            ORDER BY total_hospitals DESC 
            LIMIT 10
        """)
        stats['top_states_by_hospitals'] = cursor.fetchall()
        
        return jsonify(stats), 200
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/stats/hospital-states', methods=['GET'])
def get_hospital_states():
    """Get hospital statistics by state"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT state_name, public_hospitals_count, private_hospitals_count,
                   public_hospitals_amount, private_hospitals_amount,
                   (public_hospitals_count + private_hospitals_count) as total_hospitals,
                   (public_hospitals_amount + private_hospitals_amount) as total_amount
            FROM Hospital_States 
            ORDER BY total_hospitals DESC
        """)
        
        states = cursor.fetchall()
        return jsonify(states), 200
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# File upload route (placeholder)
@app.route('/api/documents/upload', methods=['POST'])
@token_required
def upload_document(current_user_id):
    """Upload document for claim"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file selected'}), 400
        
        file = request.files['file']
        claim_id = request.form.get('claim_id')
        document_type = request.form.get('document_type')
        
        if not claim_id or not document_type:
            return jsonify({'error': 'claim_id and document_type are required'}), 400
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # In production, save to cloud storage (AWS S3, etc.)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Create upload directory if it doesn't exist
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            file.save(file_path)
            
            # Save document info to database
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                INSERT INTO Documents (claim_id, document_name, document_type, 
                                     file_path, file_size, mime_type, uploaded_by) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (claim_id, filename, document_type, file_path, 
                  os.path.getsize(file_path), file.mimetype, current_user_id))
            
            connection.commit()
            
            return jsonify({'message': 'Document uploaded successfully'}), 201
        
        return jsonify({'error': 'Invalid file type'}), 400
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting ClaimEase API Server...")
    print("📋 Available endpoints:")
    print("   POST /api/auth/register - User registration")
    print("   POST /api/auth/login - User login")
    print("   GET  /api/user/profile - Get user profile")
    print("   GET  /api/hospitals - Get hospitals list")
    print("   GET  /api/claims - Get user claims")
    print("   POST /api/claims - Create new claim")
    print("   GET  /api/insurance-companies - Get insurance companies")
    print("   GET  /api/policies - Get policies")
    print("   GET  /api/stats/dashboard - Get dashboard statistics")
    print("   GET  /api/stats/hospital-states - Get hospital statistics by state")
    print("   POST /api/documents/upload - Upload documents")
    print("\n🌐 Server running on http://localhost:5000")
    
    app.run(debug=True, port=5000)
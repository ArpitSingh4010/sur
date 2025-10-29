"""
ClaimEase Simple API - Database Connection Test
This version provides better error handling and fallback data
"""

from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mahalakshmi',
    'database': 'claimease'
}

def get_db_connection():
    """Get database connection with error handling"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def home():
    return jsonify({
        'message': 'ClaimEase API is running!',
        'version': '1.0',
        'endpoints': [
            '/api/test-db',
            '/api/stats/hospital-states',
            '/api/insurance-companies',
            '/api/hospitals'
        ]
    })

@app.route('/api/test-db')
def test_database():
    """Test database connection"""
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE(), VERSION();")
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return jsonify({
                'status': 'success',
                'database': result[0],
                'mysql_version': result[1],
                'message': 'Database connection successful!'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Could not connect to database'
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Database error: {str(e)}'
        }), 500

@app.route('/api/stats/hospital-states')
def get_hospital_states():
    """Get hospital statistics by state with fallback data"""
    try:
        connection = get_db_connection()
        if connection:
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
            cursor.close()
            connection.close()
            return jsonify(states)
        else:
            # Fallback data if database is not available
            return jsonify([
                {
                    'state_name': 'Andhra Pradesh',
                    'public_hospitals_count': 660094,
                    'private_hospitals_count': 305840,
                    'total_hospitals': 965934,
                    'public_hospitals_amount': 693.57,
                    'private_hospitals_amount': 404.17,
                    'total_amount': 1097.74,
                    'source': 'fallback_data'
                },
                {
                    'state_name': 'Karnataka',
                    'public_hospitals_count': 903417,
                    'private_hospitals_count': 22361,
                    'total_hospitals': 925778,
                    'public_hospitals_amount': 337.77,
                    'private_hospitals_amount': 20.49,
                    'total_amount': 358.26,
                    'source': 'fallback_data'
                }
            ])
    except Exception as e:
        return jsonify({
            'error': f'Error retrieving hospital states: {str(e)}'
        }), 500

@app.route('/api/insurance-companies')
def get_insurance_companies():
    """Get insurance companies with fallback data"""
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Insurance_Companies ORDER BY company_name")
            companies = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify(companies)
        else:
            # Fallback data
            return jsonify([
                {
                    'company_id': 1,
                    'company_name': 'HDFC ERGO Health Insurance',
                    'helpline': '1800-266-0625',
                    'email': 'info@hdfcergo.com',
                    'website': 'www.hdfcergo.com',
                    'source': 'fallback_data'
                },
                {
                    'company_id': 2,
                    'company_name': 'ICICI Lombard General Insurance',
                    'helpline': '1800-266-7766',
                    'email': 'care@icicilombard.com',
                    'website': 'www.icicilombard.com',
                    'source': 'fallback_data'
                }
            ])
    except Exception as e:
        return jsonify({
            'error': f'Error retrieving insurance companies: {str(e)}'
        }), 500

@app.route('/api/hospitals')
def get_hospitals():
    """Get hospitals with fallback data"""
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Hospitals WHERE is_active = TRUE ORDER BY hospital_name")
            hospitals = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify(hospitals)
        else:
            # Fallback data
            return jsonify([
                {
                    'hospital_id': 1,
                    'hospital_name': 'Apollo Hospital Delhi',
                    'hospital_type': 'Private',
                    'city': 'New Delhi',
                    'state': 'Delhi',
                    'contact_number': '011-26925858',
                    'bed_capacity': 500,
                    'source': 'fallback_data'
                },
                {
                    'hospital_id': 2,
                    'hospital_name': 'AIIMS New Delhi',
                    'hospital_type': 'Public',
                    'city': 'New Delhi',
                    'state': 'Delhi',
                    'contact_number': '011-26588500',
                    'bed_capacity': 2500,
                    'source': 'fallback_data'
                }
            ])
    except Exception as e:
        return jsonify({
            'error': f'Error retrieving hospitals: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🏥 ClaimEase Simple API Starting...")
    print("🔧 Testing database connection...")
    
    # Test database connection at startup
    connection = get_db_connection()
    if connection:
        print("✅ Database connection successful!")
        connection.close()
    else:
        print("⚠️  Database connection failed - using fallback data")
    
    print("\n📋 Available endpoints:")
    print("   GET  / - API status")
    print("   GET  /api/test-db - Test database connection")
    print("   GET  /api/stats/hospital-states - Hospital statistics")
    print("   GET  /api/insurance-companies - Insurance companies")
    print("   GET  /api/hospitals - Hospital list")
    
    print("\n🌐 Starting server on http://localhost:5000")
    app.run(debug=True, port=5000)
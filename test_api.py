"""
ClaimEase API Test Script
Test all available endpoints to ensure they're working correctly
"""

import requests
import json

# API Base URL
BASE_URL = "http://localhost:5000/api"

def test_endpoint(method, endpoint, data=None, headers=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        
        print(f"\n🔹 {method.upper()} {endpoint}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS")
            # Pretty print first 200 chars of response
            response_text = response.text[:200]
            if len(response.text) > 200:
                response_text += "..."
            print(f"Response: {response_text}")
        else:
            print("❌ ERROR")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION ERROR - Make sure Flask server is running on {BASE_URL}")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

def main():
    print("🏥 ClaimEase API Test Suite")
    print("=" * 50)
    
    # Test public endpoints (no authentication required)
    print("\n📋 Testing Public Endpoints:")
    
    test_endpoint("GET", "/insurance-companies")
    test_endpoint("GET", "/policies")
    test_endpoint("GET", "/hospitals")
    test_endpoint("GET", "/stats/dashboard")
    test_endpoint("GET", "/stats/hospital-states")
    
    # Test authentication endpoints
    print("\n🔐 Testing Authentication Endpoints:")
    
    # Test registration
    test_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "phone": "1234567890",
        "date_of_birth": "1990-01-01",
        "password": "testpassword123"
    }
    test_endpoint("POST", "/auth/register", test_data)
    
    # Test login
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    test_endpoint("POST", "/auth/login", login_data)
    
    print("\n" + "=" * 50)
    print("🎉 API Test Complete!")
    print("\nIf you see connection errors, make sure to:")
    print("1. Run: python flask_api.py")
    print("2. Wait for 'Server running on http://localhost:5000'")
    print("3. Try accessing http://localhost:5000/api/hospitals in your browser")

if __name__ == "__main__":
    main()
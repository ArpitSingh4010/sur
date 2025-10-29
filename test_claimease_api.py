import requests
import json

# Test ClaimEase API endpoints
BASE_URL = "http://localhost:5000/api"

def test_api():
    print("🏥 Testing ClaimEase API with MySQL Database")
    print("=" * 50)
    
    try:
        # Test 1: Get hospital states (your data)
        print("\n📊 Testing Hospital States Data...")
        response = requests.get(f"{BASE_URL}/stats/hospital-states")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: Retrieved {len(data)} states")
            print("Top 3 states by hospital count:")
            for i, state in enumerate(data[:3], 1):
                total = state.get('public_hospitals_count', 0) + state.get('private_hospitals_count', 0)
                print(f"  {i}. {state['state_name']}: {total:,} hospitals")
        else:
            print(f"❌ ERROR: {response.status_code} - {response.text}")
        
        # Test 2: Get insurance companies
        print("\n🏢 Testing Insurance Companies...")
        response = requests.get(f"{BASE_URL}/insurance-companies")
        if response.status_code == 200:
            companies = response.json()
            print(f"✅ SUCCESS: Retrieved {len(companies)} insurance companies")
            for company in companies:
                print(f"  - {company['company_name']}")
        else:
            print(f"❌ ERROR: {response.status_code} - {response.text}")
            
        # Test 3: Get hospitals
        print("\n🏥 Testing Hospitals Data...")
        response = requests.get(f"{BASE_URL}/hospitals")
        if response.status_code == 200:
            hospitals = response.json()
            print(f"✅ SUCCESS: Retrieved {len(hospitals)} hospitals")
            for hospital in hospitals[:3]:
                print(f"  - {hospital['hospital_name']} ({hospital['city']})")
        else:
            print(f"❌ ERROR: {response.status_code} - {response.text}")
            
        # Test 4: Get policies
        print("\n📋 Testing Policies...")
        response = requests.get(f"{BASE_URL}/policies")
        if response.status_code == 200:
            policies = response.json()
            print(f"✅ SUCCESS: Retrieved {len(policies)} policies")
            for policy in policies:
                print(f"  - {policy['policy_name']}: ₹{policy['coverage_amount']:,}")
        else:
            print(f"❌ ERROR: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Make sure Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 ClaimEase API Test Complete!")

if __name__ == "__main__":
    test_api()
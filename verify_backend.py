import requests
import json

# Test the API client functionality similar to what the frontend does
BASE_URL = "http://localhost:8001"

def test_agent_status():
    try:
        response = requests.get(f"{BASE_URL}/api/v1/agent/status")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Parsed JSON: {json.dumps(data, indent=2)}")
            print("SUCCESS: Agent status API is working correctly!")
        else:
            print(f"ERROR: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    test_agent_status()
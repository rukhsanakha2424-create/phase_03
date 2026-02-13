import requests
import traceback

try:
    response = requests.get("http://localhost:8001/api/v1/agent/status")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error making request: {e}")
    traceback.print_exc()
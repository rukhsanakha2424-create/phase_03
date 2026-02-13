import requests
import traceback

print("Testing agent status endpoint...")
try:
    response = requests.get("http://localhost:8001/api/v1/agent/status")
    print(f"Agent status - Status Code: {response.status_code}")
    print(f"Agent status - Response: {response.text}")
except Exception as e:
    print(f"Agent status - Error: {e}")
    traceback.print_exc()

print("\nTesting todos endpoint...")
try:
    response = requests.get("http://localhost:8001/api/v1/todos")
    print(f"Todos - Status Code: {response.status_code}")
    print(f"Todos - Response: {response.text}")
except Exception as e:
    print(f"Todos - Error: {e}")
    traceback.print_exc()
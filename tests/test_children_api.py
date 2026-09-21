import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
for p in [root, os.path.join(root, 'app'), os.path.join(root, 'utils'), os.path.join(root, 'chatbots'), os.path.join(root, 'scripts')]:
    if p not in sys.path:
        sys.path.insert(0, p)

"""Test if Flask server is accessible and API works"""
import requests
import json

try:
    # Test if server is running
    response = requests.get('http://127.0.0.1:5000/api/get-children', timeout=3)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except requests.exceptions.ConnectionError:
    print("ERROR: Flask server is not running!")
    print("Start the server with: python flask_app.py")
except Exception as e:
    print(f"Error: {e}")

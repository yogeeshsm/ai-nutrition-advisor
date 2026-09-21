import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
for p in [root, os.path.join(root, 'app'), os.path.join(root, 'utils'), os.path.join(root, 'chatbots'), os.path.join(root, 'scripts')]:
    if p not in sys.path:
        sys.path.insert(0, p)

import requests
import json

url = "http://127.0.0.1:5000/api/get-children"
print(f"Testing {url}...")

try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"[OK] Success! Found {len(data['children'])} children.")
            for child in data['children'][:3]: # Show first 3
                print(f"  - {child['name']} (ID: {child['id']}, Age: {child['age_years']}y, Weight: {child['weight_kg']}kg)")
        else:
            print(f"[FAIL] API Error: {data.get('error')}")
    else:
        print(f"[FAIL] HTTP Error: {response.text}")
        
except Exception as e:
    print(f"[FAIL] Connection Failed: {e}")

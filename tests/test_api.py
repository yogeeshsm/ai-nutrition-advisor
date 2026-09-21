import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
for p in [root, os.path.join(root, 'app'), os.path.join(root, 'utils'), os.path.join(root, 'chatbots'), os.path.join(root, 'scripts')]:
    if p not in sys.path:
        sys.path.insert(0, p)

"""Test API endpoints"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_get_children():
    """Test GET /api/get-children endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/get-children", timeout=5)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"\n{json.dumps(data, indent=2)}")
        
        if data.get('success') and data.get('children'):
            print(f"\n[OK] Found {len(data['children'])} children:")
            for child in data['children']:
                print(f"   - ID {child['id']}: {child['name']} ({child['age']}y old)")
    except Exception as e:
        print(f"[FAIL] Error: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Child Identity API")
    print("=" * 50)
    test_get_children()

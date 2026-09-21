import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
for p in [root, os.path.join(root, 'app'), os.path.join(root, 'utils'), os.path.join(root, 'chatbots'), os.path.join(root, 'scripts')]:
    if p not in sys.path:
        sys.path.insert(0, p)

from flask_app import app
import json

with app.test_client() as client:
    response = client.get('/api/get-children')
    data = json.loads(response.data)
    
    if data['success'] and data['children']:
        first_child = data['children'][0]
        print("First child data:")
        for key, value in first_child.items():
            print(f"  {key}: {value}")
        
        # Check for required fields
        required = ['age_years', 'weight_kg']
        missing = [f for f in required if f not in first_child]
        
        if missing:
            print(f"\n[WARN]  Missing fields: {missing}")
        else:
            print("\n[OK] All required fields present!")

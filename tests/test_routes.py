import sys
import os

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
for p in [root, os.path.join(root, 'app'), os.path.join(root, 'utils'), os.path.join(root, 'chatbots')]:
    if p not in sys.path:
        sys.path.insert(0, p)

import flask_app

print("\n" + "="*70)
print("REGISTERED ROUTES IN FLASK_APP.PY")
print("="*70 + "\n")

routes = []
for rule in flask_app.app.url_map.iter_rules():
    if rule.endpoint != 'static':
        routes.append((rule.endpoint, rule.rule, ','.join(rule.methods - {'HEAD', 'OPTIONS'})))

routes.sort()

for endpoint, rule, methods in routes:
    print(f"  {endpoint:45s} {methods:15s} {rule}")

print(f"\n  Total routes: {len(routes)}\n")

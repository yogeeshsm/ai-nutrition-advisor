import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
for p in [root, os.path.join(root, 'app'), os.path.join(root, 'utils'), os.path.join(root, 'chatbots'), os.path.join(root, 'scripts')]:
    if p not in sys.path:
        sys.path.insert(0, p)

import sqlite3

conn = sqlite3.connect('nutrition_advisor.db')
cursor = conn.cursor()

# Search for peanuts
cursor.execute("SELECT name, category, protein_per_100g, iron_per_100g FROM ingredients WHERE LOWER(name) LIKE LOWER('%peanut%')")
results = cursor.fetchall()

print("Found ingredients containing 'peanut':")
for r in results:
    print(f"  [OK] {r[0]} ({r[1]}) - Protein: {r[2]}g, Iron: {r[3]}mg")

conn.close()

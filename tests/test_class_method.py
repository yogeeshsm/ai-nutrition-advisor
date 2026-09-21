import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
for p in [root, os.path.join(root, 'app'), os.path.join(root, 'utils'), os.path.join(root, 'chatbots'), os.path.join(root, 'scripts')]:
    if p not in sys.path:
        sys.path.insert(0, p)

from ml_recommender import MealRecommendationSystem
import sqlite3
import pandas as pd

print("Testing MealRecommendationSystem.prepare_child_profile directly\n")

# Create instance
rec = MealRecommendationSystem()

# Test child_id
child_id = 1

# Get direct connection to verify data exists
conn = sqlite3.connect('nutrition_advisor.db')
test_query = "SELECT * FROM children WHERE id = ?"
test_result = pd.read_sql_query(test_query, conn, params=(child_id,))
print(f"Direct DB query: {len(test_result)} rows")
conn.close()

# Now test through the class method
print(f"\nCalling rec.prepare_child_profile({child_id})...")
profile = rec.prepare_child_profile(child_id)

if profile:
    print(f"[OK] Profile returned: {profile}")
else:
    print("[FAIL] Profile is None!")

# Check the connection method
print(f"\nChecking rec.get_connection()...")
conn2 = rec.get_connection()
print(f"Connection object: {conn2}")
print(f"Database: {conn2.execute('PRAGMA database_list').fetchall()}")

# Try query directly through the class connection
test2 = pd.read_sql_query(test_query, conn2, params=(child_id,))
print(f"Query through class connection: {len(test2)} rows")
conn2.close()

import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
for p in [root, os.path.join(root, 'app'), os.path.join(root, 'utils'), os.path.join(root, 'chatbots'), os.path.join(root, 'scripts')]:
    if p not in sys.path:
        sys.path.insert(0, p)

"""Test Soya Chunks ingredient with comma"""
import sqlite3

# Test database query
conn = sqlite3.connect('nutrition_advisor.db')
cursor = conn.cursor()

# Check if Soya Chunks exists
print("Testing 'Soya Chunks' search:")
cursor.execute("SELECT name, category, protein_per_100g FROM ingredients WHERE LOWER(name) LIKE LOWER(?)", ('%soya chunks%',))
result = cursor.fetchone()
if result:
    print(f"[OK] Found: {result[0]} ({result[1]}) - Protein: {result[2]}g")
else:
    print("[FAIL] Not found")

conn.close()

# Test ML recommender with sanitization
print("\nTesting ML Recommender with 'Soya Chunks,' (with comma):")
from ml_recommender import MealRecommendationSystem

recommender = MealRecommendationSystem()
acceptance, found = recommender.predict_ingredient_acceptance(1, "Soya Chunks,")

if found:
    print(f"[OK] SUCCESS! 'Soya Chunks,' handled correctly")
    print(f"   Acceptance Probability: {acceptance * 100:.1f}%")
else:
    print("[FAIL] FAILED: Ingredient not found even with comma")

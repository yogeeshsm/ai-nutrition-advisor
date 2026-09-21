import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
for p in [root, os.path.join(root, 'app'), os.path.join(root, 'utils'), os.path.join(root, 'chatbots'), os.path.join(root, 'scripts')]:
    if p not in sys.path:
        sys.path.insert(0, p)

"""Direct test of predict_ingredient_acceptance"""
from ml_recommender import MealRecommendationSystem

recommender = MealRecommendationSystem()

# Test direct prediction
print("Testing predict_ingredient_acceptance:")
result = recommender.predict_ingredient_acceptance(1, "Soya Chunks")
print(f"Result type: {type(result)}")
print(f"Result value: {result}")

if isinstance(result, tuple):
    prob, found = result
    print(f"[OK] Tuple unpacked correctly: prob={prob}, found={found}")
else:
    print(f"[FAIL] ERROR: Expected tuple but got {type(result)}")

# Test get_recommendation_explanation
print("\nTesting get_recommendation_explanation:")
try:
    explanation = recommender.get_recommendation_explanation(1, "Soya Chunks")
    print(f"[OK] Success! Explanation keys: {list(explanation.keys())}")
    print(f"  Acceptance probability: {explanation.get('acceptance_probability')}%")
except Exception as e:
    print(f"[FAIL] ERROR: {e}")
    import traceback
    traceback.print_exc()

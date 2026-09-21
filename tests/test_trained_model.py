import sys
import os

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
for p in [root, os.path.join(root, 'app'), os.path.join(root, 'utils'), os.path.join(root, 'chatbots')]:
    if p not in sys.path:
        sys.path.insert(0, p)

from malnutrition_predictor import get_predictor

p = get_predictor()
result = p.predict(59, 18.0, 109.0)

print(f"\n=== TESTING TRAINED MODEL ===")
print(f"Lakshmi Iyer (59 months, 18kg, 109cm)")
print(f"  Status: {result['nutrition_status']}")
print(f"  Risk: {result['risk_level']}")
print(f"  Confidence: {result['confidence']*100:.1f}%")
print(f"\nProbabilities:")
for status, prob in result['probabilities'].items():
    print(f"  {status}: {prob*100:.1f}%")

import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
for p in [root, os.path.join(root, 'app'), os.path.join(root, 'utils'), os.path.join(root, 'chatbots'), os.path.join(root, 'scripts')]:
    if p not in sys.path:
        sys.path.insert(0, p)

"""Test if malnutrition predictor can be imported"""
try:
    from malnutrition_predictor import get_predictor
    print("[OK] Predictor imports successfully")
    predictor = get_predictor()
    print("[OK] Predictor loads successfully")
except Exception as e:
    print(f"[ERROR] Failed: {e}")
    import traceback
    traceback.print_exc()

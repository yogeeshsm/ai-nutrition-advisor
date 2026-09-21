import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
for p in [root, os.path.join(root, 'app'), os.path.join(root, 'utils'), os.path.join(root, 'chatbots'), os.path.join(root, 'scripts')]:
    if p not in sys.path:
        sys.path.insert(0, p)

"""
Test Food Recognition System
Tests the Gemini-based food recognition without needing images
"""

try:
    from gemini_food_recognition import GeminiFoodRecognizer, INDIAN_FOOD_DATABASE
except ImportError as e:
    print(f"[INFO] Food recognition system test skipped: {e}")
    GeminiFoodRecognizer = None
    INDIAN_FOOD_DATABASE = {}
import json

print("\n" + "="*80)
print("   [TEST] TESTING FOOD RECOGNITION SYSTEM")
print("="*80 + "\n")

if GeminiFoodRecognizer is None:
    print("[INFO] GeminiFoodRecognizer module not installed or available.")
else:
    recognizer = GeminiFoodRecognizer()
    if recognizer.model:
        print("[OK] Gemini Vision API initialized successfully")
    else:
        print("[FAIL] Gemini API not available")
        print("   Please ensure GEMINI_API_KEY is set in .env file")

    # Test 2: Check food database
    print("\n\nTEST 2: Food Database")
    print("-" * 80)
    print(f"[OK] Food database loaded with {len(INDIAN_FOOD_DATABASE)} items")
    print("\nSample foods:")
    for food in list(INDIAN_FOOD_DATABASE.keys())[:5]:
        data = INDIAN_FOOD_DATABASE[food]
        print(f"    {food:15s} - {data['calories']} cal, {data['protein']}g protein")

    # Test 3: Calculate nutrition
    print("\n\nTEST 3: Nutrition Calculation")
    print("-" * 80)
    test_food = 'rice'
    test_weight = 150  # grams

    nutrition = recognizer.calculate_nutrition(test_food, test_weight)
    print(f"Food: {test_food.title()}")
    print(f"Weight: {test_weight}g")
    print(f"Nutrition:")
    print(f"   Calories: {nutrition['calories']} kcal")
    print(f"   Protein: {nutrition['protein']}g")
    print(f"   Carbs: {nutrition['carbs']}g")
    print(f"   Fat: {nutrition['fat']}g")

    # Test 4: Assess nutrition
    print("\n\nTEST 4: Nutritional Assessment")
    print("-" * 80)
    assessment = recognizer.assess_nutrition(nutrition)
    print(f"Daily percentages:")
    for nutrient, percent in assessment['daily_percentages'].items():
        print(f"   {nutrient:10s}: {percent:5.1f}%")

    print(f"\nRecommendations:")
    for rec in assessment['recommendations']:
        emoji = "[WARN]" if rec['type'] == 'warning' else "[OK]"
        print(f"   {emoji} {rec['message']}")
        print(f"       {rec['suggestion']}")

# Test 5: Check if ready for deployment
print("\n\n" + "="*80)
print("    DEPLOYMENT READINESS")
print("="*80)

checks = {
    'Gemini API configured': recognizer.model is not None,
    'Food database loaded': len(INDIAN_FOOD_DATABASE) > 0,
    'Nutrition calculator working': nutrition['calories'] > 0,
    'Assessment working': len(assessment['recommendations']) > 0
}

all_pass = all(checks.values())

for check, status in checks.items():
    status_icon = "[OK]" if status else "[FAIL]"
    print(f"{status_icon} {check}")

print("\n" + "="*80)
if all_pass:
    print("   [OK] FOOD RECOGNITION IS READY FOR DEPLOYMENT!")
else:
    print("   [WARN]  Some components need attention (see above)")
print("="*80 + "\n")

print("\n HOW TO USE:")
print("   1. Upload food image via web interface:")
print("      http://localhost:5000/food-recognition")
print("   2. Or use API:")
print("      POST /api/analyze-food-image")
print("      Content-Type: multipart/form-data")
print("      Body: image file")
print("\n No training required - works immediately!\n")

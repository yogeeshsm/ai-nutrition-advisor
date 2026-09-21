import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
for p in [root, os.path.join(root, 'app'), os.path.join(root, 'utils'), os.path.join(root, 'chatbots'), os.path.join(root, 'scripts')]:
    if p not in sys.path:
        sys.path.insert(0, p)

"""
Quick test to verify Groq chatbot is working
"""

from gemini_chatbot import NutritionChatbot

print("[TEST] Testing Groq-powered Nutrition Chatbot...\n")
print("=" * 80)

# Initialize chatbot
try:
    chatbot = NutritionChatbot()
    print("[OK] Chatbot initialized successfully!")
    print(f"   Model: {chatbot.GROQ_MODEL}")
    print(f"   API Key: {chatbot.api_key[:20]}...")
except Exception as e:
    print(f"[INFO] Chatbot test skipped or API key not set: {e}")

print("\n" + "=" * 80)
print(" Testing Chat Functionality")
print("=" * 80 + "\n")

# Test questions
test_questions = [
    "What are good iron sources for preventing anemia in children?",
    "How much protein does a 5-year-old child need daily?",
    "What are budget-friendly calcium sources?"
]

for i, question in enumerate(test_questions, 1):
    print(f"\n{i}. Question: {question}")
    print("-" * 80)
    
    try:
        response = chatbot.chat(question)
        print(f"[OK] Response received ({len(response)} chars):")
        print(response)
    except Exception as e:
        print(f"[FAIL] Error: {e}")

print("\n" + "=" * 80)
print("[OK] CHATBOT TEST COMPLETE!")
print("=" * 80)

print("\n To use in Flask app:")
print("   1. Run: python flask_app.py")
print("   2. Open: http://localhost:5000/chatbot")
print("   3. Or POST to: http://localhost:5000/api/chatbot")

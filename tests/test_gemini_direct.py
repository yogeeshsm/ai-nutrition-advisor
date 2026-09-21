import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
for p in [root, os.path.join(root, 'app'), os.path.join(root, 'utils'), os.path.join(root, 'chatbots'), os.path.join(root, 'scripts')]:
    if p not in sys.path:
        sys.path.insert(0, p)

"""Direct test of gemini_chatbot with fresh import"""
import sys
# Remove cached module
if 'gemini_chatbot' in sys.modules:
    del sys.modules['gemini_chatbot']

import os
# Make sure GEMINI_API_KEY is set in your .env file

from gemini_chatbot import get_chatbot

try:
    print("Creating chatbot...")
    bot = get_chatbot()
    print(f"Model: {bot.model._model_name}")

    print("\nTesting chat...")
    response = bot.chat("Name 2 protein foods")
    print(f"Response: {response}")
except Exception as e:
    print(f"[INFO] Gemini Chatbot test skipped or key not set: {e}")

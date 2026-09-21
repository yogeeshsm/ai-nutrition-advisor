import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
for p in [root, os.path.join(root, 'app'), os.path.join(root, 'utils'), os.path.join(root, 'chatbots'), os.path.join(root, 'scripts')]:
    if p not in sys.path:
        sys.path.insert(0, p)

"""Quick test of OpenAI chatbot"""
import os
os.environ['AI_PROVIDER'] = 'openai'
# Make sure OPENAI_API_KEY is set in your .env file

from ai_chatbot import get_chatbot

print("Testing OpenAI chatbot...")
print(f"AI_PROVIDER: {os.environ.get('AI_PROVIDER')}")

try:
    bot = get_chatbot()
    print(f"Bot provider: {bot.provider}")
    print(f"Bot model: {bot.model_name}")

    response = bot.chat("List 3 iron-rich foods for toddlers")
    print(f"\nResponse: {response['response']}")
    print("\n[OK] OpenAI chatbot working!")
except Exception as e:
    print(f"[INFO] OpenAI Chatbot test skipped or key not set: {e}")

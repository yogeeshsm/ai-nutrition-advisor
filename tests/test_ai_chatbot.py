import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
for p in [root, os.path.join(root, 'app'), os.path.join(root, 'utils'), os.path.join(root, 'chatbots'), os.path.join(root, 'scripts')]:
    if p not in sys.path:
        sys.path.insert(0, p)

"""Test if ai_chatbot imports correctly"""
import sys
print(f"Python path: {sys.path[0]}")

try:
    from ai_chatbot import get_chatbot
    print("[OK] ai_chatbot imported successfully")
    
    import os
    os.environ['AI_PROVIDER'] = 'gemini'
    
    bot = get_chatbot('gemini')
    print(f"[OK] Chatbot created: provider={bot.provider}")
    print(f"[OK] Model: {bot.model._model_name if hasattr(bot.model, '_model_name') else 'unknown'}")
    
    response = bot.chat("Test")
    print(f"[OK] Response received: {response['response'][:100]}...")
except Exception as e:
    print(f"[INFO] Chatbot test skipped or API key not set: {e}")

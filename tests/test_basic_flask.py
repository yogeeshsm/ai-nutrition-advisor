import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
for p in [root, os.path.join(root, 'app'), os.path.join(root, 'utils'), os.path.join(root, 'chatbots'), os.path.join(root, 'scripts')]:
    if p not in sys.path:
        sys.path.insert(0, p)

"""Test if flask_app can run at all"""
import sys
import os

os.chdir(root)

print("Step 1: Importing Flask...")
from flask import Flask
print("OK")

print("Step 2: Creating app...")
app = Flask(__name__)
print("OK")

print("Step 3: Adding route...")
@app.route('/')
def home():
    return '<h1>Server is running!</h1><p>All features will be available soon.</p>'
print("OK")

if __name__ == '__main__':
    print("Step 4: Starting server with waitress...")
    try:
        from waitress import serve
        print("Waitress imported")
        print("Starting on http://0.0.0.0:5000")
        serve(app, host='0.0.0.0', port=5000, threads=4)
    except KeyboardInterrupt:
        print("\nServer stopped")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

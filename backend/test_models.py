import sys
import os
import google.generativeai as genai

api_key = sys.argv[1] if len(sys.argv) > 1 else None
if not api_key:
    print("Please provide an API key")
    sys.exit(1)

genai.configure(api_key=api_key)

try:
    print("Available Models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error checking models: {e}")

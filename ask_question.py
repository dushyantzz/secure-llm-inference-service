#!/usr/bin/env python3
"""
Simple script to ask questions to the LLM model
"""
import requests
import json
import sys

# Configuration
BASE_URL = "http://127.0.0.1:8000"
USERNAME = "demo"
PASSWORD = "demo1234"

def get_token():
    """Get authentication token"""
    print("🔐 Getting authentication token...")
    response = requests.post(
        f"{BASE_URL}/auth/token",
        data={"username": USERNAME, "password": PASSWORD},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if response.status_code == 200:
        token_data = response.json()
        print(f"✅ Token obtained successfully!")
        return token_data["access_token"]
    else:
        print(f"❌ Authentication failed: {response.status_code}")
        print(response.text)
        return None

def ask_question(prompt, token):
    """Ask a question to the model"""
    print(f"\n🤔 Asking: {prompt}")
    print("⏳ Waiting for response...\n")
    
    response = requests.post(
        f"{BASE_URL}/v1/infer",
        json={"prompt": prompt},
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Response received:")
        print("-" * 60)
        print(result["response"])
        print("-" * 60)
        return result["response"]
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

def main():
    print("=" * 60)
    print("Secure LLM Inference Service - Question Interface")
    print("=" * 60)
    
    # Get token
    token = get_token()
    if not token:
        return
    
    # Check if we have command-line arguments (non-interactive mode)
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        print("\n" + "=" * 60)
        print("Non-Interactive Mode")
        print("=" * 60)
        ask_question(question, token)
        return
    
    # Example questions (only shown in interactive mode)
    questions = [
        "What is artificial intelligence?",
        "Explain quantum computing in simple terms.",
        "Write a haiku about technology."
    ]
    
    print("\n" + "=" * 60)
    print("Example Questions:")
    print("=" * 60)
    
    for i, question in enumerate(questions, 1):
        print(f"\n[Question {i}]")
        ask_question(question, token)
        print()
    
    # Interactive mode (only if stdin is a TTY)
    if sys.stdin.isatty():
        print("\n" + "=" * 60)
        print("Interactive Mode - Type your questions (or 'quit' to exit)")
        print("=" * 60)
        
        while True:
            try:
                user_question = input("\n💬 Your question: ").strip()
                
                if user_question.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if user_question:
                    ask_question(user_question, token)
                else:
                    print("Please enter a question.")
            except (EOFError, KeyboardInterrupt):
                print("\n\n👋 Goodbye!")
                break
    else:
        # Non-interactive mode - read from stdin
        print("\n" + "=" * 60)
        print("Reading questions from stdin...")
        print("=" * 60)
        try:
            for line in sys.stdin:
                question = line.strip()
                if question:
                    ask_question(question, token)
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Done!")

if __name__ == "__main__":
    main()


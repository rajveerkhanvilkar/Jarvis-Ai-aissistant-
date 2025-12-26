"""
Google Gemini Chat Integration (FREE)
No cost, 1500 requests per day
Very natural conversations
"""

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ Google Gemini not installed. Run: pip install google-generativeai")

# ==================== CONFIGURATION ====================

# Get your FREE API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your free key

# ==================== CHAT FUNCTION ====================

def chat_with_gemini(message, context="You are Jarvis, a helpful AI assistant."):
    """
    Chat with Google Gemini AI (free tier)
    
    Args:
        message: User's message
        context: System context/personality
        
    Returns:
        AI response as string
    """
    if not GEMINI_AVAILABLE:
        return "Gemini AI is not installed. Please run: pip install google-generativeai"
    
    if GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        return "Please add your free Gemini API key in backend/gemini_chat.py"
    
    try:
        # Configure API
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Create model
        model = genai.GenerativeModel('gemini-pro')
        
        # Add context to message
        full_prompt = f"{context}\n\nUser: {message}\nJarvis:"
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        return response.text
        
    except Exception as e:
        print(f"Gemini error: {e}")
        return "I'm having trouble connecting to my AI brain right now."


def chat_with_personality(message):
    """
    Chat with Jarvis personality
    """
    context = """You are Jarvis, an advanced AI assistant inspired by Iron Man's AI.
You are helpful, intelligent, and have a slightly witty personality.
You assist with tasks, answer questions, and have natural conversations.
Keep responses concise (2-3 sentences) unless asked for details."""
    
    return chat_with_gemini(message, context)


# ==================== TEST ====================

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Gemini Chat")
    print("=" * 60)
    
    if GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        print("\n⚠️ Please add your FREE API key!")
        print("Get it from: https://makersuite.google.com/app/apikey")
        print("\nSteps:")
        print("1. Go to the link above")
        print("2. Click 'Create API Key'")
        print("3. Copy the key")
        print("4. Paste it in backend/gemini_chat.py (line 16)")
    else:
        # Test conversation
        test_messages = [
            "Hello, how are you?",
            "What can you do?",
            "Tell me a joke"
        ]
        
        for msg in test_messages:
            print(f"\nYou: {msg}")
            response = chat_with_personality(msg)
            print(f"Jarvis: {response}")
    
    print("\n" + "=" * 60)

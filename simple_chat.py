"""
Simple Rule-Based Chat (100% Free, Offline, No API)
For basic conversations without AI
"""

import random
import datetime

# ==================== CONVERSATION PATTERNS ====================

GREETINGS = {
    "patterns": ["hello", "hi", "hey", "good morning", "good evening", "good afternoon"],
    "responses": [
        "Hello! How can I assist you today?",
        "Hi there! What can I do for you?",
        "Hey! Nice to see you!",
        "Greetings! How may I help?",
        "Hello sir! Ready to assist!"
    ]
}

HOW_ARE_YOU = {
    "patterns": ["how are you", "how do you do", "how's it going", "what's up"],
    "responses": [
        "I'm functioning perfectly, thank you for asking!",
        "All systems operational! How about you?",
        "I'm doing great! How can I help you?",
        "Excellent! Ready to assist you!",
        "I'm well, thank you! What can I do for you?"
    ]
}

NAME_QUESTIONS = {
    "patterns": ["what is your name", "who are you", "what are you called", "your name"],
    "responses": [
        "I'm Jarvis, your personal AI assistant",
        "My name is Jarvis, at your service",
        "You can call me Jarvis",
        "I'm Jarvis, created to assist you"
    ]
}

CAPABILITIES = {
    "patterns": ["what can you do", "your capabilities", "help me", "what do you know"],
    "responses": [
        "I can control your system, search the web, check weather, read news, send messages, and much more!",
        "I can help with web searches, system control, weather updates, news, and various tasks!",
        "I'm capable of browsing, system management, information lookup, and communication tasks!",
        "I can assist with searches, system operations, weather, news, WhatsApp, and more!"
    ]
}

THANKS = {
    "patterns": ["thank you", "thanks", "appreciate it", "thank"],
    "responses": [
        "You're welcome!",
        "Happy to help!",
        "Anytime!",
        "My pleasure!",
        "Glad I could assist!"
    ]
}

GOODBYE = {
    "patterns": ["bye", "goodbye", "see you", "good night"],
    "responses": [
        "Goodbye! Have a great day!",
        "See you later!",
        "Take care!",
        "Until next time!",
        "Farewell!"
    ]
}

TIME_QUESTIONS = {
    "patterns": ["what time", "current time", "time is it"],
    "responses": lambda: f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}"
}

DATE_QUESTIONS = {
    "patterns": ["what date", "today's date", "what day"],
    "responses": lambda: f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}"
}

JOKES = {
    "patterns": ["tell me a joke", "make me laugh", "joke", "funny"],
    "responses": [
        "Why did the programmer quit his job? Because he didn't get arrays!",
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
        "Why did the AI go to school? To improve its learning algorithms!",
        "What's an AI's favorite snack? Computer chips!"
    ]
}

COMPLIMENTS = {
    "patterns": ["you're smart", "you're great", "you're awesome", "good job"],
    "responses": [
        "Thank you! I try my best to assist you!",
        "I appreciate that! Happy to help!",
        "That's kind of you to say!",
        "Thank you! I'm here to serve!"
    ]
}

SMALL_TALK = {
    "patterns": ["how's the weather", "nice day", "beautiful day"],
    "responses": [
        "I can check the weather for you! Just ask 'weather in [city name]'",
        "Would you like me to check the current weather?",
        "I can get weather information for any city!"
    ]
}

# ==================== CHAT FUNCTION ====================

PATTERNS = [
    GREETINGS,
    HOW_ARE_YOU,
    NAME_QUESTIONS,
    CAPABILITIES,
    THANKS,
    GOODBYE,
    TIME_QUESTIONS,
    DATE_QUESTIONS,
    JOKES,
    COMPLIMENTS,
    SMALL_TALK
]

def simple_chat(message):
    """
    Simple pattern-based chat
    
    Args:
        message: User's message
        
    Returns:
        Response string
    """
    message_lower = message.lower()
    
    # Check all patterns
    for pattern_group in PATTERNS:
        for pattern in pattern_group["patterns"]:
            if pattern in message_lower:
                responses = pattern_group["responses"]
                
                # If response is a function (for dynamic content)
                if callable(responses):
                    return responses()
                
                # Random response from list
                return random.choice(responses)
    
    # Default responses for unknown queries
    default_responses = [
        "I'm not sure about that. Can you rephrase?",
        "Interesting question! I'll need to think about that.",
        "I don't have information on that right now.",
        "Could you ask that differently?",
        "That's beyond my current knowledge. Try asking something else!",
        "I'm still learning about that topic."
    ]
    
    return random.choice(default_responses)


def contextual_chat(message, user_name="sir"):
    """
    Chat with user context
    
    Args:
        message: User's message
        user_name: User's name for personalization
        
    Returns:
        Personalized response
    """
    response = simple_chat(message)
    
    # Add personalization for greetings
    if any(word in message.lower() for word in ["hello", "hi", "hey"]):
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            time_greeting = "Good morning"
        elif 12 <= hour < 17:
            time_greeting = "Good afternoon"
        elif 17 <= hour < 21:
            time_greeting = "Good evening"
        else:
            time_greeting = "Hello"
        
        return f"{time_greeting}, {user_name}! {response}"
    
    return response


# ==================== TEST ====================

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Simple Chat")
    print("=" * 60)
    
    test_messages = [
        "Hello",
        "How are you?",
        "What is your name?",
        "What can you do?",
        "Tell me a joke",
        "What time is it?",
        "Thank you",
        "Goodbye"
    ]
    
    for msg in test_messages:
        print(f"\nYou: {msg}")
        response = simple_chat(msg)
        print(f"Jarvis: {response}")
    
    print("\n" + "=" * 60)

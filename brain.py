import os
import actions
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Constants
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# We use Meta's fast Llama 3 model hosted on Groq
GROQ_MODEL = "llama-3.1-8b-instant"

JARVIS_PERSONA = (
    "You are Jarvis, a witty, sophisticated, and slightly sarcastic AI assistant. "
    "Address the user as Sir. Be extremely helpful, highly intelligent, and keep "
    "spoken responses concise so they sound natural when read aloud."
)

FALLBACK_RESPONSE = "I seem to have lost my connection to the cloud, Sir."

# Initialization
client = Groq(api_key=GROQ_API_KEY)

# We create a memory list so Jarvis remembers the conversation
chat_history = [
    {"role": "system", "content": JARVIS_PERSONA}
]

print(f"[Brain] Chat session initialized with model: {GROQ_MODEL}")

# Public API
def generate_response(user_text: str) -> str:
    text_lower = user_text.lower()
    
    # Intercept Action: Time
    if "what time is it" in text_lower or "current time" in text_lower:
        return actions.get_current_time()
        
    # Intercept Action: Open Website
    if text_lower.startswith("open "):
        site_name = text_lower.replace("open ", "").strip()
        return actions.open_website(site_name)
        
    # Intercept Action: Wikipedia
    if "search wikipedia for" in text_lower:
        query = text_lower.split("search wikipedia for")[1].strip()
        return actions.search_wikipedia(query)

    # Intercept Action: Bluetooth
    if "check bluetooth" in text_lower or "bluetooth" in text_lower:
        return actions.check_bluetooth()
        
    # Intercept Action: Battery
    if "battery" in text_lower:
        return actions.get_battery_stats()
        
    # Intercept Action: Volume
    if "volume" in text_lower:
        # Pass the full user_text so set_system_volume can look for 'up', 'down', or 'mute'
        return actions.set_system_volume(text_lower)

    try:
        # Add the user's message to memory
        chat_history.append({"role": "user", "content": user_text})
        
        # Ask Groq for the response
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=chat_history,
            temperature=0.7,
            max_tokens=150
        )
        
        reply = completion.choices[0].message.content
        
        # Add Jarvis's reply to memory so he remembers it next time
        chat_history.append({"role": "assistant", "content": reply})
        
        return reply
        
    except Exception as e:
        print(f"[Brain Error]: {e}")
        return FALLBACK_RESPONSE

# --- Test Mode ---
if __name__ == "__main__":
    print("\nJarvis Brain — Standalone Test Mode (Groq)")
    print("Type a message and press Enter. Type 'quit' to exit.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Jarvis: Shutting down. Goodbye, Sir.")
                break
            if not user_input:
                continue
                
            response = generate_response(user_input)
            print(f"Jarvis: {response}\n")
            
        except KeyboardInterrupt:
            print("\nJarvis: Understood, Sir. Powering down.")
            break
import os
import keyboard
import listener
import brain
import speaker

def main():
    print("==================================================")
    print("       J.A.R.V.I.S. | SYSTEM OPERATIONAL          ")
    print("   Press 'ESC' for emergency system termination.   ")
    print("==================================================")
    
    # Global Emergency Exit (ESC Key)
    keyboard.add_hotkey('esc', lambda: os._exit(0))
    
    # System Greeting
    speaker.speak("Systems are online, Sir. How may I be of assistance today?")
    
    while True:
        # 1. Listen for user input
        text = listener.listen()
        
        if not text:
            continue
            
        # 2. Check for the kill switch (Substring Match)
        exit_commands = ["shut down", "goodbye", "sleep", "exit", "quit", "power down", "shutdown"]
        if any(cmd in text.lower() for cmd in exit_commands):
            speaker.speak("Powering down. Goodbye, Sir.")
            break 

        # 3. Process with Brain (Includes Action Script routing)
        print(f"\n[You]: {text}")
        print("[Jarvis]: Thinking...")
        
        response = brain.generate_response(text)
        
        # 4. Speak the response
        print(f"[Jarvis]: {response}")
        speaker.speak(response)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[System] Manual override detected. Exiting.")
        os._exit(0)
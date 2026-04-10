import os
import sys
import keyboard
import listener
import brain
import speaker
import traceback
import ctypes

# --- Console Visibility Logic ---
# This allows us to build an EXE WITH a console, but hide it immediately on startup.
# Then we can toggle it back on when the user wants to monitor Jarvis!
SW_HIDE = 0
SW_SHOW = 5
console_visible = False

def toggle_console():
    global console_visible
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        if console_visible:
            ctypes.windll.user32.ShowWindow(hwnd, SW_HIDE)
            console_visible = False
        else:
            ctypes.windll.user32.ShowWindow(hwnd, SW_SHOW)
            console_visible = True

def hide_console_on_boot():
    global console_visible
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, SW_HIDE)
        console_visible = False

def main():
    # Hide the black window right when Jarvis boots up!
    hide_console_on_boot()

    # Emergency termination hotkey (Changing from ESC to CTRL+ALT+SHIFT+K)
    keyboard.add_hotkey('ctrl+alt+shift+k', lambda: os._exit(0))
    
    # Dashboard Toggle Hotkey! (Windows Key + Ctrl + J)
    keyboard.add_hotkey('windows+ctrl+j', toggle_console)
    
    # System Greeting
    speaker.speak("Jarvis is online and on standby in the background, Sir.")
    
    while True:
        # Halt execution until the hotkey is pressed
        keyboard.wait('ctrl+alt+shift+j')
        
        # --- Conversation Triggered ---
        if not os.environ.get('GROQ_API_KEY') and not os.path.exists(".env"):
            speaker.speak("Sir, I cannot find your API key.")
            continue

        speaker.speak("Yes, Sir? Jarvis here.")
        active_conversation = True
        is_first_command = True
        
        while active_conversation:
            # 1. Listen
            text = listener.listen(timeout_val=None if is_first_command else 10)
            
            if not text:
                active_conversation = False
                continue
            
            is_first_command = False
            text_lower = text.lower()
            
            # --- Check for Direct Action (Standby after execution) ---
            action_keywords = ["open ", "search wikipedia", "time", "battery", "bluetooth", "volume"]
            is_action = any(keyword in text_lower for keyword in action_keywords)
            
            # 2. Voice Standby Switch
            sleep_commands = ["shut down", "goodbye", "sleep", "exit", "quit", "power down", "shutdown", "stop listening"]
            if any(cmd in text_lower for cmd in sleep_commands):
                speaker.speak("Understood, Sir. Returning to standby mode.")
                active_conversation = False
                continue 

            # 3. Process & Speak
            response = brain.generate_response(text)
            speaker.speak(response)
            
            # IF this was a direct action (opening site, checking time), go to standby now
            if is_action:
                print("[System] Action completed. Returning to standby.")
                active_conversation = False

if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Create an error log file if the EXE crashes
        with open("jarvis_error.log", "a") as f:
            f.write("\n--- JARVIS CRASH REPORT ---\n")
            traceback.print_exc(file=f)
        
        try:
            speaker.speak("A fatal system error occurred. Check the error log.")
        except:
            pass
        os._exit(1)
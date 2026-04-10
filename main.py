import os
import sys
import keyboard
import listener
import brain
import speaker
import traceback
import ctypes

# console logic to hide or show the black window
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
    # hide window on startup
    hide_console_on_boot()

    # kill switch - press ctrl+alt+shift+k to close everything
    keyboard.add_hotkey('ctrl+alt+shift+k', lambda: os._exit(0))
    
    # press windows+ctrl+j to toggle the logs window
    keyboard.add_hotkey('windows+ctrl+j', toggle_console)
    
    # say something when jarvis turns on    speaker.speak("Jarvis is online and on standby in the background, Sir.")
    
    while True:
        # wait for me to press the hotkey
        keyboard.wait('ctrl+alt+shift+j')
        
        # convo starts here
        if not os.environ.get('GROQ_API_KEY') and not os.path.exists(".env"):
            speaker.speak("Sir, I cannot find your API key.")
            continue

        speaker.speak("Yes, Sir? Jarvis here.")
        active_conversation = True
        is_first_command = True
        
        while active_conversation:
            # step 1: listen to the microphone
            text = listener.listen(timeout_val=None if is_first_command else 10)
            
            if not text:
                active_conversation = False
                continue
            
            is_first_command = False
            text_lower = text.lower()
            
            # check if it is a system action so we can go back to sleep instantly
            action_keywords = ["open ", "search wikipedia", "time", "battery", "bluetooth", "volume"]
            is_action = any(keyword in text_lower for keyword in action_keywords)
            
            # step 2: check if i told him to shut up
            sleep_commands = ["shut down", "goodbye", "sleep", "exit", "quit", "power down", "shutdown", "stop listening"]
            if any(cmd in text_lower for cmd in sleep_commands):
                speaker.speak("Understood, Sir. Returning to standby mode.")
                active_conversation = False
                continue 

            # step 3: get response and speak it
            response = brain.generate_response(text)
            speaker.speak(response)
            
            # if it was an action then go back to standby 
            if is_action:
                print("[System] Action completed. Returning to standby.")
                active_conversation = False

if __name__ == "__main__":
    try:
        main()
    except Exception:
        # logs the error to a file if it crashes
        with open("jarvis_error.log", "a") as f:
            f.write("\n--- JARVIS CRASH REPORT ---\n")
            traceback.print_exc(file=f)
        
        try:
            speaker.speak("A fatal system error occurred. Check the error log.")
        except:
            pass
        os._exit(1)
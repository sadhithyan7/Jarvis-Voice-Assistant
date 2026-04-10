import os
import threading
import winsound
import speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()

def _beep(freq: int, duration: int = 150):
    """Fires a simple system beep on a side thread."""
    threading.Thread(target=winsound.Beep, args=(freq, duration), daemon=True).start()

def listen(timeout_val=None):
    """
    Listens to the microphone and returns the transcribed text.
    - timeout_val: Seconds to wait for speech to start. Use None for the first command.
    """
    recognizer = sr.Recognizer()
    
    # We want to beep BEFORE we open the mic so the user knows it's hot
    _beep(400, 100) # Soft, low-pitched "blonk" tone
    
    try:
        with sr.Microphone() as source:
            print(f"[Listener] 🔴 Mic active (Timeout: {timeout_val}s)...")
            # Faster calibration for better responsiveness
            recognizer.adjust_for_ambient_noise(source, duration=0.8)
            
            # Record...
            audio = recognizer.listen(source, timeout=timeout_val, phrase_time_limit=15)
            
            print("[Listener] Processing audio...")
            
            text = recognizer.recognize_google(audio)
            print(f"[Listener] Transcribed: '{text}'")
            return text
            
    except sr.WaitTimeoutError:
        print("[Listener] Standby: No speech detected within timeout.")
        return None
    except sr.UnknownValueError:
        print("[Listener] Could not understand audio.")
        _beep(300, 400) # Low error buzz
        return None
    except sr.RequestError as e:
        print(f"[Listener] Internet error: {e}")
        return None
    except Exception as e:
        print(f"[Listener] Critical Error: {e}")
        return None

# --- Standalone Test ---
if __name__ == "__main__":
    print("Testing listener logic")
    while True:
        res = listen()
        if res and "shut down" in res.lower():
            break

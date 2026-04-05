import speech_recognition as sr

def listen():
    """
    Listens to the microphone, adjusts for ambient noise, and returns the recognized text.
    Handles timeouts and unrecognizable audio gracefully.
    """
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\n[Listener] Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("[Listener] Listening...")
        
        try:
            # timeout: how long to wait for speech to start before throwing WaitTimeoutError
            # phrase_time_limit: max seconds the recording can last
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
            print("[Listener] Processing audio...")
            
            text = recognizer.recognize_google(audio)
            print(f"[Listener] You said: '{text}'")
            return text
            
        except sr.WaitTimeoutError:
            print("[Listener] Timeout: No speech detected.")
            return None
        except sr.UnknownValueError:
            print("[Listener] Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"[Listener] API error from Speech Recognition service; {e}")
            return None
        except Exception as e:
            print(f"[Listener] An unexpected error occurred: {e}")
            return None

# --- Test Mode ---
if __name__ == "__main__":
    print("Testing listener...")
    while True:
        result = listen()
        if result and "shut down" in result.lower():
            print("Shutting down test loop.")
            break

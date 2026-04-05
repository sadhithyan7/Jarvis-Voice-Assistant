# speaker.py
# =============================================================================
# Phase 3 — The Mouth
# Responsibilities:
#   1. Accept a text string from brain.py.
#   2. Call edge-tts to generate an MP3 audio file asynchronously.
#   3. Play back the audio using pygame without blocking the main thread.
# TODO: Implementation will be added in the next phase.
# =============================================================================
import pyttsx3

def speak(text: str):
    """
    Takes a string of text and converts it to spoken audio using the local OS voice.
    """
    # Initialize the TTS engine
    engine = pyttsx3.init()
    
    # Jarvis Customizations (The Vibe)
    # 1. Speed: Default is around 200. We slow it down slightly for a more sophisticated, deliberate tone.
    engine.setProperty('rate', 175) 
    
    # 2. Voice: We tell Python to use your computer's default voice.
    voices = engine.getProperty('voices')
    
    # Optional: If you are on Windows, voices[0] is usually a male voice (David) and voices[1] is female (Zira).
    # We will set it to the first available voice for now.
    if voices:
        engine.setProperty('voice', voices[0].id)
    
    # Command the engine to speak
    engine.say(text)
    
    # Block the script from closing until he finishes talking
    engine.runAndWait()

# --- Test Mode ---
# If you run this file directly, it will test the speaker.
if __name__ == "__main__":
    print("Testing audio output...")
    speak("Hello Sir. My vocal systems are now fully online and operational.")
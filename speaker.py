# speaker.py
#Phase 3 — The Mouth
#1.accept a text string from brain.py.
#2.call edge-tts to generate an MP3 audio file.
#3.play back the audio using pygame.
import pyttsx3
def speak(text: str):
    # setup tts
    engine = pyttsx3.init()
    # 1.speed
    engine.setProperty('rate', 175) 
    
    # 2.voice - default
    voices = engine.getProperty('voices')
    
    #voices[0] - Male
    #voices[1] - Female
    if voices:
        engine.setProperty('voice', voices[0].id)
    
    # Command engine to speak
    engine.say(text)
    
    # Block the script from closing until he finishes talking
    engine.runAndWait()

# to test
if __name__ == "__main__":
    print("Testing audio output...")
    speak("Hello Sir. My vocal systems are now fully online and operational.")
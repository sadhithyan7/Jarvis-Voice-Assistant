# pip install wikipedia
import datetime
import webbrowser
import wikipedia
import subprocess
import psutil
import ctypes

def get_current_time():
    """Returns the current local time as a natural string."""
    try:
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"It is currently {time_str}, Sir."
    except Exception as e:
        print(f"[Actions Error - Time]: {e}")
        return "I am unable to determine the current time, Sir."

def open_website(site_name):
    """Opens common websites based on the spoken name."""
    try:
        url = f"https://www.{site_name.lower().strip()}.com"
        webbrowser.open(url)
        return f"Opening {site_name}, Sir."
    except Exception as e:
        print(f"[Actions Error - Website]: {e}")
        return f"I encountered an error trying to open {site_name}, Sir."

def search_wikipedia(query):
    """Fetches a concise 2-sentence summary of the query from Wikipedia."""
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"There are multiple results for {query}, Sir. Please be more specific."
    except wikipedia.exceptions.PageError:
        return f"I could not find any Wikipedia page for {query}, Sir."
    except Exception as e:
        print(f"[Actions Error - Wikipedia]: {e}")
        return "I encountered an error searching Wikipedia, Sir."

def check_bluetooth():
    """Uses PowerShell to check if Bluetooth is ON or OFF."""
    try:
        # Get-PnpDevice -Class Bluetooth returns the bluetooth devices. Status OK implies ON.
        result = subprocess.run(
            ["powershell", "-Command", "Get-PnpDevice -Class Bluetooth"],
            capture_output=True, text=True, check=True
        )
        if "OK" in result.stdout:
            return "Bluetooth is ON, Sir."
        else:
            return "Bluetooth is OFF, Sir."
    except Exception as e:
        print(f"[Actions Error - Bluetooth]: {e}")
        return "I could not determine the Bluetooth status at this time, Sir."

def get_battery_stats():
    """Uses psutil to return the current battery percentage and plugged-in status."""
    try:
        battery = psutil.sensors_battery()
        if not battery:
            return "I cannot detect a battery on this system, Sir."
        
        percent = battery.percent
        plugged = battery.power_plugged
        status = "plugged in and charging" if plugged else "running on battery power"
        return f"The system is currently at {percent}% battery and is {status}, Sir."
    except Exception as e:
        print(f"[Actions Error - Battery]: {e}")
        return "I could not retrieve the battery statistics, Sir."

def set_system_volume(level):
    """Uses ctypes to change the laptop volume using virtual key codes."""
    try:
        level_str = str(level).lower()
        if "up" in level_str or "increase" in level_str or "higher" in level_str:
            # 0xAF is VK_VOLUME_UP
            ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xAF, 0, 2, 0)
            return "I have increased the volume, Sir."
        elif "down" in level_str or "decrease" in level_str or "lower" in level_str:
            # 0xAE is VK_VOLUME_DOWN
            ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xAE, 0, 2, 0)
            return "I have decreased the volume, Sir."
        elif "mute" in level_str or "silence" in level_str:
            # 0xAD is VK_VOLUME_MUTE
            ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xAD, 0, 2, 0)
            return "The system is now muted, Sir."
        else:
            return f"I received the volume command, Sir. However, setting absolute numeric levels like '{level}' directly requires third-party audio libraries, so I have kept it steady."
    except Exception as e:
        print(f"[Actions Error - Volume]: {e}")
        return "I encountered an error trying to change the volume, Sir."

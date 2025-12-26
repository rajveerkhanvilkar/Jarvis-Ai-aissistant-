import time
import subprocess
import pyttsx3
import speech_recognition as sr
import eel
import sqlite3
import os
import psutil   # 🔹 for battery status
import webbrowser  # 🔹 for opening websites
import imaplib
import email
from email.header import decode_header
import audioop   # 🔹 for emotion (volume / tone)
import ctypes    # 🔹 for volume keys
import difflib   # 🔹 for fuzzy matching in DB answers

# 🔹 NEW: for live news / weather / cricket + web answers
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import urllib.parse   # 🔹 for encoding search / wiki queries
import json           # 🔹 for parsing JSON from Wikipedia

# ==================== EMAIL CONFIG ====================

EMAIL_ADDRESS = "rajveer.khanvilkarbhosle70@gmail.com"
EMAIL_PASSWORD = "qjtu ykbl lxcs jnfq"
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

# ======================================================
# 🔹 WINDOWS VOLUME CONTROL (no extra libs)
# ======================================================

VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002


def _press_key(key):
    try:
        ctypes.windll.user32.keybd_event(key, 0, KEYEVENTF_EXTENDEDKEY, 0)
        ctypes.windll.user32.keybd_event(key, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)
    except Exception as e:
        print("Volume key error:", e)


def increase_volume(steps: int = 5):
    speak("Increasing volume.")
    for _ in range(steps):
        _press_key(VK_VOLUME_UP)


def decrease_volume(steps: int = 5):
    speak("Decreasing volume.")
    for _ in range(steps):
        _press_key(VK_VOLUME_DOWN)


def mute_volume():
    speak("Muting volume.")
    _press_key(VK_VOLUME_MUTE)

# ======================================================
# 🔹 WINDOWS BRIGHTNESS CONTROL (via PowerShell)
# ======================================================


def _get_brightness():
    try:
        cmd = [
            "powershell",
            "-Command",
            "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        val = result.stdout.strip()
        if not val:
            raise ValueError("Empty brightness value")
        return int(val)
    except Exception as e:
        print("Get brightness error:", e)
        return None


def _set_brightness(level: int):
    try:
        level = max(0, min(100, int(level)))
        cmd = [
            "powershell",
            "-Command",
            f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})"
        ]
        subprocess.run(cmd, capture_output=True, text=True)
        return True
    except Exception as e:
        print("Set brightness error:", e)
        return False


def increase_brightness(step: int = 20):
    current = _get_brightness()
    if current is None:
        speak("Sorry, I cannot control brightness on this device.")
        return
    new_level = min(100, current + step)
    if _set_brightness(new_level):
        speak(f"Increasing brightness to around {new_level} percent.")


def decrease_brightness(step: int = 20):
    current = _get_brightness()
    if current is None:
        speak("Sorry, I cannot control brightness on this device.")
        return
    new_level = max(0, current - step)
    if _set_brightness(new_level):
        speak(f"Decreasing brightness to around {new_level} percent.")

# ======================================================
# 🔹 EMOTION ANALYSIS (angry / sad) – no API
# ======================================================


def analyze_and_respond_emotion(audio, text):
    """
    Simple emotion detection using loudness + speaking speed + words.
    Called every time you speak (inside takecommand()).
    """
    try:
        if not audio or not text:
            return

        raw = audio.get_raw_data()
        sample_width = audio.sample_width
        sample_rate = audio.sample_rate

        rms = audioop.rms(raw, sample_width)  # loudness
        duration = len(raw) / float(sample_rate * sample_width) if sample_rate > 0 else 0.0

        words = len(text.split())
        words_per_sec = (words / duration) if duration > 0 else 0

        emotion = "neutral"

        # Loud & fast -> probably angry / excited
        if rms > 3000 or words_per_sec > 3.0:
            emotion = "angry"
        # Very soft & slow -> probably sad / low
        elif rms < 800 and words_per_sec < 1.2:
            emotion = "sad"

        lower = text.lower()
        if any(w in lower for w in ["angry", "upset", "irritated", "frustrated", "what is this", "nonsense"]):
            emotion = "angry"
        if any(w in lower for w in ["sad", "tired", "exhausted", "not good", "bad day"]):
            emotion = "sad"

        if emotion == "angry":
            speak("You sound upset sir, is everything okay?")
        elif emotion == "sad":
            speak("Your voice sounds a bit low today. I'm here if you want to talk or need any help.")
        # neutral → stay silent
    except Exception as e:
        print("Emotion analysis error:", e)

# ======================================================
# 🔹 REAL-TIME INDIA NEWS / WEATHER / CRICKET (NO PAID API)
# ======================================================


def get_india_news():
    """
    Very fast India news using Google News RSS.
    No API key required.
    """
    try:
        speak("Getting latest India news.")
        url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
        resp = requests.get(url, timeout=3)
        resp.raise_for_status()

        root = ET.fromstring(resp.content)
        items = root.findall(".//item")[:3]  # top 3 headlines

        headlines = [item.find("title").text for item in items if item.find("title") is not None]

        if not headlines:
            speak("I could not find fresh India headlines right now.")
            return

        speak("Here are the top India headlines.")
        for h in headlines:
            speak(h)

    except Exception as e:
        print("India news error:", e)
        speak("Sorry, I could not fetch the latest India news right now.")


def get_weather_for_city(city: str = "Pune"):
    """
    Uses wttr.in free service. No API key.
    Example output: 'Pune: 🌦  +25°C'
    """
    try:
        city = (city or "Pune").strip()
        city_q = city.replace(" ", "+")
        url = f"https://wttr.in/{city_q}?format=3"

        speak(f"Checking weather for {city}.")
        resp = requests.get(url, timeout=3)
        text = resp.text.strip()

        if "Unknown location" in text or text == "":
            speak(f"Sorry, I could not find weather for {city}.")
        else:
            speak(text)

    except Exception as e:
        print("Weather error:", e)
        speak("Sorry, I could not fetch the weather right now.")


def get_live_cricket_score():
    """
    Scrapes Cricbuzz mobile live scores page.
    No API, just HTML parse.
    """
    try:
        speak("Getting live cricket scores.")
        url = "https://m.cricbuzz.com/cricket-match/live-scores"
        headers = {"User-Agent": "Mozilla/5.0"}

        resp = requests.get(url, headers=headers, timeout=4)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # First match card
        match_block = soup.find("div", class_="cb-mtch-lst")
        if not match_block:
            speak("Sorry, I did not find any live cricket scores right now.")
            return

        title = match_block.find("h3")
        status = match_block.find("span", class_="cb-text-live") \
                 or match_block.find("span", class_="cb-text-complete") \
                 or match_block.find("span", class_="cb-text-preview")

        score_lines = match_block.find_all("div", class_="cb-lv-scrs-col")
        scores = [s.get_text(strip=True) for s in score_lines]

        speak("Here is the latest live cricket update.")

        if title:
            speak(title.get_text(strip=True))

        for s in scores:
            if s:
                speak(s)

        if status:
            speak(status.get_text(strip=True))

    except Exception as e:
        print("Cricket score error:", e)
        speak("Sorry, I could not fetch live cricket scores right now.")

# ======================================================
# 🔹 GENERIC WEB ANSWER (WIKIPEDIA + GOOGLE SNIPPET)
# ======================================================


def get_quick_web_answer(query: str):
    """
    Try to fetch a short summary from Wikipedia (no API key).
    Returns a short text answer or None.
    """
    try:
        q = query.strip()
        if not q:
            return None

        # Encode query as a title for Wikipedia
        title = urllib.parse.quote(q)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        headers = {"User-Agent": "JarvisAssistant/1.0"}

        resp = requests.get(url, headers=headers, timeout=3)
        if resp.status_code != 200:
            return None

        data = resp.json()
        extract = data.get("extract") or ""

        if not extract:
            return None

        # Cut to ~400 chars for TTS
        if len(extract) > 400:
            cut = extract[:400]
            last_dot = cut.rfind(".")
            if last_dot > 80:
                extract = cut[:last_dot + 1]
            else:
                extract = cut

        return extract

    except Exception as e:
        print("Quick web answer error:", e)
        return None


def get_google_snippet_answer(query: str):
    """
    Scrape the first answer snippet from Google Search results page.
    No API key, just HTML.
    """
    try:
        q_enc = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={q_enc}&hl=en"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=3)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Common snippet containers (Google changes HTML often; we try multiple)
        selectors = [
            "div.BNeawe.s3v9rd.AP7Wnd",                           # generic answer / snippet
            "div[data-attrid='wa:/description'] span",             # definition box
            "div[data-attrid='kc:/location/location:short description'] span"
        ]

        for sel in selectors:
            el = soup.select_one(sel)
            if el and el.get_text(strip=True):
                text = el.get_text(" ", strip=True)
                if len(text) > 400:
                    cut = text[:400]
                    last_dot = cut.rfind(".")
                    if last_dot > 80:
                        text = cut[:last_dot + 1]
                    else:
                        text = cut
                return text

        return None

    except Exception as e:
        print("Google snippet error:", e)
        return None


def open_general_web_search(query: str):
    """
    Open a standard Google search in **Chrome** using the same method
    as your search_on_chrome() so it surely opens.
    """
    try:
        q_enc = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={q_enc}"

        # Use Chrome directly (same path you use everywhere)
        path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(path):
            subprocess.Popen([path, url])
        else:
            # Fallback to default browser if Chrome not found
            webbrowser.open(url)
    except Exception as e:
        print("General web search error:", e)

# ======================================================


def open_chrome():
    speak("Opening Chrome.")
    path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    subprocess.Popen([path])


# 🔹 WhatsApp Function
def open_whatsapp():
    speak("Opening WhatsApp.")
    path = r"C:\Users\HP\Desktop\WhatsApp.lnk"
    if os.path.exists(path):
        os.startfile(path)
    else:
        speak("WhatsApp shortcut not found at the given path.")
        print("Path not found:", path)


# 🔹 Shutdown Function
def shutdown():
    speak("Shutting down the system.")
    os.system("shutdown /s /t 1")


# 🔹 Lock System
def lock_system():
    speak("Locking the system.")
    os.system("rundll32.exe user32.dll,LockWorkStation")


# 🔹 Restart System
def restart_system():
    speak("Restarting the system.")
    os.system("shutdown /r /t 1")


# 🔹 Sleep System
def sleep_system():
    speak("Putting the system to sleep.")
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


# 🔹 Battery Status
def battery_status():
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            speak("Sorry, I cannot access battery information on this device.")
            return

        percent = battery.percent
        plugged = battery.power_plugged

        if plugged:
            speak(f"Battery is {percent} percent and charging.")
        else:
            if battery.secsleft in (psutil.POWER_TIME_UNLIMITED, psutil.POWER_TIME_UNKNOWN):
                speak(f"Battery is {percent} percent and not charging.")
            else:
                minutes_left = battery.secsleft // 60
                speak(f"Battery is {percent} percent with approximately {minutes_left} minutes remaining.")
    except Exception:
        speak("Unable to read battery status.")

# 🔹 Chrome Search Function


def search_on_chrome(query):
    search_query = ""
    if "open chrome and search" in query:
        search_query = query.split("open chrome and search", 1)[1].strip()
    elif "search on chrome" in query:
        search_query = query.split("search on chrome", 1)[1].strip()

    if search_query == "":
        speak("What should I search on Chrome?")
        return

    speak(f"Searching on Chrome for {search_query}")
    path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    try:
        url = "https://www.google.com/search?q=" + search_query.replace(" ", "+")
        subprocess.Popen([path, url])
    except Exception:
        speak("Sorry, I could not open Chrome search.")

# 🔹 YouTube Search Function


def search_on_youtube(query):
    search_query = ""
    if "open youtube and search" in query:
        search_query = query.split("open youtube and search", 1)[1].strip()
    elif "search on youtube" in query:
        search_query = query.split("search on youtube", 1)[1].strip()

    if search_query == "":
        speak("What should I search on YouTube?")
        return

    speak(f"Searching on YouTube for {search_query}")
    path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    try:
        url = "https://www.youtube.com/results?search_query=" + search_query.replace(" ", "+")
        subprocess.Popen([path, url])
    except Exception:
        speak("Sorry, I could not open YouTube search.")

# ================= EMAIL NOTIFICATIONS =================


def _decode_mime_text(raw):
    if not raw:
        return ""
    parts = decode_header(raw)
    decoded = ""
    for txt, enc in parts:
        if isinstance(txt, bytes):
            try:
                decoded += txt.decode(enc or "utf-8", errors="ignore")
            except Exception:
                decoded += txt.decode("utf-8", errors="ignore")
        else:
            decoded += txt
    return decoded


# 🔹 UPDATED read_notifications WITH DEBUG PRINTS
def read_notifications():
    try:
        print("🔹 Connecting to Gmail IMAP...")
        imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        imap.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        print("✅ IMAP login success")
    except Exception as e:
        print("❌ IMAP login error:", e)
        speak("I could not log into your email. Please check your email ID, app password, and IMAP settings.")
        return

    try:
        status, _ = imap.select("INBOX")
        print("INBOX select status:", status)
        if status != "OK":
            speak("I could not open your inbox.")
            imap.logout()
            return

        status, messages = imap.search(None, '(UNSEEN)')
        print("UNSEEN search status:", status)
        if status != "OK":
            speak("I could not search your emails.")
            imap.logout()
            return

        mail_ids = messages[0].split()
        print("Unread mail IDs:", mail_ids)
        if not mail_ids:
            speak("You have no new unread emails.")
            imap.logout()
            return

        latest_ids = mail_ids[-5:]
        speak(f"You have {len(mail_ids)} unread emails. Reading the latest.")

        for num in latest_ids:
            status, msg_data = imap.fetch(num, "(RFC822)")
            if status != "OK":
                print("Fetch failed for ID:", num)
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = _decode_mime_text(msg.get("Subject", ""))
            sender = _decode_mime_text(msg.get("From", ""))

            if "<" in sender:
                sender = sender.split("<")[0].strip()

            print(f"Email from {sender} | Subject: {subject}")
            speak(f"Email from {sender}. Subject: {subject}")

        imap.close()
        imap.logout()

    except Exception as e:
        print("❌ Error while reading notifications:", e)
        speak("Something went wrong while reading your notifications.")

# ================= OPEN WEBSITE (FIXED) =================

WEBSITE_MAP = {
    "instagram": "https://www.instagram.com/",
    "insta": "https://www.instagram.com/",
    "github": "https://github.com/",
    "git hub": "https://github.com/",
    "flipkart": "https://www.flipkart.com/",
    "amazon": "https://www.amazon.in/",
    "google": "https://www.google.com/",
    "linkedin": "https://www.linkedin.com/",
    "twitter": "https://x.com/",
    "youtube": "https://www.youtube.com/",
    "spotify": "https://open.spotify.com/",
    "whatsapp web": "https://web.whatsapp.com/"
}


def open_website(query):
    q = query.lower()
    url = None

    for key, u in WEBSITE_MAP.items():
        if key in q:
            url = u
            break

    if url is None and "open" in q:
        name = q.split("open", 1)[1].strip()
        for rm in ["website", "site", "page"]:
            name = name.replace(rm, "")
        base = name.replace(" ", "")
        domain = domain[4:]
        site_name = domain.split(".")[0]

        speak(f"Opening {site_name}.")
        webbrowser.open(url)
    else:
        speak("I could not understand which website to open.")

# ===============================================================


def speak(text):
    """Text-to-speech with Indian accent support"""
    # Import config (with fallback defaults)
    try:
        from backend import voice_config as vc
    except:
        class vc:
            USE_INDIAN_ACCENT = True
            INDIAN_VOICE_SLOW = False
            FALLBACK_TO_WINDOWS = True
            VOICE_GENDER = 'male'
            SPEECH_RATE = 155
            SPEECH_VOLUME = 0.95
            SHOW_AVAILABLE_VOICES = False
    
    text = str(text)
    
    # 🇮🇳 TRY INDIAN ACCENT FIRST (if enabled)
    if vc.USE_INDIAN_ACCENT:
        try:
            print(f"🇮🇳 Attempting Indian accent for: {text[:50]}...")
            from backend.indian_voice import IndianVoice
            indian_voice = IndianVoice()
            success = indian_voice.speak(text, slow=vc.INDIAN_VOICE_SLOW)
            if success:
                print("✅ Indian voice successful!")
                eel.DisplayMessage(text)
                eel.receiverText(text)
                return
            else:
                print("⚠️ Indian voice returned False")
        except Exception as e:
            print(f"⚠️ Indian voice exception: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            if vc.FALLBACK_TO_WINDOWS:
                print("→ Falling back to Windows voice")
            else:
                eel.DisplayMessage(text)
                eel.receiverText(text)
                return
    
    # 🔹 FALLBACK TO WINDOWS SAPI5 VOICE
    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')

        # 🔹 SELECT VOICE based on config
        selected_voice = None
        
        if vc.SHOW_AVAILABLE_VOICES:
            print("\n📢 Available voices:")
            for v in voices:
                print(f"  - {getattr(v, 'name', 'Unknown')}")
        
        # Search for preferred voice gender
        search_terms = ['david', 'male'] if vc.VOICE_GENDER == 'male' else ['zira', 'female']
        
        for v in voices:
            n = getattr(v, 'name', '') or getattr(v, 'id', '')
            if any(term in n.lower() for term in search_terms):
                selected_voice = v.id
                break
        
        # Fallback: if no matching voice found
        if selected_voice is None and len(voices) > 1:
            selected_voice = voices[1].id  # Usually index 1 is male (David)
        elif selected_voice is None and len(voices) > 0:
            selected_voice = voices[0].id

        if selected_voice:
            engine.setProperty('voice', selected_voice)

        # 🔹 Apply voice settings from config
        engine.setProperty('rate', vc.SPEECH_RATE)
        engine.setProperty('volume', vc.SPEECH_VOLUME)
        
        eel.DisplayMessage(text)
        engine.say(text)
        engine.runAndWait()
        eel.receiverText(text)
    except Exception as e:
        print(f"❌ All voice engines failed: {e}")
        eel.DisplayMessage(text)
        eel.receiverText(text)


def takecommand():
    r = sr.Recognizer()
    
    # 🔹 ENHANCED NOISE HANDLING for high-noise environments
    r.energy_threshold = 4000  # Higher threshold filters background noise (default: 300)
    r.dynamic_energy_threshold = True  # Automatically adjust to ambient noise
    r.dynamic_energy_adjustment_damping = 0.15  # Faster adaptation to noise changes
    r.dynamic_energy_ratio = 1.5  # More aggressive noise filtering
    
    try:
        with sr.Microphone() as source:
            eel.DisplayMessage("I'm listening...")
            
            # 🔹 LONGER ambient noise adjustment for noisy rooms (3 seconds)
            print("🎤 Adjusting for ambient noise... Please wait.")
            r.adjust_for_ambient_noise(source, duration=3)
            print(f"✅ Energy threshold set to: {r.energy_threshold}")
            
            # 🔹 Better pause detection for natural speech
            r.pause_threshold = 1.2  # Slightly longer pause before stopping
            r.phrase_threshold = 0.3  # Minimum audio before considering it speech
            r.non_speaking_duration = 0.8  # How long to listen for silence
            
            # 🔹 Extended timeout for noisy environments
            audio = r.listen(source, timeout=15, phrase_time_limit=10)

        eel.DisplayMessage("Recognizing...")
        
        # 🔹 Use Google Speech Recognition with better language model
        query = r.recognize_google(audio, language='en-IN', show_all=False)
        eel.DisplayMessage(query)

        # 🔹 Emotion detection hook
        analyze_and_respond_emotion(audio, query)

        return query.lower()

    except sr.WaitTimeoutError:
        eel.DisplayMessage("Listening timeout. Please try again.")
        return None
    except sr.UnknownValueError:
        eel.DisplayMessage("Could not understand. Please speak clearly.")
        return None
    except sr.RequestError as e:
        eel.DisplayMessage(f"Recognition service error: {e}")
        return None
    except Exception as e:
        print(f"Error in takecommand: {e}")
        eel.DisplayMessage("Could not understand.")
        return None


@eel.expose
def takeAllCommands(message=None):
    if message is None:
        query = takecommand()
        if not query:
            return
        eel.senderText(query)
    else:
        query = message.lower()
        eel.senderText(query)

    try:
        if query:

            if "hi jarvis" in query:
                speak("Hii rajveer how was your day")
                response = takecommand()
                if response and "fine" in response:
                    speak("That's great rajveer, how can I help you")

            elif "open chrome and search" in query or "search on chrome" in query:
                search_on_chrome(query)

            elif "open chrome" in query:
                open_chrome()

            elif "open whatsapp" in query:
                open_whatsapp()

            # 🔹 Volume controls
            elif "increase volume" in query or "volume up" in query or "inc volume" in query:
                increase_volume()
            elif "decrease volume" in query or "volume down" in query or "dec volume" in query:
                decrease_volume()
            elif "mute volume" in query or "mute the volume" in query or "mute sound" in query:
                mute_volume()

            # 🔹 Brightness controls
            elif "increase brightness" in query or "brightness up" in query or "inc brightness" in query:
                increase_brightness()
            elif "decrease brightness" in query or "brightness down" in query or "dec brightness" in query:
                decrease_brightness()

            elif "lock system" in query:
                lock_system()

            elif "restart" in query:
                restart_system()

            elif "sleep mode" in query:
                sleep_system()

            elif "shutdown" in query:
                shutdown()

            elif "battery" in query:
                battery_status()

            # 🔹 UPDATED: more flexible triggers for email notifications
            elif (
                "read notifications" in query
                or "read my notifications" in query
                or "read notification" in query
                or "read my emails" in query
                or "read my email" in query
                or "check my email" in query
                or "check emails" in query
            ):
                read_notifications()

            elif "open youtube and search" in query or "search on youtube" in query:
                search_on_youtube(query)

            elif "open " in query:
                open_website(query)

            elif "on youtube" in query:
                speak(f"Playing {query.replace('on youtube','')}")
                from backend.feature import PlayYoutube
                PlayYoutube(query)

            elif "send message" in query or "call" in query or "video call" in query:
                speak(f"Sure, {query}")
                from backend.feature import findContact, whatsApp

                clean = query.replace("on whatsapp", "").replace("jarvis", "").strip()

                Phone, name = findContact(clean)
                if Phone != 0:
                    if "send message" in query:
                        speak("What message to send?")
                        msg = takecommand()
                        if msg:
                            whatsApp(Phone, msg, "message", name)
                    elif "video call" in query:
                        whatsApp(Phone, query, "video call", name)
                    else:
                        whatsApp(Phone, query, "call", name)
                else:
                    speak("Sorry, I could not find that contact.")

            # 🔹 INDIA NEWS / WEATHER / CRICKET FAST HANDLERS
            elif "india news" in query or "indian news" in query or "latest india news" in query:
                get_india_news()

            elif "weather" in query:
                city = "Pune"
                if " in " in query:
                    after_in = query.split(" in ", 1)[1].strip()
                    city = " ".join(after_in.split()[:3])
                get_weather_for_city(city)

            elif "cricket score" in query or "live cricket" in query or "match score" in query:
                get_live_cricket_score()

            else:
                # 1️⃣ Try DB first (fast)
                answer = get_answer_from_db(query)
                if answer:
                    speak(answer)
                else:
                    # 2️⃣ Try quick web answer (Wikipedia)
                    web_ans = get_quick_web_answer(query)

                    # 3️⃣ If still no answer, try Google snippet
                    if not web_ans:
                        web_ans = get_google_snippet_answer(query)

                    if web_ans:
                        speak(web_ans)
                        # also open Google so user can see full results
                        open_general_web_search(query)
                    else:
                        # Final fallback: just open Google + optional chatBot
                        open_general_web_search(query)
                        try:
                            from backend.feature import chatBot
                            chatBot(query)
                        except Exception as e:
                            print("chatBot error:", e)
                            speak("I have searched this on the internet. Please check your browser for more details.")

        else:
            speak("No command was given.")
    except Exception as e:
        print(e)
        speak("Sorry, something went wrong.")

    eel.ShowHood()

# ================= SMART DB ANSWER (WITH FUZZY MATCH) ==================


def get_answer_from_db(question):
    try:
        conn = sqlite3.connect("jarvis.db")
        cursor = conn.cursor()
        q = question.strip().lower()

        # 1) Fetch all questions from DB
        cursor.execute("SELECT question, answer FROM knowledge_base")
        data = cursor.fetchall()

        if data:
            questions = [row[0].lower() for row in data if row[0]]

            # Fuzzy match for spelling mistakes / similar questions
            best_match = difflib.get_close_matches(q, questions, n=1, cutoff=0.55)

            if best_match:
                matched_question = best_match[0]
                cursor.execute(
                    "SELECT answer FROM knowledge_base WHERE LOWER(question)=?",
                    (matched_question,)
                )
                row = cursor.fetchone()
                if row:
                    conn.close()
                    return row[0]

        # 2) Fallback LIKE search
        cursor.execute(
            "SELECT answer FROM knowledge_base WHERE LOWER(question) LIKE ? OR LOWER(question) LIKE ?",
            ('%' + q + '%', q + '%')
        )
        results = cursor.fetchall()
        conn.close()

        if results:
            return results[0][0]
        else:
            return None

    except Exception as e:
        print("DB ERROR in get_answer_from_db:", e)
        return None

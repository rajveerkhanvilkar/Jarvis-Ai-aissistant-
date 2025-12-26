# import playsound
# import eel


# @eel.expose
# def playAssistantSound():
#     music_dir = "frontend\\assets\\audio\\start_sound.mp3"
#     playsound(music_dir)


from compileall import compile_path
import os
import re
from shlex import quote
import struct
import subprocess
import time
import webbrowser
import eel
from hugchat import hugchat 
import pvporcupine
import pyaudio
import pyautogui
import pywhatkit as kit
import pygame
from backend.command import speak
from backend.config import ASSISTANT_NAME
import sqlite3

from backend.helper import extract_yt_term, remove_words
conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()
# Initialize pygame mixer
pygame.mixer.init()

# Define the function to play sound
@eel.expose
def play_assistant_sound():
    # Use a project-relative path so the file loads regardless of user folder
    sound_file = os.path.join(os.getcwd(), 'frontend', 'assets', 'audio', 'start_sound.mp3')
    if not os.path.exists(sound_file):
        # fallback to path relative to this module
        sound_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'assets', 'audio', 'start_sound.mp3')
    try:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    except Exception:
        pass


def openCommand(query):
    query = query.replace(ASSISTANT_NAME,"")
    query = query.replace("open","")
    query.lower()
    
    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute( 
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    if "chrome" in query:
                        speak("Opening Chrome")
                        os.startfile("C:\Program Files\Google\Chrome\Application\chrome.exe")
                    elif ".com" in query or ".co" in query or ".org" in query or ".in" in query:
                        speak("Opening "+query)
                        webbrowser.open(f"https://www.{query}")
                    else:
                        speak("Opening "+query)
                        try:
                            os.system('start '+query)
                        except:
                            speak("not found")
        except:
            speak("some thing went wrong")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def hotword():
    """
    Hotword detection using Porcupine. Requires an access_key from Picovoice.
    If access key is not available, this function logs a message and returns.
    Users can use the microphone button in the UI as an alternative.
    """
    porcupine = None
    paud = None
    audio_stream = None
    try:
        print("Initializing hotword detection...")
        print("Note: Hotword detection requires a Porcupine access key.")
        print("Skipping hotword detection. Use the microphone button in the UI to record commands.")
        return
        
    except Exception as e:
        print(f"Error in hotword detection: {e}")
        print("Hotword detection failed. Use the microphone button in the UI to record commands.")
    finally:
        if porcupine is not None:
            try:
                porcupine.delete()
            except:
                pass
        if audio_stream is not None:
            try:
                audio_stream.close()
            except:
                pass
        if paud is not None:
            try:
                paud.terminate()
            except:
                pass


def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT Phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
    
def whatsApp(Phone, message, flag, name):
    

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={Phone}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)


def chatBot(query):
    user_input = query.lower()
    try:
        chatbot = hugchat.ChatBot(cookie_path="backend/cookie.json")
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        response = chatbot.chat(user_input)
        print(response)
        speak(response)
        return response
    except Exception as e:
        print(f"ChatBot error: {e}")
        fallback_response = f"I heard you say {user_input}. I'm unable to process that right now."
        print(fallback_response)
        speak(fallback_response)
        return fallback_response

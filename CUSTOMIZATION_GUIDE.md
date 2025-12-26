# 🎛️ JARVIS CUSTOMIZATION GUIDE - ALL POSSIBLE CHANGES

## 🎙️ VOICE CUSTOMIZATION

### 1. Voice Gender (Male/Female)
**File:** `backend/voice_config.py`

```python
# Current: Male voice (David)
VOICE_GENDER = 'male'

# Change to female voice (Zira)
VOICE_GENDER = 'female'
```

### 2. Voice Speed (Heaviness)
**File:** `backend/voice_config.py`

```python
# Current: Heavy/slow (155)
SPEECH_RATE = 155

# Options:
SPEECH_RATE = 140   # Very heavy/slow (deep, authoritative)
SPEECH_RATE = 155   # Heavy (current - good balance)
SPEECH_RATE = 170   # Normal speed
SPEECH_RATE = 185   # Fast
SPEECH_RATE = 200   # Very fast (default Windows)
```

**Recommendation:** 140-160 for heavy male voice, 170-180 for normal

### 3. Voice Volume
**File:** `backend/voice_config.py`

```python
# Current: 95% volume
SPEECH_VOLUME = 0.95

# Options:
SPEECH_VOLUME = 0.8   # Quieter
SPEECH_VOLUME = 0.95  # Current (recommended)
SPEECH_VOLUME = 1.0   # Maximum volume
```

---

## 🔊 NOISE HANDLING CUSTOMIZATION

### 4. Energy Threshold (Noise Filtering)
**File:** `backend/voice_config.py`

```python
# Current: 4000 (good for noisy rooms)
ENERGY_THRESHOLD = 4000

# Adjust based on your room:
ENERGY_THRESHOLD = 2000   # Quiet room (home office)
ENERGY_THRESHOLD = 3000   # Normal room
ENERGY_THRESHOLD = 4000   # Noisy room (current)
ENERGY_THRESHOLD = 5000   # Very noisy (traffic, construction)
ENERGY_THRESHOLD = 6000   # Extremely noisy
```

**Higher = More noise filtering (but might miss quiet speech)**
**Lower = More sensitive (but might pick up background noise)**

### 5. Calibration Duration
**File:** `backend/voice_config.py`

```python
# Current: 3 seconds
CALIBRATION_DURATION = 3

# Options:
CALIBRATION_DURATION = 2   # Quick calibration (quiet rooms)
CALIBRATION_DURATION = 3   # Standard (current)
CALIBRATION_DURATION = 4   # Thorough (noisy rooms)
CALIBRATION_DURATION = 5   # Very thorough (very noisy)
```

**Stay quiet during this time for best results!**

### 6. Listening Timeout
**File:** `backend/voice_config.py`

```python
# Current: 15 seconds
LISTENING_TIMEOUT = 15

# Options:
LISTENING_TIMEOUT = 10   # Shorter wait
LISTENING_TIMEOUT = 15   # Current (good balance)
LISTENING_TIMEOUT = 20   # Longer wait (if you speak slowly)
```

### 7. Phrase Time Limit
**File:** `backend/voice_config.py`

```python
# Current: 10 seconds per command
PHRASE_TIME_LIMIT = 10

# Options:
PHRASE_TIME_LIMIT = 8    # Short commands only
PHRASE_TIME_LIMIT = 10   # Current (normal)
PHRASE_TIME_LIMIT = 15   # Long commands (complex queries)
```

---

## 🌐 LANGUAGE & RECOGNITION

### 8. Recognition Language
**File:** `backend/voice_config.py`

```python
# Current: Indian English
RECOGNITION_LANGUAGE = 'en-IN'

# Options:
RECOGNITION_LANGUAGE = 'en-IN'  # Indian English (current)
RECOGNITION_LANGUAGE = 'en-US'  # American English
RECOGNITION_LANGUAGE = 'en-GB'  # British English
RECOGNITION_LANGUAGE = 'en-AU'  # Australian English
```

**Recommendation:** Keep 'en-IN' for Indian accent recognition

---

## 🎯 ASSISTANT BEHAVIOR

### 9. Assistant Name
**File:** `backend/config.py`

```python
# Current: "Jarvis"
ASSISTANT_NAME = "Jarvis"

# Change to anything:
ASSISTANT_NAME = "Friday"
ASSISTANT_NAME = "Alfred"
ASSISTANT_NAME = "Computer"
```

### 10. Greeting Messages
**File:** `backend/command.py` (line ~679)

```python
# Current greeting
if "hi jarvis" in query:
    speak("Hii rajveer how was your day")

# Customize to:
if "hi jarvis" in query:
    speak("Hello sir, how may I assist you today")
    # or
    speak("Good to see you, what can I do for you")
```

---

## 🔧 ADVANCED CUSTOMIZATIONS

### 11. Pause Detection
**File:** `backend/voice_config.py`

```python
# How long to wait before stopping listening
PAUSE_THRESHOLD = 1.2   # Current (1.2 seconds)

# Options:
PAUSE_THRESHOLD = 0.8   # Quick stop (for fast speakers)
PAUSE_THRESHOLD = 1.2   # Normal (current)
PAUSE_THRESHOLD = 1.5   # Longer pause (for slow speakers)
```

### 12. Dynamic Energy Settings
**File:** `backend/voice_config.py`

```python
# Auto-adjust to noise
DYNAMIC_ENERGY = True   # Recommended

# Fixed threshold (no auto-adjust)
DYNAMIC_ENERGY = False

# Adjustment speed
ENERGY_DAMPING = 0.15   # Current (faster adaptation)
ENERGY_DAMPING = 0.25   # Slower adaptation

# Noise ratio
ENERGY_RATIO = 1.5   # Current (speech must be 1.5x louder than noise)
ENERGY_RATIO = 2.0   # More aggressive filtering
```

---

## 📊 PRESET CONFIGURATIONS

### Preset 1: QUIET HOME OFFICE
```python
ENERGY_THRESHOLD = 2500
CALIBRATION_DURATION = 2
SPEECH_RATE = 165
LISTENING_TIMEOUT = 12
```

### Preset 2: NORMAL ROOM (CURRENT)
```python
ENERGY_THRESHOLD = 4000
CALIBRATION_DURATION = 3
SPEECH_RATE = 155
LISTENING_TIMEOUT = 15
```

### Preset 3: VERY NOISY ENVIRONMENT
```python
ENERGY_THRESHOLD = 6000
CALIBRATION_DURATION = 5
SPEECH_RATE = 145
ENERGY_RATIO = 2.0
LISTENING_TIMEOUT = 20
```

### Preset 4: VERY HEAVY VOICE
```python
SPEECH_RATE = 140
SPEECH_VOLUME = 1.0
VOICE_GENDER = 'male'
```

### Preset 5: FAST & RESPONSIVE
```python
SPEECH_RATE = 180
LISTENING_TIMEOUT = 10
PHRASE_TIME_LIMIT = 8
CALIBRATION_DURATION = 2
```

---

## 🎨 CUSTOM RESPONSES

### Add Custom Commands
**File:** `backend/command.py` (in `takeAllCommands` function)

Add your own commands around line ~750:

```python
# Add after existing commands
elif "tell me a joke" in query:
    speak("Why did the programmer quit his job? Because he didn't get arrays!")

elif "what's your name" in query:
    speak("I am Jarvis, your personal AI assistant")

elif "who created you" in query:
    speak("I was created by Rajveer to assist with daily tasks")

elif "good morning" in query:
    speak("Good morning sir, I hope you have a productive day")

elif "good night" in query:
    speak("Good night sir, sleep well")
```

---

## 🌟 RECOMMENDED SETTINGS FOR DIFFERENT SCENARIOS

### For Clear, Professional Voice:
```python
SPEECH_RATE = 155
SPEECH_VOLUME = 0.95
VOICE_GENDER = 'male'
```

### For Very Heavy, Deep Voice:
```python
SPEECH_RATE = 140
SPEECH_VOLUME = 1.0
VOICE_GENDER = 'male'
```

### For Noisy Room (Traffic, Construction):
```python
ENERGY_THRESHOLD = 5500
CALIBRATION_DURATION = 4
ENERGY_RATIO = 2.0
```

### For Quiet Room (Better Sensitivity):
```python
ENERGY_THRESHOLD = 2500
CALIBRATION_DURATION = 2
DYNAMIC_ENERGY = True
```

---

## 🚀 HOW TO APPLY CHANGES

1. **Edit** `backend/voice_config.py`
2. **Save** the file
3. **Restart** Jarvis: `python run.py`
4. **Test** your changes!

**No code editing needed** - just change values in `voice_config.py`!

---

## 💡 TIPS FOR BEST RESULTS

1. **Start with defaults** and adjust one thing at a time
2. **Test after each change** to see the effect
3. **For heavy voice**: Lower SPEECH_RATE (140-155)
4. **For noisy rooms**: Increase ENERGY_THRESHOLD (4000-6000)
5. **For quiet rooms**: Decrease ENERGY_THRESHOLD (2000-3000)
6. **Stay quiet during calibration** for best noise handling

---

## 📝 QUICK REFERENCE

| Want to... | Change this... | To... |
|------------|----------------|-------|
| Heavier voice | SPEECH_RATE | 140-150 |
| Faster voice | SPEECH_RATE | 180-200 |
| Female voice | VOICE_GENDER | 'female' |
| Better noise filtering | ENERGY_THRESHOLD | 5000-6000 |
| More sensitive | ENERGY_THRESHOLD | 2000-3000 |
| Longer listening time | LISTENING_TIMEOUT | 20-25 |
| Louder voice | SPEECH_VOLUME | 1.0 |

---

**All settings are in `backend/voice_config.py` - easy to customize!** 🎛️

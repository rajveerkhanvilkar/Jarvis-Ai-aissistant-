"""
Voice Configuration for Jarvis Assistant
Adjust these settings to customize voice and noise handling
"""

# ==================== INDIAN ACCENT SETTINGS ====================

# Use Indian English Accent (requires gTTS - Google Text-to-Speech)
# True = Natural Indian accent using Google TTS (requires internet)
# False = Windows SAPI5 voices (David/Zira - American/British accent)
USE_INDIAN_ACCENT = True

# Indian Voice Speed (only for gTTS)
# True = Slower speech (more clear)
# False = Normal speed
INDIAN_VOICE_SLOW = False

# Fallback to Windows voice if Indian voice fails
FALLBACK_TO_WINDOWS = True

# ==================== VOICE SETTINGS ====================

# Voice Selection (options: 'male', 'female', 'auto')
VOICE_GENDER = 'male'  # 'male' for David, 'female' for Zira

# Speech Rate (default: 200, slower: 140-160, faster: 180-220)
# Lower = heavier/deeper sound
SPEECH_RATE = 155

# Volume (0.0 to 1.0)
SPEECH_VOLUME = 0.95

# ==================== NOISE HANDLING ====================

# Energy Threshold (how loud sound must be to register as speech)
# Quiet room: 2000-3000
# Normal room: 3000-4000
# Noisy room: 4000-5000
# Very noisy: 5000-7000
ENERGY_THRESHOLD = 4000

# Ambient Noise Calibration Duration (seconds)
# How long to listen to room noise before accepting commands
CALIBRATION_DURATION = 3

# Dynamic Energy Threshold (True = auto-adjust to noise)
DYNAMIC_ENERGY = True

# Dynamic Energy Adjustment Damping (0.1-0.3)
# Lower = faster adaptation to noise changes
ENERGY_DAMPING = 0.15

# Dynamic Energy Ratio (1.0-2.0)
# How much louder speech must be than background noise
ENERGY_RATIO = 1.5

# ==================== LISTENING SETTINGS ====================

# Pause Threshold (seconds of silence before stopping)
PAUSE_THRESHOLD = 1.2

# Phrase Threshold (minimum audio length to consider as speech)
PHRASE_THRESHOLD = 0.3

# Non-Speaking Duration (how long to wait for silence)
NON_SPEAKING_DURATION = 0.8

# Listening Timeout (max seconds to wait for speech to start)
LISTENING_TIMEOUT = 15

# Phrase Time Limit (max seconds for a single phrase)
PHRASE_TIME_LIMIT = 10

# ==================== LANGUAGE SETTINGS ====================

# Recognition Language
# 'en-US' = American English
# 'en-IN' = Indian English
# 'en-GB' = British English
RECOGNITION_LANGUAGE = 'en-IN'

# ==================== PRESETS ====================

# Uncomment one of these to quickly switch settings

# PRESET: Quiet Home Office
# ENERGY_THRESHOLD = 2000
# CALIBRATION_DURATION = 2
# SPEECH_RATE = 165

# PRESET: Normal Room
# ENERGY_THRESHOLD = 3500
# CALIBRATION_DURATION = 3
# SPEECH_RATE = 155

# PRESET: Noisy Environment (Construction, Traffic, etc.)
# ENERGY_THRESHOLD = 6000
# CALIBRATION_DURATION = 5
# SPEECH_RATE = 145
# ENERGY_RATIO = 2.0

# PRESET: Very Heavy/Deep Voice
# SPEECH_RATE = 140
# SPEECH_VOLUME = 1.0

# PRESET: Faster Response (Less Heavy)
# SPEECH_RATE = 170
# LISTENING_TIMEOUT = 10
# PHRASE_TIME_LIMIT = 8

# ==================== DEBUG SETTINGS ====================

# Show debug information during voice recognition
DEBUG_MODE = True

# Print energy threshold after calibration
SHOW_ENERGY_THRESHOLD = True

# Print available voices on startup
SHOW_AVAILABLE_VOICES = False

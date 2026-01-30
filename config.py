"""
Configuration constants for ABook application
"""

# --- DISPLAY SETTINGS ---
# Physical window: 1024x600 landscape (what you see on laptop)
# Logical content: Portrait orientation (tall and narrow like phone)
DISPLAY_WIDTH = 1024  # Window width
DISPLAY_HEIGHT = 600  # Window height

# Content dimensions (portrait inside landscape window)
CONTENT_WIDTH = 600   # Portrait width (matches old DISPLAY_WIDTH)
CONTENT_HEIGHT = 1024 # Portrait height (matches old DISPLAY_HEIGHT)  

FPS = 60

# --- COLORS ---
# Modern, professional color palette (Y Combinator style)
COLOR_PRIMARY = (45, 55, 72)        # Dark slate
COLOR_SECONDARY = (99, 102, 241)    # Indigo  
COLOR_ACCENT = (59, 130, 246)       # Bright blue
COLOR_SUCCESS = (16, 185, 129)      # Green
COLOR_WARNING = (245, 158, 11)      # Amber
COLOR_DANGER = (239, 68, 68)        # Red
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (30, 41, 59)
COLOR_PAPER = (252, 252, 253)
COLOR_GRAY_100 = (241, 245, 249)
COLOR_GRAY_200 = (226, 232, 240)
COLOR_GRAY_300 = (203, 213, 225)
COLOR_GRAY_400 = (148, 163, 184)
COLOR_GRAY_500 = (100, 116, 139)
COLOR_GRAY_600 = (71, 85, 105)
COLOR_GRAY_700 = (51, 65, 85)
COLOR_GRAY_800 = (30, 41, 59)

# Notepad theme - Pure black and white
NOTEPAD_BG = (255, 255, 255)        # Pure white background
NOTEPAD_INK = (0, 0, 0)             # Pure black ink
NOTEPAD_TOOLBAR = (240, 240, 240)   # Light gray toolbar
NOTEPAD_BUTTON = (50, 50, 50)       # Dark gray buttons
NOTEPAD_BUTTON_ACTIVE = (0, 0, 0)   # Black for active

# Legacy compatibility
COLOR_UI_LIGHT = COLOR_GRAY_100
COLOR_UI_DARK = COLOR_GRAY_600

# --- BOOT ANIMATION SETTINGS ---
FORMATION_DURATION = 1.5
HOLD_DURATION = 1.0
DISPERSE_DURATION = 1.0
TOTAL_BOOT_TIME = FORMATION_DURATION + HOLD_DURATION + DISPERSE_DURATION

# --- LOGO LETTERS ---
LETTERS = {
    'A': ["  ###  ", " #   # ", "#     #", "#######", "#     #", "#     #", "#     #"],
    'B': ["###### ", "#    # ", "#    # ", "###### ", "#    # ", "#    # ", "###### "],
    'O': [" ####  ", "#    # ", "#    # ", "#    # ", "#    # ", "#    # ", " ####  "],
    'K': ["#    # ", "#   #  ", "#  #   ", "###    ", "#  #   ", "#   #  ", "#    # "]
}

# --- TEXT SETTINGS ---
AVAILABLE_FONTS = [
    ('Arial', 'sans-serif'),
    ('Times New Roman', 'serif'),
    ('Courier New', 'monospace'),
    ('Comic Sans MS', 'comic'),
    ('Georgia', 'serif'),
    ('Verdana', 'sans-serif')
]

TEXT_SIZES = [12, 14, 16, 18, 20, 24, 28, 32]
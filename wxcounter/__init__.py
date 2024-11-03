from pyautogui import size

SCREEN_SIZE = size()
CHAT_WINDOW_AREA = (    # In the order of (left, upper, right, lower), the same as the argument `box` in PIL.Image.crop
    0,
    120,  # Y start of the chat window, may vary on different monitors
    SCREEN_SIZE.width,
    1446  # Y end of the chat window, may vary on different monitors
)

PROFILE_SIZE = 68   # length of both sides of profile

PROFILE_RANGE = (
    60,   # X start of the other's profile, may vary on different monitors
    2752, # X start of your own profile, may vary on different monitors
)


from wxcounter.GUIutility import *
from wxcounter.counterutility import *

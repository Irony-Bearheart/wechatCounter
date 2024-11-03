# -*- encoding: utf-8 -*-
from collections.abc import Generator

import pyautogui
from PIL.Image import Image
from imagehash import dhash_vertical

from wxcounter import SCREEN_SIZE, CHAT_WINDOW_AREA

def focus2center():
    pyautogui.moveTo(SCREEN_SIZE.width // 2, SCREEN_SIZE.height // 2)
    pyautogui.click()   # Set the focus to the dialogue area


def scroll_screenshot() -> Generator[Image]:
    last_hash = None

    while True:
        screen = pyautogui.screenshot().convert('L').crop(CHAT_WINDOW_AREA)

        screen_hash = dhash_vertical(screen)
        if screen_hash != last_hash:
            last_hash = dhash_vertical(screen)
            yield screen
        else:
            break

        pyautogui.typewrite(["pgdn"]) # noqa, scroll to next page

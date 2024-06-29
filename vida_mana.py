import pyautogui
import keyboard

LIFE_REGION = (1766, 304, 92, 5)
MANA_REGION = (1766, 316, 92, 5)
LIFE_COLOR = (240, 97, 97)
MANA_COLOR = (83, 80, 217)
WIDTH = 92

def calculate_width(percent):
    return int(WIDTH * percent / 100)

def pixel_mathches_color(region, percent, color):
    result_percent = calculate_width(percent)
    x = region[0] + result_percent
    y = region[1] + region[3]
    return pyautogui.pixelMatchesColor(int(x), int(y), color, 10)

def manager_suplies(event):
    while not event.is_set():
        if not pixel_mathches_color(LIFE_REGION, 30, LIFE_COLOR):
            pyautogui.press('F1')
        if event.is_set():
            return
        else:
            if not pixel_mathches_color(LIFE_REGION, 80, LIFE_COLOR):
                pyautogui.press('F3')
            if not pixel_mathches_color(MANA_REGION, 20, MANA_COLOR):
                pyautogui.press('F2')
            if event.is_set():
                return
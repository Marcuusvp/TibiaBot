import pyautogui
import keyboard
import constants

LIFE_REGION = (1766, 304, 92, 5)
MANA_REGION = (1766, 316, 92, 5)
# LIFE_COLOR = (240, 97, 97)  # MONITOR
# MANA_COLOR = (83, 80, 217)  # MONITOR
LIFE_COLOR = (254, 112, 112) # NOTEBOOK
MANA_COLOR = (101, 98, 239)  # NOTEBOOK
WIDTH = 92
def calculate_width(percent):
    return int(WIDTH * percent / 100)

def pixel_matches_color(region, percent, color):
    result_percent = calculate_width(percent)
    x = region[0] + result_percent
    y = region[1] + region[3]
    print('coordenadas x: ', x, 'coordenadas y: ', y)
    print(pyautogui.pixel(x, y))
    print('deu certo? ', pyautogui.pixelMatchesColor(int(x), int(y), color, 10))
    return pyautogui.pixelMatchesColor(int(x), int(y), color, 10)

while True:
    keyboard.wait('s')
    # pyautogui.moveTo(1812, 309, 0.5)
    # print(pyautogui.pixel(1812, 309))
    # print(pyautogui.position())
    # print(pyautogui.pixel(pyautogui.position().x, pyautogui.position().y))
    pixel_matches_color(MANA_REGION, 50, MANA_COLOR)
    mana = pyautogui.screenshot(region=MANA_REGION)
    life = pyautogui.screenshot(region=LIFE_REGION)
    mana.save('mana.png')
    life.save('life.png')
    # img = pyautogui.screenshot(region=constants.RING_AREA)
    # img.save('xpng.png')
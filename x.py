import pyautogui
import keyboard
import constants

while True:
    keyboard.wait('h')
    # pyautogui.moveTo(1848, 321, 0.5)
    # print(pyautogui.pixel(1854, 321))
    # print(pyautogui.position())
    # print(pyautogui.pixel(pyautogui.position().x, pyautogui.position().y))
    img = pyautogui.screenshot(region=constants.RING_AREA)
    img.save('xpng.png')